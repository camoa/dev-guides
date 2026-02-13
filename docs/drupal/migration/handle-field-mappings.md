---
description: Process plugins for transforming source data to destination format
drupal_version: "11.x"
---

# Handle Field Mappings

## When to Use

Process plugins transform source data to destination format. Core provides 50+ plugins for common transformations. Chain plugins in pipelines for complex mappings.

## Decision

| Transformation needed | Process plugin | Example |
|---|---|---|
| Direct copy | Source field name | `nid: nid` |
| Static value | default_value | Set content type, format |
| Conditional mapping | static_map | Map D7 format IDs to D11 |
| Related entity lookup | migration_lookup | User, taxonomy, file references |
| Array element extraction | extract | Get specific index from array |
| Skip on empty | skip_on_empty | Prevent errors on null values |
| Substring/regex | substr, callback | Text transformations |
| Multi-value processing | sub_process | Process each array item |

## Pattern

**Process plugin pipeline (multiple steps):**

```yaml
process:
  # Simple copy
  title: title

  # Static value
  type:
    plugin: default_value
    default_value: article

  # Conditional mapping
  body/format:
    plugin: static_map
    source: body:format
    map:
      1: basic_html
      2: full_html
    default_value: basic_html

  # Entity reference with error handling
  field_author:
    -
      plugin: migration_lookup
      migration: d7_user
      source: field_author_uid
      no_stub: true
    -
      plugin: skip_on_empty
      method: process
    -
      plugin: default_value
      default_value: 1  # Fallback to admin user

  # Multi-value field with sub-process
  field_images:
    -
      plugin: sub_process
      source: field_images
      process:
        target_id:
          -
            plugin: migration_lookup
            migration: d7_file
            source: fid
          -
            plugin: skip_on_empty
            method: row
        alt: alt
        title: title
```

**Reference**: `/core/modules/migrate/src/Plugin/migrate/process/` for core process plugins

## Common Mistakes

- **Wrong**: Not chaining skip_on_empty after migration_lookup → **Right**: Null references cause migration failures
- **Wrong**: Using extract without checking array structure → **Right**: Index errors on variable data
- **Wrong**: Not setting no_stub: true → **Right**: Creates unwanted placeholder entities
- **Wrong**: Missing default values → **Right**: Empty required fields fail destination validation

## See Also

- [Complex field mappings](complex-field-mappings.md) for paragraphs/advanced scenarios
- Reference: [Process plugin list](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-process-plugins/list-of-process-plugins)
- Reference: [Process pipelines](https://www.drupal.org/docs/drupal-apis/migrate-api/process-pipelines)
