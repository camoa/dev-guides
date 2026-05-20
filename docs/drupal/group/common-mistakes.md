---
description: Common Group module mistakes — architecture, access, API, plugin, and Views errors with explanations
tldr: "Review this before shipping group-related code to catch frequent errors."
drupal_version: "11.x"
---

# Common Mistakes

## When to Use

> Review this before shipping group-related code to catch frequent errors.

## Decision

| Category | Mistake | Why it fails |
|---|---|---|
| Architecture | Group type IDs longer than 22 characters | Role IDs append suffixes like `-anonymous` and must stay under 32 characters |
| Architecture | Expecting all content to be scoped immediately after install | Group only restricts entities that ARE in a group with `entity_access: TRUE` |
| Architecture | No config schema for custom `defaultConfiguration()` keys | Config import/export fails validation |
| Access | Using `AccessResult::allowedIfHasPermission()` for group permissions | Checks global permissions, not group-level |
| Access | Missing `user.group_permissions` context in permission-checking blocks | All users see same cached output — security leak |
| Access | `entity_access: FALSE` (default) on plugin but expecting group access control | Group never calls `entityAccess()` without `entity_access: TRUE` |
| API | Using `group.membership_loader` service | Removed in 4.0.0 (deprecated since 3.2.0) |
| API | Passing string to `$roles` filter in 4.x | Must be an array: `loadByGroup($group, ['role_id'])` |
| API | Calling `$group->addRelationship()` before saving the group | Throws `EntityStorageException: "Cannot add an entity to an unsaved group."` |
| API | Expecting auto-created creator membership from programmatic `Group::save()` | In 4.x, creator_membership is form-only — call `addMember()` explicitly |
| API | Loading members with entity storage in a loop | Each call fires a SQL query; use `GroupMembership::loadByGroup()` which uses the cache |
| API | Expecting `hook_ENTITY_TYPE_update()` on entity when added to a group | In 4.x, Group only invalidates cache tags — it does not re-save the entity |
| Config | Keeping `creator_wizard` in group type config for 4.x | Removed in 4.x — config validation flags it |
| Config | Keeping `use_creation_wizard` in relationship type plugin_config for 4.x | Removed in 4.x — config validation flags it |
| Plugin | Handler services without `shared: false` | Each handler instance is tied to a specific plugin ID — must be unshared |
| Plugin | Not calling `clearCachedDefinitions()` when a bundle is added | New bundle plugins won't appear until plugin cache is cleared |
| Plugin | Using `flexible_permissions_calculator` service tag in 4.x | Tag changed to `access_policy`; re-implement as `AccessPolicyBase` subclass |
| Views | Relying on Group auto-filtering for `group_relationship_field_data` Views | Only entity-based Views get automatic access filtering |

## Common Mistakes

- **Wrong**: Installing Group and expecting all content to be immediately group-scoped → **Right**: Configure plugins with `entity_access: TRUE` and add entities to groups.
- **Wrong**: Using `admin: true` on roles without careful thought → **Right**: Admin roles bypass ALL permission checks — assign to trusted users only.

## See Also

All other sections — common mistakes are duplicated in context within each section.
