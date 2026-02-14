---
description: When configuring how Views formats output (style) and renders individual rows (row).
drupal_version: "11.x"
---

## 15. Style & Row Plugins

### When to Use
When configuring how Views formats output (style) and renders individual rows (row).

### Style Plugins

#### Table Style
```yaml
style:
  type: table
  options:
    grouping: {}
    row_class: ''
    default_row_class: true
    columns:
      title: title
      type: type
      name: name
    default: changed  # Default sort column
    info:
      title:
        sortable: true
        default_sort_order: asc
        align: ''
        separator: ''
        empty_column: false
        responsive: ''
      type:
        sortable: true
        default_sort_order: asc
        align: ''
        separator: ''
        empty_column: false
        responsive: priority-low  # Hide on mobile
    override: true  # Override default columns
    sticky: true  # Sticky table headers
    summary: ''
    empty_table: true  # Show table structure when empty
    caption: ''
    description: ''
```

Reference: `core/modules/node/config/optional/views.view.content.yml` lines 535-625

#### Unformatted List
```yaml
style:
  type: default  # Unformatted list
  options:
    grouping: {}
    row_class: ''
    default_row_class: true
    uses_fields: false
```

#### HTML List
```yaml
style:
  type: html_list
  options:
    grouping: {}
    row_class: ''
    default_row_class: true
    type: ul  # ul, ol
    wrapper_class: item-list
    class: ''
```

#### Grid
```yaml
style:
  type: grid
  options:
    grouping: {}
    columns: 4
    automatic_width: true
    alignment: horizontal  # horizontal, vertical
    col_class: ''
    row_class: ''
```

#### Serializer (for REST Export)
```yaml
style:
  type: serializer
  options:
    formats:
      json: json
      xml: xml
    uses_fields: false  # Use entity serialization
```

### Row Plugins

#### Fields Row
```yaml
row:
  type: fields
  options: {}
```

Uses field configuration from `fields` section. Most flexible.

#### Entity Row
```yaml
row:
  type: 'entity:node'
  options:
    view_mode: teaser  # View mode for entity rendering
```

Renders full entity using view mode display. Simpler than fields but less control.

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 897-902

#### Data Entity (for REST Export)
```yaml
row:
  type: data_entity
  options:
    view_mode: default
```

#### Data Field (for REST Export)
```yaml
row:
  type: data_field
  options: {}
```

Uses field-level serialization instead of entity-level.

### Decision
| If you need... | Use style... | Use row... | Why |
|---|---|---|---|
| Admin table with sortable columns | table | fields | Full control over columns, sorting |
| Teaser listings | default/html_list | entity:node | Reuse view mode theming |
| Grid layout (products, images) | grid | fields/entity | Automatic responsive columns |
| JSON API output | serializer | data_entity | Entity serialization |
| Custom field-only JSON | serializer | data_field | Field-level control |

### Pattern
Table with responsive columns:

```yaml
style:
  type: table
  options:
    grouping: {}
    row_class: ''
    default_row_class: true
    columns:
      title: title
      changed: changed
      operations: operations
    default: changed
    info:
      title:
        sortable: true
        default_sort_order: asc
        responsive: ''
      changed:
        sortable: true
        default_sort_order: desc
        responsive: priority-low
      operations:
        sortable: false
        responsive: ''
    override: true
    sticky: true
    empty_table: true
row:
  type: fields
```

### Common Mistakes
- Table style with entity row → Table expects fields; use `row: fields`
- Serializer style with fields row when entity serialization intended → Use `row: data_entity` for entity serialization, `data_field` for field-based
- Not setting `responsive` on table columns → All columns show on mobile; use `priority-low`, `priority-medium` to hide on narrow screens
- Grid style with odd number of items and `automatic_width: false` → Last row looks broken; use `automatic_width: true`
- Forgetting `override: true` on table style → Default columns used instead of custom config

### See Also
- Section 8: Fields Configuration — configuring fields for fields row
- Section 6: REST Export Display — serializer configuration
- Reference: [views.style schema](https://api.drupal.org/api/drupal/core!modules!views!config!schema!views.data_types.schema.yml/11.x)
