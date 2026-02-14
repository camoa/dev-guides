---
description: When configuring field output, labels, formatters, rewriting, and CSS classes in views using fields-based rows.
drupal_version: "11.x"
---

## 8. Fields Configuration

### When to Use
When configuring field output, labels, formatters, rewriting, and CSS classes in views using fields-based rows.

### Field Handler Schema

#### Core Field Options
```yaml
fields:
  field_id:
    id: field_id  # Unique ID for this field instance
    table: node_field_data  # Views data table
    field: title  # Field name from table
    entity_type: node  # Optional: entity type
    entity_field: title  # Optional: entity field name
    plugin_id: field  # Field handler plugin ID
    relationship: none  # Or relationship ID
    group_type: group  # Or aggregation type
    admin_label: ''  # Admin UI identifier
    label: 'Title'  # Public field label
    exclude: false  # Hide from output (for rewriting)
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 489-628

#### Field Formatting Options
| Option | Type | Purpose |
|--------|------|---------|
| `type` | string | Formatter plugin ID (e.g., `string`, `timestamp`, `entity_reference_label`) |
| `settings` | mapping | Formatter-specific settings (link_to_entity, date_format, etc.) |
| `click_sort_column` | string | Which column to sort by (for multi-value fields) |
| `group_column` | string | Column for grouping |

#### Rewrite & Alteration
```yaml
fields:
  title:
    alter:
      alter_text: false  # Enable rewriting
      text: ''  # Rewrite pattern with tokens
      make_link: false  # Turn output into link
      path: ''  # Link path (supports tokens)
      absolute: false  # Absolute URL
      external: false  # External link
      replace_spaces: false  # Replace spaces with dashes in path
      path_case: none  # none, lower, upper
      trim_whitespace: false
      alt: ''  # Link title attribute
      rel: ''  # Link rel attribute
      link_class: ''  # Link CSS class
      prefix: ''  # Text before field
      suffix: ''  # Text after field
      target: ''  # Link target (_blank, etc.)
      nl2br: false  # Convert newlines to <br>
      max_length: 0  # Trim to N characters (0 = no limit)
      word_boundary: true  # Trim on word boundary
      ellipsis: true  # Add … when trimmed
      more_link: false  # Add read-more link if trimmed
      more_link_text: ''
      more_link_path: ''
      strip_tags: false  # Strip HTML tags
      trim: false  # Enable trimming
      preserve_tags: ''  # Tags to preserve when stripping
      html: false  # Field contains HTML
```

Reference: lines 498-578 in views.data_types.schema.yml

#### Element Wrappers
```yaml
fields:
  title:
    element_type: ''  # HTML element for field (div, span, etc.)
    element_class: ''  # CSS class for field wrapper
    element_label_type: ''  # HTML element for label
    element_label_class: ''  # CSS class for label
    element_label_colon: true  # Show colon after label
    element_wrapper_type: ''  # Outer wrapper element
    element_wrapper_class: ''  # Outer wrapper CSS class
    element_default_classes: true  # Add Views default classes
```

#### Empty Field Handling
```yaml
fields:
  title:
    empty: ''  # Text to show if field is empty
    hide_empty: false  # Hide entire field if value is empty
    empty_zero: false  # Treat 0 as empty
    hide_alter_empty: true  # Hide rewrite if field is empty
```

### Pattern
Field with link, trimming, and custom CSS:

```yaml
fields:
  title:
    id: title
    table: node_field_data
    field: title
    entity_type: node
    entity_field: title
    plugin_id: field
    label: 'Article Title'
    exclude: false
    alter:
      alter_text: false
      make_link: true
      path: 'node/{{ nid }}'
      trim: true
      max_length: 100
      word_boundary: true
      ellipsis: true
    element_type: h3
    element_class: 'view-title'
    element_default_classes: false
    hide_empty: true
    type: string
    settings:
      link_to_entity: false  # We're using custom link
```

Reference: `core/modules/node/config/optional/views.view.content.yml` lines 39-55

### Common Mistakes
- Setting `exclude: true` without using field in rewrite → Field is queried but not shown; wastes performance
- Using `alter.text` without `alter_text: true` → Rewrite pattern is ignored
- Token syntax errors in rewrite patterns → Use `{{ field_name }}` not `[field_name]`
- Forgetting `trim: true` when setting `max_length` → max_length has no effect without trim enabled
- Using `element_type` for semantic meaning in non-table styles → Element wrappers only affect fields row style, not entity rendering
- Setting `link_to_entity: true` in formatter AND `make_link: true` → Double-wrapped links; choose one approach

### See Also
- Section 15: Style & Row Plugins — fields vs entity row rendering
- Section 9: Filters & Exposed Filters — using field values in filters
- Reference: [views_field schema](https://api.drupal.org/api/drupal/core!modules!views!config!schema!views.data_types.schema.yml/11.x)
