---
description: Form performance optimization - rendering, caching, validation, and AJAX performance
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Optimize forms when buildForm() takes >200ms, AJAX callbacks >300ms, or you have >50 options. Target: <1s load, <2s submit.

## Decision

| Situation | Optimization | Why |
|-----------|--------------|-----|
| >50 options in select | entity_autocomplete | 200KB+ HTML, slow DOM rendering |
| Expensive options generation | Cache in State/Config | Generate once, reuse thousands of times |
| Entity loads in buildForm() | Defer to submit | buildForm() runs on every rebuild |
| N+1 query pattern | loadMultiple() | 100 queries → 1 query |
| AJAX on keyup | Debounce or use 'change' | 50+ requests → 1-3 requests |

## Critical Rule: What NOT to Put in buildForm()

buildForm() runs on:
- Initial display
- Every AJAX callback
- Every validation error
- Every multi-step navigation
- Every form alter hook

**Avoid:**
- Heavy database queries (>100 rows): 1-5s per query
- Entity loading in loops (N+1): 100 entities = 3-10s
- Remote API calls: 500ms-10s, timeout risk
- File system operations: 50-500ms per file
- Complex calculations: 100ms-5s depending on complexity

## Pattern 1: Use Autocomplete for Large Sets

```php
// WRONG - 10,000 options = 5 second page load
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadByProperties(['type' => 'article']); // 10,000 nodes!
$options = [];
foreach ($nodes as $node) {
  $options[$node->id()] = $node->label();
}
$form['article'] = [
  '#type' => 'select',
  '#options' => $options, // 200KB+ HTML
];

// CORRECT - lazy load via autocomplete
$form['article'] = [
  '#type' => 'entity_autocomplete',
  '#target_type' => 'node',
  '#selection_settings' => ['target_bundles' => ['article']],
];
```

**Decision threshold:**
- <20 options: radios/checkboxes
- 20-50 options: select dropdown
- >50 options: entity_autocomplete (REQUIRED)
- >1000 options: Custom AJAX autocomplete

## Pattern 2: Cache Expensive Options

```php
// CORRECT - cache in state system
$options = \Drupal::state()->get('mymodule.options');
if (!$options) {
  $options = $this->generateExpensiveOptions(); // Once per cache clear
  \Drupal::state()->set('mymodule.options', $options);
}
$form['field']['#options'] = $options;

// OR cache in custom cache bin
$cid = 'mymodule:form:options';
if ($cache = \Drupal::cache()->get($cid)) {
  $options = $cache->data;
} else {
  $options = $this->generateExpensiveOptions();
  \Drupal::cache()->set($cid, $options, time() + 3600); // 1 hour TTL
}
```

**Cache decision:**
- Never changes: Configuration
- Changes daily: State API
- Changes hourly: Cache API with TTL
- Per-request: Don't cache, use lazy load

## Pattern 3: Defer to Validation/Submit

```php
// WRONG - loads entity every display
public function buildForm(array $form, FormStateInterface $form_state) {
  $node = Node::load(123); // Runs on every rebuild!
}

// CORRECT - only load when needed
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['node_id'] = ['#type' => 'value', '#value' => 123];
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $nid = $form_state->getValue('node_id');
  $node = Node::load($nid); // Only on submit
}
```

## Pattern 4: Use loadMultiple()

```php
// WRONG - N+1 queries (3-10 seconds)
$nids = [1, 2, 3, ..., 100];
foreach ($nids as $nid) {
  $node = Node::load($nid); // 100 queries!
  $options[$nid] = $node->label();
}

// CORRECT - single query (50-200ms)
$nids = [1, 2, 3, ..., 100];
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadMultiple($nids); // 1 query
foreach ($nodes as $nid => $node) {
  $options[$nid] = $node->label();
}
```

## Form Caching Strategy

| Scenario | Cache? | Why |
|----------|--------|-----|
| Multi-step form | Yes (REQUIRED) | Persist state across steps |
| Expensive #options | Yes | Avoid regenerating on rebuild |
| Frequent AJAX rebuilds | Yes | Reduce database queries |
| Simple single-step | No | Unnecessary overhead |

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form_state->setCached(TRUE); // Enable caching

  // Expensive operation runs once, cached
  if (!$form_state->has('expensive_data')) {
    $data = $this->expensiveOperation();
    $form_state->set('expensive_data', $data);
  }
}
```

## AJAX Performance

**User Perception Thresholds:**
- <100ms: Instant (excellent)
- 100-300ms: Responsive (acceptable)
- 300-1000ms: Noticeable lag (poor UX)
- >1000ms: Broken (users abandon)

**AJAX Anti-Patterns:**
- AJAX on every keyup → Use debounce or 'change' event
- Large render arrays → Return minimal containers
- Complex AJAX callbacks → Cache results
- AJAX when #states works → Use #states (instant)

```php
// WRONG - no debouncing
$form['search'] = [
  '#type' => 'textfield',
  '#ajax' => [
    'callback' => '::searchCallback',
    'event' => 'keyup', // 50+ requests!
  ],
];

// CORRECT - debounced
$form['search'] = [
  '#type' => 'textfield',
  '#ajax' => [
    'callback' => '::searchCallback',
    'event' => 'change', // OR custom JS with debounce
    'debounce' => 300, // Drupal 9.3+
  ],
];
```

## Common Mistakes

- **Wrong**: Loading entities in loops → **Right**: Use loadMultiple()
- **Wrong**: External APIs in buildForm() → **Right**: Defer to submit or use queue
- **Wrong**: Not caching expensive #options → **Right**: Cache in State/Config/Cache
- **Wrong**: AJAX when #states works → **Right**: #states is instant
- **Wrong**: No performance monitoring → **Right**: Use Webprofiler in dev

## See Also

- [Cache API Guide](https://www.drupal.org/docs/drupal-apis/cache-api)
- [Entity API Performance](https://www.drupal.org/docs/drupal-apis/entity-api)
- [State API Guide](https://www.drupal.org/docs/drupal-apis/state-api)
- Reference: [Performance Optimization 2025](https://kinematic.digital/index.php/2025/06/20/advanced-drupal-performance-optimization-techniques/)
