---
description: Theming and templates in Plus Suite — CSS library map, color configuration, template overrides, hook implementations, and theme integration
tldr: "Override color configuration at `/admin/config/content/plus-suite` for brand customization. Override templates only when structural changes are needed."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> Override color configuration at `/admin/config/content/plus-suite` for brand customization. Override templates only when structural changes are needed.

## Decision

| Customization | Where |
|---------------|-------|
| Brand colors | `/admin/config/content/plus-suite` global settings |
| Toolbar/sidebar styles | Override `navigation_plus/modes` CSS library |
| Block template | Override `block--inline-block--*.html.twig` in your theme |
| Nested layout page | Override `page--lb-plus-layout-block.html.twig` |

## Pattern

**Available templates:**

| Template | Module | Purpose |
|----------|--------|---------|
| `page--lb-plus-layout-block.html.twig` | lb_plus | Minimal page for nested layout editing |

**CSS libraries by module:**

| Library | Module | Contains |
|---------|--------|---------|
| `navigation_plus/modes` | navigation_plus | Toolbar, sidebar, mode buttons |
| `navigation_plus/edit_mode` | navigation_plus | Drop zones, context menus, tool indicators |
| `navigation_plus/sidebar` | navigation_plus | Sidebar panels, scrollable content |
| `lb_plus/place_block` | lb_plus | Place block sidebar styling |
| `lb_plus/layout` | lb_plus | Layout outlines, nested layout UI |
| `edit_plus/library` | edit_plus | Inline editing, CKEditor integration |

**Global color configuration:**

```yaml
navigation_plus.settings:
  colors:
    main: '#1a73e8'
    secondary: '#ffffff'
    highlight: '#ff6b35'
```

**Theme integration requirements:**
1. Support core Navigation module (`navigation` core module enabled)
2. Do not override the admin toolbar (Plus Suite replaces it)
3. Provide proper body classes for Edit Mode CSS targeting

**Preprocessing hooks:**

| Hook | Module | Purpose |
|------|--------|---------|
| `preprocess_field` | navigation_plus | Adds field editing attributes |
| `preprocess_navigation` | navigation_plus | Adds mode toolbars to sidebar |
| `preprocess_top_bar` | navigation_plus | Adds Edit Mode top bar |

## Common Mistakes

- **Wrong**: Using `!important` to override Plus Suite CSS → **Right**: Use CSS specificity or the global color configuration
- **Wrong**: Removing the Navigation module → **Right**: Plus Suite depends on the Navigation sidebar

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [JavaScript Architecture](javascript-architecture.md)
- Reference: `navigation_plus/templates/`, `lb_plus/templates/`
