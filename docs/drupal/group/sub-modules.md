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
| `group_content_menu` (contrib) | Groups need their own menus | Per-group menus |
| `gflex` (contrib) | Groups need flexible visibility or join methods | Open, private, or invite-only groups |
| `subgroup` (contrib) | You need nested group hierarchies | Parent/child group relationships |

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
content_plugin: 'group_node:article'
plugin_config:
  entity_cardinality: 1
```

## Common Mistakes

- **Wrong**: Enabling `gnode` without understanding the access implications → **Right**: Once enabled, nodes added to groups are access-controlled by Group. Nodes NOT in any group still use standard node access. Incomplete permission configuration can lock users out.
- **Wrong**: Installing sub-modules before creating any group types → **Right**: Define group types first, then install plugins. This avoids confusing plugin-not-installed errors.

## See Also

- [Plugin System](plugin-system.md)
- [Access Control](access-control.md)
- Reference: `web/modules/contrib/group/modules/gnode/`
