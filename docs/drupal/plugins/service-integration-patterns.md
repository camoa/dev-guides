---
description: Integrate consumer services with plugin managers and service collectors
tldr: "Use provider abstraction for internal Drupal services consuming plugins. Use REST API controller pattern for external systems consuming service collectors."
drupal_version: "11.x"
---

# Service Integration Patterns

## When to Use

> Use provider abstraction for internal Drupal services consuming plugins. Use REST API controller pattern for external systems consuming service collectors.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Internal Drupal service consuming providers | Consumer Service with Provider Abstraction | Auto-select provider based on configuration |
| External system consuming services | REST API Controller with Service Collector | JSON serialization, stateless execution |
| Need provider-agnostic operations | Consumer Service Pattern | Consumers don't know which provider executes |
| REST API-first architecture | Service Collector Consumer Pattern | Built-in endpoints for external integration |

## Pattern

**Consumer Service with Provider Abstraction**:

**Reference Pattern**: AI module consumer services pattern

```yaml
# Consumer service registration
services:
  my_module.service:
    class: Drupal\my_module\MyModuleService
    arguments:
      - '@my_module.service_provider'
      - '@config.factory'
      - '@event_dispatcher'
```

**Consumer Service Pattern**:

**Key Methods**:
- `executeOperation($operation_type, $data, $options)` - Auto-select provider
- `executeWithProvider($provider_id, $config_id, $data, $options)` - Specific provider

**Service Collector Consumer Pattern**:

**Reference**: `/web/modules/contrib/orchestration/src/Controller/Connect.php`

```php
// REST API controller consuming service collector manager
public function execute(): JsonResponse {
  $data = json_decode($this->request->getContent(), TRUE);
  try {
    return new JsonResponse(
      $this->servicesProviderManager->executeService(
        $data['id'] ?? '',
        $data['config'] ?? []
      )
    );
  }
  catch (\Exception $e) {
    return new JsonResponse(['error' => $e->getMessage()], 500);
  }
}
```

**Key Difference**: Service collector pattern exposes services via REST API for external consumption, while provider plugin pattern focuses on internal Drupal service consumption.

## Common Mistakes

- **External systems calling the plugin manager directly** → WHY: The plugin manager has no HTTP contract; the service collector's REST endpoints are the supported external surface
- **Hardcoding a consumer service to one provider** → WHY: Provider selection belongs in configuration, so the consumer keeps working when the provider changes
- **No try/catch in the REST API controller** → WHY: An uncaught provider exception returns a 500 with a stack trace instead of a structured error body

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- [Configuration Architecture](configuration-architecture.md)
- Reference: AI module consumer services pattern
- Reference: `/web/modules/contrib/orchestration/src/Controller/Connect.php`
