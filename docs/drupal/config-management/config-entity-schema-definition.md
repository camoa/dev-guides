---
description: Define config schema for config entities — matching exported YAML structure and including all entity keys.
---

# Config Entity Schema Definition

## When to Use

When defining config schema for config entities — schema must match exported YAML structure and include all entity keys.

## Required Entity Keys

| Key | Type | Description |
|-----|------|-------------|
| `id` | `machine_name` | Unique identifier |
| `label` | `label` or `required_label` | Human-readable name |
| `uuid` | `uuid` | Universal unique ID |
| `status` | `boolean` | Enabled/disabled state |
| `langcode` | `langcode` | Language code |
| `dependencies` | `config_dependencies` | Module, theme, config, content dependencies |

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
      label: 'Machine name'
      constraints:
        NotBlank: {}
        Regex:
          pattern: '/^[a-z0-9_]+$/'
    label:
      type: required_label
      label: 'Label'
    uuid:
      type: uuid
      label: 'UUID'
      constraints:
        Uuid: []
    status:
      type: boolean
      label: 'Status'
    langcode:
      type: langcode
      label: 'Language code'
    dependencies:
      type: config_dependencies
      label: 'Dependencies'
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
    settings:
      type: mapping
      label: 'Settings'
      mapping:
        timeout:
          type: integer
          label: 'Timeout (seconds)'
          constraints:
            Range:
              min: 1
              max: 300
        retry:
          type: boolean
          label: 'Retry on failure'
    third_party_settings:
      type: sequence
      label: 'Third party settings'
      sequence:
        type: mymodule.example.third_party.[%parent.%parent.%key]
```

**Reference:** `/core/config/schema/core.data_types.schema.yml`, `/core/modules/system/config/schema/system.schema.yml`

## Core Entity Schema Types

| Type | Use For |
|------|---------|
| `config_entity` | Top-level wrapper for config entities |
| `config_dependencies` | Dependencies mapping (module, theme, config, content, enforced) |
| `config_object` | Nested config objects within entity |
| `entity_reference` | References to other entities |
| `machine_name` | Machine-readable IDs |
| `required_label` | Non-empty labels |

## Example: Entity with Plugin Configuration

```yaml
mymodule.plugin_entity.*:
  type: config_entity
  label: 'Plugin-based entity'
  constraints:
    FullyValidatable: ~
  mapping:
    id:
      type: machine_name
    label:
      type: required_label
    plugin_id:
      type: string
      label: 'Plugin ID'
      constraints:
        NotBlank: {}
    plugin_config:
      type: mymodule.plugin.[%parent.plugin_id]
      label: 'Plugin configuration'
```

**Reference:** `/core/modules/views/config/schema/views.view.schema.yml` — complex example with plugins

## Common Mistakes

- Missing entity keys in schema — `id`, `label`, `uuid`, `status` required
- Schema name doesn't match export path — Must use `MODULE.ENTITY_TYPE.*` wildcard pattern
- No FullyValidatable constraint — Validation is lenient, allows missing keys
- Wrong type for dependencies — Must use `config_dependencies`, not custom mapping
- Not accounting for third-party settings — All config entities support third-party settings
- Missing `config_export` in entity annotation — All properties exported, including internal state

## See Also

- [Config Entities](config-entities.md) — creating config entity types
- [Core Data Types Schema](core-data-types-schema.md) — available types
- [Writing Config Schema](writing-config-schema.md) — schema creation workflow
- Reference: [Configuration Schema/Metadata](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)
