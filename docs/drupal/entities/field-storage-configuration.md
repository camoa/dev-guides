---
description: Field storage — technical specs for reusable fields across bundles
tldr: "When creating fields that can be reused across multiple bundles, defining the technical specifications (data type, cardinality, storage schema) independent of bundle-specific settings."
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

## Shared Storage by Concern

When the SAME concern recurs on ≥2 bundles of one entity type, model it as ONE shared storage — but name it by the CONCERN, not by a bundle. The mechanics of shared storage are above; this is the decision discipline that keeps it maintainable.

- **Concern-named, not bundle-named:** for an eyebrow, CTA, or publish date that appears on several bundles, create one concern-named storage (`field_eyebrow`) instanced across those bundles — NOT `field_hero_eyebrow` + `field_card_eyebrow`. Bundle-named proliferation blocks cross-bundle queries and future reuse, and multiplies near-identical storage tables.
- **Cardinality reconciliation:** cardinality is a STORAGE-level property — it lives on `field.storage.*` and there is no per-bundle cardinality override. When one shared storage serves bundles with different needs, set the storage cardinality to the MAX any bundle requires, then enforce a lower per-bundle limit through WIDGET configuration, not storage.
- **entity_reference settings placement (load-bearing):** on a shared `entity_reference` storage the storage carries only `target_type`. The `handler`, `handler_settings`, and `target_bundles` belong on the field INSTANCE (`field.field.*`), never on the storage. Putting `handler_settings` on a storage YAML fails config schema validation.
- **Cross-entity-type boundary:** storage cannot cross entity types. The same concern on `node` vs `block_content` is legitimately TWO storages — sharing is only possible within one entity type.

## Common Mistakes

- **Wrong**: Trying to change immutable properties → **Right**: These are locked after creation; create new field instead
- **Wrong**: Missing module dependencies → **Right**: Field storage requires providing module (core, file, image, etc.)
- **Wrong**: Setting cardinality = 0 → **Right**: Invalid; use cardinality = 1 for single value, -1 for unlimited
- **Wrong**: Wrong entity_type → **Right**: Field storage tied to entity type; can't reuse across node/user/etc.
- **Wrong**: Not setting translatable → **Right**: Defaults to FALSE; explicitly set TRUE for multi-language sites
- **Wrong**: Forgetting indexes → **Right**: Add indexes for commonly filtered/sorted fields for performance
- **Wrong**: Sharing a storage for something that is really a classification → **Right**: Use a vocabulary + `entity_reference` so the dimension is governed, hierarchical, and reusable (see [Field & Storage Decision Order](field-storage-decision.md))
- **Wrong**: Bundle-naming a shared concern (`field_hero_eyebrow` + `field_card_eyebrow`) → **Right**: Name shared storage by the concern (`field_eyebrow`) and instance it per bundle
- **Wrong**: Putting `handler_settings`/`target_bundles` on a shared `entity_reference` storage → **Right**: Those settings belong on the field INSTANCE, not the storage

**Performance**:
- Add database indexes for fields used in views filters/sorts: `indexes: {value: [value]}`
- Consider cardinality carefully. Unlimited fields create separate table rows per value.
- Set persist_with_no_fields: true only if field storage should remain when all instances deleted.

**Security**:
- Lock system-critical fields: `locked: true` prevents accidental deletion
- Validate target_type on entity_reference fields to prevent invalid references

## See Also

- [Field Storage Decision Order](field-storage-decision.md)
- [Field Type Selection](field-type-selection.md)
- [Field Instance Configuration](field-instance-configuration.md)
- Reference: [Field storage configuration](https://git.drupalcode.org/project/drupal/-/blob/11.x/core/modules/field/config/schema/field.schema.yml)
