---
description: When you need to access fields from related entities (entity references, users, taxonomy terms, etc.) or apply filters/sorts on related entity data.
drupal_version: "11.x"
---

## 11. Relationships

### When to Use
When you need to access fields from related entities (entity references, users, taxonomy terms, etc.) or apply filters/sorts on related entity data.

### Relationship Configuration

#### Basic Relationship
```yaml
relationships:
  uid:
    id: uid
    table: node_field_data
    field: uid  # Entity reference field
    relationship: none  # Parent relationship (or 'none')
    entity_type: node
    entity_field: uid
    plugin_id: standard  # Relationship plugin
    admin_label: 'author'  # Admin UI label
    required: false  # INNER JOIN (true) or LEFT JOIN (false)
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 866-883

#### Required vs Optional
- `required: true` → INNER JOIN → Only rows with relationship present
- `required: false` → LEFT JOIN → All rows, related data if available

### Common Relationship Patterns

#### Author Relationship (Node → User)
```yaml
relationships:
  uid:
    id: uid
    table: node_field_data
    field: uid
    admin_label: 'author'
    plugin_id: standard
    required: true
```

Then use author fields:
```yaml
fields:
  name:
    id: name
    table: users_field_data
    field: name
    relationship: uid  # References relationship ID
    plugin_id: field
    label: 'Author Name'
```

Reference: `core/modules/node/config/optional/views.view.content.yml` lines 633-640

#### Entity Reference Field Relationship
```yaml
relationships:
  field_tags:
    id: field_tags
    table: node__field_tags
    field: field_tags_target_id
    admin_label: 'field_tags: Taxonomy term'
    plugin_id: standard
    required: false
```

#### Reverse Relationships (Referenced Entity → Referencing)
```yaml
relationships:
  reverse__node__field_tags:
    id: reverse__node__field_tags
    table: taxonomy_term_field_data
    field: reverse__node__field_tags
    admin_label: 'Nodes referencing this term'
    plugin_id: entity_reverse
    required: false
```

Used when base table is `taxonomy_term_field_data` and you want fields from nodes that reference those terms.

### Pattern
Node view with author name from relationship:

```yaml
display:
  default:
    display_options:
      relationships:
        uid:
          id: uid
          table: node_field_data
          field: uid
          admin_label: 'author'
          plugin_id: standard
          required: true
      fields:
        title:
          id: title
          table: node_field_data
          field: title
          plugin_id: field
        name:
          id: name
          table: users_field_data
          field: name
          relationship: uid  # Uses author relationship
          plugin_id: field
          label: 'Author'
      filters:
        status_1:
          id: status_1
          table: users_field_data
          field: status
          relationship: uid  # Filter on author status
          value: '1'
          plugin_id: boolean
```

### Chained Relationships
```yaml
relationships:
  uid:
    id: uid
    table: node_field_data
    field: uid
    admin_label: 'author'
    plugin_id: standard
    required: false

  user_picture:
    id: user_picture
    table: user__user_picture
    field: user_picture
    relationship: uid  # Chain off author relationship
    admin_label: 'author picture'
    plugin_id: standard
    required: false
```

### Common Mistakes
- Using `required: true` when relationship might not exist → Results disappear unexpectedly; use LEFT JOIN unless you specifically want to exclude rows
- Chaining relationships incorrectly → Child relationship must reference parent relationship ID in `relationship` key
- Not setting `admin_label` → Generic labels in UI make debugging hard; always use descriptive admin labels
- Forgetting to set `relationship` on fields/filters → Field comes from base table instead of related entity
- Circular relationship references → Views doesn't detect this; leads to invalid queries
- Overusing relationships → Each relationship is a JOIN; performance degrades with many JOINs

### See Also
- Section 8: Fields Configuration — using relationship fields
- Section 9: Filters & Exposed Filters — filtering on relationship data
- Section 16: Query Settings — DISTINCT to handle multiple relationship matches
