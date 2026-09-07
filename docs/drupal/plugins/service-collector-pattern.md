---
description: Aggregate stateless services via tagged service collection with REST API-first architecture
tldr: "Use Service Collector for REST API-first external integrations with stateless services. Use Provider Plugin for internal Drupal service abstraction."
drupal_version: "11.x"
---

# Service Collector Pattern

## When to Use

> ✅ **Stateless service aggregation** with minimal coordination
> ✅ **REST API-first architecture** for external system integration
> ✅ **Webhook-driven workflows** requiring persistent callback storage
> ✅ **Polling-based event systems** (timestamp or ID-based)
> ✅ **Lightweight DTOs** for auto-generated UI metadata
> ✅ **No plugin configuration needed** - services self-describe
> ✅ **Simple 3-method interface** for service providers
> ✅ **Auto-discovery via tags** without annotation overhead

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

## Architecture Overview

**Main Module** creates service aggregation:
- Service collector manager aggregates tagged services
- Minimal interface contract (3 methods)
- Lightweight DTOs with `JsonSerializable` for REST exposure
- REST API endpoints for external consumption
- Webhook persistence via KeyValue store
- Dual polling patterns (timestamp and ID-based)

**Service Provider Modules** implement services:
- Implement `ServicesProviderInterface` (3 methods only)
- Return array of `Service` objects with `ServiceConfig` metadata
- Execute service logic via `execute()` method
- No plugin annotations or complex discovery

## Pattern

**Pattern Reference**: `/web/modules/contrib/orchestration/`
**Provider Reference**: `/web/modules/contrib/orchestration/modules/eca/src/ServicesProvider.php`

**Core Components**:

**1. ServicesProviderInterface** - Minimal Contract:
- Reference: `/web/modules/contrib/orchestration/src/ServicesProviderInterface.php`

```php
interface ServicesProviderInterface {
  public function getId(): string;
  public function getAll(): array; // Returns Service[]
  public function execute(Service $service, array $config): array|string;
}
```

**2. ServicesProviderManager** - Service Collector:
- Reference: `/web/modules/contrib/orchestration/src/ServicesProviderManager.php`
- Aggregates via `service_collector` tag
- Method: `addServicesProvider()` called for each tagged service
- Collects all services across providers via `getAllServices()`

**3. Lightweight DTOs**:

- **Service**: `/web/modules/contrib/orchestration/src/Service.php`
  - Properties: provider, id, label, description
  - Method: `addConfig(ServiceConfig)` for configuration fields
  - Implements `JsonSerializable` for REST API exposure

- **ServiceConfig**: `/web/modules/contrib/orchestration/src/ServiceConfig.php`
  - Properties: key, label, description, required, type, constraints
  - Method: `getOptionsFromConstraints()` auto-generates UI metadata
  - Constraint-driven configuration (e.g., Choice constraint → select options)

**4. REST API Endpoints**:
- Reference: `/web/modules/contrib/orchestration/orchestration.routing.yml`
- `GET /orchestration/services` - List all services with config forms
- `POST /orchestration/service/execute` - Execute service with config
- `POST /orchestration/webhook/register` - Register webhook callback
- `POST /orchestration/webhook/unregister` - Remove webhook callback
- `POST /orchestration/poll` - Poll for events (timestamp or ID-based)

**5. Webhook System**:
- Reference: `/web/modules/contrib/orchestration/src/Webhooks.php`
- KeyValue storage: `$keyvalue->get('orchestration')`
- Methods: `register()`, `unregister()`, `dispatch()`
- Persistence: Webhooks stored by ID with callback URL

**6. Polling Event System**:
- **Base Event**: `/web/modules/contrib/orchestration/src/Event/PollEventBase.php`
- **Timestamp Polling**: `/web/modules/contrib/orchestration/src/Event/PollEventTimestamp.php`
  - Pattern: Get all items with `timestamp > $lastTimestamp`
  - Method: `addItem($timestamp, $data)`
- **ID Polling**: `/web/modules/contrib/orchestration/src/Event/PollEventId.php`
  - Pattern: Get all items with `id > $lastId`
  - Method: `addItem($id, $data)`

**Service Registration**:

