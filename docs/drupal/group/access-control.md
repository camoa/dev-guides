---
description: Group access control — explicit forbid philosophy, access check flow, query access, GroupAccessResult, custom handlers, and revision access
tldr: "Read this when diagnosing access issues, understanding the \"explicit forbid\" pattern, or writing custom access control for group-related entities. In 4.x the entity_access hook is implemented as EntityHooks::entityAccess() (OOP), not group_entity_access() (procedural)."
drupal_version: "11.x"
---

# Access Control

## When to Use

> Read this when diagnosing access issues, understanding the "explicit forbid" pattern, or writing custom access control for group-related entities.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Entity in a group, `entity_access: TRUE` | Group owns access | Either allows or forbids — never neutral |
| Entity NOT in any group | Neutral result | Other modules handle access normally |
| Entity in group, `entity_access: FALSE` (default) | Neutral result | Group defers to other modules |
| Unsaved entity | Always neutral | No ID means no relationships can exist |
| Custom access logic | Override `access_control` handler | Decorator pattern, preserves defaults |

## The "Explicit Forbid" Philosophy

Group's fundamental access philosophy: if an entity is grouped and a plugin with `entity_access: TRUE` handles it, Group will either explicitly **allow** or explicitly **forbid** access — it never returns `neutral` for grouped entities.

This means: if a node is in a group via a plugin with `entity_access: TRUE`, standard Drupal node access grants (like `node_access()` from the `node` module or other contrib) are overridden. Group takes ownership of access for that entity.

If the plugin has `entity_access: FALSE` (default), Group returns `neutral` for entity access, deferring to other modules.

## Access Check Flow

```
hook_entity_access($entity, $operation, $account)
    |
    +-- EntityHooks::entityAccess()
            |
            +-- Find all plugin IDs with entity_access for this entity type
            +-- Load all group_relationship records for this entity
            +-- For each plugin in use:
                    AccessControl handler->entityAccess()
                    |
                    +-- Load group_relationships for entity+plugin
                    +-- For each group relationship:
                            GroupAccessResult::allowedIfHasGroupPermissions()
                            (checks outsider/insider/individual scopes)
                    |
                    +-- If no group allows it: return Forbidden
```

The flow above is the 4.x implementation: an OOP hook — `EntityHooks::entityAccess()`, tagged with the `#[Hook('entity_access')]` attribute — rather than the procedural `group_entity_access()` function of 3.x. The behavior is identical. Every group-permission check inside the flow resolves through the Access Policy API (see [Permissions System](permissions-system.md)); the "explicit forbid" semantics and `GroupAccessResult` are unchanged from 3.x.

> **3.x:** In Group 3.x the same logic lives in the procedural function `group_entity_access()` in `group.module`. The `.module` file was deleted in 4.x when hooks were converted to OOP hook classes.

## Query Access (Entity Queries & Views)

Group automatically alters entity queries using three alter classes:

| Entity Type | Alter Class |
|---|---|
| `group` | `GroupQueryAlter` |
| `group_relationship` | `GroupRelationshipQueryAlter` |
| Any other entity type | `EntityQueryAlter` |

These classes LEFT JOIN the `group_relationship_field_data` table and add conditions based on the user's calculated permissions. The joins are only added when plugins with `entity_access: TRUE` are actually in use (checked via a fast `plugin_id IN (...)` query before proceeding).

Group uses `hook_module_implements_alter()` to ensure its query alters run last, after all other modules.

## `GroupAccessResult`

Group provides `GroupAccessResult` as a cache-aware wrapper around `AccessResult`:

```php
use Drupal\group\Access\GroupAccessResult;

// Allow if the user has a single permission.
$result = GroupAccessResult::allowedIfHasGroupPermission($group, $account, 'edit group');

// Allow if the user has any of multiple permissions (OR).
$result = GroupAccessResult::allowedIfHasGroupPermissions(
  $group, $account, ['edit group', 'administer group'], 'OR'
);

// These automatically add the group entity and user.group_permissions
// cache context to the result.
```

## Access Control Handler for Custom Entities

If you write a plugin with `entity_access: TRUE` and need to customize access logic, override the `access_control` handler:

```php
// mymodule.services.yml
group.relation_handler.access_control.my_plugin:
  class: 'Drupal\mymodule\Plugin\Group\RelationHandler\MyAccessControl'
  arguments: ['@group.relation_handler.access_control']  # decorated default
  shared: false
```

```php
// MyAccessControl.php
class MyAccessControl implements AccessControlInterface {
  use AccessControlTrait;

  public function __construct(AccessControlInterface $decorated) {
    $this->decorated = $decorated;
  }

  public function entityAccess(EntityInterface $entity, $operation, AccountInterface $account, $return_as_object = FALSE) {
    // Custom logic, then fall back to decorated:
    return $this->decorated->entityAccess($entity, $operation, $account, $return_as_object);
  }
}
```

## Access for Revision Operations

`GroupAccessControlHandler` maps revision operations to group permissions:

| Revision operation | Required permission | Also requires |
|---|---|---|
| `view all revisions` | `view all group revisions` | `view` |
| `view revision` | `view group revisions` | `view` |
| `revert revision` | `revert group revisions` | `update` |
| `delete revision` | `delete group revisions` | `delete` |

## Common Mistakes

- Assuming that ungrouped entities are affected by Group access. Group only checks access for entities that have at least one `group_relationship` record. An ungrouped entity returns `neutral` from `EntityHooks::entityAccess()`.
- Checking access on new (unsaved) entities via `$entity->access()` from group-aware code. Group explicitly returns `neutral` for new entities since they have no ID and cannot have relationships.
- Forgetting that Views query access is also handled. Group hooks into `hook_views_query_alter()` to add access-aware LEFT JOINs. If you are building Views that bypass access (`disable_sql_rewrite`), you lose Group's access filtering.

## See Also

- [Permissions System](permissions-system.md)
- [Caching](caching.md)
- Reference: `web/modules/contrib/group/src/Plugin/Group/RelationHandler/AccessControlTrait.php`
