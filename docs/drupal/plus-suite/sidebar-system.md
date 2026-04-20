---
description: Plus Suite sidebar system — left/right/settings sidebar types, cookie-based visibility, JS architecture, and building custom sidebar content
tldr: "Build custom sidebar content in tool plugins. Avoid heavy content in sidebars — they rebuild on every tool switch."
drupal_version: "11.x"
---

# Sidebar System

## When to Use

> Build custom sidebar content in tool plugins. Avoid heavy content in sidebars — they rebuild on every tool switch.

## Decision

| Type | Position | Built By | Example |
|------|----------|----------|---------|
| Left sidebar | Left of content | `buildLeftSideBar()` | PlaceBlock block list, Section Library templates |
| Right sidebar | Right of content | `buildRightSideBar()` | Tool-specific options |
| Settings sidebar | Right of content | `buildSettings()` | Hotkeys, media associations |

## Pattern

**Visibility control** (cookie-based):

| Cookie | Values | Purpose |
|--------|--------|---------|
| `{tool_id}_sidebar` | `open` / `closed` | Left sidebar toggle |
| `{sidebar_id}_sidebar` | `open` / `closed` | Right sidebar toggle |

**Building custom sidebar content in a tool plugin:**

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

**JavaScript architecture:**
```
sidebar-manager.js → Manages all sidebar instances
  ├── sidebar-plugin-base.js → Base class for sidebar plugins
  ├── default-sidebar.js → Standard sidebar behavior
  └── notifications-sidebar.js → Notifications panel
```

Sidebar buttons use `data-right-sidebar-button-for` attribute to correlate with sidebar panels.

## Common Mistakes

- **Wrong**: Rendering heavy DB queries or API calls in sidebar content → **Right**: Sidebars rebuild on every tool switch; cache or lazy-load expensive content
- **Wrong**: Mixing left and right sidebar content in a single tool unless the workflow requires both → **Right**: Use left for browsing lists, right for selected-item options

## See Also

- [Tool Plugins](tool-plugins.md)
- [Hotkeys & User Settings](hotkeys-user-settings.md)
- [JavaScript Architecture](javascript-architecture.md)
