---
description: Cache API calls, batch entity loading, and optimize token access in ECA plugins
drupal_version: "11.x"
---

# Performance Patterns

## When to Use

> Apply performance optimizations when plugins perform expensive operations like external API calls, complex calculations, or repeated database queries. Cache results, batch operations, and avoid N+1 queries.

## Decision

| Operation Type | Optimization | When to Apply |
|----------------|--------------|---------------|
| External API calls | Cache results | API call takes >100ms |
| Complex calculations | Cache computed values | Calculation used multiple times |
| Entity loading | Use entity loader service | Loading multiple entities |
| Repeated token access | Store in variable | Same token accessed 3+ times |
| Database queries | Batch operations | Processing >10 items |

## Pattern

```php
use Drupal\Core\Cache\CacheBackendInterface;

class MyAction extends ConfigurableActionBase {

  protected CacheBackendInterface $cache;

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
    $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
    $instance->cache = $container->get('cache.default');
    return $instance;
  }

  public function execute(): void {
    // Cache expensive API calls
    $cache_key = 'my_module:api_result:' . md5(serialize($this->configuration));

    if ($cached = $this->cache->get($cache_key)) {
      $result = $cached->data;
    } else {
      $result = $this->callExpensiveApi();

      // Cache for 1 hour
      $this->cache->set($cache_key, $result, time() + 3600, ['my_module_api']);
    }

    $this->tokenService->addTokenData($this->configuration['result_token'], $result);
  }

  /**
   * Batch entity loading to avoid N+1 queries.
   */
  protected function batchLoadEntities(array $ids): array {
    // Bad: Loading one by one in loop
    // foreach ($ids as $id) { $entity = Entity::load($id); }

    // Good: Batch load all at once
    return $this->entityTypeManager
      ->getStorage('node')
      ->loadMultiple($ids);
  }

  /**
   * Store frequently accessed tokens in variables.
   */
  protected function processItems(): void {
    // Bad: Accessing token in loop
    // foreach ($items as $item) {
    //   $config = $this->tokenService->getTokenData('config');
    // }

    // Good: Access once, use many times
    $config = $this->tokenService->getTokenData('config');
    foreach ($items as $item) {
      $this->processWithConfig($item, $config);
    }
  }
}
```

## Common Mistakes

- **Wrong**: No cache invalidation → **Right**: Stale data persists indefinitely (use cache tags)
- **Wrong**: Caching user-specific data in shared cache → **Right**: Privacy/security issue
- **Wrong**: Loading entities in loops → **Right**: N+1 query problem (use loadMultiple)
- **Wrong**: Not setting cache expiration → **Right**: Memory bloat over time
- **Wrong**: Premature optimization → **Right**: Profile first, then optimize hot paths
- **Wrong**: Caching in development → **Right**: Can't see changes (clear cache or disable caching)

## See Also

- [Security Best Practices](security-best-practices.md) for secure caching
- [Advanced Action Patterns](advanced-action-patterns.md) for API patterns
- [Debugging Workflows](debugging-workflows.md) for profiling

**References:**
- Drupal: https://api.drupal.org/api/drupal/core!core.api.php/group/cache
- Performance: https://www.drupal.org/docs/drupal-apis/cache-api
