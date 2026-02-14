---
description: Available core data types for config schema — scalars, containers, extended types, and special types.
---

# Core Data Types Schema

## When to Use

When writing config schema and you need to know which core data types are available for scalars (string, integer, boolean), containers (mapping, sequence), and specialized types (email, uri, label).

## Core Scalar Types

| Type | Description | Use For |
|------|-------------|---------|
| `boolean` | TRUE/FALSE | Feature toggles, checkboxes |
| `integer` | Whole numbers | Counts, limits, IDs |
| `float` | Decimal numbers | Percentages, weights, ratios |
| `string` | Any text | Machine names, paths, unstructured text |
| `email` | Email addresses | Validated email with Email constraint |
| `uri` | URIs/URLs | External links, API endpoints |
| `timestamp` | Unix timestamp | Date/time as integer |

## Core Container Types

| Type | Description | Use For |
|------|-------------|---------|
| `mapping` | Key-value pairs with known keys | Nested config objects |
| `sequence` | Indexed arrays, all same type | Lists of strings, integers, etc. |
| `config_object` | Top-level simple config | Wraps entire simple config file |
| `config_entity` | Top-level config entity | Wraps entire config entity export |

## Core Extended Types

| Type | Description | Constraints |
|------|-------------|-------------|
| `label` | Single-line translatable text | No control characters, `translatable: true` |
| `required_label` | Non-empty label | `NotBlank` constraint |
| `plural_label` | Pluralized label variants | Allows ASCII 3 separator |
| `path` | Internal Drupal path | Path-like strings |
| `text` | Multi-line text | Paragraphs, descriptions |
| `color_hex` | Hex color code | `#RRGGBB` format |
| `date_format` | PHP date format string | Date/time formatting |
| `uuid` | UUID string | `Uuid` constraint |
| `langcode` | Language code | `en`, `fr`, etc. |
| `machine_name` | Machine name | Lowercase, underscores |

## Core Special Types

| Type | Description | When to Use |
|------|-------------|-------------|
| `undefined` | No schema | Avoid — use typed schema instead |
| `ignore` | Unstructured data | Only for truly dynamic data structures |

## Usage Example

```yaml
# Using core types
mymodule.settings:
  type: config_object
  mapping:
    site_name:
      type: label
    contact_email:
      type: email
      constraints:
        Email: {}
    max_age:
      type: integer
      constraints:
        Range:
          min: 0
          max: 86400
    api_endpoint:
      type: uri
    feature_enabled:
      type: boolean
    weights:
      type: sequence
      sequence:
        type: float
```

**Reference:** `/core/config/schema/core.data_types.schema.yml`

## Common Mistakes

- Using `string` for everything — Prefer specialized types (email, uri, label) for better validation
- Using `text` for single-line labels — Use `label` instead, prevents multi-line input
- No constraints on specialized types — Add Email, Range, NotBlank constraints
- Using `ignore` without reason — Drupal can't validate, defeats purpose of schema
- Forgetting `translatable: true` on labels — User-facing text won't be translatable

## See Also

- [Config Schema YAML](config-schema-yaml.md) — defining schema structure
- [Writing Config Schema](writing-config-schema.md) — step-by-step schema creation
- Reference: `/core/config/schema/core.data_types.schema.yml`
