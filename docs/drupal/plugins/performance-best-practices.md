---
description: Performance optimization for plugin discovery, instantiation, and external API calls
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

> Apply these patterns to any plugin system handling more than a handful of plugins or processing external API calls.

## Decision

| Issue | Solution | Why |
|-------|----------|-----|
| Slow plugin discovery | Use `CachedDiscovery` (default in `DefaultPluginManager`) | Discovery scans filesystem on every request without caching |
| Provider API latency | Implement proxy caching with cache tags | External API calls add 100-500ms per request |
| Large plugin definitions | Use `service_id_collector` for lazy loading | Loading all services on every request wastes memory |
| Service collector overhead | Aggregate during container compilation, not runtime | Container rebuild is rare; runtime collection is every request |
| Plugin instantiation cost | Use `MapFactory` for lightweight instantiation | Full DI container resolution per plugin is expensive |

## Pattern

**Plugin Discovery Caching**:

```php
// DefaultPluginManager extends CachedDiscoveryInterface automatically
class MyPluginManager extends DefaultPluginManager {
  public function __construct(\Traversable $namespaces, CacheBackendInterface $cache_backend, ModuleHandlerInterface $module_handler) {
    parent::__construct(
      'Plugin/MyPluginType',
      $namespaces,
      $module_handler,
      'Drupal\my_module\Plugin\MyPluginTypeInterface',
      'Drupal\my_module\Annotation\MyPluginType'
    );
    $this->setCacheBackend($cache_backend, 'my_plugin_type_plugins');
  }
}
```

**Provider API Caching**:

```php
// Cache provider responses with invalidation
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

**Lazy Service Collection**:

```yaml
# Use service_id_collector for lazy loading
services:
  my_module.service_manager:
    class: Drupal\my_module\ServiceManager
    tags:
      - { name: 'service_id_collector', tag: 'my_module_service', call: 'addServiceId' }
```

```php
// Load service only when needed
public function getService($service_id) {
  if (!isset($this->services[$service_id])) {
    $this->services[$service_id] = $this->container->get($service_id);
  }
  return $this->services[$service_id];
}
```

**Check Before Instantiate**:

```php
// Use hasDefinition() to avoid expensive exception handling
public function getPlugin($plugin_id, array $config = []) {
  if (!$this->pluginManager->hasDefinition($plugin_id)) {
    $this->logger->warning('Plugin @id not found', ['@id' => $plugin_id]);
    return NULL;
  }
  return $this->pluginManager->createInstance($plugin_id, $config);
}
```

## Common Mistakes

- **Wrong**: Calling `getDefinitions()` in hot paths → **Right**: Cache results at request level or use `hasDefinition()`
- **Wrong**: Not using `hasDefinition()` before `createInstance()` → **Right**: Check existence to avoid expensive exception handling
- **Wrong**: Loading all providers to find one → **Right**: Use capability-based discovery to filter first
- **Wrong**: No timeout on external provider calls → **Right**: Set reasonable timeouts (30s default, configurable)

## See Also

- [Plugin Manager Implementation](plugin-manager-implementation.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: [Plugin API Performance](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Drupal Cache API](https://www.drupal.org/docs/drupal-apis/cache-api)
