---
description: Performance optimization for plugin discovery, instantiation, and external API calls
tldr: "Apply these patterns to any plugin system handling more than a handful of plugins or processing external API calls."
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

> Any plugin system handling more than a handful of plugins or processing external API calls.

## Decision

| Issue | Solution | Why |
|-------|----------|-----|
| Slow plugin discovery | Use `CachedDiscovery` (default in `DefaultPluginManager`) | Discovery scans filesystem on every request without caching |
| Provider API latency | Implement proxy caching with cache tags | External API calls add 100-500ms per request |
| Large plugin definitions | Use `service_id_collector` for lazy loading | Loading all services on every request wastes memory |
| Service collector overhead | Aggregate during container compilation, not runtime | Container rebuild is rare; runtime collection is every request |
| Plugin instantiation cost | Use `MapFactory` for lightweight instantiation | Full DI container resolution per plugin is expensive |

## Pattern

**Plugin discovery caching** - `DefaultPluginManager` implements `CachedDiscoveryInterface`, but only caches once you give it a backend:

```php
class MyPluginManager extends DefaultPluginManager {

  public function __construct(\Traversable $namespaces, CacheBackendInterface $cache_backend, ModuleHandlerInterface $module_handler) {
    parent::__construct(
      'Plugin/MyPluginType',
      $namespaces,
      $module_handler,
      'Drupal\my_module\Plugin\MyPluginTypeInterface',
      'Drupal\my_module\Attribute\MyPluginType',
      'Drupal\my_module\Annotation\MyPluginType'
    );
    $this->setCacheBackend($cache_backend, 'my_plugin_type_plugins');
  }
}
```

The fifth argument is the **attribute** class and the sixth the annotation class kept for backward compatibility. Passing an annotation class in the attribute position triggers a deprecation in Drupal 11.2 and stops working in Drupal 12.

**Provider response caching** - tag the entry so a provider change can invalidate it:

```php
public function executeWithCache($operation, $data) {
  $cid = 'provider:' . $this->providerId . ':' . md5(serialize($data));

  if ($cached = $this->cache->get($cid)) {
    return $cached->data;
  }

  $result = $this->provider->execute($operation, $data);

  $this->cache->set($cid, $result, Cache::PERMANENT, [
    'provider:' . $this->providerId,
    'provider_operation:' . $operation,
  ]);

  return $result;
}
```

**Check before instantiate** - `hasDefinition()` costs a lookup, a failed `createInstance()` costs an exception:

```php
public function getPlugin($plugin_id, array $config = []) {
  if (!$this->pluginManager->hasDefinition($plugin_id)) {
    $this->logger->warning('Plugin @id not found', ['@id' => $plugin_id]);
    return NULL;
  }
  return $this->pluginManager->createInstance($plugin_id, $config);
}
```

## Common Mistakes

- **Calling `getDefinitions()` in hot paths** → WHY: Even cached, deserialization of large definition arrays is expensive
- **Not using `hasDefinition()` before `createInstance()`** → WHY: Failed instantiation throws exceptions which are expensive
- **Loading all providers to find one** → WHY: Use capability-based discovery (`getProvidersByCapability()`) to filter first
- **No timeout on external provider calls** → WHY: One slow provider blocks the entire request

## See Also

- [Plugin Manager Implementation](plugin-manager-implementation.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: [Plugin API Performance](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Drupal Cache API](https://www.drupal.org/docs/drupal-apis/cache-api)
