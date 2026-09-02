---
description: "Plus Suite sidebar system — left/right/settings sidebar types, cookie-based visibility, JS architecture, and building custom sidebar content"
tldr: "Customize sidebar content for your tools or modes. Sidebar visibility is cookie-based, and sidebars rebuild on every tool switch."
drupal_version: "11.x"
---

# Sidebar System

## When to Use

> When customizing sidebar content for your tools or modes, or understanding the sidebar visibility system.

## Sidebar Types

| Type | Position | Built By | Example |
|---|---|---|---|
| Left sidebar | Left of content | `buildLeftSideBar()` | PlaceBlock block list, Section Library templates |
| Right sidebar | Right of content | `buildRightSideBar()` | Tool-specific options |
| Settings sidebar | Right of content | `buildSettings()` | Hotkeys, media associations |

## Visibility Control

Sidebar visibility is **cookie-based**:

| Cookie | Values | Purpose |
|---|---|---|
| `{tool_id}_sidebar` | `open` / `closed` | Left sidebar toggle |
| `{sidebar_id}_sidebar` | `open` / `closed` | Right sidebar toggle |

## JavaScript Architecture

```
sidebar-manager.js → Manages all sidebar instances
  ├── sidebar-plugin-base.js → Base class for sidebar plugins
  ├── default-sidebar.js → Standard sidebar behavior
  └── notifications-sidebar.js → Notifications panel
```

Sidebar buttons use `data-right-sidebar-button-for` attribute to correlate with sidebar panels.

## Building Custom Sidebar Content

In your tool plugin:

```php
public function buildLeftSideBar(): array {
  return [
    '#theme' => 'my_tool_sidebar',
    '#items' => $this->getItems(),
    '#attached' => [
      'library' => ['my_module/sidebar_styles'],
    ],
  ];
}
```

## Common Mistakes

- **Do not** render heavy content in sidebars — they're rebuilt on every tool switch.
- **Do not** mix left and right sidebar content in a single tool unless the workflow requires it.

## See Also

- [Tool Plugins](tool-plugins.md)
- [Hotkeys & User Settings](hotkeys-user-settings.md)
- [JavaScript Architecture](javascript-architecture.md)
