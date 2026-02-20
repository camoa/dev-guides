## 2. View Config Schema (views.view.*.yml)

### When to Use
When writing or editing views.view.*.yml files directly, or understanding config structure for recipes and exports.

### Top-Level Keys

#### Essential Keys
| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `id` | machine_name | Unique ID, max 128 chars | `my_view` |
| `label` | required_label | Human-readable name | `My Content Listing` |
| `module` | string | Module that provides the view | `views` |
| `base_table` | string | Database table to query | `node_field_data`, `users_field_data`, `comment_field_data` |
| `base_field` | string | Primary field for the base table | `nid`, `uid`, `cid` |

#### Optional Keys
| Key | Type | Description |
|-----|------|-------------|
| `description` | text | Admin-only description shown in Views UI |
| `tag` | string | Categorization tag for Views UI grouping |
| `display` | sequence | Array of display configurations (see below) |

### Display Structure
Each display in the `display` array contains:

```yaml
display:
  display_id:  # e.g., 'default', 'page_1', 'block_1'
    id: display_id
    display_title: 'Human Title'
    display_plugin: page  # page, block, rest_export, etc.
    position: 0  # Order in UI
    display_options:
      # Display-specific config (see Section 3)
    cache_metadata:
      max-age: 0
      contexts: ['languages:language_interface', 'url.query_args']
      tags: []
```

Reference: `core/modules/views/config/schema/views.schema.yml` lines 62-136

### Pattern
Minimal working view config:

```yaml
langcode: en
status: true
dependencies:
  module:
    - node
    - user
id: simple_list
label: 'Simple Node List'
module: views
base_table: node_field_data
base_field: nid
display:
  default:
    id: default
    display_title: Default
    display_plugin: default
    position: 0
    display_options:
      title: 'Simple List'
      fields:
        title:
          id: title
          table: node_field_data
          field: title
          entity_type: node
          entity_field: title
          plugin_id: field
```

Reference: `core/modules/node/config/optional/views.view.content.yml`

### Common Mistakes
- Omitting `base_field` when base_table requires it → Query fails to join properly
- Wrong `base_table` for entity type → Use `{entity_type}_field_data` for most entities, not raw entity table
- Invalid `display_plugin` value → Must be registered display plugin (page, block, etc.)
- Exceeding 128 character limit on `id` → Schema validation fails on config import

### See Also
- Section 3: Display Configuration — full `display_options` schema
- Section 32: Code Reference Map — View entity class
- Reference: [views.schema.yml API docs](https://api.drupal.org/api/drupal/core!modules!views!config!schema!views.schema.yml/11.x)

