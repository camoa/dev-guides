---
description: Extend mature plugin ecosystems with specialized implementations
drupal_version: "11.x"
---

# Foundation + Extension Pattern

## When to Use

> Use Foundation+Extension when mature plugin ecosystem exists (Commerce, Views). Use Provider Plugin when creating new service abstraction from scratch.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Mature plugin ecosystem exists in core/contrib | Foundation+Extension | Leverage proven systems and admin interfaces |
| Need entity integration with bundle fields | Foundation+Extension | `BundlePluginInterface` standard workflow |
| Want standard admin interfaces | Foundation+Extension | Existing configuration and management UI |
| Multiple plugin types work together | Foundation+Extension | Gateway + Method Type + Entity Type coordination |
| No existing ecosystem for your service | Provider Plugin | Need to create abstraction from scratch |

## Pattern

**Foundation Module** creates plugin ecosystem:

```yaml
# Foundation module service definition pattern
services:
  plugin.manager.foundation_service_gateway:
    class: Drupal\foundation_module\ServiceGatewayManager
    parent: default_plugin_manager
```

**Extension Module** specializes foundation:

```php
// Gateway + Method Type + Entity Type coordination
$gateway = $this->gatewayManager->createInstance('stripe');
$method_types = $gateway->getSupportedMethodTypes(); // ['credit_card', 'bank_transfer']

foreach ($method_types as $method_type_id) {
  $method_type = $this->methodTypeManager->createInstance($method_type_id);
  $fields = $method_type->buildFieldDefinitions(); // Entity bundle fields
}
```

**Key Architecture Elements**:
- Multiple plugin types with defined relationships
- Plugin managers for each type
- Standard admin interfaces and workflows
- Entity integration via `BundlePluginInterface`

## Common Mistakes

- **Wrong**: Creating new plugin manager when Commerce Payment exists → **Right**: Extend Commerce Payment gateway
- **Wrong**: Bypassing bundle field definitions → **Right**: Implement `buildFieldDefinitions()` for entity integration
- **Wrong**: Validation in plugin constructor → **Right**: Validation in plugin manager's `processDefinition()`

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Plugin Manager Implementation](plugin-manager-implementation.md)
- Reference: `/web/modules/contrib/commerce/modules/payment/`
- Reference: [Entity Bundle Plugins](https://www.drupal.org/project/entity)
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
