---
description: Integrate plugin architectures with Drupal event system
drupal_version: "11.x"
---

# Event System Integration

## When to Use

> Use Provider pattern events for internal Drupal workflow integration. Use Service Collector polling events for external system integration via REST API.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Internal plugin execution workflow | Provider Pattern Events | Pre/post execution hooks for logging, caching |
| External system integration | Service Collector Polling Events | REST API-triggered events for data synchronization |
| Webhook push notifications | Service Collector Webhook Dispatch | Push data to external callbacks on Drupal events |
| Timestamp-based polling | Service Collector PollEventTimestamp | Get items modified after timestamp |
| ID-based polling | Service Collector PollEventId | Get items with ID greater than last ID |

## Pattern

**Provider Pattern - Internal Events**:

```yaml
# Event subscriber registration
services:
  my_module.service_audit_subscriber:
    class: Drupal\my_module\EventSubscriber\ServiceAuditSubscriber
    arguments: ['@logger.factory']
    tags:
      - { name: 'event_subscriber' }
```

**Event Types**:
- `my_module.service.pre_execute` - Before service execution
- `my_module.service.post_execute` - After successful execution
- `my_module.service.error` - On execution error

**Service Collector - Polling Events**:

```php
// External system triggers poll via REST API
POST /orchestration/poll
{
  "name": "entity_updates",
  "timestamp": 1234567890
}

// Event dispatched to Drupal event subscribers
$event = new PollEventTimestamp($name, $timestamp);
$this->eventDispatcher->dispatch($event, 'orchestration_poll.timestamp');

// Event subscribers add items to poll result
$event->addItem($timestamp, $data);

// REST API returns collected items
return new JsonResponse($event->getOutput());
```

**Webhook Dispatch Pattern**:

```php
// Drupal dispatches to registered webhooks
$this->webhooks->dispatch('entity_updates', [
  'entity_id' => 123,
  'type' => 'node',
  'operation' => 'update'
]);
// POSTs to registered external callback URLs
```

**Key Difference**: Service collector events designed for external system integration via REST API, not internal Drupal event workflow.

## Common Mistakes

- **Wrong**: Using provider pattern events for external integration → **Right**: Use service collector polling/webhook events
- **Wrong**: Webhook dispatch without error handling → **Right**: Log failed webhook calls, implement retry logic
- **Wrong**: Polling without pagination → **Right**: Limit poll results, use cursor-based pagination

## See Also

- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- [Service Integration Patterns](service-integration-patterns.md)
- Reference: AI module event system
- Reference: `/web/modules/contrib/orchestration/src/Event/`
- Reference: [Event API](https://www.drupal.org/docs/creating-modules/subscribe-to-and-dispatch-events)
- Reference: [Webhooks vs APIs](https://stytch.com/blog/webhooks-vs-apis/)
