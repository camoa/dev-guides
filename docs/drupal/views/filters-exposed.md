---
description: When restricting query results via fixed criteria (filters) or user-selectable criteria (exposed filters).
drupal_version: "11.x"
---

## 9. Filters & Exposed Filters

### When to Use
When restricting query results via fixed criteria (filters) or user-selectable criteria (exposed filters).

### Filter Handler Schema

#### Core Filter Options
```yaml
filters:
  filter_id:
    id: filter_id
    table: node_field_data
    field: status
    entity_type: node
    entity_field: status
    plugin_id: boolean  # Filter plugin type
    relationship: none
    group_type: group
    operator: '='  # Filter operator (=, !=, <, >, IN, etc.)
    value: '1'  # Filter value (type varies by plugin)
    group: 1  # Filter group number
    exposed: false  # Expose to users
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 738-850

#### Exposed Filter Configuration
```yaml
filters:
  title:
    exposed: true
    expose:
      operator_id: title_op  # HTML name for operator field
      label: 'Title'  # Exposed form label
      description: ''  # Help text
      use_operator: false  # Show operator select
      operator: title_op  # Operator field name
      operator_limit_selection: false  # Limit available operators
      operator_list: {}  # Which operators to show
      identifier: title  # Query parameter name
      required: false  # Required field
      remember: false  # Remember via session
      multiple: false  # Allow multiple selections
      remember_roles:
        authenticated: authenticated  # Roles that can remember
```

#### Grouped Filters (Alternative to Basic Exposed)
```yaml
filters:
  status:
    is_grouped: true
    group_info:
      label: 'Publication Status'
      description: ''
      identifier: status
      optional: true  # Include "Any" option
      widget: select  # select, radios, checkboxes
      multiple: false
      remember: false
      default_group: All
      default_group_multiple: []
      group_items:
        1:
          title: Published
          operator: '='
          value: '1'
        2:
          title: Unpublished
          operator: '='
          value: '0'
```

Reference: lines 799-840 in views.data_types.schema.yml

### Filter Groups (AND/OR Logic)
```yaml
display_options:
  filter_groups:
    operator: AND  # AND or OR
    groups:
      1: AND  # Group 1 logic
      2: OR   # Group 2 logic
  filters:
    title:
      group: 1  # Belongs to group 1
    type:
      group: 1  # Belongs to group 1
    status:
      group: 2  # Belongs to group 2
```

**Logic**: `(title AND type) AND (status)`

### Pattern
Exposed filter with grouped options:

```yaml
filters:
  status:
    id: status
    table: node_field_data
    field: status
    entity_type: node
    entity_field: status
    plugin_id: boolean
    operator: '='
    value: '1'
    group: 1
    exposed: true
    expose:
      operator_id: ''
      label: 'Publication Status'
      use_operator: false
      operator: status_op
      identifier: status
      required: false
      remember: false
      multiple: false
      remember_roles:
        authenticated: authenticated
    is_grouped: true
    group_info:
      label: 'Published status'
      identifier: status
      optional: true
      widget: select
      multiple: false
      remember: false
      default_group: All
      group_items:
        1:
          title: Published
          operator: '='
          value: '1'
        2:
          title: Unpublished
          operator: '='
          value: '0'
```

Reference: `core/modules/node/config/optional/views.view.content.yml` lines 430-477

### Exposed Form Configuration
```yaml
display_options:
  exposed_form:
    type: basic  # basic, or custom plugin
    options:
      submit_button: Filter
      reset_button: true
      reset_button_label: Reset
      exposed_sorts_label: 'Sort by'
      expose_sort_order: true
      sort_asc_label: Asc
      sort_desc_label: Desc
```

Reference: views.data_types.schema.yml lines 464-487

### Exposed Filter Block (Separate from Results)
```yaml
display_options:
  exposed_block: true  # Creates separate exposed filter block
```

When enabled, exposed form renders in a separate block (`views_exposed_filter_block:{view_id}-{display_id}`) that can be placed independently.

### Common Mistakes
- Exposed filter without `identifier` → Defaults to field name; conflicts if same field used twice
- Using `remember: true` without understanding session → Filters persist across visits; confusing for users who don't expect it
- Not setting `required: false` intentionally → Required exposed filters prevent "View all" use case
- Grouped filters with `optional: false` → No way to clear filter; always set `optional: true` for flexibility
- Forgetting `expose.label` → Shows machine field name in form
- Complex filter groups without testing logic → AND/OR combinations can produce unexpected results; verify with known data
- Exposed filters without validation → User input is sanitized but logical validation (e.g., date ranges) must be handled by filter plugin

### See Also
- Section 5: Block Display — exposed filter blocks
- Section 31: Security & Performance — exposed filter security
- Reference: [Better Exposed Filters module](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/better-exposed-filters) for enhanced UX
