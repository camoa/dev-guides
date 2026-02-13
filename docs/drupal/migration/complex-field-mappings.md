---
description: Multi-step process pipelines for paragraphs and entity references with revisions
drupal_version: "11.x"
---

# Complex Field Mappings

## When to Use

Paragraphs, entity references with revisions, and nested structures require multi-step process pipelines. Understand target field structure before mapping.

## Decision

| Field type | Complexity | Required properties |
|---|---|---|
| Simple reference | Low | target_id only |
| Paragraph reference | High | target_id + target_revision_id |
| File/image field | Medium | target_id + alt + title |
| Link field | Medium | uri + title + options |
| Date range | Medium | value + end_value |

## Pattern

**Paragraph migration (most complex):**

```yaml
# Step 1: Migrate paragraph entities
id: d7_paragraph_quote
source:
  plugin: d7_field_collection_item
  field_name: field_quotes
process:
  id: item_id
  revision_id: revision_id
  type:
    plugin: default_value
    default_value: quote
  field_quote_text: field_quote_text
  field_quote_author: field_quote_author
destination:
  plugin: entity:paragraph
migration_dependencies:
  required: []

# Step 2: Reference paragraphs in node (requires BOTH IDs)
id: d7_node_testimonial
process:
  field_quotes:
    -
      plugin: sub_process
      source: field_quotes
      process:
        target_id:
          -
            plugin: migration_lookup
            migration: d7_paragraph_quote
            source: value
          -
            plugin: extract
            index: [0]  # Get target_id from lookup result
        target_revision_id:
          -
            plugin: migration_lookup
            migration: d7_paragraph_quote
            source: value
          -
            plugin: extract
            index: [1]  # Get target_revision_id from lookup result
    -
      plugin: skip_on_empty
      method: process
```

**Link field mapping:**

```yaml
process:
  field_external_link/uri:
    plugin: callback
    callable: trim
    source: field_external_link:url
  field_external_link/title: field_external_link:title
  field_external_link/options:
    plugin: default_value
    default_value:
      attributes:
        target: _blank
```

**Reference**: [Drupal at your Fingertips - Paragraph migration](https://www.drupalatyourfingertips.com/migrate)

## Common Mistakes

- **Wrong**: Using extract without sub_process → **Right**: Index errors on arrays
- **Wrong**: Not separating paragraph migration → **Right**: Circular dependencies fail
- **Wrong**: Missing target_revision_id on paragraphs → **Right**: References break, orphaned content
- **Wrong**: Not handling empty multi-value fields → **Right**: Use skip_on_empty to prevent errors
- **Wrong**: Assuming migration_lookup returns single value → **Right**: Returns [target_id, revision_id] for revisionable entities

## See Also

- [Handle field mappings](handle-field-mappings.md) for basic process plugins
- Reference: [Process plugin extract](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-process-plugins/process-plugin-extract)
- Reference: [Process plugin sub_process](https://www.drupal.org/docs/drupal-apis/migrate-api/migrate-process-plugins/process-plugin-sub_process)
