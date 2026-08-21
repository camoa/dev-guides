---
description: "Getting menu link cache metadata right — entity: vs internal: link URIs, the route.menu_active_trails context, and the config:system.menu.{id} tag."
tldr: The single highest-leverage menu-caching fix is writing menu link URIs as entity:node/N rather than internal:/node/N, so title/alias/publish-state changes invalidate the cached menu; route.menu_active_trails varying the menu per route and user.permissions varying it per role are correct, not bugs — never patch a stale menu with max-age 0.
drupal_version: "11.x"
---

# Menu Caching & Performance

## When to Use

> Use this when a menu is rendering slowly, caching wrong (stale or per-user when it shouldn't be), or you're auditing render performance. Menus are cached by default; the failures come from how link paths and cache metadata are set.

## Decision

| Symptom | Likely cause / fix |
|---|---|
| Menu shows stale after a node's title/URL changes | Links use `internal:/node/N`, not `entity:node/N` — no cache tag bubbles |
| Menu caches per-user when it needn't | Links pointing at access-controlled routes add `user.permissions` context (often correct) |
| Menu doesn't update when links change | Missing/incorrect `config:system.menu.{id}` cache tag invalidation |
| Same menu differs per page as expected | `route.menu_active_trails` context — correct, not a bug |

## Pattern

A rendered menu block carries three kinds of cache metadata, and getting the link path right is what makes them work:

- **Cache context `route.menu_active_trails`** — the active trail differs per route, so the menu varies by it (`SystemMenuBlock::getCacheContexts()`). This is why the "current section" highlight works and is expected.
- **Cache tag `config:system.menu.{id}`** — invalidated when the menu's structure changes, so a placed menu updates when links are added/reordered.
- **Per-link metadata** — this is the one you control. A menu link written as `entity:node/42` (rather than `internal:/node/42`) carries the node's **cache tags and access** into the menu. When the node's title, alias, or publish state changes, the `entity:` link invalidates; the `internal:` link does not — producing a stale menu label or a link to a now-unpublished node.

```php
// Correct — the link inherits node:42's cache tags and access:
'link' => ['uri' => 'entity:node/42'],

// Stale-prone — a bare path with no entity metadata:
'link' => ['uri' => 'internal:/node/42'],
```

This `entity:` vs `internal:` distinction is durable, long-standing advice (not a recent change) and is the single highest-leverage menu-caching fix. Beyond it, menus rarely need manual caching work — the tree is built once and cached with the metadata above.

## Common Mistakes

- **Wrong**: Linking menu items with `internal:/node/N` for internal content → **Right**: Use `entity:node/N` so title/alias/access changes invalidate the cached menu
- **Wrong**: Adding `#cache max-age 0` to "fix" a stale menu → **Right**: Fix the link path so the correct cache tag bubbles; don't disable caching
- **Wrong**: Assuming the per-route variation is a caching bug → **Right**: `route.menu_active_trails` varying the menu per route is correct behavior
- **Wrong**: Manually invalidating menu caches after editing a link → **Right**: The `config:system.menu.{id}` tag already invalidates on structural change

## See Also

- [Menu System Fundamentals](menu-system-fundamentals.md) — where link URIs are set
- Related: [Cache Contexts](../caching/cache-contexts.md) and [Cache Tags](../caching/cache-tags.md) for the general mechanisms
- Related: [Menu Blocks & Placement](menu-blocks-and-placement.md) for the block that carries this metadata
