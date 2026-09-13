---
description: Extend mature plugin ecosystems with specialized implementations
tldr: "Use Foundation+Extension when mature plugin ecosystem exists (Commerce, Views). Use Provider Plugin when creating new service abstraction from scratch."
drupal_version: "11.x"
---

# Foundation + Extension Pattern

## When to Use

> ✅ **Mature plugin ecosystem exists** in core or contrib
> ✅ **Need entity integration** with bundle field definitions
> ✅ **Want standard admin interfaces** and configuration workflows
> ✅ **Extending proven systems** rather than creating new abstractions
> ✅ **Multiple plugin types** work together (gateway + method type + entity type)

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Mature plugin ecosystem exists in core/contrib | Foundation+Extension | Leverage proven systems and admin interfaces |
| Need entity integration with bundle fields | Foundation+Extension | `BundlePluginInterface` standard workflow |
| Want standard admin interfaces | Foundation+Extension | Existing configuration and management UI |
| Multiple plugin types work together | Foundation+Extension | Gateway + Method Type + Entity Type coordination |
| No existing ecosystem for your service | Provider Plugin | Need to create abstraction from scratch |

## Architecture Overview

**Foundation Module** creates plugin ecosystem:
- Multiple plugin types with defined relationships
- Plugin managers for each type
- Standard admin interfaces and workflows
- Entity integration via `BundlePluginInterface`

**Extension Modules** specialize foundation:
- Create service-specific plugin implementations
- Extend base interfaces with specialized methods
- Use existing plugin managers and infrastructure
- Focus on service optimization rather than abstraction

## Pattern

**Pattern Reference**: `/web/modules/contrib/commerce/modules/payment/` (foundation)
**Extension Reference**: `/web/modules/contrib/commerce_stripe/` (extension)

**Key Interfaces**:
- `/web/modules/contrib/commerce/modules/payment/src/Plugin/Commerce/PaymentGateway/PaymentGatewayInterface.php`
- `/web/modules/contrib/commerce/modules/payment/src/Plugin/Commerce/PaymentMethodType/PaymentMethodTypeInterface.php`

**Plugin Managers**:
- `/web/modules/contrib/commerce/modules/payment/src/PaymentGatewayManager.php`
- `/web/modules/contrib/commerce/modules/payment/src/PaymentMethodTypeManager.php`

**Entity Integration**:
- Reference: `/web/modules/contrib/commerce/modules/payment/src/Entity/PaymentMethod.php`
- Bundle Plugin Interface: `Drupal\entity\BundlePlugin\BundlePluginInterface`

**Service Registration**:

```yaml
# Foundation module service definition pattern
services:
  plugin.manager.foundation_service_gateway:
    class: Drupal\foundation_module\ServiceGatewayManager
    parent: default_plugin_manager
```

## Critical Pattern Elements

1. **Multiple Plugin Types**: Gateway + Method Type + Entity Type working together
2. **Validation in Plugin Manager**: `processDefinition()` validates each plugin definition at discovery time (Commerce's `PaymentGatewayManager` and `PaymentMethodTypeManager` both override it)
3. **Bundle Field Definitions**: `buildFieldDefinitions()` for entity integration
4. **Service Method Relationship**: Gateways specify supported method types in annotation

## Common Mistakes

- **Creating a new plugin manager when Commerce Payment already exists** → WHY: The foundation already ships the gateway, method-type and entity plumbing, so reimplementing it forfeits the admin UI
- **Bypassing bundle field definitions** → WHY: Without `buildFieldDefinitions()` the plugin contributes no fields to the entity bundle
- **Validating in the plugin constructor** → WHY: The constructor runs on every instantiation; `processDefinition()` runs once per definition at discovery time and rejects a bad plugin before it is ever built

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Plugin Manager Implementation](plugin-manager-implementation.md)
- Reference: `/web/modules/contrib/commerce/modules/payment/` (foundation)
- Reference: `/web/modules/contrib/commerce_stripe/` (extension)
- Reference: `/web/modules/contrib/commerce/modules/payment/src/Plugin/Commerce/PaymentGateway/PaymentGatewayInterface.php`
- Reference: `/web/modules/contrib/commerce/modules/payment/src/Plugin/Commerce/PaymentMethodType/PaymentMethodTypeInterface.php`
- Reference: `/web/modules/contrib/commerce/modules/payment/src/PaymentGatewayManager.php`
- Reference: `/web/modules/contrib/commerce/modules/payment/src/PaymentMethodTypeManager.php`
- Reference: `/web/modules/contrib/commerce/modules/payment/src/Entity/PaymentMethod.php`
- Reference: `Drupal\entity\BundlePlugin\BundlePluginInterface`
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Entity Bundle Plugins](https://www.drupal.org/project/entity)
