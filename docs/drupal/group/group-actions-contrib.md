---
description: Group Actions contrib module — action plugins for VBO, ECA, and token-driven group operations
tldr: "Automates group operations via VBO/ECA — but drupal/group_action 1.2.2 caps at Group ^3@beta and excludes 4.x entirely. On Group 4.0.x, write the actions yourself against the PHP API instead."
drupal_version: "11.x"
---

# Group Actions (contrib)

## When to Use

> Read this when you need to automate group operations — adding/removing members or content — via Views Bulk Operations (VBO), ECA workflows, or any Drupal action-based system.

> **This section applies to Group 3.3.x, not Group 4.x.** `drupal/group_action` 1.2.2 (2025-08-29) declares `"drupal/group": "^1 || ^2@beta || ^3@beta"`, and the HEAD of its only branch carries the identical constraint — 4.x is excluded, so the install command below will not resolve on a Group 4.x site. Verified 2026-08-16. Until the module declares 4.x support, automating group operations on 4.0.x means either staying on Group 3.3.x or writing the actions yourself against the [PHP API](php-api.md).

## Decision

| Use case | Method | Notes |
|---|---|---|
| Bulk add/remove nodes via Views | VBO + `group_add_content` action | Select action in VBO field, configure group ID |
| Event-driven group management | ECA + Group Action action plugin | Trigger on entity save/update |
| Idempotent membership | `add_method: skip_existing` | Default — creates only if not already in group |
| Update existing relationship fields | `add_method: update_existing` | Updates fields if relationship exists |
| Dynamic group from token | `group_id: [node:field_department:entity:id]` | Tokens resolved at execution time |

Install (Group 3.3.x sites only): `composer require 'drupal/group_action:^1.2'`

## Overview

The **Group Actions** module (`drupal/group_action`, newest release 1.2.2) provides configurable Drupal action plugins for Group operations. It bridges Group's API with Drupal's action system, enabling bulk and event-driven group management without custom code.

**Install (Group 3.3.x sites):** `composer require 'drupal/group_action:^1.2'`

## Pattern

Available action plugins:

| Action ID | Label | Entity Type | Operation | Derived |
|---|---|---|---|---|
| `group_add_content` | Group: add content | `node` | create | Yes (per entity type) |
| `group_add_member` | Group: add user as member | `user` | create | No |
| `group_remove_content` | Group: remove content | `node` | delete | Yes (per entity type) |
| `group_remove_member` | Group: remove user as member | `user` | delete | No |
| `group_update_content` | Group: update content | `node` | update | Yes (per entity type) |
| `group_update_member` | Group: update user membership | `user` | update | No |

Content actions use a **deriver** (`GroupActionDeriver`) that creates per-entity-type derivatives automatically. Member actions target `user` entities with a hardcoded `group_membership` plugin.

## Configuration Options

Every action accepts these configuration keys:

| Key | Description | Supports Tokens |
|---|---|---|
| `operation` | `create`, `update`, or `delete` | No |
| `relation_type` | Group relation type plugin ID (e.g., `group_node:article`). Named `content_plugin` at `4.0.0-alpha1`; renamed in `alpha2`. | No |
| `group_id` | Group ID (numeric) or UUID | Yes |
| `entity_id` | Entity ID or UUID; blank = use the entity the action runs on | Yes |
| `values` | Key-value field values for the group relationship (e.g., `group_roles: mygroup-myrole`) | Yes |
| `add_method` | `skip_existing` (default), `always_add`, or `update_existing` | No |

## Add Method Behavior

| Method | Behavior |
|---|---|
| `skip_existing` | Only creates the relationship if the entity is not already in the group |
| `always_add` | Creates the relationship regardless (allows duplicates) |
| `update_existing` | If relationship exists, updates its field values; otherwise creates |

## Usage with VBO

Create a View of nodes or users, add a VBO field, and select a Group Action:

1. Add a "Views Bulk Operations" field to your View
2. Select "Group: add content" (or the entity-type-specific derivative)
3. Configure: select the group relation type, enter the target group ID
4. Optionally set field values (e.g., `group_roles: mygroup-editor`)
5. Users execute the bulk action from the View

## Usage with ECA

ECA provides event-driven automation. Group Actions integrate as ECA action plugins:

```
Event: "After saving new content" (node)
Condition: Content type = "article"
Action: "Group: add content"
  - relation_type: group_node:article
  - group_id: [node:field_target_group:entity:id]
  - add_method: skip_existing
```

**ECA compatibility note:** The module includes a `Compatibility` class that temporarily raises ECA's recursion threshold by 1 during group operations. On **Group 3.x** this is necessary because Group re-saves the content entity to update access policies, which ECA would otherwise interpret as recursion and halt. The premise does not hold on Group 4.x — adding an entity to a group no longer re-saves the entity, it only invalidates cache tags (see [PHP API](php-api.md)) — but since `group_action` does not declare Group 4.x support, there is no released combination in which that matters.

## Token Support

Group and entity IDs support Drupal tokens, enabling dynamic resolution:

```
group_id: [node:field_department:entity:id]
entity_id: [current-user:uid]
values:
  group_roles: [node:field_assigned_role]
```

Token data automatically includes the entity being acted on plus the resolved group.

## Access Control

Actions check Group-level permissions before executing:

1. Checks `PermissionProvider::getPermission($operation, 'relationship', 'any')`
2. Falls back to `getPermission($operation, 'relationship', 'own')`
3. Falls back to `getAdminPermission()`
4. Admin users (uid 1 or admin role) bypass all checks

## Dynamic Plugin Resolution

When the content plugin ID has no bundle suffix (e.g., `group_node` instead of `group_node:article`), the action automatically appends the entity's bundle if the entity type supports bundles:

```php
// Automatic resolution:
// relation_type = "group_node" + entity bundle = "article"
// → resolved to "group_node:article"
```

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Using `always_add` without understanding | Creates duplicate relationships | Use `skip_existing` (default) or `update_existing` |
| Setting `group_id` to a group title | Only numeric IDs and UUIDs are supported | Use the entity autocomplete in config forms, or tokens |
| Forgetting to install the relation type on the group type | Action silently skips if plugin not installed | Install the group relation type (e.g., `group_node:article`) on the target group type first |
| Not handling dynamic bundles | Wrong or missing content plugin match | Let automatic resolution handle it, or explicitly set `group_node:article` |
| ECA recursion errors on group save (Group 3.x) | Group 3.x re-saves the entity for the access cache, triggering ECA recursion | Module handles this automatically via `Compatibility` class — ensure `group_action` is enabled |

Requiring `drupal/group_action` on a Group 4.x site does not work: the module caps at `^3@beta`; Composer refuses to resolve it against `drupal/group:^4.0`. Stay on Group 3.3.x, or write the actions against the [PHP API](php-api.md) directly.

## See Also

- [PHP API](php-api.md) — programmatic alternatives without the action system
- [Permissions System](permissions-system.md) — understanding what permissions the actions check
- [Plugin System](plugin-system.md) — how group relation type plugins work
- Reference: https://www.drupal.org/project/group_action
