---
description: Integrate consumer services with plugin managers and service collectors
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

```php
// Consumer service methods
public function executeOperation($operation_type, $data, $options) {
  // Auto-select provider based on configuration
}

public function executeWithProvider($provider_id, $config_id, $data, $options) {
  // Use specific provider
}
```

**Service Collector Consumer Pattern**:

```php
// REST API controller consuming service collector manager
public function execute(): JsonResponse {
  $data = json_decode($this->request->getContent(), TRUE);
  return new JsonResponse(
    $this->servicesProviderManager->executeService(
      $data['id'] ?? '',
      $data['config'] ?? []
    )
  );
}
```

**Key Difference**: Service collector pattern exposes services via REST API for external consumption, while provider plugin pattern focuses on internal Drupal service consumption.

## Common Mistakes

- **Wrong**: External systems calling plugin manager directly → **Right**: Use service collector with REST API endpoints
- **Wrong**: Consumer service hardcoded to specific provider → **Right**: Use provider-agnostic interface with configuration-driven selection
- **Wrong**: No error handling in REST API controller → **Right**: Wrap execution in try/catch, return proper HTTP status codes

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- [Configuration Architecture](configuration-architecture.md)
- Reference: AI module consumer services pattern
- Reference: `/web/modules/contrib/orchestration/src/Controller/Connect.php`
