---
description: Drupal visitor-facing menu system — three-source menu trees, menu blocks, access control, programmatic links, and menu caching
guide-meta:
  concepts:
    - system.menu.*
    - menu_ui
    - menu_link_content
    - system_menu_block
    - active trail
    - administer menu permission
    - links.menu.yml
    - hook_menu_links_discovered_alter
    - route.menu_active_trails
    - config:system.menu cache tag
  not:
    - Navigation module admin sidebar (core/modules/navigation, system.menu.content, system.menu.navigation-user-links)
    - Toolbar module
  requires: []
  complements:
    - drupal/blocks
    - drupal/taxonomy
    - drupal/breadcrumbs
  specializes: ""
  category: drupal
---

# Drupal Menus & Navigation

> Reference for building visitor-facing navigation in Drupal — the menu system's three layers, placing menus as blocks, access control, programmatic and altered links, and menu caching. Verified against Drupal core 11.3.

## Scope note: this is content/site navigation, not the admin Navigation module

This topic covers the **visitor-facing menu system** (`menu_ui`, `menu_link_content`, `system.menu.*`) — main menu, footer menu, custom menus rendered as blocks in your theme.

It does **not** cover Drupal 11's core **Navigation module** (`core/modules/navigation`). That module is the modern collapsible **admin sidebar** that replaces Toolbar; it is backend UX built on Layout Builder, it creates its own dedicated admin menus (`system.menu.content`, `system.menu.navigation-user-links`), and it shares no configuration with the site-facing menus below. It is also not enabled by core's Standard profile (that still ships `toolbar`) — it arrives via the Drupal CMS `drupal_cms_admin_ui` recipe. If you are looking for the admin sidebar, see the [Navigation module documentation](https://www.drupal.org/docs/develop/core-modules-and-themes/core-modules/navigation-module) rather than this topic.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand how menus, menu links, and static links fit together | [Menu System Fundamentals](menu-system-fundamentals.md) | A Drupal menu tree merges three sources — the system.menu.{id} config container, editor-created menu_link_content entities, and module-shipped *.links.menu.yml — and only the container and static links deploy via config export; editor links need content staging instead. |
| Render a menu on the page and control its levels/depth | [Menu Blocks & Placement](menu-blocks-and-placement.md) | Every menu auto-exposes as a system_menu_block:{id} plugin derivative — place it in a region and control the rendered slice with level (start depth), depth (levels shown), and expand_all_items (active-trail vs always-open); the same menu can be placed multiple times with different settings. |
| Control who can edit menus and hide links a user can't reach | [Menu Access & Permissions](menu-access-and-permissions.md) | Menu access has two distinct layers — administer menu (all-or-nothing edit access, needs menu_admin_per_menu contrib for per-menu scoping) and automatic per-link route access filtering during tree build; external/pathless links are never access-filtered, so don't rely on menu absence to secure them. |
| Define menu links in code and alter existing ones | [Programmatic Menu Links & Alter Hooks](menu-programmatic-links-and-alter-hooks.md) | Ship structural links as *.links.menu.yml (cached plugin definitions, requires cache rebuild after changes) and reserve menu_link_content entities for editor-managed links; alter your own or another module's links at discovery time with hook_menu_links_discovered_alter(), never by editing the defining module. |
| Keep menus fast and cache them correctly | [Menu Caching & Performance](menu-caching-and-performance.md) | The single highest-leverage menu-caching fix is writing menu link URIs as entity:node/N rather than internal:/node/N, so title/alias/publish-state changes invalidate the cached menu; route.menu_active_trails varying the menu per route and user.permissions varying it per role are correct, not bugs — never patch a stale menu with max-age 0. |
