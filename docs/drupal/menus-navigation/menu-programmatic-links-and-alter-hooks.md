---
description: Shipping menu links declaratively in *.links.menu.yml and altering discovered links via hook_menu_links_discovered_alter().
tldr: Ship structural links as *.links.menu.yml (cached plugin definitions, requires cache rebuild after changes) and reserve menu_link_content entities for editor-managed links; alter your own or another module's links at discovery time with hook_menu_links_discovered_alter(), never by editing the defining module.
drupal_version: "11.x"
---

# Programmatic Menu Links & Alter Hooks

## When to Use

> Use this when a module needs to ship a menu link (so it deploys as code, not content), or needs to modify links other modules or the site define — adding, removing, or re-pointing them at build time.

## Decision

| You need to... | Use |
|---|---|
| Ship a static link with your module | A `{module}.links.menu.yml` entry |
| Add/remove/change links programmatically at discovery | `hook_menu_links_discovered_alter()` |
| Change local task tabs (e.g. node Edit/View) | `hook_menu_local_tasks_alter()` |
| Let an editor manage the link instead | A `menu_link_content` entity (content, not code) |

## Pattern

A module ships a static menu link declaratively:

```yaml
# my_module.links.menu.yml
my_module.reports:
  title: 'Reports'
  description: 'Site reports'
  route_name: my_module.reports
  menu_name: admin
  parent: system.admin
  weight: 10
```

These are **plugin definitions**, discovered and cached — after adding or changing one you must rebuild caches. To alter links (yours or another module's) at discovery time, implement the alter hook:

```php
function my_module_menu_links_discovered_alter(&$links) {
  // Re-point or remove a link another module defined.
  if (isset($links['standard.link_id'])) {
    $links['standard.link_id']['weight'] = 50;
  }
  // Add a link in code.
  $links['my_module.dynamic'] = [
    'title' => 'Dynamic',
    'route_name' => 'my_module.dynamic',
    'menu_name' => 'main',
  ];
}
```

Local task tabs (the View/Edit/Delete tabs on an entity) are a separate plugin type driven by `{module}.links.task.yml` and altered via `hook_menu_local_tasks_alter()`. Reference: `core/lib/Drupal/Core/Menu/menu.api.php`.

Choose **code** for links that are structurally part of the site (admin sections, module features) and **content** (`menu_link_content`) for links editors will manage — code links deploy and can't be deleted in the UI; content links are editable but need content staging.

## Common Mistakes

- **Wrong**: Editing a `*.links.menu.yml` and not seeing the change → **Right**: Menu links are cached plugin definitions; rebuild caches after changing them
- **Wrong**: Using `hook_menu()` (Drupal 7) to define links → **Right**: `hook_menu()` is gone; use `*.links.menu.yml` + route definitions
- **Wrong**: Shipping an editor-managed link as a static YAML link → **Right**: If editors must reorder/rename it, make it a `menu_link_content` entity instead
- **Wrong**: Altering another module's link by editing that module → **Right**: Use `hook_menu_links_discovered_alter()` so the change survives updates

## See Also

- [Menu System Fundamentals](menu-system-fundamentals.md) for content-vs-code link choice
- [Menu Caching & Performance](menu-caching-and-performance.md) — why a cache rebuild is needed after changing static links
- Reference: [Providing module-defined menu links](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-menu-links)
