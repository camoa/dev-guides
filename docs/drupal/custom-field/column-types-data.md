---
description: "Structured-data column types in Custom Field 5.0.2 -- link, map, map_string, uuid -- with serialization and validation gotchas."
tldr: "link stores URI plus title/options extended properties; map and map_string serialize as PHP arrays (not JSON, not queryable); uuid auto-generates and must never be set by hand."
drupal_version: "11.x"
---

# Column Types: Data Fields

## When to Use

Storing structured data, links, UUIDs, or key-value maps in custom field columns.

## link

Full link with URI, title, and options (target, class, etc.).

**Schema:** URI `VARCHAR(2048)`

**Extended properties:**

- `field__title` -- VARCHAR(255) link title
- `field__options` -- BLOB serialized link options array

```yaml
columns:
  external_link:
    name: external_link
    type: link
```

**Gotchas:** Options array stores attributes like `target`, `class`, `rel`. Access via `$item->{'link__options'}`. Validation constraints: LinkAccessConstraint, LinkExternalProtocolsConstraint, LinkNotExistingInternalConstraint, LinkTypeConstraint.

## map

Key-value pairs (associative array).

**Schema:** `BLOB` (serialized array)

```yaml
columns:
  metadata:
    name: metadata
    type: map
```

**Gotchas:** Stored as serialized PHP array -- not queryable in database. Use map_string for simple key-value text, map for mixed types.

## map_string

Key-value pairs (string values only).

**Schema:** `BLOB` (serialized array)

```yaml
columns:
  attributes:
    name: attributes
    type: map_string
```

**Gotchas:** Similar to map but enforces string values. Widget provides key-value input interface.

## uuid

Universally unique identifier.

**Schema:** `VARCHAR(128)`

```yaml
columns:
  external_id:
    name: external_id
    type: uuid
```

**Gotchas:** Auto-generated on creation. No configuration UI. Has `never_check_empty` flag -- doesn't affect field empty state.

## Common Mistakes

- **Using map for queryable data** -- BLOB columns can't be queried efficiently; use discrete columns for searchable/filterable data
- **Not sanitizing link options** -- Link options array can contain XSS vectors; sanitize in formatter
- **Expecting map to be JSON** -- Stored as PHP serialized array, not JSON; use JSON:API normalizer for API exposure
- **Manually setting UUID** -- UUID auto-generated; setting manually can cause collisions

## See Also

- [Column Types: File Fields](column-types-file.md)
- [Widget Plugins Overview](widget-plugins-overview.md)
- [Link Sub-Fields](link-fields.md) -- widget configuration and security patterns for the link type
