---
description: You need to query and display lists of content, users, taxonomy terms, or other entities with filtering, sorting, and display formatting.
drupal_version: "11.x"
---

## 1. Views System Overview

### When to Use
You need to query and display lists of content, users, taxonomy terms, or other entities with filtering, sorting, and display formatting.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Admin UI to build queries | Views | Zero code, exportable config, UI-friendly |
| Complex custom query logic | Custom query + controller | Full control, but harder to maintain |
| Simple entity lists with filters | Views | Faster, config-based, non-developers can modify |
| Performance-critical unique query | EntityQuery + custom code | Optimize at code level, avoid Views overhead |
| Lists that change frequently (filters, sorts) | Views | Config changes don't require code deploys |

### Pattern
Views config is a config entity stored in `config/sync/views.view.{view_id}.yml`. Example structure:

```yaml
id: my_view
label: 'My Custom View'
module: views
base_table: node_field_data
display:
  default:
    display_plugin: default
    display_options:
      # Common options shared by all displays
  page_1:
    display_plugin: page
    display_options:
      path: my-path
```

Reference: `core/modules/views/src/Entity/View.php` lines 38-45 (config_export keys)

### Display Types
- **Page**: Full page with URL and menu integration
- **Block**: Placed in block regions or Layout Builder
- **REST Export**: JSON/XML output via serializer
- **Embed**: Programmatically embedded, no direct URL
- **Attachment**: Attached to other displays (before/after)
- **Feed**: RSS/Atom feeds

### Common Mistakes
- Using Views for one-off queries → Write custom query instead for clarity and performance
- Not exporting Views to config → Manual DB-only views break on sync, can't track in version control
- Creating page displays when a block would suffice → Blocks are more flexible (Layout Builder, context placement)

### See Also
- Section 2: View Config Schema — full YAML structure
- Section 17: Views Config Export & Recipes — managing views as config
- Reference: [Drupal Views API Overview](https://www.drupal.org/docs/drupal-apis/views-api)
