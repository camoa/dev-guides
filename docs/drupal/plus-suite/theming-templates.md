---
description: Theming and templates in Plus Suite — CSS library map, color configuration, template overrides, hook implementations, and theme integration
tldr: "Override color configuration at `/admin/config/content/plus-suite` for brand customization. Override templates only when structural changes are needed."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> When customizing the visual appearance of Plus Suite's editing interface or overriding default templates.

## Template Overrides

Plus Suite provides one template:

| Template | Module | Purpose |
|---|---|---|
| `page--lb-plus-layout-block.html.twig` | lb_plus | Minimal page for nested layout editing (renders only `{{ page.content }}`) |

## CSS Architecture

| Library | Module | Contains |
|---|---|---|
| `navigation_plus/modes` | navigation_plus | Toolbar, sidebar, mode buttons |
| `navigation_plus/edit_mode` | navigation_plus | Drop zones, context menus, tool indicators, messages |
| `navigation_plus/sidebar` | navigation_plus | Sidebar panels, scrollable content |
| `lb_plus/place_block` | lb_plus | Place block sidebar styling |
| `lb_plus/layout` | lb_plus | Layout outlines, nested layout UI |
| `lb_plus/editing_ui` | lb_plus | Blank page state, dialog overrides |
| `edit_plus/library` | edit_plus | Inline editing, CKEditor integration |

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Brand color customization | Set global colors at `/admin/config/content/plus-suite` | These become CSS custom properties available in all Plus Suite contexts |
| Nested layout page structure | Override `page--lb-plus-layout-block.html.twig` | The only page template Plus Suite provides |

## Color Configuration

Global colors set at `/admin/config/content/plus-suite`:

```yaml
navigation_plus.settings:
  colors:
    main: '#1a73e8'
    secondary: '#ffffff'
    highlight: '#ff6b35'
```

These CSS custom properties are available in all Plus Suite contexts.

## Theme Integration

Plus Suite uses core's Navigation module sidebar. Ensure your theme:

1. Supports the Navigation module (`navigation` core module)
2. Does not override the admin toolbar (Plus Suite replaces it)
3. Provides proper body classes for Edit Mode CSS targeting

## Hook Implementations for Theming

| Hook | Module | Purpose |
|---|---|---|
| `preprocess_field` | navigation_plus | Adds field editing attributes |
| `preprocess_navigation` | navigation_plus | Adds mode toolbars to sidebar |
| `preprocess_top_bar` | navigation_plus | Adds Edit Mode top bar |
| `element_info_alter` | navigation_plus | Alters element defaults |
| `theme_registry_alter` | navigation_plus | Ensures preprocessors run last |

## Common Mistakes

- **Do not override Plus Suite CSS with `!important`** — use CSS specificity or the color configuration.
- **Do not remove the Navigation module** — Plus Suite depends on its sidebar.

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [JavaScript Architecture](javascript-architecture.md)
- Reference: `navigation_plus/templates/`, `lb_plus/templates/`
