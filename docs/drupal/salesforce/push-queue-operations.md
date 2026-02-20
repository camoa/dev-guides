---
description: Push queue programmatic operations — queue entity for push, process queue via service
drupal_version: "11.x"
---

# Push Queue Operations

## When to Use

> Use the `queue.salesforce_push` service when you need to programmatically queue entities for push outside of the normal entity save trigger — for example, in migrations, batch operations, or after importing data bypassing hooks.

## Decision

| Need | Approach |
|---|---|
| Queue single entity for push | `$push_queue->claimItem($mapped_object, 'push_create')` |
| Process the entire push queue | `$push_queue->processQueue()` |
| Requeue all entities for a mapping via Drush | `drush sfrq {mapping_id}` |
| Push unmapped entities | `drush sfpu {mapping_id}` |

## Pattern

```php
$push_queue = \Drupal::service('queue.salesforce_push');
$storage = \Drupal::entityTypeManager()->getStorage('salesforce_mapped_object');
$entity = \Drupal\node\Entity\Node::load(123);
$mapping = \Drupal\salesforce_mapping\Entity\SalesforceMapping::load('contact_mapping');

// Load or create mapped object first
$mapped_object = $storage->loadByEntityAndMapping($entity, $mapping);

// Queue for push
$push_queue->claimItem($mapped_object, 'push_create');

// Process queue programmatically
$push_queue->processQueue();
```

## Common Mistakes

- **Wrong**: Calling `processQueue()` on every entity save — duplicates queue processing → **Right**: Let cron or standalone endpoints handle processing; call `processQueue()` only in batch/migration contexts where you control the queue lifecycle
- **Wrong**: Using push queue operations without a `MappedObject` — the queue item requires a mapped object entity → **Right**: Create or load the `MappedObject` before queuing

## See Also

- [Push Synchronization](push-synchronization.md)
- [Mapped Objects API](mapped-objects-api.md)
- [Queue Processing](queue-processing.md)
- [Drush Commands](drush-commands.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueue.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueueInterface.php`
