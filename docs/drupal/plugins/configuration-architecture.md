---
description: Store and manage plugin configuration across patterns
drupal_version: "11.x"
---

# Configuration Architecture

## When to Use

> Store plugin configuration in entities for Foundation pattern. Use config objects for Provider pattern. Use constraint-driven ServiceConfig for Service Collector pattern.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Entity-based plugin instances | Foundation Pattern Entity Configuration | Plugin ID stored as entity field |
| Provider-specific settings | Provider Pattern Config Objects | Multiple named configs per provider |
| REST API-exposed configuration | Service Collector ServiceConfig | Constraint-driven metadata auto-generation |
| Admin UI configuration forms | Foundation or Provider Pattern | Entity forms or config forms |
| External system configuration | Service Collector Pattern | JSON-serializable configuration metadata |

## Pattern

**Foundation Pattern - Entity Configuration**:

```yaml
# Entity configuration stores plugin ID
id: example
label: 'Example Gateway'
plugin: example_gateway
configuration:
  api_endpoint: 'https://api.example.com'
  timeout: 30
```

**Provider Pattern - Config Objects**:

```yaml
# Provider module configuration
configs:
  default:
    api_key: ''
    timeout: 30
  production:
    api_key: ''
    timeout: 60

# Main module default provider settings
default_providers:
  process: 'example'
default_configs:
  process: 'default'
```

**Service Collector - Constraint-Driven ServiceConfig**:

```php
// ServiceConfig with constraints auto-generates UI metadata
new ServiceConfig(
  key: 'webhook_id',
  label: 'Webhook',
  description: 'Select registered webhook',
  required: true,
  type: 'string',
  constraints: [
    'Choice' => [
      'choices' => ['webhook1' => 'Webhook 1', 'webhook2' => 'Webhook 2']
    ]
  ]
)
// Auto-generates: {options: [{key: 'webhook1', name: 'Webhook 1'}, ...]}
```

**Key Advantage**: Service Collector configuration metadata embedded in service definition, automatically exposed via REST API for external UI generation.

## Common Mistakes

- **Wrong**: Hardcoding API keys in annotations → **Right**: Use Key module or config overrides with environment variables
- **Wrong**: Complex config schema when ServiceConfig suffices → **Right**: Use ServiceConfig constraints for auto-generated metadata
- **Wrong**: Entity configuration without plugin validation → **Right**: Validate in plugin manager's `processDefinition()`

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: `/web/modules/contrib/commerce/modules/payment/config/install/`
- Reference: `/web/modules/contrib/orchestration/src/ServiceConfig.php`
