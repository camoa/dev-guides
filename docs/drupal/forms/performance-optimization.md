---
description: Performance optimization — form rendering, caching, validation strategies
drupal_version: "11.x"
---

# Performance Optimization

**WHY Performance Matters:**

Slow forms = frustrated users, abandoned submissions, failed conversions, poor SEO (Google penalizes slow sites), server resource exhaustion, hosting cost increase. Target: Forms should load in <1 second, submit in <2 seconds.

### Form Rendering Optimization

**CRITICAL: What NOT to Put in buildForm()**

buildForm() is called on:
- Initial form display
- Every AJAX callback
- Every validation error (form redisplays)
- Every multi-step navigation
- Every form alter hook

**WHY This Matters:** If buildForm() takes 2 seconds, user waits 2 seconds on EVERY AJAX interaction. With 3 AJAX callbacks = 6 seconds total wait time.

**Expensive Operations to Avoid in buildForm():**
```
✗ Heavy database queries (>100 rows)
  Impact: 1-5 seconds per query, blocks PHP thread
  Example: Loading 10,000 nodes for select #options

✗ Entity loading in loops (N+1 problem)
  Impact: 100 entities = 100 queries = 3-10 seconds
  Example: foreach ($ids as $id) { Node::load($id); }

✗ Remote API calls
  Impact: 500ms-10s per call, timeout risk, blocks form
  Example: $this->weatherApi->getForecast()

✗ File system operations
  Impact: 50-500ms per file, NFS even slower
  Example: file_exists(), scandir(), file_get_contents()

✗ Complex calculations
  Impact: 100ms-5s depending on complexity
  Example: Recursive algorithms, image processing, PDF generation

✗ External service calls
  Impact: 200ms-30s, failure breaks form
  Example: CRM sync, payment gateway check, geocoding
```

**Performance Thresholds (2025 Research-Backed):**

| Operation | Acceptable | Slow | Critical |
|-----------|-----------|------|----------|
| buildForm() total | <200ms | 200ms-1s | >1s |
| Database query | <50ms | 50-200ms | >200ms |
| Entity load | <10ms | 10-50ms | >50ms |
| API call | <100ms | 100-500ms | >500ms |
| File operation | <20ms | 20-100ms | >100ms |

