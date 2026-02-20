---
description: Salesforce event system — all available push/pull/delete events, EventSubscriber pattern, service definition
drupal_version: "11.x"
---

# Event System

## When to Use

> Use EventSubscriber pattern for all Salesforce customization. The legacy hook system is deprecated. Use push events to modify or veto outbound data; use pull events to modify inbound data or control entity creation.

## Decision

| Event | Class | Use For |
|---|---|---|
| `PUSH_ALLOWED` | `SalesforcePushAllowedEvent` | Veto push — call `$event->disallowPush()` |
| `PUSH_MAPPING_OBJECT` | `SalesforcePushOpEvent` | Modify SFID or mapping relationship |
| `PUSH_PARAMS` | `SalesforcePushParamsEvent` | Modify field values before API call |
| `PUSH_SUCCESS` | `SalesforcePushParamsEvent` | Post-push processing, notifications |
| `PUSH_FAIL` | `SalesforcePushOpEvent` | Error handling, custom retry logic |
| `PULL_QUERY` | `SalesforceQueryEvent` | Modify SOQL query — add fields, subqueries |
| `PULL_PREPULL` | `SalesforcePullEvent` | Veto pull — call `$event->disallowPull()` |
| `PULL_ENTITY_VALUE` | `SalesforcePullEntityValueEvent` | Transform field values during mapping |
| `PULL_PRESAVE` | `SalesforcePullEvent` | Final entity changes, fetch attachments |
| `PULL_ENQUEUE` | `SalesforcePullEnqueueEvent` | Modify queue item before enqueueing |
| `DELETE_ALLOWED` | `SalesforceDeleteAllowedEvent` | Veto delete — call `$event->disallowDelete()` |
| `ERROR` | `SalesforceErrorEvent` | Custom error logging |

## Pattern

**Service definition:**
```yaml
services:
  my_module.salesforce_subscriber:
    class: Drupal\my_module\EventSubscriber\MyModuleSalesforceSubscriber
    arguments: ['@logger.factory', '@salesforce.client']
    tags:
      - { name: event_subscriber }
```

**Subscriber class structure:**
```php
public static function getSubscribedEvents(): array {
  return [
    SalesforceEvents::PUSH_ALLOWED => 'pushAllowed',
    SalesforceEvents::PUSH_PARAMS  => 'pushParamsAlter',
    SalesforceEvents::PULL_PRESAVE => 'pullPresave',
  ];
}

public function pushAllowed(SalesforcePushAllowedEvent $event): void {
  if ($event->getEntity()->bundle() === 'draft') {
    $event->disallowPush();
  }
}
```

## Common Mistakes

- **Wrong**: Implementing legacy hooks from `salesforce.api.php` → **Right**: Use EventSubscriber — hooks are deprecated and may be removed
- **Wrong**: Modifying field values in `PULL_PRESAVE` without checking that the field exists on the entity → **Right**: Check field existence with `$entity->hasField('field_name')` first
- **Wrong**: Forgetting to tag the service with `event_subscriber` → **Right**: Service tag is required for Drupal's event dispatcher to discover the subscriber

## See Also

- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Extension Patterns](extension-patterns.md)
- Reference: `/web/modules/contrib/salesforce/src/Event/SalesforceEvents.php`
- Reference example: `/web/modules/contrib/salesforce/modules/salesforce_example/src/EventSubscriber/SalesforceExampleSubscriber.php`
