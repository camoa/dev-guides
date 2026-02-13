---
description: Register plugin managers and service collectors for plugin discovery
drupal_version: "11.x"
---

# Plugin Manager Implementation

## When to Use

> Use plugin manager for Foundation+Extension and Provider Plugin patterns. Use service collector for Service Collector pattern. Choose based on whether you need annotation-based discovery (plugin manager) or tagged service discovery (service collector).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Annotation-based plugin discovery | Plugin Manager | Scan directories for `@PluginID` annotations |
| Multiple configured instances | Plugin Manager | `createInstance()` with configuration array |
| Plugin alterations needed | Plugin Manager | Support for `hook_plugin_info_alter` |
| Simple tagged service aggregation | Service Collector | Auto-discovered during container compilation |
| REST API-first architecture | Service Collector | Built-in JSON serialization |

## Pattern

**Plugin Manager Registration**:

```yaml
# module.services.yml
services:
  _defaults:
    autowire: true

  # Foundation Pattern - Multiple Managers
  plugin.manager.foundation_service_gateway:
    class: Drupal\foundation_module\ServiceGatewayManager
    parent: default_plugin_manager

  # Provider Pattern - Single Manager with Proxy
  my_module.service_provider:
    class: Drupal\my_module\ServiceProviderPluginManager
    parent: default_plugin_manager
    arguments: ['@service_container']
```

**Service Collector Registration**:

```yaml
# Service Collector Pattern - Manager with Tagged Collection
services:
  orchestration.services_manager:
    class: Drupal\orchestration\ServicesProviderManager
    tags:
      - { name: 'service_collector', tag: 'orchestration_services_provider', call: 'addServicesProvider' }
```

**Plugin Manager Key Methods**:
- `getDefinitions()` - Get all plugin definitions
- `createInstance($plugin_id, array $configuration)` - Instantiate plugin
- `hasDefinition($plugin_id)` - Check if plugin exists

**Service Collector Key Methods**:
- `addServicesProvider(ServicesProviderInterface $provider)` - Called by service collector
- `getAllServices()` - Aggregate services from all providers
- `executeService($serviceId, array $config)` - Execute specific service

## Common Mistakes

- **Wrong**: Using plugin manager for stateless REST API services → **Right**: Use service collector with tagged services
- **Wrong**: Not calling `hasDefinition()` before `createInstance()` → **Right**: Check existence to avoid expensive exception handling
- **Wrong**: Multiple service collector tags on one service → **Right**: One tag per service, manager aggregates across all tagged services

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: `/web/core/lib/Drupal/Core/Plugin/DefaultPluginManager.php`
- Reference: [Service Tags Documentation](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags)
- Reference: [Service ID Collector Pattern](https://www.drupal.org/node/2598944)
