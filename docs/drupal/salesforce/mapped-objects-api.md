---
description: "MappedObject programmatic API — load by SFID, by entity, by mapping, create records"
tldr: "Use the `MappedObjectStorage` service when you need to programmatically query or manage the link between Drupal entities and Salesforce records — checking sync status, loading by SFID, or creating links manually."
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

**Storage Service:** `entity_type.manager->getStorage('salesforce_mapped_object')`

**Interface:** `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorageInterface.php`

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

## Common Pitfalls

- `$storage->load($id)` (the generic entity-storage `load()`) loads by the `MappedObject` entity's own ID — not by the linked Drupal entity's ID. Use `loadByEntity($entity)` or `loadByDrupal($entity_type_id, $entity_id)` to look up by the Drupal entity instead.
- Creating a `MappedObject` without first checking for an existing one can fail validation: the entity's `MappingEntity` constraint enforces uniqueness on the combination of Drupal entity type, Drupal entity ID, and mapping. Call `loadByEntityAndMapping($entity, $mapping)` first to avoid the error.

## See Also

- [Mapping Framework](mapping-framework.md)
- [Push Queue Operations](push-queue-operations.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorage.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorageInterface.php`
