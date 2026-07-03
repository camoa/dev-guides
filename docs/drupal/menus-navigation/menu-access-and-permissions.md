---
description: The two layers of menu access — the coarse administer menu permission for editing, and automatic per-link route access filtering for visibility.
tldr: Menu access has two distinct layers — administer menu (all-or-nothing edit access, needs menu_admin_per_menu contrib for per-menu scoping) and automatic per-link route access filtering during tree build; external/pathless links are never access-filtered, so don't rely on menu absence to secure them.
drupal_version: "11.x"
---

# Menu Access & Permissions

## When to Use

> Use this when you need to control who can administer menus, and to ensure links a visitor cannot reach don't render for them. Menu access has two distinct layers — administrative (who edits the menu) and per-link (whether a given link shows) — and conflating them is a common security/UX bug.

## Decision

| Concern | Mechanism |
|---|---|
| Who can add/edit/reorder menu links | The `administer menu` permission (single, coarse) |
| Whether a link to a route renders for this user | Automatic — the tree runs each link's **route access check** |
| Whether a link to an external URL renders | Always renders (no route to access-check) |
| Restrict editing to one menu only | Not in core — needs the contrib `menu_admin_per_menu` module |

## Pattern

**Administrative access** is governed by one permission, `administer menu`, which is also the `admin_permission` on the `menu_link_content` entity type and its access control handler (`core/modules/menu_link_content/src/MenuLinkContentAccessControlHandler.php`). Core does not split menu editing per-menu — any user with `administer menu` can edit every menu. Per-menu delegation requires the `menu_admin_per_menu` contrib module.

**Per-link visibility** is automatic and is the important part: when the menu tree is built, each link that points to an internal **route** is access-checked against the current user, and links the user cannot access are removed from the rendered tree. This is why a menu link to `/admin/content` simply doesn't appear for an anonymous visitor — you do not hide it manually.

Two consequences to design around:
- A link to an **external URL** or a plain path with no route is **not** access-filtered — it always renders. Don't rely on a menu link to "hide" a restricted external resource.
- Access filtering adds the relevant **cache contexts** (typically `user.permissions`) to the rendered menu, so the same menu block caches differently per permission set — correct, but see [Menu Caching & Performance](menu-caching-and-performance.md).

## Common Mistakes

- **Wrong**: Manually hiding admin links in the theme for anonymous users → **Right**: Route access already removes unreachable links from the tree; don't duplicate it
- **Wrong**: Assuming `administer menu` can be scoped to a single menu in core → **Right**: It's all-or-nothing; use `menu_admin_per_menu` for per-menu delegation
- **Wrong**: Trusting a menu link's absence to secure an external URL → **Right**: External/pathless links aren't access-filtered; secure the resource itself
- **Wrong**: Granting `administer menu` to content editors so they can reorder one menu → **Right**: That grants edit on *all* menus; scope it with contrib or a dedicated role

## See Also

- [Menu System Fundamentals](menu-system-fundamentals.md) for the link entity being access-controlled
- Related: [Route Access Checks](../routing/index.md) — the per-link check the tree runs
- Related: [Menu Caching & Performance](menu-caching-and-performance.md) for the cache contexts access adds
