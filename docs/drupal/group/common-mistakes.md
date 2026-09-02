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
| API | Calling `$group->addRelationship()` before saving the group | Throws `EntityStorageException: "Cannot add an entity to an unsaved group."` |
| API | Loading members with entity storage in a loop | Each call fires a SQL query; use `GroupMembership::loadByGroup()` which uses the cache |
| Plugin | Handler services without `shared: false` | Each handler instance is tied to a specific plugin ID — must be unshared |
| Plugin | Not calling `clearCachedDefinitions()` when a bundle is added | New bundle plugins won't appear until plugin cache is cleared |
| Views | Relying on Group auto-filtering for `group_relationship_field_data` Views | Only entity-based Views get automatic access filtering |

## Architecture Mistakes

**Mistake**: Installing Group and expecting all content to be immediately scoped by groups.
**Why it fails**: Group only restricts access to entities that ARE in a group (via a plugin with `entity_access: TRUE`). Ungrouped entities are unaffected. You must add entities to groups for access control to apply.

**Mistake**: Creating group types with IDs longer than 22 characters.
**Why it fails**: `GroupTypeInterface::ID_MAX_LENGTH = 22`. Group role IDs append suffixes like `-anonymous` and must stay under 32 characters. Longer group type IDs break role creation.

**Mistake**: Defining a `GroupRelationType` plugin without a config schema entry for each custom `defaultConfiguration()` key.
**Why it fails**: Config system validation fails on config import/export. Follow the `group_relation.config.{KEY}` schema pattern.

## Access Mistakes

**Mistake**: Using `AccessResult::allowedIfHasPermission($account, 'some group permission')` for group permissions.
**Why it fails**: This checks global Drupal permissions. Use `GroupAccessResult::allowedIfHasGroupPermission($group, $account, 'some group permission')` for group-scoped permission checks.

**Mistake**: Building render arrays that depend on group permissions without `user.group_permissions` cache context.
**Why it fails**: Users with different group permissions see the same cached output, causing security leaks or broken UI.

**Mistake**: Not checking `entity_access: TRUE` on your plugin when you expect Group to restrict access to that entity type.
**Why it fails**: Without `entity_access: TRUE`, Group never calls `entityAccess()` and never forbids access to the entity. The entity remains governed by Drupal's default access system.

**Mistake**: Using `admin: true` on a group role without careful thought.
**Why it fails**: Admin roles bypass ALL permission checks. Assign to trusted users only.

## API Mistakes

**Mistake**: Using the `group.membership_loader` service.
**Why it fails**: Removed in 4.0.0 (deprecated since 3.2.0). Use the `GroupMembership::loadSingle()`, `::loadByGroup()`, `::loadByUser()` static methods.

**Mistake**: Calling `$group->addRelationship()` before saving the group.
**Why it fails**: Throws `EntityStorageException: "Cannot add an entity to an unsaved group."` Both group and entity must be saved first.

**Mistake**: Loading group members with `\Drupal::entityTypeManager()->getStorage('group_relationship')->loadByGroup($group, 'group_membership')` in a loop.
**Why it fails**: Each call fires a SQL query. Use `GroupMembership::loadByGroup($group)` which uses the chained cache.

## Plugin Mistakes

**Mistake**: Registering handler services without `shared: false`.
**Why it fails**: Handler services must be unshared (`shared: false` in services.yml) because each handler instance is tied to a specific plugin ID.

**Mistake**: Forgetting to call `clearCachedDefinitions()` on the plugin manager when a bundle is added/removed.
**Why it fails**: Derived plugins (like `group_node:{bundle}`) are cached. New bundles will not appear as available plugins until the cache is cleared.

## Views Mistakes

**Mistake**: Relying on Group's automatic access filtering for a View based on `group_relationship_field_data`.
**Why it fails**: Group only auto-filters Views based on entity base tables (node, media, etc.). Views on `group_relationship_field_data` directly are NOT access-filtered.

## See Also

All other sections — common mistakes are duplicated in context within each section.
