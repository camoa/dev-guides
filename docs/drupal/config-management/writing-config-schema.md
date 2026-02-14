---
description: Step-by-step guide to creating config schema for new modules with simple config or config entities.
---

# Writing Config Schema

## When to Use

When creating a new module with config (simple or entity) and you need to define schema so Drupal validates and casts config values correctly.

## Steps

1. **Create schema directory** — `MODULE/config/schema/`
2. **Create schema file** — `MODULE/config/schema/MODULE.schema.yml`
3. **Define top-level config name** — Must match config file name
4. **Set container type** — `config_object` for simple config, `config_entity` for entities
5. **Add FullyValidatable constraint** — Enables strict validation (recommended)
6. **Define mapping** — Each config key with type, label, constraints
7. **Add constraints** — NotBlank, Range, Email, etc. based on validation needs
8. **Mark translatable strings** — `translatable: true` on user-facing text
9. **Test schema** — `drush config:inspect MODULE.settings --validate-constraints`

## Example: Simple Config Schema

```yaml
# mymodule/config/schema/mymodule.schema.yml
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
      label: 'Enable API integration'
    max_retries:
      type: integer
      label: 'Maximum retries'
      constraints:
        Range:
          min: 1
          max: 10
    notification_email:
      type: email
      label: 'Notification email'
      constraints:
        Email: {}
    allowed_types:
      type: sequence
      label: 'Allowed content types'
      sequence:
        type: string
```

## Example: Config Entity Schema

```yaml
# mymodule/config/schema/mymodule.schema.yml
mymodule.example.*:
  type: config_entity
  label: 'Example configuration'
  constraints:
    FullyValidatable: ~
  mapping:
    id:
      type: machine_name
      label: 'ID'
    label:
      type: required_label
      label: 'Label'
    description:
      type: text
      label: 'Description'
      translatable: true
    weight:
      type: integer
      label: 'Weight'
      constraints:
        Range:
          min: -50
          max: 50
    status:
      type: boolean
      label: 'Enabled'
```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Defining type | Single config file | Use `config_object` |
| Defining type | Config entity | Use `config_entity` with wildcard `*` |
| Adding constraints | Field is required | Add `NotBlank: {}` constraint |
| Adding constraints | Numeric range validation | Add `Range: {min: X, max: Y}` |
| Adding constraints | Email validation | Use `type: email` + `Email: {}` |
| Marking translatable | User-facing text | Add `translatable: true` |

## Common Mistakes

- Schema file in wrong location — Must be `config/schema/MODULE.schema.yml`
- Schema name doesn't match config name — Must match exactly (e.g., `mymodule.settings`)
- No constraints on required fields — Invalid data can be saved
- Using dots in mapping keys — Not allowed, use nested mappings
- Missing FullyValidatable — Validation is lenient, allows missing keys
- Forgetting to clear cache after schema changes — Schema is cached, `drush cr` required

## See Also

- [Config Schema YAML](config-schema-yaml.md) — schema structure and syntax
- [Core Data Types Schema](core-data-types-schema.md) — available types
- [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md) — schema validation failures
- Reference: [Configuration Schema/Metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)
