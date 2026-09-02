---
description: Cache AJAX responses for public or permission-gated content using CacheableAjaxResponse with tags and contexts
tldr: "Use CacheableAjaxResponse for AJAX responses containing cacheable data: public content, configuration results, or expensive calculations that don't vary per user. Do not cache user-specific data without proper cache contexts."
drupal_version: "11.x"
---

# Response Caching

## When to Use

AJAX responses contain cacheable data (public content, configuration, expensive calculations) that doesn't vary by user.

## Pattern

```php
use Drupal\Core\Cache\CacheableAjaxResponse;
use Drupal\Core\Cache\CacheableMetadata;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new CacheableAjaxResponse();

  $content = $this->buildContent();  // Expensive operation
  $response->addCommand(new ReplaceCommand('#target', $content));

  // Configure caching
  $cache_metadata = new CacheableMetadata();
  $cache_metadata->setCacheMaxAge(3600);  // 1 hour
  $cache_metadata->setCacheContexts([
    'user.permissions',  // Vary by permissions
    'languages:language_interface',  // Vary by language
  ]);
  $cache_metadata->setCacheTags([
    'node_list:article',  // Invalidate when article nodes change
    'config:my_module.settings',  // Invalidate when config changes
  ]);

  $response->addCacheableDependency($cache_metadata);

  return $response;
}
```

Reference: `core/lib/Drupal/Core/Cache/CacheableAjaxResponse.php`

## Common Mistakes

- Caching user-specific data without context → Privacy leak; always include 'user' or 'user.permissions' context
- Missing cache tags → Stale data after content updates; add all relevant entity/config tags
- Over-aggressive max-age → Users see stale content; match max-age to content update frequency
- Caching error responses → Errors cached indefinitely; only cache successful responses
- Not understanding cache contexts → Data shows wrong content; review [cache contexts documentation](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts)

## See Also

- ← Previous: [Performance Optimization](performance-optimization.md) | Next: [WCAG Compliance Patterns](wcag-compliance-patterns.md)
- Reference: [Cache API documentation](https://www.drupal.org/docs/drupal-apis/cache-api)
