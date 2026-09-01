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

## Common Mistakes

- **Wrong**: Enabling `gnode` without understanding the access implications → **Right**: Once enabled, nodes added to groups are access-controlled by Group. Nodes NOT in any group still use standard node access. Incomplete permission configuration can lock users out.
- **Wrong**: Installing sub-modules before creating any group types → **Right**: Define group types first, then install plugins. This avoids confusing plugin-not-installed errors.
- **Wrong**: Assuming `group_content_menu`, `group_permissions`, `group_flex`, or `subgroup` install alongside `drupal/group:^4.0` → **Right**: none of them declares Group 4.x support (verified 2026-08-16); Composer will refuse to resolve. Stay on Group 3.3.x if you need one of these.

## See Also

- [Plugin System](plugin-system.md)
- [Access Control](access-control.md)
- Reference: `web/modules/contrib/group/modules/gnode/`
