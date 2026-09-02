---
description: All entity types provided by Group 4.x — IDs, base tables, key fields, shared bundle classes, and membership loading
tldr: "Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides. In 4.x the $roles filter on loadByGroup() and loadByUser() must be an array."
drupal_version: "11.x"
---

# Entity Types

## When to Use

> Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides.

## Decision

| Entity Type ID | Class | Type | Bundle of |
|---|---|---|---|
| `group` | `Drupal\group\Entity\Group` | Content | — |
| `group_type` | `Drupal\group\Entity\GroupType` | Config (bundle for `group`) | — |
| `group_relationship` | `Drupal\group\Entity\GroupRelationship` | Content | — |
| `group_relationship_type` | `Drupal\group\Entity\GroupRelationshipType` | Config (bundle for `group_relationship`) | — |
| `group_role` | `Drupal\group\Entity\GroupRole` | Config | — |
| `group_config_wrapper` | `Drupal\group\Entity\ConfigWrapper` | Content | — |

## Group Entity (`group`)

Base tables: `groups` (base), `groups_field_data` (data), `groups_revision`, `groups_field_revision`

Key base fields: `id`, `uuid`, `uid` (owner), `langcode`, `type` (bundle), `label`, `status` (published), `revision_id`, `created`, `changed`

Implements: `ContentEntityInterface`, `EntityOwnerInterface`, `EntityChangedInterface`, `EntityPublishedInterface`, `RevisionLogInterface`

The Group entity supports full revisioning, translation, and publishing workflow out of the box.

## GroupRelationship Entity (`group_relationship`)

Base tables: `group_relationship` (base), `group_relationship_field_data` (data)

Key fields: `id`, `uuid`, `type` (bundle, equals `GroupRelationshipType` id), `gid` (group reference), `entity_id` (related entity reference), `plugin_id` (denormalized for fast querying), `group_type` (denormalized), `uid` (owner), `created`, `changed`

The `plugin_id` and `group_type` fields are denormalized copies stored on the data table to allow fast SQL filtering without joins.

The bundle of `group_relationship` is `group_relationship_type`, which is an internal config entity (marked `internal = TRUE`) and not directly user-facing.

## GroupRole Entity (`group_role`)

Config entity. ID format: `{group_type_id}-{role_machine_name}` (e.g., `project-editor`).

Key fields: `scope` (`outsider`, `insider`, or `individual`), `global_role` (if scope is `outsider`/`insider`, references a Drupal user role), `admin` (boolean bypass), `permissions` (array).

Config file pattern: `group.role.{group_type_id}-{role_id}.yml`

## GroupConfigWrapper (`group_config_wrapper`)

Internal entity that wraps config entities so they can be used as group relationship targets. Created automatically. Never interact with this directly unless writing a plugin that handles config entity types.

## Shared Bundle Classes

A `GroupRelationship` entity can have a **shared bundle class** — a PHP class that gets used for all relationship bundles backed by the same plugin. The `group_membership` plugin uses `Drupal\group\Entity\GroupMembership` as its shared bundle class, providing membership-specific methods (`getRoles()`, `addRole()`, `removeRole()`, `hasPermission()`).

To leverage the shared bundle class, load membership entities through normal entity storage and cast to `GroupMembership` (or `GroupMembershipInterface`).

## Pattern

```php
use Drupal\group\Entity\GroupMembership;

// Load a single membership (cached via chained cache backend).
$membership = GroupMembership::loadSingle($group, $account);
if ($membership) {
  $roles = $membership->getRoles(); // includes synchronized roles
}

// Load all memberships for a user.
$memberships = GroupMembership::loadByUser($account);

// Load all memberships for a group.
$members = GroupMembership::loadByGroup($group);

// Load filtered by role (4.x: the role filter is an array).
$editors = GroupMembership::loadByGroup($group, ['project-editor']);
```

## Common Mistakes

- Calling `GroupRelationshipType::label()` and displaying it to users. It is labeled "INTERNAL USE ONLY" and is not user-facing. Use the plugin's label instead.
- Querying `group_relationship` with `accessCheck(TRUE)` in non-user-context code. Access checks on group relationships require full permission calculation which can be expensive. Use `accessCheck(FALSE)` in backend operations and apply manual authorization checks.

## See Also

- [PHP API](php-api.md)
- [Permissions System](permissions-system.md)
- Reference: `web/modules/contrib/group/src/Entity/GroupMembership.php`
