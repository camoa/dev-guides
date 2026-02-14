---
description: When you need a full page with a dedicated URL, menu integration, and optional admin theme.
drupal_version: "11.x"
---

## 4. Page Display

### When to Use
When you need a full page with a dedicated URL, menu integration, and optional admin theme.

### Steps
1. **Add page display** to existing view
2. **Configure path** for the page URL
3. **Set menu options** (none, normal menu link, tab, default tab)
4. **Configure access** (who can view this page)
5. **Override display options** as needed (pager, fields, filters)

### Page-Specific Options

#### Path Configuration
```yaml
page_1:
  display_plugin: page
  display_options:
    path: admin/content/node
```

- **Path**: URL pattern, can include wildcards `%` for arguments
- **Wildcards become arguments**: `/user/%/posts` → `%` is UID argument

#### Menu Configuration
```yaml
display_options:
  menu:
    type: tab  # none, normal, tab, default tab
    title: 'My Menu Link'
    description: 'Hover text'
    weight: 0
    menu_name: main  # For 'normal' type
    parent: ''  # Parent menu item ID
    context: '0'  # Show in contextual links (tabs only)
    expanded: false  # Show children expanded
```

**Menu types:**
- `none`: No menu link
- `normal`: Regular menu link in specified menu
- `tab`: Local task tab
- `default tab`: Primary tab (creates parent automatically if needed)

#### Tab Parent Options (for `default tab` type)
```yaml
display_options:
  tab_options:
    type: normal  # none, normal, tab
    title: 'Parent Tab Title'
    description: 'Parent description'
    weight: 0
```

Reference: `core/modules/views/src/Plugin/views/display/Page.php` lines 148-174

### Pattern
Page display with menu tab:

```yaml
page_published:
  id: page_published
  display_title: 'Published Content'
  display_plugin: page
  position: 1
  display_options:
    path: admin/content/published
    menu:
      type: tab
      title: 'Published'
      description: 'Published content'
      weight: 0
      menu_name: admin
      context: '0'
    access:
      type: perm
      options:
        perm: 'access content overview'
```

Reference: `core/modules/comment/config/optional/views.view.comment.yml` lines 870-888

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Choosing menu type | Path has wildcards (%) | Cannot use 'normal' menu type (validation error) |
| Setting path | Path starts with `admin/` | Admin theme auto-applied regardless of setting |
| Creating tabs | Using 'default tab' | Must configure tab_options for parent menu link |

### Common Mistakes
- Path with `%` and menu type 'normal' → Validation error; wildcards incompatible with normal menu links (code reference: Page.php line 504)
- Ending path with `%` for tab display → Cannot create tab; path cannot end with wildcard (Page.php line 511)
- Empty menu title when type is not 'none' → Validation error; menu links require title (Page.php line 516)
- Using 'default tab' without defining parent → Works, but creates default parent with view label as title

### See Also
- Section 10: Sort & Contextual Filters — using % wildcards in paths as arguments
- Section 14: Access Control — setting page-level permissions
- Section 17: Views Config Export & Recipes — exporting page displays with menu links
