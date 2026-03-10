---
description: Group Views integration — base tables, join paths, plugin_id filtering, group_id argument, and access filtering behavior
drupal_version: "11.x"
---

# Views Integration

## When to Use

> Reference this when building Views that display groups, group members, or content within groups.

## Decision

| Base table | Entity type | Use for |
|---|---|---|
| `groups_field_data` | `group` | Lists of groups |
| `group_relationship_field_data` | `group_relationship` | Lists of relationships (members, content) |

| Scenario | Access-filtered by Group? | Action needed |
|---|---|---|
| View on `node_field_data` | Yes | Automatic via `hook_views_query_alter()` |
| View on `group_relationship_field_data` | **No** | Add explicit `_group_permission` on route or manual filter |
| View with `disable_sql_rewrite` | No | Group's LEFT JOINs are removed |

## Pattern

Join path from group to content:

```
groups_field_data
  → "Group relationship" relationship (id: group_to_group_relationship)
    base: group_relationship_field_data, field: gid
    → "Node from group relationship" (field: gc__node)
      base: node_field_data, base_field: nid, field: entity_id
```

Filtering by plugin in Views:
1. Add relationship from base table through `group_relationship_field_data`
2. Add filter: `group_relationship_field_data` → `Plugin ID` = `group_node:article`

For the `group_id` contextual filter, use the `group_id` argument handler — it provides group label replacement tokens for view titles.

## Common Mistakes

- **Wrong**: Expecting Group to access-filter a relationship-based View → **Right**: Only entity-based Views get automatic access filtering. Views on `group_relationship_field_data` directly show all records.
- **Wrong**: Not filtering by `plugin_id` when joining from group to content → **Right**: Without this filter, a node in multiple groups could appear multiple times.
- **Wrong**: Using the default numeric contextual filter on group ID → **Right**: Use the `group_id` argument plugin to get token replacements for group labels in the view title.

## See Also

- [Access Control](access-control.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/src/Plugin/views/`