```yaml
# orchestration.services.yml
services:
  orchestration.services_manager:
    class: Drupal\orchestration\ServicesProviderManager
    tags:
      - { name: 'service_collector', tag: 'orchestration_services_provider', call: 'addServicesProvider' }

# Provider module service definition
# orchestration_eca.services.yml
services:
  orchestration_eca.services_provider:
    class: Drupal\orchestration_eca\ServicesProvider
    arguments:
      - '@entity_type.manager'
      - '@state'
      - '@event_dispatcher'
      - '@eca.token_services'
    tags:
      - { name: 'orchestration_services_provider' }
```

## Critical Pattern Elements

1. **Service Collector Tag**: `service_collector` tag with `call` parameter for aggregation method
2. **Stateless Execution**: Each `execute()` call is independent, no state maintained
3. **Self-Describing Services**: `ServiceConfig` constraints auto-generate UI metadata
4. **JSON Serialization**: All DTOs implement `JsonSerializable` for REST exposure
5. **KeyValue Webhook Storage**: Persistent webhook callbacks without entity overhead
6. **Dual Polling Patterns**: Timestamp-based for temporal data, ID-based for sequential data
7. **Service UUID Pattern**: `{provider_id}::{service_id}` for global uniqueness

## Advantages Over Plugin Manager

**Simplicity**:
- No annotation overhead or plugin discovery complexity
- 3-method interface vs complex plugin base classes
- Tagged services auto-discovered during container compilation

**Performance**:
- Services collected once during container build
- No plugin cache invalidation concerns
- Lazy loading via `service_id_collector` possible

**REST API Integration**:
- DTOs designed for JSON serialization
- Services auto-expose via REST endpoints
- Configuration metadata included in service list

**External System Integration**:
- Webhook callbacks for push notifications
- Polling endpoints for pull-based integration
- Stateless execution model ideal for HTTP requests

## Disadvantages vs Plugin Manager

**Limited Flexibility**:
- No plugin alterations (`hook_plugin_info_alter`)
- No derivative plugins
- Cannot provide multiple configured instances
- No annotation-based metadata

**No Configuration UI**:
- Services describe configuration but don't provide forms
- External systems consume via REST API
- Drupal admin UI requires custom implementation

**Tighter Coupling**:
- All providers must use exact same DTOs (Service, ServiceConfig)
- Cannot extend interfaces for specialized needs
- Manager implementation not pluggable

## Use Case: ECA Tools Integration

**Reference**: `/web/modules/contrib/orchestration/modules/eca/src/ServicesProvider.php`

Pattern demonstrates:
- Dynamic service discovery from ECA models
- YAML-based argument configuration
- Event dispatcher integration for execution
- Token service for dynamic data injection

```php
// ECA tools discovered from state management
$subscribed = $this->state->get('eca.subscribed', [])['eca_base.tool'];

// Each ECA tool becomes a Service with ServiceConfig from YAML
foreach ($arguments as $name => $argument) {
  $service->addConfig(new ServiceConfig(
    $name,
    $argument['label'],
    $argument['description'],
    $argument['required'] ?? FALSE,
  ));
}
```

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
- Reference: `/web/modules/contrib/orchestration/src/ServicesProviderInterface.php`
- Reference: `/web/modules/contrib/orchestration/src/ServicesProviderManager.php`
- Reference: `/web/modules/contrib/orchestration/src/Service.php`
- Reference: `/web/modules/contrib/orchestration/src/ServiceConfig.php`
- Reference: `/web/modules/contrib/orchestration/orchestration.routing.yml`
- Reference: `/web/modules/contrib/orchestration/src/Webhooks.php`
- Reference: `/web/modules/contrib/orchestration/src/Event/PollEventBase.php`
- Reference: `/web/modules/contrib/orchestration/src/Event/PollEventTimestamp.php`
- Reference: `/web/modules/contrib/orchestration/src/Event/PollEventId.php`
- Reference: `/web/modules/contrib/orchestration/modules/eca/src/ServicesProvider.php`
- Reference: [Service Tags](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags)
- Reference: [Service Collector Deep Dive](https://tech.sparkfabrik.com/en/blog/drupal-service-container-deep-dive-part-1/)
- Reference: [RESTful Web Services API](https://www.drupal.org/docs/drupal-apis/restful-web-services-api/restful-web-services-api-overview)
- Reference: [Capturing Webhooks in Drupal](https://atendesigngroup.com/articles/capturing-webhooks-drupal-8)
