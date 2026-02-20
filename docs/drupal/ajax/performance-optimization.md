---
description: Reduce AJAX response times — minimal DOM updates, batch processing, query limits, and CacheableAjaxResponse
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Apply these patterns when AJAX requests are slow, causing excessive database queries, large DOM updates, or timeouts on large operations.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Reduce DOM updates | Return smallest possible element | Replace only changed elements, not entire containers |
| Large operations | Batch API | Prevents timeout for >100 items or >30s operations |
| Fast repeated requests | CacheableAjaxResponse | Avoids redundant server processing |
| Efficient queries | Entity query with range() | Reduces database load and memory use |

## Pattern

```php
// Return smallest possible element (not entire form)
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  return $form['subcategory'];  // NOT $form
}

// Limit database results
private function loadItems($category_id) {
  $nids = $this->entityTypeManager->getStorage('node')->getQuery()
    ->condition('type', 'item')
    ->condition('field_category', $category_id)
    ->range(0, 50)    // Always limit results
    ->sort('title')
    ->accessCheck(TRUE)
    ->execute();

  return $this->entityTypeManager->getStorage('node')->loadMultiple($nids);
}

// Cacheable response for shared content
use Drupal\Core\Cache\CacheableAjaxResponse;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new CacheableAjaxResponse();
  $response->addCommand(new ReplaceCommand('#target', $content));
  $response->getCacheableMetadata()
    ->setCacheMaxAge(300)
    ->setCacheContexts(['user.permissions']);

  return $response;
}
```

**Performance thresholds:**

| Operation Type | Target Time | Action if Exceeded |
|----------------|-------------|--------------------|
| Simple field update | <200ms | Optimize query, reduce DOM update size |
| Autocomplete query | <500ms | Add result limit, index search fields |
| File upload (2MB) | <5s | Use progress bar, increase PHP limits |
| Batch operation | <30s total | Use Batch API with progress tracking |

Reference: `core/lib/Drupal/Core/Cache/CacheableAjaxResponse.php`

## Common Mistakes

- **Wrong**: Returning entire form when only one element changed → **Right**: Return only the specific element that changed
- **Wrong**: No result limits on database queries → **Right**: Memory exhaustion; always use `range(0, N)`
- **Wrong**: Not using Batch API for large operations → **Right**: Timeouts; use batch for >100 items
- **Wrong**: Caching user-specific content without context → **Right**: Data leaks; verify cache contexts match data sensitivity
- **Wrong**: No progress indicators for long operations → **Right**: Add progress for operations taking >2 seconds

## See Also

- [Response Caching](response-caching.md)
- [CSRF Protection](csrf-protection.md)
- Reference: `core/lib/Drupal/Core/Entity/Query/QueryInterface.php`
