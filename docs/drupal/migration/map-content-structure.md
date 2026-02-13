---
description: Map D7 field collections and content architecture to D11 entities
drupal_version: "11.x"
---

# Map Content Structure

## When to Use

After inventory, map D7 content architecture to D11 entity structure. D7 field collections become D11 paragraphs, D7 nodes may become media entities, taxonomy structure may consolidate.

## Decision

| D7 structure | D11 equivalent | Notes |
|---|---|---|
| Field Collection | Paragraph entity | Requires separate migration, target_id + target_revision_id |
| Node with file fields | Media entity | Use media library, better asset management |
| Body field with images | Media + entity reference | Separate media migration, reference in body |
| Taxonomy terms (simple) | Taxonomy terms | Direct 1:1 migration |
| Taxonomy terms (complex fields) | Custom entity or content type | Consider if taxonomy appropriate |

## Pattern

**Field collection to paragraph migration:**

```yaml
# Migration 1: Create paragraphs
id: d7_paragraph_slide
source:
  plugin: d7_field_collection_item
  field_name: field_slides
process:
  id: item_id
  type:
    plugin: default_value
    default_value: slide
  field_slide_title: field_slide_title
  field_slide_image:
    plugin: migration_lookup
    migration: d7_file
    source: field_slide_image
destination:
  plugin: entity:paragraph

# Migration 2: Reference paragraphs in node
id: d7_node_landing_page
process:
  field_slides:
    -
      plugin: migration_lookup
      migration: d7_paragraph_slide
      source: field_slides
      no_stub: true
    -
      plugin: sub_process
      process:
        target_id:
          - plugin: extract
            index: [0]
        target_revision_id:
          - plugin: extract
            index: [1]
```

**Reference**: `/modules/contrib/migrate_plus/` for process plugins

## Common Mistakes

- **Wrong**: Mapping D7 nodes to D11 nodes when media entity better → **Right**: Use media for files/images, better organization
- **Wrong**: Ignoring paragraph revision IDs → **Right**: Must set both target_id AND target_revision_id for paragraphs
- **Wrong**: Not planning migration order → **Right**: Migrate dependencies first (users, files, taxonomy before nodes)
- **Wrong**: Skipping field type changes → **Right**: Some D7 field types deprecated, require new field types in D11

## See Also

- [Handle field mappings](handle-field-mappings.md) for process plugin details
- [Complex field mappings](complex-field-mappings.md) for paragraphs/references
- Reference: [Drupal at your Fingertips - Migrate patterns](https://www.drupalatyourfingertips.com/migrate)
