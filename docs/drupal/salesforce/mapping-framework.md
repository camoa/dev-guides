---
description: "Salesforce mapping framework — SalesforceMapping config entity, MappedObject content entity, field mapping plugins"
tldr: "Use `salesforce_mapping` for any entity sync between Drupal and Salesforce. It provides the `SalesforceMapping` config entity (defines the relationship) and `MappedObject` content entity (tracks individual record links)."
drupal_version: "11.x"
---

# Mapping Framework

## When to Use

> Use `salesforce_mapping` for any entity sync between Drupal and Salesforce. It provides the `SalesforceMapping` config entity (defines the relationship) and `MappedObject` content entity (tracks individual record links).

**Purpose:** Core mapping framework - defines relationships between Drupal entities and Salesforce objects

## Decision: Field Mapping Plugin

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
| `Broken` | Placeholder for invalid mappings |

**Available Field Mapping Plugins:**
- `Properties` - Standard entity field mapping
- `PropertiesExtended` - Extended property mapping with transformations
- `RelatedProperties` - Map related entity properties
- `RelatedIDs` - Map entity reference IDs
- `RelatedTermString` - Map taxonomy term names
- `Token` - Token-based field values
- `Constant` - Static constant values
- `DrupalConstant` - PHP constant values
- `RecordType` - Salesforce RecordType mapping
- `Broken` - Placeholder for invalid mappings

## Decision: Creating a Custom Field Mapping Plugin

**Decision Point - Creating Custom Field Mapping Plugin:**
- Extend `PropertiesBase` for standard field mappings
- Implement `SalesforceMappingFieldPluginInterface` for custom logic
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_example/src/Plugin/SalesforceMappingField/Hardcoded.php`

## Key Entities

**SalesforceMapping (Config Entity):**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Entity/SalesforceMapping.php`
- Storage: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/SalesforceMappingStorage.php`
- Defines: Entity type, bundle, Salesforce object, field mappings, sync triggers

**MappedObject (Content Entity):**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Entity/MappedObject.php`
- Storage: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorage.php`
- Tracks: Individual entity-to-Salesforce-record relationships
- Revisionable: Maintains sync history

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

## Key Services

```
plugin.manager.salesforce_mapping_field - Field mapping plugin manager
salesforce_mapping.mappable_entity_types - Service for entity type discovery
entity_type.manager->getStorage('salesforce_mapped_object')
```

## Mapping Field Plugin System

- Base: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Plugin/SalesforceMappingField/PropertiesBase.php`
- Interface: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/SalesforceMappingFieldPluginInterface.php`
- Plugin directory: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Plugin/SalesforceMappingField/`

## Configuration Schema

- Location: `/web/modules/contrib/salesforce/modules/salesforce_mapping/config/schema/salesforce_mapping.schema.yml`
- Export path: `config/sync/salesforce_mapping.salesforce_mapping.[mapping_id].yml`

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
