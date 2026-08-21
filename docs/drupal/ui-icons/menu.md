---
description: "Attach an icon to each menu link; icons render automatically into link titles, no template override needed."
tldr: "Enable ui_icons_menu to add an icon widget to the menu_link_content form. Three hooks inject the icon markup into link titles automatically — no preprocess or template override is needed, and there is no data-icon-id attribute to read."
drupal_version: "11.x"
---

# Menu Integration

## When to Use

> Adding an icon to each menu item (used by navigation, sidebar menus, mega-menu themes).

## Pattern

Enable `ui_icons_menu`. The module alters the `menu_link_content` entity to add an icon widget on the standard menu link form (`/admin/structure/menu/manage/{menu}/add`).

Editors pick an icon (and settings) per menu link, plus an `icon_position` (before or after the title). The icon data is stored as link options — `icon` and `icon_display` — not as `data-*` attributes.

## Rendering

**Icons render automatically. No template override or preprocess is needed.** `UiIconsMenuHooks` injects the icon markup into the link title, positioned by `icon_display`, through three hooks:

| Hook | Covers |
|---|---|
| `hook_preprocess_menu` | Ordinary rendered menus (skips `navigation_menu__*` hooks, which the next one handles) |
| `hook_navigation_menu_link_tree_alter` | Core's Navigation module, on its own path |
| `hook_link_alter` | Loose links, so icons also appear in the admin listing at `/admin/structure/menu/manage/{menu}` |

Write a preprocess only if you want markup the module doesn't produce — and read the icon from `$url->getOption('icon')` / `$url->getOption('icon_display')`, since there is no `data-icon-id` attribute anywhere in this path.

Core's Navigation module is handled by `hook_navigation_menu_link_tree_alter`, not by the menu preprocess — icons appear there without extra work. Define a `class` setting in your icon pack if navigation styles need a hook to target — see [Settings & Rendering](settings-rendering.md).

## Common Mistakes

- **Wrong**: writing a preprocess that reads `$options['attributes']['data-icon-id']` → **Right**: that attribute does not exist; the preprocess silently does nothing. Read the `icon` link option instead
- **Wrong**: overriding `menu.html.twig` to add icons → **Right**: icons are already in the link title; an override duplicates or fights the injected markup

## See Also

- [Settings & Rendering](settings-rendering.md)
- [UI Icons Overview](overview.md)
- Reference: `modules/ui_icons_menu/src/Hook/UiIconsMenuHooks.php`
