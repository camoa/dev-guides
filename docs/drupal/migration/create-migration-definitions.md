---
description: YAML migration definition structure for source, process, and destination
drupal_version: "11.x"
---

# Create Migration Definitions

## When to Use

Migration definitions are YAML files defining source, process, and destination. Core provides templates for D7→D11 migrations. Custom migrations extend base patterns.

## Decision

| Migration type | Base template | Location |
|---|---|---|
| Simple content type | d7_node base | custom_module/config/install/ |
| Custom entity migration | Base migrate plugin | custom_module/migrations/ |
| User-provided migrations | No base | custom_module/config/install/migrate_plus.migration.*.yml |

## Pattern

**Complete migration definition structure:**

```yaml
id: d7_node_blog_post
label: D7 Blog Post nodes
migration_group: d7_content

source:
  plugin: d7_node
  node_type: blog_post
  # Optional: limit by node ID for testing
  # node_id_range: [1, 100]

process:
  # Simple 1:1 mapping
  nid: nid
  vid: vid
  langcode: language
  title: title
  uid:
    plugin: migration_lookup
    migration: d7_user
    source: uid
  status: status
  created: created
  changed: changed

  # Complex field with transformation
  body/value: body
  body/format:
    plugin: static_map
    source: body:format
    map:
      1: basic_html
      2: full_html
      3: plain_text
    default_value: basic_html

  # Entity reference field
  field_category:
    plugin: migration_lookup
    migration: d7_taxonomy_term_category
    source: field_category
    no_stub: true

  # Multi-value field
  field_tags:
    -
      plugin: sub_process
      source: field_tags
      process:
        target_id:
          plugin: migration_lookup
          migration: d7_taxonomy_term_tags
          source: tid
    -
      plugin: skip_on_empty
      method: process

destination:
  plugin: entity:node
  default_bundle: blog_post

migration_dependencies:
  required:
    - d7_user
    - d7_taxonomy_term_category
    - d7_taxonomy_term_tags
  optional: []

migration_tags:
  - Drupal 7
  - Content
```

**Reference**: `/core/modules/migrate/src/Plugin/Migration.php` for base migration class

## Common Mistakes

- **Wrong**: Not declaring migration dependencies → **Right**: Migrations run out of order, lookups fail
- **Wrong**: Missing no_stub: true on lookups → **Right**: Creates unwanted stub entities for missing references
- **Wrong**: Not testing with limited node ranges → **Right**: Full migration failures waste time
- **Wrong**: Hardcoding format IDs instead of mapping → **Right**: D7 format IDs don't match D11

## See Also

- [Configure migration sources](configure-migration-sources.md) for source plugin setup
- [Handle field mappings](handle-field-mappings.md) for process plugin details
- Reference: [Migration configuration](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-api-overview)
