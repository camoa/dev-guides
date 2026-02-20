---
description: Performance standards for Drupal AJAX — DOM minimization, query limits, Batch API thresholds, and asset optimization
drupal_version: "11.x"
---

# Best Practices: Performance

## When to Use

> Apply these standards to every AJAX implementation. Slow AJAX destroys UX. Set performance expectations before building, not after.

## Decision

| Operation Type | Target Time | Action if Exceeded |
|----------------|-------------|--------------------|
| Simple field update | <200ms | Optimize query, reduce DOM update size |
| Autocomplete query | <500ms | Add result limit, index search fields |
| File upload (2MB) | <5s | Use progress bar, increase PHP limits if needed |
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

## Common Mistakes

- **Wrong**: Returning entire form when one element changed → **Right**: Return only the specific element that changed
- **Wrong**: No result limits on database queries → **Right**: Memory exhaustion; always use `range(0, N)`
- **Wrong**: Not using Batch API for large operations → **Right**: PHP timeouts; use batch for >100 items or >30s operations
- **Wrong**: Loading unused entity fields → **Right**: Use targeted entity queries; avoid loading full entity graphs
- **Wrong**: No progress indicator for long operations → **Right**: Users assume the request failed; show progress for >2s operations

## See Also

- [Performance Optimization](performance-optimization.md)
- [Response Caching](response-caching.md)
- Reference: [Database performance best practices](https://www.drupal.org/docs/develop/using-the-entity-api/database-abstraction-layer)
