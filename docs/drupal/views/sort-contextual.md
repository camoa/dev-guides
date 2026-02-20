## 10. Sort & Contextual Filters (Arguments)

### When to Use
When ordering results (sorts) or filtering based on URL parameters (contextual filters/arguments).

### Sort Criteria Configuration

#### Basic Sort
```yaml
sorts:
  changed:
    id: changed
    table: node_field_data
    field: changed
    entity_type: node
    entity_field: changed
    plugin_id: date
    order: DESC  # ASC or DESC
    expose:
      label: ''
    exposed: false
    granularity: second
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 283-303

#### Exposed Sort
```yaml
sorts:
  title:
    order: ASC
    exposed: true
    expose:
      label: 'Sort by title'
      field_identifier: title
```

Exposed sorts appear in exposed form, allowing users to choose sort field and direction.

### Contextual Filters (Arguments) Configuration

#### Core Argument Options
```yaml
arguments:
  nid:
    id: nid
    table: node_field_data
    field: nid
    entity_type: node
    entity_field: nid
    plugin_id: numeric
    relationship: none
    default_action: ignore  # ignore, not found, summary, empty, default
    exception:
      value: all  # Exception value that triggers special handling
      title_enable: false
      title: ''
    title_enable: false  # Override page/block title
    title: ''  # Title pattern with tokens
```

Reference: views.data_types.schema.yml lines 366-462

#### Default Argument Behavior
| default_action | Behavior |
|---|---|
| `ignore` | No argument → show all results (no filter applied) |
| `not found` | No argument → return 404 |
| `summary` | No argument → show summary list |
| `empty` | No argument → show empty text |
| `default` | No argument → use default argument plugin |

#### Default Argument Plugins
```yaml
arguments:
  nid:
    default_action: default
    default_argument_type: node  # Plugin ID
    default_argument_options:
      # Plugin-specific options (e.g., 'node' uses current node)
```

Common default argument plugins:
- `node`: Current node ID from route
- `user`: Current user ID
- `raw`: Raw value from URL
- `fixed`: Fixed value

#### Argument Validation
```yaml
arguments:
  nid:
    specify_validation: true
    validate:
      type: entity:node  # Validator plugin
      fail: 'not found'  # not found, empty, ignore
    validate_options:
      # Validator-specific options
      bundles: {}  # For entity validator
      access: true  # Check entity access
      operation: view
```

### Pattern
Contextual filter for user content:

```yaml
arguments:
  uid:
    id: uid
    table: node_field_data
    field: uid
    entity_type: node
    entity_field: uid
    plugin_id: numeric
    default_action: default
    default_argument_type: user
    default_argument_options:
      user: false  # false = current user
    summary:
      sort_order: asc
      number_of_records: 0
      format: default_summary
    specify_validation: true
    validate:
      type: 'entity:user'
      fail: 'not found'
    validate_options:
      access: true
      operation: view
    title_enable: true
    title: 'Content by {{ arguments.uid }}'
```

### Pattern: URL Structure with Arguments
Path: `/user/%/articles/%/comments`
Arguments:
1. `uid` (position 0) from first `%`
2. `nid` (position 1) from second `%`

Configure two arguments in order:
```yaml
arguments:
  uid:
    # First % in path
  nid:
    # Second % in path
```

### Common Mistakes
- Argument order doesn't match path wildcards → Argument 1 maps to first %, argument 2 to second %, etc.; order matters
- Using `default_action: not found` too liberally → 404s instead of empty results; usually `ignore` is safer
- Not validating arguments → Arbitrary input can cause query errors; always use `specify_validation: true` for user-provided arguments
- Validation type mismatch → Using `entity:node` validator on taxonomy term argument fails validation
- Forgetting `access: true` in validation → Users can see content they shouldn't access; always check entity access
- Not handling multiple values → By default, arguments accept single value; enable `break_phrase: true` for comma-separated values

### See Also
- Section 4: Page Display — using % in paths for arguments
- Section 11: Relationships — arguments on related entities
- Section 31: Security & Performance — argument validation security

