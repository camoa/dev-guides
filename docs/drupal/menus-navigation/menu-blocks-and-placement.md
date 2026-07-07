---
description: Rendering a menu on the page via the system_menu_block plugin and controlling its start level, depth, and expansion.
tldr: Every menu auto-exposes as a system_menu_block:{id} plugin derivative — place it in a region and control the rendered slice with level (start depth), depth (levels shown), and expand_all_items (active-trail vs always-open); the same menu can be placed multiple times with different settings.
drupal_version: "11.x"
---

# Menu Blocks & Placement

## When to Use

> Use this when you need a menu to actually appear on the page. A menu holds links but renders nothing on its own — you render it by placing a menu block in a theme region, then constraining which slice of the tree shows.

## Decision

| You want to show... | Block settings |
|---|---|
| The whole top-level menu | `level: 1`, `depth: 0` (unlimited) |
| Only the current section's children (contextual sidebar) | `level: 2+`, `depth: 1`, rely on active trail |
| A flat top bar, no sub-items | `level: 1`, `depth: 1` |
| The full tree always expanded (mega-menu source) | `expand_all_items: true` |

## Pattern

Every menu is exposed as a derivative of the `system_menu_block` block plugin — one derivative per menu (`SystemMenuBlock`, `core/modules/system/src/Plugin/Block/SystemMenuBlock.php`). Place it like any block, in config:

```yaml
# block.block.olivero_main_menu.yml (real Olivero example)
plugin: 'system_menu_block:main'   # deriver id = the menu id
region: primary_menu
settings:
  level: 1                 # tree level to start at (1 = top)
  depth: 0                 # how many levels to show (0 = unlimited)
  expand_all_items: false  # force-expand every item regardless of active trail
```

Three settings do all the shaping:

- **`level`** — where the visible tree *starts*. `level: 2` renders only the children of the active top item — the standard "section sidebar" pattern.
- **`depth`** — how many levels deep to render from `level`. `depth: 1` = one level only.
- **`expand_all_items`** — when `false` (default), only the active trail's children expand; when `true`, the whole subtree renders (needed to feed a CSS/JS mega-menu).

The same menu can be placed multiple times with different settings (a full top bar + a contextual sidebar) — they are independent block instances over one menu.

## Common Mistakes

- **Wrong**: Building a "current section" sidebar with `level: 1` and hiding items in CSS → **Right**: Set `level: 2` so Drupal renders only the active section's children
- **Wrong**: Expecting sub-items to show with `expand_all_items: false` when the user isn't on that branch → **Right**: Default expansion follows the active trail; set `expand_all_items: true` for always-open trees
- **Wrong**: Creating a custom block to render a menu → **Right**: The core `system_menu_block:{id}` derivative already exists for every menu
- **Wrong**: Placing the block but seeing nothing → **Right**: Check the menu has links and the region exists in the active theme

## See Also

- [Menu System Fundamentals](menu-system-fundamentals.md) for where the links come from
- [Menu Caching & Performance](menu-caching-and-performance.md) — a placed menu block carries the `route.menu_active_trails` cache context
- Related: [Core Block Plugins](../blocks/core-block-plugins.md) and [Block System Architecture](../blocks/block-system-architecture.md)
