---
description: Group sub-modules — gnode, group_support_revisions, and key contrib modules
tldr: "Reference this when enabling node support, revision support for grouped entities, or looking at how official sub-modules structure their plugins."
drupal_version: "11.x"
---

# Sub-modules

## When to Use

> Reference this when enabling node support, revision support for grouped entities, or looking at how official sub-modules structure their plugins.

## Decision

| Sub-module | Enable when | Key effect |
|---|---|---|
| `gnode` | You want group-scoped node access | Nodes in groups use Group's access system instead of node.module |
| `group_support_revisions` | Site uses content revisions + group-level revision access control | Group permissions control who views/reverts revisions |
| `group_content_menu` (contrib) | Groups need their own menus | **Group 3.3.x only** — newest release 3.0.8 declares `^3.0@beta`, excludes 4.x |
| `group_permissions` (contrib) | Extra permission-UI improvements | **Group 3.3.x only** — newest release 2.0.0-alpha13 declares `^2.0 \|\| ^3.0`, excludes 4.x |
| `group_flex` (contrib) | Groups need flexible visibility or join methods | **No Drupal 11 support at all** — newest release 1.0.0-beta5 (2021), core `^8.8 \|\| ^9`, never had a stable |
| `subgroup` (contrib) | You need nested group hierarchies | **Group 3.3.x only** — newest release 3.1.0 declares `^3.0`, excludes 4.x; project is *Minimally maintained* |

If your site needs any of these on Group 4.x, plan on Group **3.3.x** instead, or budget the work to add 4.x compatibility upstream.

## gnode (Group Node)

**File**: `modules/gnode/`
**Dependency**: `drupal:node`

Provides the `group_node` plugin type which makes every node type a potential relation type. Uses a deriver so that when a new node type is created, a new `group_node:{bundle}` plugin derivative becomes available.

Enables `entity_access: TRUE` so that nodes within groups are access-controlled by Group.

Default entity cardinality: 1 (a node can only be in the same group once).

Also provides:
- `gnode.group.permissions.yml` with `access group_node overview` permission
- Entity operation link to the group nodes View (if Views exists and the default view is present)
- Clears plugin definitions cache on node type creation via `gnode_node_type_insert()`

**When to enable**: Enable gnode whenever you want to scope node access to groups. Without gnode, all nodes are accessible by their standard Drupal node access regardless of group membership.

## group_support_revisions

**File**: `modules/group_support_revisions/`

Enables revision access for grouped entities (the ability to view, revert, and delete revisions of grouped entities) to be controlled by Group permissions rather than only by global Drupal permissions.

**When to enable**: When your site uses content revisions and you want group-level access to control who can view or revert revisions of grouped entities.

## Contrib Sub-modules (External)

These are separate projects, not bundled with Group. **None of them declares support for Group 4.x** — every one caps at Group 3.x or lower, so Composer will refuse to install them alongside `drupal/group:^4.0`. Verified 2026-08-16 against each project's newest tag:

| Module | drupal.org project | Purpose | Newest release | Declared `drupal/group` constraint |
|---|---|---|---|---|
| Group Content Menu | `group_content_menu` | Per-group menus | 3.0.8 (2026-01-01) | `^3.0@beta` — excludes 4.x |
| Group permissions | `group_permissions` | Extra permission UI improvements | 2.0.0-alpha13 (2026-08-14) | `^2.0 \|\| ^3.0` — excludes 4.x |
| Group Flex | `group_flex` | Flexible group visibility and join methods | 1.0.0-beta5 (2021-05-19) | Core `^8.8 \|\| ^9`; no Drupal 11 support at all, never had a stable |
| Subgroup | `subgroup` | Nested groups (parent/child group hierarchy) | 3.1.0 (2025-01-15) | `^3.0` — excludes 4.x; project is *Minimally maintained* |

If your site needs any of these, plan on Group **3.3.x** (the current stable) rather than 4.0.x, or budget the work to add 4.x compatibility upstream.

## Pattern

gnode installs one derived plugin per node type:

```
Plugin ID: group_node:article
entity_access: TRUE
default entity_cardinality: 1 (a node can only be in the same group once)
```

Install via config (after enabling `gnode`):

```yaml
# group.relationship_type.project-group_node__article.yml
relation_type: 'group_node:article'
plugin_config:
  entity_cardinality: 1
```

## Common Mistakes

- Enabling `gnode` without understanding the access implications. Once enabled, nodes added to groups are access-controlled by Group. Nodes NOT in any group still use standard node access. But if a node is in a group with a plugin that has `entity_access: TRUE`, Group may forbid access that would otherwise be allowed by node.module.
- Installing sub-modules before creating any group types. The plugin system works fine before group types exist, but it is easier to reason about the configuration flow when group types are defined first.

## See Also

- [Plugin System](plugin-system.md)
- [Access Control](access-control.md)
- Reference: `web/modules/contrib/group/modules/gnode/`
