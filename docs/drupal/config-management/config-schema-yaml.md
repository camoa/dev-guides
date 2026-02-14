---
description: Define the structure and data types for module configuration so Drupal can validate, cast, and translate config values.
---

# Config Schema YAML

## When to Use

When defining the structure and data types for your module's configuration so Drupal can validate, cast, and translate config values.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Module config schema | `config/schema/MODULE.schema.yml` | Defines all config types for your module |
| Simple settings object | `type: config_object` | Top-level wrapper for simple config |
| Config entity schema | `type: config_entity` | Top-level wrapper for config entities |
| Nested structures | `type: mapping` | Key-value pairs with defined child types |
| Lists of items | `type: sequence` | Arrays with all items of same type |
| Dynamic keys | `type: sequence` with `[%key]` | Associative arrays with unknown keys |
| Translatable text | `translatable: true` | Marks strings for interface translation |
| Optional keys | `requiredKey: false` | Key can be absent without validation error |
| Strict validation | `constraints: FullyValidatable: ~` | Enforces all keys present, types correct |

## Pattern

```yaml
# config/schema/mymodule.schema.yml
mymodule.settings:
  type: config_object
  label: 'My Module Settings'
  constraints:
    FullyValidatable: ~
  mapping:
    api_key:
      type: string
      label: 'API Key'
      constraints:
        NotBlank: {}
    enabled:
      type: boolean
      label: 'Enable feature'
    max_items:
      type: integer
      label: 'Maximum items'
      constraints:
        Range:
          min: 1
          max: 100
    allowed_types:
      type: sequence
      label: 'Allowed types'
      sequence:
        type: string
```

**Reference:** `/core/config/schema/core.data_types.schema.yml`, `/core/modules/system/config/schema/system.schema.yml`

## Schema File Structure

1. **Top-level key** — Matches config name (e.g., `mymodule.settings`)
2. **Type definition** — `type: config_object` or `type: config_entity`
3. **Label** — Human-readable name for admin UI
4. **Constraints** — Validation rules (optional but recommended)
5. **Mapping** — Each config key with type, label, constraints

## Common Mistakes

- No schema defined — Drupal can't validate, config saved as untyped data
- Using `type: string` for structured data — Use `mapping` or `sequence` instead
- Missing `translatable: true` on user-facing text — Text won't appear in translation UI
- No constraints on required fields — Invalid data can be saved
- Using `type: ignore` unnecessarily — Prefer typed schema, only use for truly dynamic data
- Dots in mapping keys — Not allowed, use nested mappings instead

## See Also

- [Core Data Types Schema](core-data-types-schema.md) — available scalar and container types
- [Writing Config Schema](writing-config-schema.md) — step-by-step schema creation
- [Config Entity Schema Definition](config-entity-schema-definition.md) — schema for config entities
- Reference: [Configuration Schema/Metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)
