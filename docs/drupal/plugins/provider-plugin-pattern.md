---
description: Abstract diverse service providers under consistent interfaces
tldr: "Use Provider Plugin when creating new service abstraction across diverse external providers. Use Foundation+Extension when mature plugin ecosystem exists."
drupal_version: "11.x"
---

# Provider Plugin Pattern

## When to Use

> ✅ **No existing plugin ecosystem** for your service category
> ✅ **Need service abstraction** across diverse external providers
> ✅ **Want cross-cutting infrastructure** (proxy, events, caching)
> ✅ **Provider-agnostic consumers** that work with any implementation
> ✅ **External API integrations** with similar but different interfaces
> ✅ **User choice** between multiple service providers

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| No existing plugin ecosystem for service category | Provider Plugin | Create standardized abstraction from scratch |
| Need service abstraction across providers | Provider Plugin | Consistent interfaces for diverse implementations |
| Want cross-cutting infrastructure | Provider Plugin | Proxy, events, caching, monitoring in main module |
| Provider-agnostic consumers | Provider Plugin | Consumers work with any implementation |
| External API integrations | Provider Plugin | Standardize different external service interfaces |
| User choice between providers | Provider Plugin | Configuration-driven provider selection |
| REST API-first external integration | Service Collector | Built-in REST endpoints, minimal overhead |

## Architecture Overview

**Main Module** creates provider abstraction:
- Single plugin manager for provider plugins
- Standardized interfaces across all providers
- Cross-cutting infrastructure (proxy, events, caching)
- Consumer services that work with any provider

**Provider Modules** implement specific services:
- Focus on service-specific optimization
- Implement standard provider interface
- No infrastructure concerns (handled by main module)
- Can be contributed separately by different maintainers

## Pattern

**Pattern Reference**: `/web/modules/contrib/ai/` (main module)
**Provider Reference**: `/web/modules/contrib/ai_provider_openai/` (a provider implementation). Providers are not submodules of `ai`; each ships as its own contrib project — `ai_provider_openai`, `ai_provider_amazeeio` and the rest — so `ai/modules/` holds consumers such as `ai_assistant_api` and `ai_automators`, never providers.

**Key Interfaces**:
- `/web/modules/contrib/ai/src/AiProviderInterface.php`
- `/web/modules/contrib/ai/src/OperationType/` (operation-specific interfaces)

**Plugin Manager**:
- `/web/modules/contrib/ai/src/AiProviderPluginManager.php`

**Service Proxy Pattern**:
- Reference: AI module's provider proxy implementation
- Features: Event dispatching, error handling, retry logic

**Data Transfer Objects**:

```php
// Pattern reference from AI module structure
// Input/Output objects for standardized data exchange
```

**Service Registration**:

```yaml
# Provider pattern service definition
services:
  my_module.service_provider:
    class: Drupal\my_module\ServiceProviderPluginManager
    parent: default_plugin_manager
    arguments: ['@service_container']
```

## Critical Pattern Elements

1. **Standardized Provider Interface** - All providers implement same contract
2. **Service Proxy** - Wraps provider execution with events, logging, retry
3. **DTOs for Data Exchange** - Input/Output objects abstract data structures
4. **Capability-Based Discovery** - `getProvidersByCapability()` method
5. **Default Provider Configuration** - Per-operation-type defaults

## Common Mistakes

- **Wrong**: Creating provider plugin when Foundation+Extension exists → **Right**: Extend mature ecosystem (e.g., Commerce Payment)
- **Wrong**: No service proxy layer → **Right**: Implement proxy for events, error handling, retry logic
- **Wrong**: Direct provider implementation in consumers → **Right**: Consumers use provider-agnostic service interface
- **Wrong**: Provider-specific DTOs → **Right**: Standardized Input/Output objects across all providers

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- [Service Integration Patterns](service-integration-patterns.md)
- Reference: `/web/modules/contrib/ai/` (main module)
- Reference: `/web/modules/contrib/ai/src/AiProviderInterface.php`
- Reference: `/web/modules/contrib/ai/src/OperationType/` (operation-specific interfaces)
- Reference: `/web/modules/contrib/ai/src/AiProviderPluginManager.php`
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection)
