---
description: Group Actions contrib module — action plugins for VBO, ECA, and token-driven group operations
tldr: "Automates group operations via VBO/ECA — but drupal/group_action 1.2.2 caps at Group ^3@beta and excludes 4.x entirely. On Group 4.0.x, write the actions yourself against the PHP API instead."
drupal_version: "11.x"
---

# Group Actions (contrib)

## When to Use

> Read this when you need to automate group operations — adding/removing members or content — via Views Bulk Operations (VBO), ECA workflows, or any Drupal action-based system.

> **This section applies to Group 3.3.x, not Group 4.x.** `drupal/group_action` 1.2.2 (2025-08-29) declares `"drupal/group": "^1 || ^2@beta || ^3@beta"`, and the HEAD of its only branch carries the identical constraint — 4.x is excluded, so `composer require` will not resolve on a Group 4.x site. Verified 2026-08-16. Until the module declares 4.x support, automating group operations on 4.0.x means either staying on Group 3.3.x or writing the actions yourself against the [PHP API](php-api.md).

## Decision

| Use case | Method | Notes |
|---|---|---|
| Bulk add/remove nodes via Views | VBO + `group_add_content` action | Select action in VBO field, configure group ID |
| Event-driven group management | ECA + Group Action action plugin | Trigger on entity save/update |
| Idempotent membership | `add_method: skip_existing` | Default — creates only if not already in group |
| Update existing relationship fields | `add_method: update_existing` | Updates fields if relationship exists |
| Dynamic group from token | `group_id: [node:field_department:entity:id]` | Tokens resolved at execution time |

Install (Group 3.3.x sites only): `composer require 'drupal/group_action:^1.2'`

## Pattern

Available action plugins:

| Action ID | Entity Type | Operation |
|---|---|---|
| `group_add_content` | `node` (per entity type via deriver) | create |
| `group_add_member` | `user` | create |
| `group_remove_content` | `node` | delete |
| `group_remove_member` | `user` | delete |
| `group_update_content` | `node` | update |
| `group_update_member` | `user` | update |

ECA configuration example:

```
Event: "After saving new content" (node)
Condition: Content type = "article"
Action: "Group: add content"
  content_plugin: group_node:article
  group_id: [node:field_target_group:entity:id]
  add_method: skip_existing
```

Token support in `group_id`, `entity_id`, `values`:

```
group_id: [node:field_department:entity:id]
entity_id: [current-user:uid]
values:
  group_roles: [node:field_assigned_role]
```

## Common Mistakes

- **Wrong**: Using `always_add` without understanding it creates duplicates → **Right**: Use `skip_existing` (default) or `update_existing`.
- **Wrong**: Setting `group_id` to a group title → **Right**: Only numeric IDs and UUIDs are supported. Use entity autocomplete in config forms or tokens.
- **Wrong**: Forgetting to install the relation type on the group type → **Right**: The action silently skips if the plugin is not installed on the target group type.
- **Wrong**: ECA recursion errors on group save → **Right**: Module handles this automatically via a `Compatibility` class. Ensure `group_action` is enabled.
- **Wrong**: Requiring `drupal/group_action` on a Group 4.x site → **Right**: The module caps at `^3@beta`; Composer refuses to resolve it against `drupal/group:^4.0`. Stay on Group 3.3.x or write the actions against the [PHP API](php-api.md) directly.

## See Also

- [PHP API](php-api.md)
- [Permissions System](permissions-system.md)
- [Plugin System](plugin-system.md)
- Reference: https://www.drupal.org/project/group_action
