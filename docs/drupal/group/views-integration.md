---
description: Group Views integration — base tables, join paths, plugin_id filtering, group_id argument, and access filtering behavior
tldr: "Reference this when building Views that display groups, group members, or content within groups."
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

## Group → GroupRelationship Join

From a `group` base table, a relationship field is added named `group_relationship_id`:

```
groups_field_data
  |
  +-- "Group relationship" relationship
      (id: group_to_group_relationship)
      base: group_relationship_field_data, field: gid
      |
      +-- From here, use the per-entity-type relationship to reach content
```

## GroupRelationship → Entity Join

From the `group_relationship_field_data` table, Group adds one relationship per entity type handled by any installed plugin:

```
group_relationship_field_data
  |
  +-- "Node from group relationship" (field: gc__node)
      (id: group_relationship_to_entity)
      base: node_field_data, base_field: nid, relationship_field: entity_id
```

And from the entity side, Group adds a reverse relationship:

```
node_field_data
  |
  +-- "Group relationship for node" (field: group_relationship)
      (id: group_relationship_to_entity_reverse)
      base: group_relationship_field_data, base_field: entity_id
```

## Filtering by Plugin in Views

After joining through `group_relationship`, add a filter on the `plugin_id` field to scope to a specific relation type:

1. Add a relationship from your base table through `group_relationship_field_data`
2. Add a filter on `group_relationship_field_data` → `Plugin ID` = `group_node:article`

## Group ID Argument

Both `groups_field_data.id` and `group_relationship_field_data.gid` have a custom argument handler (`group_id`) that provides group label replacement tokens for view titles.

## Access in Views

Group hooks into `hook_views_query_alter()` to add LEFT JOINs and conditions for access filtering. This only applies to Views that:

- Use an entity base table
- Do NOT have `disable_sql_rewrite = TRUE`
- Have the base entity as the primary entity (not through a relationship)

**Important**: Views based on `group_relationship_field_data` directly are NOT automatically access-filtered by Group — they show all relationships regardless of the current user's permissions. Add explicit access filters or use `_group_permission` on the route.

## Common Mistakes

- Expecting Group to access-filter a relationship-based View. Only entity-based Views get automatic access filtering. A View on `group_relationship_field_data` shows all records.
- Not filtering by `plugin_id` when joining from group to content. Without this filter, a single node could appear multiple times if it is in multiple groups.
- Using Views contextual filters on group ID without the `group_id` argument plugin. The default numeric argument does not provide token replacements for group labels in the view title.

## See Also

- [Access Control](access-control.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/src/Plugin/views/`
