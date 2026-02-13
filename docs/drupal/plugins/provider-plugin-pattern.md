---
description: Abstract diverse service providers under consistent interfaces
drupal_version: "11.x"
---

# Provider Plugin Pattern

## When to Use

> Use Provider Plugin when creating new service abstraction across diverse external providers. Use Foundation+Extension when mature plugin ecosystem exists. Use Service Collector when building REST API-first integrations.

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

## Pattern

**Main Module** creates provider abstraction:

```yaml
# Provider pattern service definition
services:
  my_module.service_provider:
    class: Drupal\my_module\ServiceProviderPluginManager
    parent: default_plugin_manager
    arguments: ['@service_container']
```

**Provider Module** implements specific service:

```php
// Consumer code works with any provider
$result = $this->myModuleService->executeOperation('text_generation', [
  'prompt' => 'Write a summary',
  'max_tokens' => 100
]);

// Different providers handle same operation differently:
// OpenAI Provider: Uses GPT-4 API
// Anthropic Provider: Uses Claude API
// Local Provider: Uses local LLM
```

**Critical Pattern Elements**:
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
- Reference: `/web/modules/contrib/ai/`
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection)
