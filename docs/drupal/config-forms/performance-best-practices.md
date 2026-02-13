---
description: Optimize configuration forms to avoid performance bottlenecks
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

> Optimize configuration forms to avoid performance bottlenecks, especially forms with many operations or large datasets.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Load 100+ entities in form | Pagination or lazy loading | Avoid memory issues, faster page load |
| Many operations per row | #type operations (not individual links) | Single dropbutton render, not N renders |
| Entity access checks | Load entities in bulk, check once | N+1 query problem |
| Complex form with conditions | #states instead of AJAX | Client-side, no server round-trip |
| Form with file uploads | Upload progress tracking | Better UX, avoid timeouts |

## Pattern

**1. Bulk Loading**:
```php
// WRONG: N+1 queries
foreach ($ids as $id) {
  $entity = $this->entityTypeManager->getStorage('node')->load($id);
  // Process entity...
}

// RIGHT: Bulk load
$entities = $this->entityTypeManager->getStorage('node')->loadMultiple($ids);
foreach ($entities as $entity) {
  // Process entity...
}
```

**2. Pagination**:
```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $page = \Drupal::request()->query->get('page', 0);
  $limit = 50;

  $query = $this->entityTypeManager->getStorage('node')->getQuery()
    ->accessCheck(TRUE)
    ->range($page * $limit, $limit);

  $ids = $query->execute();
  $entities = $this->entityTypeManager->getStorage('node')->loadMultiple($ids);

  // Build form with paginated data...

  // Add pager
  $form['pager'] = [
    '#type' => 'pager',
  ];
}
```

**3. Conditional Fields (Client-Side)**:
```php
$form['enable_feature'] = [
  '#type' => 'checkbox',
  '#title' => $this->t('Enable feature'),
];

$form['feature_settings'] = [
  '#type' => 'fieldset',
  '#title' => $this->t('Feature settings'),
  '#states' => [
    'visible' => [
      ':input[name="enable_feature"]' => ['checked' => TRUE],
    ],
  ],
];
```

**4. Caching Form Options**:
```php
public function buildForm(array $form, FormStateInterface $form_state) {
  // Cache expensive option loading
  $cid = 'mymodule:form_options';
  if ($cache = \Drupal::cache()->get($cid)) {
    $options = $cache->data;
  }
  else {
    $options = $this->loadExpensiveOptions();
    \Drupal::cache()->set($cid, $options, Cache::PERMANENT, ['mymodule:options']);
  }

  $form['option'] = [
    '#type' => 'select',
    '#options' => $options,
  ];
}
```

**Performance Thresholds**:
- **< 50 items**: Load all, no pagination needed
- **50-200 items**: Consider pagination, depends on entity complexity
- **> 200 items**: Always paginate or use autocomplete
- **> 1000 operations**: Use Views instead of custom form

## Common Mistakes

- **Wrong**: Loading all entities without pagination → **Right**: Out of memory on large datasets
- **Wrong**: Using AJAX for simple show/hide → **Right**: #states is faster, no server load
- **Wrong**: Not bulk loading entities → **Right**: N+1 query problem
- **Wrong**: Not caching expensive computations → **Right**: Slow form builds on every page load
- **Wrong**: Loading entities just to count them → **Right**: Use countQuery() instead
- **Wrong**: Not setting cache tags on cached form options → **Right**: Stale data after updates

## See Also

- [Security Best Practices](security-best-practices.md)
- [Common Mistakes](common-mistakes.md)
- Reference: core/modules/views/src/Form/ViewsFormMainForm.php
- Reference: Entity API documentation, Drupal performance best practices