**Reference:** [Drupal Performance Optimization 2025](https://kinematic.digital/index.php/2025/06/20/advanced-drupal-performance-optimization-techniques/)

### Optimization Patterns

**Pattern 1: Use Autocomplete for Large Option Sets (>50 Items)**

**WHY:** Select with 1000 options = 200KB HTML, 500ms DOM rendering, poor mobile UX, accessibility nightmare.

```php
// WRONG - 10,000 options = massive page load time
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadByProperties(['type' => 'article']); // Loads 10,000 nodes!
$options = [];
foreach ($nodes as $node) {
  $options[$node->id()] = $node->label(); // 10,000 iterations
}
$form['article'] = [
  '#type' => 'select',
  '#options' => $options, // 200KB+ HTML
];
// Impact: 3-5 second page load, poor mobile experience

// CORRECT - lazy load via autocomplete
$form['article'] = [
  '#type' => 'entity_autocomplete',
  '#target_type' => 'node',
  '#selection_settings' => ['target_bundles' => ['article']],
];
// Impact: <100ms page load, options loaded on demand via AJAX
```

**Decision Threshold:**
```
<20 options: radios/checkboxes (best UX)
20-50 options: select dropdown
>50 options: entity_autocomplete (REQUIRED for performance)
>1000 options: Custom AJAX autocomplete with database search
```

**Pattern 2: Cache Expensive Options (State API or Config)**

**WHY:** Generating options from database/API on every form load = wasted resources. Cache once, reuse thousands of times.

```php
// CORRECT - cache in state system (faster than config for frequently-changing data)
$options = \Drupal::state()->get('mymodule.options');
if (!$options) {
  $options = $this->generateExpensiveOptions(); // Runs once per cache clear
  \Drupal::state()->set('mymodule.options', $options);
}
$form['field']['#options'] = $options;
// Impact: First load 500ms, subsequent loads <10ms

// OR cache in configuration (better for rarely-changing data)
$config = $this->config('mymodule.settings');
$options = $config->get('cached_options');
// Impact: Cached by configuration system, exported with config

// OR cache in custom cache bin (best for frequently-changing data)
$cid = 'mymodule:form:options';
if ($cache = \Drupal::cache()->get($cid)) {
  $options = $cache->data;
} else {
  $options = $this->generateExpensiveOptions();
  \Drupal::cache()->set($cid, $options, time() + 3600); // 1 hour TTL
}
```

**Cache Decision Matrix:**
```
Changes: Never → Configuration (exported with site config)
Changes: Daily → State API (simple, no export needed)
Changes: Hourly → Cache API with TTL
Changes: Per-request → Don't cache, use lazy load
```

**Pattern 3: Defer to Validation/Submit**

**WHY:** Entity loads in buildForm() run even when form not submitted. If form displayed 1000 times but submitted 10 times, you loaded entity 990 unnecessary times.

```php
// WRONG - loads entity every time form displays
public function buildForm(array $form, FormStateInterface $form_state) {
  $nid = 123;
  $node = \Drupal::entityTypeManager()
    ->getStorage('node')
    ->load($nid); // Runs on every display, AJAX, error
  $form['info']['#markup'] = $node->label(); // Just displaying label, not modifying
}
// Impact: 10-50ms wasted on every form view

// CORRECT - only load when actually needed
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['node_id'] = [
    '#type' => 'value',
    '#value' => 123, // Store ID only
  ];
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $nid = $form_state->getValue('node_id');
  $node = \Drupal::entityTypeManager()
    ->getStorage('node')
    ->load($nid); // Loads only on submit
  $node->setTitle($form_state->getValue('title'));
  $node->save();
}
// Impact: Saves 10-50ms on every form display
```

**Pattern 4: Use loadMultiple() Not load() in Loops**

**WHY:** N+1 query problem. Loading 100 entities individually = 100 database queries = 3-10 seconds.

```php
// WRONG - N+1 queries
$nids = [1, 2, 3, ..., 100]; // 100 node IDs
foreach ($nids as $nid) {
  $node = Node::load($nid); // 100 separate queries!
  $options[$nid] = $node->label();
}
// Impact: 3-10 seconds (100 queries × 30-100ms each)

// CORRECT - single query
$nids = [1, 2, 3, ..., 100];
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadMultiple($nids); // 1 query loads all
foreach ($nodes as $nid => $node) {
  $options[$nid] = $node->label();
}
// Impact: 50-200ms (1 query for all entities)
```

### Form Caching Strategy

**When to Enable Form Caching:**
| Scenario | Cache? | Why |
|----------|--------|-----|
| Multi-step form | Yes (REQUIRED) | Persist state across steps |
| Expensive #options generation | Yes | Avoid regenerating on rebuild |
| Frequent AJAX rebuilds | Yes | Reduce database queries |
| Simple single-step form | No | Unnecessary overhead |
| GET method form (search) | No | Not allowed |

**Implementation:**
```php
public function buildForm(array $form, FormStateInterface $form_state) {
  // Enable caching
  $form_state->setCached(TRUE);

  // Expensive operation runs once, cached
  if (!$form_state->has('expensive_data')) {
    $data = $this->expensiveOperation();
    $form_state->set('expensive_data', $data);
  }

  $form['field']['#options'] = $form_state->get('expensive_data');
}
```

**Cache Storage:**
```
Location: database cache_form table
Expiration: 6 hours default
Cleanup: Cron purges expired entries
```

### Validation Performance

**Expensive Validation (Avoid):**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  // SLOW - remote API call in validation
  $result = $this->remoteApi->validate($value);

  // SLOW - database query for every validate
  $exists = \Drupal::database()->query('SELECT ...');
}
```

**Better Patterns:**
```php
// Move remote validation to queue (async)
public function submitForm(array &$form, FormStateInterface $form_state) {
  \Drupal::queue('mymodule.validation')->createItem($data);
}

