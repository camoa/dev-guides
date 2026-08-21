---
description: "The entity_reference column type in Custom Field 5.0.2 -- referencing nodes, taxonomy terms, users, or media from a sub-field."
tldr: "entity_reference is the only reference column type; target_type is required and locked after data exists, and it never auto-checks access -- validate in the widget and check in the formatter."
drupal_version: "11.x"
---

# Column Types: Reference Fields

## When to Use

Referencing other entities (nodes, taxonomy terms, users, media) from custom field columns.

## entity_reference

Reference to any entity type.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | NULL | Entity type ID (node, taxonomy_term, user, media, etc.) |

**Schema:** `INT UNSIGNED NOT NULL DEFAULT 0` (stores target entity ID)

```yaml
columns:
  category:
    name: category
    type: entity_reference
    target_type: taxonomy_term
  author:
    name: author
    type: entity_reference
    target_type: user
```

**Gotchas:** target_type required and locked after data exists. Only entity types with ID key allowed. No bundle filtering at storage level -- use widget settings for that.

## Common Mistakes

- **Not setting target_type** -- Required field; entity_reference won't save without it
- **Trying to change target_type after data** -- Locked once data exists; requires field recreation
- **Forgetting access checks** -- Entity references don't auto-check access; validate in widget and check in formatter
- **Not configuring widget handler settings** -- Use EntityReferenceAutocompleteWidget or EntityReferenceSelectWidget settings to filter by bundle, sort, etc.

## See Also

- [Column Types: Date/Time Fields](column-types-datetime.md)
- [Column Types: File Fields](column-types-file.md)
- [Entity Reference Sub-Fields](entity-references.md) -- widget selection and access-check patterns
