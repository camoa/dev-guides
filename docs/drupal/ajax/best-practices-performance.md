---
description: Performance standards for Drupal AJAX — DOM minimization, query limits, Batch API thresholds, and asset optimization
tldr: "Apply these standards to every AJAX implementation. Slow AJAX destroys UX."
drupal_version: "11.x"
---

# Best Practices: Performance

## When to Use

AJAX requests are slow, database queries are inefficient, or large operations cause timeouts.

## Performance Optimization Strategies

**Performance Optimization Strategies:**

1. **Minimize DOM Updates**
   - Return smallest possible element, not entire form
   - Use HtmlCommand instead of ReplaceCommand when wrapper unchanged
   - Batch multiple updates into single AJAX response

2. **Database Optimization**
   - Always use `range(0, N)` to limit query results
   - Load only needed fields with `loadMultiple()` instead of full entities
   - Use `accessCheck(TRUE)` to leverage query access caching
   - Index custom fields used in AJAX queries

3. **Batch Processing**
   - Use Batch API for operations processing >100 items
   - Set progress indicators for operations >2 seconds
   - Break large operations into chunks to prevent timeouts

4. **Caching**
   - Use CacheableAjaxResponse for cacheable content
   - Configure proper cache contexts (user.permissions, languages, etc.)
   - Add cache tags for automatic invalidation
   - Set realistic max-age (match content update frequency)

5. **Asset Optimization**
   - Aggregate JavaScript/CSS in production
   - Use `#attached` libraries instead of AddJsCommand/AddCssCommand
   - Lazy load libraries only when needed
   - Minimize third-party dependencies

## Performance Thresholds

**Performance Thresholds:**

| Operation Type | Target Time | Action if Exceeded |
|---|---|---|
| Simple form field update | <200ms | Optimize query, reduce DOM update size |
| Autocomplete query | <500ms | Add result limit, index search fields |
| File upload | <5s for 2MB | Use progress bar, increase PHP limits |
| Batch operation | <30s total | Use Batch API with progress tracking |

## Pattern

```php
// 1. Return smallest element
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  return $form['subcategory'];  // NOT return $form
}

// 2. Always limit query results
$nids = $this->entityTypeManager->getStorage('node')->getQuery()
  ->condition('type', 'article')
  ->range(0, 50)
  ->accessCheck(TRUE)
  ->execute();

// 3. Use Batch API for large operations (>100 items / >30 seconds)
public function processBatch(array &$form, FormStateInterface $form_state) {
  $batch = [
    'operations' => [[[$this, 'processBatchOp'], [range(0, 99)]]],
    'finished' => [$this, 'batchFinished'],
  ];
  batch_set($batch);
  return batch_process();
}

// 4. Use #attached instead of AddCssCommand/AddJsCommand
$build['#attached']['library'][] = 'my_module/dynamic-feature';

// 5. Progress indicator for slow operations
$form['trigger']['#ajax']['progress'] = [
  'type' => 'bar',
  'url' => Url::fromRoute('my_module.batch_progress')->toString(),
  'interval' => 1000,
];
```

## See Also

- ← Previous: [Best Practices: Security](best-practices-security.md) | Next: [Best Practices: Development Standards](best-practices-development.md)
- [Performance Optimization](performance-optimization.md)
- [Response Caching](response-caching.md)
- Reference: [Database performance best practices](https://www.drupal.org/docs/develop/using-the-entity-api/database-abstraction-layer)