// Use batch for bulk validation
public function submitForm(array &$form, FormStateInterface $form_state) {
  $batch = [
    'operations' => [[$this, 'batchValidate'], [$items]],
  ];
  batch_set($batch);
}
```

**Good Validation (Fast):**
```
Format checks (regex, strlen)
In-memory comparisons
Required field checks
Range validation (>, <, between)
Type checks (is_numeric, etc.)
```

### Element-Level Optimization

**Avoid Nested Loops:**
```php
// SLOW - nested entity loads
foreach ($items as $item) {
  $entity = $storage->load($item['id']); // N+1 queries
}

// FAST - batch load
$ids = array_column($items, 'id');
$entities = $storage->loadMultiple($ids); // 1 query
```

**Library Attachment:**
```php
// Attach libraries only when needed
if ($complex_widget_needed) {
  $form['#attached']['library'][] = 'mymodule/complex-widget';
}

// Not on every form:
// $form['#attached']['library'][] = 'mymodule/rarely-used';
```

### AJAX Performance

**WHY AJAX Performance Matters:**

AJAX callbacks feel instant or feel broken - no middle ground. Users expect <300ms response time. Slow AJAX = perceived as broken, users click repeatedly, creates server load cascade.

**Performance Thresholds (User Perception):**
```
<100ms: Instant (excellent)
100-300ms: Responsive (acceptable)
300-1000ms: Noticeable lag (poor UX)
>1000ms: Broken (users abandon)
```

**AJAX Anti-Patterns (Avoid):**
```
✗ AJAX on every keyup
  Impact: 50+ requests for typing "hello world", server overload
  Example: Autocomplete without debouncing = DOS yourself

✗ Large render arrays in AJAX responses
  Impact: 100KB response = 500ms+ network time on mobile
  Example: Returning entire form instead of just updated container

✗ Complex AJAX callbacks with DB queries
  Impact: 200ms+ per callback, locks database, blocks other requests
  Example: Loading 50 related entities in AJAX callback

✗ AJAX when #states would work
  Impact: Network roundtrip (200ms) vs instant client-side (<1ms)
  Example: Show/hide based on checkbox = use #states
```

**Optimized AJAX Patterns:**
```
✓ AJAX on change/blur events (not keyup)
  Impact: 1 request per field change vs 10+ per word typed

✓ Return minimal render arrays
  Impact: 5KB response vs 100KB, 50ms vs 500ms render time
  Example: Return only updated container, not entire form

✓ Cache AJAX callback results
  Impact: 5ms cached vs 200ms database query
  Example: Country/state dropdown - cache state list

✓ Use client-side validation first
  Impact: 0ms vs 200ms roundtrip for simple validation
  Example: Email format validation via HTML5 pattern attribute

✓ Debounce AJAX autocomplete
  Impact: 3 requests vs 50+ for typing "example"
  Example: Wait 300ms after last keyup before triggering AJAX
```

**Concrete Example - Autocomplete Optimization:**
```php
// WRONG - no debouncing, triggers on every keyup
$form['search'] = [
  '#type' => 'textfield',
  '#ajax' => [
    'callback' => '::searchCallback',
    'event' => 'keyup', // 50+ AJAX requests for one search term!
  ],
];

// CORRECT - debounced, triggers after pause
$form['search'] = [
  '#type' => 'textfield',
  '#ajax' => [
    'callback' => '::searchCallback',
    'event' => 'change', // OR use custom JS with debounce
    'debounce' => 300, // Wait 300ms after last keystroke (Drupal 9.3+)
  ],
];
// Impact: 50+ requests reduced to 1-3 requests
```

**Reference:** [Performance Optimization Tips 2025](https://www.tutorials24x7.com/drupal/optimizing-drupal-website-performance-best-practices-for-2025)

### Monitoring and Profiling

**Identify Slow Forms:**
```php
// Add timing to log
$start = microtime(TRUE);
// ... form building ...
$duration = microtime(TRUE) - $start;
\Drupal::logger('mymodule')->debug('Form build time: @time', [
  '@time' => $duration,
]);
```

**Use Webprofiler Module (Development):**
```
Install devel and webprofiler modules
Enable profiling toolbar
Check form build time, query count
```

**Common Mistakes:**
- Loading entities in loops (use loadMultiple)
- Calling external APIs in buildForm()
- Not caching expensive #options
- Using AJAX when simple #states would work
- Not considering form rebuild impact

**See Also:**
- Cache API Guide
- Database Query Optimization
- Entity API Performance
- State API Guide
