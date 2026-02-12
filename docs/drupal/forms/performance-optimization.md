---
description: Performance optimization — form rendering, caching, validation strategies
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Avoid expensive operations in buildForm(). Use entity_autocomplete for many options. Cache expensive #options generation.

## Decision

| Scenario | Strategy | Why |
|----------|----------|-----|
| >100 options | entity_autocomplete | Avoid loading all |
| Expensive options | Cache in state/config | Avoid regenerating |
| Entity loading | Defer to submit | Don't load in build |
| Multi-step form | setCached(TRUE) | Avoid rebuilding |
| Remote API calls | Queue/batch | Async processing |

## Expensive Operations to Avoid in buildForm()

```
Heavy database queries for #options (load thousands of nodes)
Entity loading in loops (N+1 query problem)
Remote API calls (timeout risk, slow response)
File system operations (disk I/O latency)
Complex calculations (heavy processing)
```

**Why It Matters:**
```
buildForm() runs on every page load
Cached forms still rebuild on form errors
AJAX rebuilds call buildForm() repeatedly
Slow buildForm = slow page load
```

## Optimization Patterns

**Pattern 1: Lazy-Load Options via AJAX**
```php
// Instead of loading 10,000 options:
$form['entity'] = [
  '#type' => 'select',
  '#options' => $this->loadThousandsOfOptions(), // SLOW
];

// Use entity autocomplete:
$form['entity'] = [
  '#type' => 'entity_autocomplete',
  '#target_type' => 'node',
  '#selection_settings' => ['target_bundles' => ['article']],
];
```

**Pattern 2: Cache Expensive Options**
```php
// Cache in state system
$options = \Drupal::state()->get('mymodule.options');
if (!$options) {
  $options = $this->generateExpensiveOptions();
  \Drupal::state()->set('mymodule.options', $options);
}
$form['field']['#options'] = $options;

// OR cache in configuration
$config = $this->config('mymodule.settings');
$options = $config->get('cached_options');
```

**Pattern 3: Defer to Validation/Submit**
```php
// DON'T load entity in buildForm:
public function buildForm(array $form, FormStateInterface $form_state) {
  $entity = \Drupal::entityTypeManager()
    ->getStorage('node')
    ->load($id); // Avoid unless necessary
}

// DO load in submit:
public function submitForm(array &$form, FormStateInterface $form_state) {
  $id = $form_state->getValue('entity_id');
  $entity = \Drupal::entityTypeManager()
    ->getStorage('node')
    ->load($id); // Only on submit
}
```

## Form Caching Strategy

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

## Validation Performance

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
- Format checks (regex, strlen)
- In-memory comparisons
- Required field checks
- Range validation (>, <, between)
- Type checks (is_numeric, etc.)

## Element-Level Optimization

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

// Not on every form
```

## AJAX Performance

**Avoid:**
- AJAX on every keyup (use debouncing)
- Large render arrays in AJAX responses
- Complex AJAX callbacks with DB queries

**Better:**
- AJAX on change/blur events
- Return minimal render arrays
- Cache AJAX callback results
- Use client-side validation first

## Common Mistakes

- **Wrong**: Loading entities in loops → **Right**: Use loadMultiple()
- **Wrong**: Calling external APIs in buildForm() → **Right**: Queue or defer
- **Wrong**: Not caching expensive #options → **Right**: Cache in state/config
- **Wrong**: Using AJAX when #states would work → **Right**: Prefer client-side
- **Wrong**: Not considering form rebuild impact → **Right**: Profile and optimize

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Forms](ajax-architecture.md)
- [Cache API](https://www.drupal.org/docs/drupal-apis/cache-api)
- [State API](https://www.drupal.org/docs/drupal-apis/state-api)
