---
description: Decision order for choosing a field storage SHAPE — compound, taxonomy, shared, wrapper entity, reference, or plain field.
tldr: "Decide field-storage SHAPE in priority order: polymorphic -> custom compound field; classification -> taxonomy + entity_reference; shared concern -> concern-named storage; entity-worthy collection -> wrapper entity; else plain core field."
drupal_version: "11.x"
---

# Field & Storage Decision Order

## When to Use

When adding a field to a bundle and you must decide what storage SHAPE it should take — a compound field, a taxonomy reference, a shared storage, a wrapper entity, a plain reference, or a bundle-private core field. This is a best-practice judgment order that Drupal does not enforce; evaluate the criteria IN ORDER and stop at the first match.

## Foundation

Field STORAGE is per entity-type; a field INSTANCE is per bundle. So this decision is about the storage *shape* — chosen once — then applied per instance on each bundle that needs it. See [Field Storage Configuration](field-storage-configuration.md) and [Field Instance Configuration](field-instance-configuration.md).

## Decision Order

Evaluate top-to-bottom; stop at the first match.

1. **Polymorphic?** — the value has ≥2 mutually-exclusive sub-shapes and only one renders per instance → a `custom` compound field (`type: custom`, custom_field module), one column per shape. This is NOT an optional single value — "optional" is the instance `required` setting, not a reason for a compound.
2. **A classification / controlled vocabulary?** — the value names a category, tag, or governed term set (even if only one bundle uses it today) → a taxonomy vocabulary + an `entity_reference` field (`target_type: taxonomy_term`). This takes precedence over "just share a storage": a classification dimension should be governed by a vocabulary so it can carry hierarchy, term-level metadata, and reuse.
3. **A concern shared across bundles** (no classification semantics)? → ONE concern-named field storage instanced across those bundles (see the shared-storage-by-concern discipline in [Field Storage Configuration](field-storage-configuration.md)).
4. **A multi-value child collection that is entity-worthy?** — it needs its own view modes, cross-parent reuse, or an independent lifecycle → a wrapper bundle + a multi-value `entity_reference`. Entity-worthiness is the trigger, NOT a claim that a compound cannot hold a reference (it can).
5. **A reference to an independently-managed entity?** → `entity_reference`.
6. **Otherwise** → a plain, bundle-private core field.

## Decision

| If the value is... | Use... | Why |
|---|---|---|
| ≥2 mutually-exclusive shapes, one per instance | `custom` compound field (`type: custom`) | No single core field type expresses all the shapes |
| A category / tag / governed term set | Taxonomy vocabulary + `entity_reference` | Classification belongs in a vocabulary (hierarchy, term metadata, reuse) |
| A plain concern on ≥2 bundles | One concern-named shared storage | Cross-bundle query + future reuse |
| An entity-worthy child collection | Wrapper bundle + multi-value `entity_reference` | Own view modes / lifecycle / cross-parent reuse |
| A reference to an independent entity | `entity_reference` | Referential integrity, access control |
| None of the above | Plain bundle-private core field | Simplest tool that fits |

## Common Mistakes

- **Wrong**: Reaching for a compound because a column would be a reference → **Right**: A `custom` field CAN hold an `entity_reference` column; entity-worthiness (not reference-ness) is what routes you to a wrapper entity
- **Wrong**: Sharing a storage for something that is really a classification → **Right**: Use a vocabulary + reference so the dimension is governed, hierarchical, and reusable
- **Wrong**: Treating "optional" as polymorphic → **Right**: An optional single value is a single-value field with `required: false`, not a compound
- **Wrong**: Skipping the order → **Right**: Evaluate top-to-bottom; a classification (step 2) outranks a bare shared storage (step 3)

## See Also

- [Field Type Selection](field-type-selection.md)
- [Field Storage Configuration](field-storage-configuration.md)
- Related: Custom Field module guide → [Overview](../custom-field/overview.md) (the two triggers for a `custom` compound field)
- Reference: [Field types overview](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters)
