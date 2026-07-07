---
description: How Drupal's rendered menu tree is assembled from three different sources — config menu container, content menu links, and static module-shipped links.
tldr: A Drupal menu tree merges three sources — the system.menu.{id} config container, editor-created menu_link_content entities, and module-shipped *.links.menu.yml — and only the container and static links deploy via config export; editor links need content staging instead.
drupal_version: "11.x"
---

# Menu System Fundamentals

## When to Use

> Use this when you are working with any Drupal menu and need to know where a given link actually lives — because Drupal builds one rendered menu tree from three different sources, and which one a link comes from determines how you edit, deploy, translate, or delete it.

## Decision

| The link is... | It lives in... | Edit / deploy it via... |
|---|---|---|
| The menu container itself (Main navigation, Footer) | A **config entity** `system.menu.{id}` | Config YAML — exported, deployed with the site |
| A link an editor added in the UI | A **content entity** `menu_link_content` | Content — created in `/admin/structure/menu`, lives in the database, not config |
| A link a module ships (e.g. an admin route) | A **static** definition in `{module}.links.menu.yml` | Code — see [Programmatic Menu Links](menu-programmatic-links-and-alter-hooks.md) |

## Pattern

A **menu** is a lightweight config entity — it defines the container, not the links:

```yaml
# system.menu.main.yml — the Main navigation menu
id: main
label: 'Main navigation'
description: 'Site section links'
locked: true          # core menus are locked (cannot be deleted in the UI)
```

The `id` is constrained to `^[a-z0-9-]+$`, max 32 chars (schema: `core/modules/system/config/schema/system.schema.yml`). Core ships `main`, `footer`, `tools`, `account`, and `admin`.

A **menu link** an editor creates is a `menu_link_content` **content entity**, not config. It extends `EditorialContentEntityBase`, so it is **revisionable and publishable** (`core/modules/menu_link_content/src/Entity/MenuLinkContent.php`), stored in the `menu_link_content` table, keyed to a menu by its `menu_name` field, and ordered by `weight` with parent/child via `parent`:

```php
$link = \Drupal::entityTypeManager()->getStorage('menu_link_content')->create([
  'title' => 'About us',
  'link' => ['uri' => 'entity:node/42'],   // prefer entity: over internal: — see caching guide
  'menu_name' => 'main',
  'weight' => 0,
  'expanded' => TRUE,
]);
$link->save();
```

Because editor-created links are **content**, they do **not** move with a `drush config:export`. Deploying them means content staging (e.g. Default Content, a migration), not config sync — a frequent surprise.

The rendered tree is assembled by the `menu.link_tree` service (`MenuLinkTree`) from all three sources, then transformed (access-checked, sorted) before rendering. Reference: `core/lib/Drupal/Core/Menu/MenuLinkTree.php`, `core/lib/Drupal/Core/Menu/menu.api.php`.

## Common Mistakes

- **Wrong**: Expecting editor-created menu links to deploy with config export → **Right**: `menu_link_content` is a content entity; it needs content staging, not `config:export`
- **Wrong**: Trying to delete a locked core menu (`main`, `footer`) in the UI → **Right**: `locked: true` menus can hold zero links but cannot be removed; leave them
- **Wrong**: Confusing the menu (`system.menu.*` config) with its links (`menu_link_content` content) → **Right**: The container is config; the links inside are usually content
- **Wrong**: Hand-editing `menu_link_content` link URIs as `internal:/node/42` → **Right**: Use `entity:node/42` so the link carries the node's cache metadata and access — see [Menu Caching & Performance](menu-caching-and-performance.md)

## See Also

- Next: [Menu Blocks & Placement](menu-blocks-and-placement.md) to render a menu
- [Programmatic Menu Links & Alter Hooks](menu-programmatic-links-and-alter-hooks.md) for code-defined links
- Reference: [Menu API](https://www.drupal.org/docs/drupal-apis/menu-api)
