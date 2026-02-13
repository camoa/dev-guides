---
description: Real-world implementation patterns from Commerce, AI, and Orchestration modules
drupal_version: "11.x"
---

# Real-World Implementation Examples

## When to Use

> Reference these patterns when implementing similar plugin architectures. Commerce Payment for Foundation pattern, AI module for Provider pattern, Orchestration module for Service Collector pattern.

## Decision

| Need | Pattern | Reference Module |
|------|---------|-----------------|
| Multiple plugin types coordination | Foundation Pattern | Commerce Payment |
| Service abstraction across providers | Provider Pattern | AI Module |
| REST API-first external integration | Service Collector | Orchestration Module |
| Entity bundle integration | Foundation Pattern | Commerce Payment Method |
| Webhook + polling events | Service Collector | Orchestration Module |

## Pattern

**Foundation Pattern: Commerce Payment**

```php
// Gateway + Method Type + Entity Type coordination
$gateway = $this->gatewayManager->createInstance('stripe');
$method_types = $gateway->getSupportedMethodTypes(); // ['credit_card', 'bank_transfer']

foreach ($method_types as $method_type_id) {
  $method_type = $this->methodTypeManager->createInstance($method_type_id);
  $fields = $method_type->buildFieldDefinitions(); // Entity bundle fields

  $result = $gateway->executeOperation($method_type_id, $parameters);
}
```

**Provider Pattern: AI Module**

```php
// Consumer code works with any provider
$result = $this->myModuleService->executeOperation('text_generation', [
  'prompt' => 'Write a summary',
  'max_tokens' => 100
]);

// Different providers handle the same operation differently
// OpenAI Provider: Uses GPT-4 API
// Anthropic Provider: Uses Claude API
// Local Provider: Uses local LLM
```

**Service Collector Pattern: Orchestration Module**

```php
// External system discovers available services
GET /orchestration/services
// Returns: [
//   {
//     "id": "eca::webhook_dispatcher",
//     "label": "Dispatch Webhook",
//     "config": [
//       {"key": "webhook_id", "label": "Webhook", "type": "string", "required": true, "options": [...]}
//     ]
//   }
// ]

// External system executes service
POST /orchestration/service/execute
{
  "id": "eca::webhook_dispatcher",
  "config": {
    "webhook_id": "external_system_callback",
    "data": {"entity_id": 123, "status": "completed"}
  }
}

// External system polls for new data (timestamp-based)
POST /orchestration/poll
{
  "name": "entity_updates",
  "timestamp": 1234567890
}
```

## Common Mistakes

- **Wrong**: Reimplementing Commerce Payment gateway structure → **Right**: Extend Commerce Payment with new gateway plugin
- **Wrong**: Provider-specific consumer code → **Right**: Use provider-agnostic service interface
- **Wrong**: Building custom REST endpoints when Orchestration pattern exists → **Right**: Use Service Collector pattern

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: `/web/modules/contrib/commerce/modules/payment/`
- Reference: `/web/modules/contrib/ai/`
- Reference: `/web/modules/contrib/orchestration/`
- Reference: [Building module-specific REST endpoints](https://drupalzone.com/tutorial/headless-drupal/100-creating-custom-api-endpoints)
