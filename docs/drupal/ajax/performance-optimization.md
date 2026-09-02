---
description: Reduce AJAX response times — minimal DOM updates, batch processing, query limits, and CacheableAjaxResponse
tldr: "Apply these patterns when AJAX requests are slow, causing excessive database queries, large DOM updates, or timeouts on large operations."
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

AJAX requests are slow, causing excessive database queries, large DOM updates, or poor user experience.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Reduce DOM updates | Minimal wrapper updates | Replace only changed elements, not entire containers |
| Batch processing | Multiple callbacks or lazy loading | Prevents timeout on large operations |
| Fast repeated requests | Response caching | Avoids redundant server processing |
| Optimize database queries | Entity query optimization | Reduces database load |
| Reduce asset size | Library aggregation | Fewer HTTP requests |

## Pattern

```php
// Minimal DOM updates - return smallest possible element
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  // BAD: Returns entire form
  // return $form;

  // GOOD: Returns only changed element
  return $form['subcategory'];
}

// Batch processing for large operations
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['process'] = [
    '#type' => 'button',
    '#value' => t('Process Items'),
    '#ajax' => [
      'callback' => '::processBatch',
      'wrapper' => 'progress-wrapper',
      'progress' => [
        'type' => 'bar',
        'url' => Url::fromRoute('my_module.batch_progress')->toString(),
        'interval' => 1000,  // Check progress every second
      ],
    ],
  ];

  return $form;
}

public function processBatch(array &$form, FormStateInterface $form_state) {
  $batch = [
    'operations' => [
      [[$this, 'processBatchOp'], [range(0, 99)]],
    ],
    'finished' => [$this, 'batchFinished'],
  ];

  batch_set($batch);
  return batch_process();
}

// Database query optimization
private function loadItems($category_id) {
  $query = $this->entityTypeManager->getStorage('node')->getQuery()
    ->condition('type', 'item')
    ->condition('field_category', $category_id)
    ->range(0, 50)  // Limit results
    ->sort('title')
    ->accessCheck(TRUE);  // Use access check

  $nids = $query->execute();

  // Load only needed fields
  return $this->entityTypeManager->getStorage('node')
    ->loadMultiple($nids);
}

// Response caching (use cautiously - most AJAX is user-specific)
use Drupal\Core\Cache\CacheableAjaxResponse;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new CacheableAjaxResponse();
  $response->addCommand(new ReplaceCommand('#target', $content));

  // Cache for 5 minutes, vary by user permissions
  $response->getCacheableMetadata()
    ->setCacheMaxAge(300)
    ->setCacheContexts(['user.permissions']);

  return $response;
}
```

Reference: `core/lib/Drupal/Core/Cache/CacheableAjaxResponse.php`

## Common Mistakes

- Returning entire form when only one element changed → Massive DOM updates; return specific element
- No result limits on database queries → Memory exhaustion; always use `range(0, N)`
- Not using batch API for large operations → Timeouts; use batch for >100 items or >30 second operations
- Caching user-specific content → Data leaks; verify cache contexts match data sensitivity
- Loading all entity fields → Wasted memory; use entity query to load only needed fields
- Not using progress indicators → Users don't know if request is processing; add progress for >2 second operations

## See Also

- ← Previous: [CSRF Protection](csrf-protection.md) | Next: [Response Caching](response-caching.md)
- Reference: `core/lib/Drupal/Core/Entity/Query/QueryInterface.php`
