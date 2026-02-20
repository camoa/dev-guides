---
description: Cache AJAX responses for public or permission-gated content using CacheableAjaxResponse with tags and contexts
drupal_version: "11.x"
---

# Response Caching

## When to Use

> Use CacheableAjaxResponse for AJAX responses containing cacheable data: public content, configuration results, or expensive calculations that don't vary per user. Do not cache user-specific data without proper cache contexts.

## Pattern

```php
use Drupal\Core\Cache\CacheableAjaxResponse;
use Drupal\Core\Cache\CacheableMetadata;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new CacheableAjaxResponse();

  $content = $this->buildContent();  // Expensive operation
  $response->addCommand(new ReplaceCommand('#target', $content));

  $cache_metadata = new CacheableMetadata();
  $cache_metadata->setCacheMaxAge(3600);  // 1 hour
  $cache_metadata->setCacheContexts([
    'user.permissions',               // Vary by permissions
    'languages:language_interface',   // Vary by language
  ]);
  $cache_metadata->setCacheTags([
    'node_list:article',              // Invalidate on article changes
    'config:my_module.settings',      // Invalidate on config changes
  ]);

  $response->addCacheableDependency($cache_metadata);

  return $response;
}
```

Reference: `core/lib/Drupal/Core/Cache/CacheableAjaxResponse.php`

## Common Mistakes

- **Wrong**: Caching user-specific data without context → **Right**: Privacy leak; always include `user` or `user.permissions` context
- **Wrong**: Missing cache tags → **Right**: Stale data after content updates; add all relevant entity/config tags
- **Wrong**: Over-aggressive max-age → **Right**: Users see stale content; match max-age to content update frequency
- **Wrong**: Caching error responses → **Right**: Errors cached indefinitely; only cache successful responses
- **Wrong**: Not understanding cache contexts → **Right**: Wrong content shown to users; review [cache contexts docs](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts)

## See Also

- [Performance Optimization](performance-optimization.md)
- [WCAG Compliance Patterns](wcag-compliance-patterns.md)
- Reference: [Cache API documentation](https://www.drupal.org/docs/drupal-apis/cache-api)
