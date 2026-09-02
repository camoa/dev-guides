---
description: "Salesforce event system — all available push/pull/delete events, EventSubscriber pattern, service definition"
tldr: "Use EventSubscriber pattern for all Salesforce customization. The legacy hook system is deprecated."
drupal_version: "11.x"
---

# Event System

## When to Use

> Use EventSubscriber pattern for all Salesforce customization. The legacy hook system is deprecated. Use push events to modify or veto outbound data; use pull events to modify inbound data or control entity creation.

All customization should use EventSubscriber pattern. Legacy hook system deprecated.

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

## Available Events

**Push Events:**

`SalesforceEvents::PUSH_ALLOWED` (`salesforce.push_allowed`)
- Event class: `SalesforcePushAllowedEvent`
- Purpose: Veto push operations
- Method: `$event->disallowPush()`
- Use case: Conditional push logic based on entity state

`SalesforceEvents::PUSH_MAPPING_OBJECT` (`salesforce.push_mapping_object`)
- Event class: `SalesforcePushOpEvent`
- Purpose: Modify mapped object before push
- Access: `$event->getMappedObject()`
- Use case: Change SFID, modify mapping relationship

`SalesforceEvents::PUSH_PARAMS` (`salesforce.push_params`)
- Event class: `SalesforcePushParamsEvent`
- Purpose: Modify field values before API call
- Access: `$event->getParams()`, `$event->setParam()`
- Use case: Field transformations, calculated values

`SalesforceEvents::PUSH_SUCCESS` (`salesforce.push_success`)
- Event class: `SalesforcePushParamsEvent`
- Purpose: Post-push processing
- Use case: Logging, notifications, related record updates

`SalesforceEvents::PUSH_FAIL` (`salesforce.push_fail`)
- Event class: `SalesforcePushOpEvent`
- Purpose: Error handling
- Use case: Custom error logging, retry logic

**Pull Events:**

`SalesforceEvents::PULL_QUERY` (`salesforce.pull_query`)
- Event class: `SalesforceQueryEvent`
- Purpose: Modify SOQL query
- Access: `$event->getQuery()`
- Use case: Add fields, subqueries, conditions, limits
- Reference: `SalesforceExampleSubscriber::pullQueryAlter()`

`SalesforceEvents::PULL_PREPULL` (`salesforce.pull_prepull`)
- Event class: `SalesforcePullEvent`
- Purpose: Pre-processing, veto pull
- Method: `$event->disallowPull()`
- Use case: Conditional pull, pre-validation

`SalesforceEvents::PULL_ENTITY_VALUE` (`salesforce.pull_entity_value`)
- Event class: `SalesforcePullEntityValueEvent`
- Purpose: Modify field values during mapping
- Use case: Field transformations, data cleanup

`SalesforceEvents::PULL_PRESAVE` (`salesforce.pull_presave`)
- Event class: `SalesforcePullEvent`
- Purpose: Final entity modifications before save
- Use case: Complex field logic, related entity operations, file attachments
- Reference: `SalesforceExampleSubscriber::pullPresave()` (attachment fetch example)

`SalesforceEvents::PULL_ENQUEUE` (`salesforce.pull_enqueue`)
- Event class: `SalesforcePullEnqueueEvent`
- Purpose: Modify queue item before enqueueing
- Use case: Priority logic, conditional enqueueing

**Delete Events:**

`SalesforceEvents::DELETE_ALLOWED` (`salesforce.delete_allowed`)
- Event class: `SalesforceDeleteAllowedEvent`
- Purpose: Veto delete operations
- Method: `$event->disallowDelete()`

**Logging Events:**

`SalesforceEvents::ERROR` (`salesforce.error`)
- Event class: `SalesforceErrorEvent`
- Purpose: Error logging

`SalesforceEvents::WARNING` (`salesforce.warning`)
- Event class: `SalesforceWarningEvent`
- Purpose: Warning logging

`SalesforceEvents::NOTICE` (`salesforce.notice`)
- Event class: `SalesforceNoticeEvent`
- Purpose: Notice logging

---

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
