---
description: Field storage — technical specs for reusable fields across bundles
drupal_version: "11.x"
---

# Field Storage Configuration

## When to Use

When creating fields that can be reused across multiple bundles, defining the technical specifications (data type, cardinality, storage schema) independent of bundle-specific settings.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single-bundle field | Dedicated storage | Simpler, no cross-bundle concerns |
| Multi-bundle field | Shared storage | Reuse field across bundles, consistent data type |
| Unlimited values | cardinality: -1 | Users can add as many values as needed |
| Specific value count | cardinality: N | Enforce exact number (1 = single value) |
| Translatable content | translatable: true | Multi-language field data |
| Immutable field | locked: true | Prevent deletion (system-critical fields) |

## Pattern

Field storage in `config/install/field.storage.node.field_tags.yml`:

```yaml
langcode: en
status: true
dependencies:
  module:
    - node
    - taxonomy
id: node.field_tags
field_name: field_tags
entity_type: node
type: entity_reference
settings:
  target_type: taxonomy_term
module: core
locked: false
cardinality: -1           # Unlimited values
translatable: true
indexes: {}
persist_with_no_fields: false
custom_storage: false
```

**Immutable properties** (cannot change after field has data):
- id, field_name, entity_type, type
- Attempting to modify these causes ImmutablePropertiesConstraintException

Reference: `/core/modules/field/src/Entity/FieldStorageConfig.php`

## Common Mistakes

- **Wrong**: Trying to change immutable properties → **Right**: These are locked after creation; create new field instead
- **Wrong**: Missing module dependencies → **Right**: Field storage requires providing module (core, file, image, etc.)
- **Wrong**: Setting cardinality = 0 → **Right**: Invalid; use cardinality = 1 for single value, -1 for unlimited
- **Wrong**: Wrong entity_type → **Right**: Field storage tied to entity type; can't reuse across node/user/etc.
- **Wrong**: Not setting translatable → **Right**: Defaults to FALSE; explicitly set TRUE for multi-language sites
- **Wrong**: Forgetting indexes → **Right**: Add indexes for commonly filtered/sorted fields for performance

**Performance**:
- Add database indexes for fields used in views filters/sorts: `indexes: {value: [value]}`
- Consider cardinality carefully. Unlimited fields create separate table rows per value.
- Set persist_with_no_fields: true only if field storage should remain when all instances deleted.

**Security**:
- Lock system-critical fields: `locked: true` prevents accidental deletion
- Validate target_type on entity_reference fields to prevent invalid references

## See Also

- [Field Type Selection](field-type-selection.md)
- [Field Instance Configuration](field-instance-configuration.md)
- Reference: [Field storage configuration](https://git.drupalcode.org/project/drupal/-/blob/11.x/core/modules/field/config/schema/field.schema.yml)
