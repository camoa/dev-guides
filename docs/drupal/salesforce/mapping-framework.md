---
description: Salesforce mapping framework — SalesforceMapping config entity, MappedObject content entity, field mapping plugins
drupal_version: "11.x"
---

# Mapping Framework

## When to Use

> Use `salesforce_mapping` for any entity sync between Drupal and Salesforce. It provides the `SalesforceMapping` config entity (defines the relationship) and `MappedObject` content entity (tracks individual record links).

## Decision

| Field Mapping Plugin | Use When |
|---|---|
| `Properties` | Standard Drupal field → Salesforce field mapping |
| `PropertiesExtended` | Need transformations on standard properties |
| `RelatedProperties` | Map a field from a related entity |
| `RelatedIDs` | Map entity reference IDs |
| `RelatedTermString` | Map taxonomy term names |
| `Token` | Value derived from token replacement |
| `Constant` | Static hardcoded value |
| `DrupalConstant` | PHP constant value |
| `RecordType` | Salesforce RecordType mapping |

## Pattern

**Two entity types:**

```
SalesforceMapping (config entity)
  - Entity type + bundle
  - Salesforce object name
  - Field mappings
  - Sync triggers (push_create, pull_update, etc.)
  └── Stored: config/sync/salesforce_mapping.salesforce_mapping.[id].yml

MappedObject (content entity, revisionable)
  - Links one Drupal entity ↔ one Salesforce record
  - Stores SFID, last sync timestamp
  - Maintains sync history via revisions
```

**Key services:**
```
plugin.manager.salesforce_mapping_field  — field mapping plugins
salesforce_mapping.mappable_entity_types — entity type discovery
entity_type.manager->getStorage('salesforce_mapped_object')
```

## Common Mistakes

- **Wrong**: Creating a custom field mapping by copying the entity and bypassing the plugin system → **Right**: Extend `PropertiesBase` for custom field mapping logic
- **Wrong**: Editing `MappedObject` records directly to change SFID → **Right**: Use the `PUSH_MAPPING_OBJECT` event to modify the mapped object during sync

## See Also

- [Mapping UI & Sync Triggers](mapping-ui.md)
- [Custom Field Mapping Plugin](custom-field-mapping-plugin.md)
- [Mapped Objects API](mapped-objects-api.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Entity/SalesforceMapping.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Entity/MappedObject.php`
- Reference example: `/web/modules/contrib/salesforce/modules/salesforce_example/src/Plugin/SalesforceMappingField/Hardcoded.php`
