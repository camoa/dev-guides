---
description: Aggregate stateless services via tagged service collection with REST API-first architecture
drupal_version: "11.x"
---

# Service Collector Pattern

## When to Use

> Use Service Collector for REST API-first external integrations with stateless services. Use Provider Plugin for internal Drupal service abstraction. Use Foundation+Extension when mature plugin ecosystem exists.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Stateless service aggregation | Service Collector | Minimal coordination, no shared state |
| REST API-first architecture | Service Collector | Built-in REST endpoints, JSON serialization |
| Webhook-driven workflows | Service Collector | Persistent callback storage via KeyValue |
| Polling-based event systems | Service Collector | Timestamp or ID-based polling events |
| Minimal interface (3 methods) | Service Collector | Simple contract, no annotation overhead |
| Self-describing configuration | Service Collector | Constraint-driven UI metadata auto-generation |
| Need plugin alterations | Provider Plugin | Service Collector doesn't support `hook_plugin_info_alter` |
| Multiple configured instances | Provider Plugin | Service Collector services are singletons |

## Pattern

**ServicesProviderInterface** - Minimal 3-method contract:

```php
interface ServicesProviderInterface {
  public function getId(): string;
  public function getAll(): array; // Returns Service[]
  public function execute(Service $service, array $config): array|string;
}
```

**Service Registration**:

```yaml
# Main module service collector
services:
  orchestration.services_manager:
    class: Drupal\orchestration\ServicesProviderManager
    tags:
      - { name: 'service_collector', tag: 'orchestration_services_provider', call: 'addServicesProvider' }

# Provider module tagged service
  orchestration_eca.services_provider:
    class: Drupal\orchestration_eca\ServicesProvider
    tags:
      - { name: 'orchestration_services_provider' }
```

**Lightweight DTOs with JSON Serialization**:

```php
// Service with configuration metadata
$service = new Service($provider, 'webhook_dispatcher', 'Dispatch Webhook', 'Send data to webhook');
$service->addConfig(new ServiceConfig(
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
));
// Auto-generates: {options: [{key: 'webhook1', name: 'Webhook 1'}, ...]}
```

**REST API Endpoints**:
- `GET /orchestration/services` - List all services with config metadata
- `POST /orchestration/service/execute` - Execute service with configuration
- `POST /orchestration/webhook/register` - Register webhook callback
- `POST /orchestration/poll` - Poll for events (timestamp or ID-based)

## Common Mistakes

- **Wrong**: Using Service Collector when plugin alterations needed → **Right**: Use Provider Plugin for flexibility
- **Wrong**: Using Service Collector for internal Drupal services → **Right**: Use Provider Plugin for internal abstraction
- **Wrong**: Complex plugin discovery when simple tagging suffices → **Right**: Tagged services auto-discovered during container compilation
- **Wrong**: Building custom REST API when Service Collector provides it → **Right**: Leverage built-in REST endpoints

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Plugin Manager Implementation](plugin-manager-implementation.md)
- [Service Integration Patterns](service-integration-patterns.md)
- Reference: `/web/modules/contrib/orchestration/`
- Reference: [Service Tags](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags)
- Reference: [Service Collector Deep Dive](https://tech.sparkfabrik.com/en/blog/drupal-service-container-deep-dive-part-1/)
- Reference: [RESTful Web Services API](https://www.drupal.org/docs/drupal-apis/restful-web-services-api/restful-web-services-api-overview)
