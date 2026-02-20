---
description: MappedObject programmatic API — load by SFID, by entity, by mapping, create records
drupal_version: "11.x"
---

# Mapped Objects API

## When to Use

> Use the `MappedObjectStorage` service when you need to programmatically query or manage the link between Drupal entities and Salesforce records — checking sync status, loading by SFID, or creating links manually.

## Decision

| Need | Method |
|---|---|
| Find Drupal entity from a Salesforce ID | `$storage->loadBySfid($sfid)` |
| Find Salesforce record(s) for a Drupal entity | `$storage->loadByEntity($entity)` |
| Find link for specific entity + mapping combo | `$storage->loadByEntityAndMapping($entity, $mapping)` |
| Find all links for a mapping | `$storage->loadByMapping($mapping)` |
| Create a new entity-to-record link | `MappedObject::create([...])` |
| Force re-pull all entities for a mapping | `$storage->setForcePull($mapping)` |

## Pattern

```php
$storage = \Drupal::entityTypeManager()->getStorage('salesforce_mapped_object');

// Load by Salesforce ID
$sfid = new \Drupal\salesforce\SFID('003000000000001AAA');
$mapped_objects = $storage->loadBySfid($sfid);

// Load by Drupal entity
$entity = \Drupal\node\Entity\Node::load(123);
$mapped_objects = $storage->loadByEntity($entity);

// Load single by entity + mapping
$mapping = \Drupal\salesforce_mapping\Entity\SalesforceMapping::load('contact_mapping');
$mapped_object = $storage->loadByEntityAndMapping($entity, $mapping);

// Create a new link
$mapped_object = \Drupal\salesforce_mapping\Entity\MappedObject::create([
  'drupal_entity' => ['target_type' => 'node', 'target_id' => 123],
  'salesforce_mapping' => 'contact_mapping',
  'salesforce_id' => '003000000000001AAA',
]);
$mapped_object->save();
```

## Common Mistakes

- **Wrong**: Loading mapped objects with `entity_type.manager->getStorage('salesforce_mapped_object')->load($id)` by Drupal entity ID — that's the mapped_object entity ID, not the Drupal entity ID → **Right**: Use `loadByEntity($entity)` or `loadByDrupal($entity_type, $entity_id)`
- **Wrong**: Creating a `MappedObject` without first checking if one already exists → **Right**: Call `loadByEntityAndMapping()` first; creating duplicates causes sync errors

## See Also

- [Mapping Framework](mapping-framework.md)
- [Push Queue Operations](push-queue-operations.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorage.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorageInterface.php`
