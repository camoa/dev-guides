---
description: Group permissions — YAML discovery, plugin-generated permissions, scope system, Access Policy API, checking permissions, route access, and cache context
tldr: "Group 4.x calculates permissions via Drupal core's Access Policy API (IndividualGroupRoleAccessPolicy + SynchronizedGroupRoleAccessPolicy); custom calculators must be re-implemented as AccessPolicyBase subclasses tagged access_policy."
drupal_version: "11.x"
---

# Permissions System

## When to Use

> Read this when you need to define custom group permissions, understand the scope system, or programmatically grant/check permissions.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Static permissions | `.group.permissions.yml` | Simplest, auto-discovered |
| Dynamic permissions based on config | `permission_callbacks` key | Generated at runtime from config entities |
| Check permission in PHP | `$group->hasPermission()` or `GroupPermissionCheckerInterface` | Direct, injectable |
| Check permission in access result | `GroupAccessResult::allowedIfHasGroupPermission()` | Automatically adds cache metadata |
| Scope: non-members | `outsider` role + `global_role` | Applies to all authenticated users not in the group |
| Scope: members | `insider` role + `global_role` | Applies to all authenticated members |
| Scope: specific role | `individual` role (no `global_role`) | Manually assigned to members |
| Custom permission source (4.x) | `AccessPolicyBase` subclass tagged `access_policy` | Replaces `flexible_permissions_calculator` from 3.x |

## Permission Discovery: `.group.permissions.yml`

Group scans all modules for `{module}.group.permissions.yml` files (analogous to Drupal's `{module}.permissions.yml`). Permissions defined here are scoped to groups, not the global Drupal system.

```yaml
# mymodule.group.permissions.yml
publish article:
  title: 'Publish article nodes'
  description: 'Allow publishing of articles within the group'

manage features:
  title: 'Manage group features'
  restrict access: true
  warning: 'Warning: Give to trusted roles only.'
  allowed for:
    - member

# Dynamic permissions via callback
permission_callbacks:
  - 'Drupal\mymodule\GroupPermissions::permissions'
```

Key fields per permission: `title` (required), `description`, `restrict access` (bool), `warning`, `allowed for` (array: `anonymous`, `outsider`, `member`).

## Plugin-Generated Permissions

When a plugin has `entity_access: TRUE`, the `PermissionProvider` handler automatically generates a set of permissions for the plugin. These follow naming conventions:

| Permission name pattern | Purpose |
|---|---|
| `{plugin_id} relationship` admin permission | Administer all relationships of this type |
| `view {plugin_id} relationship` | View any relationship entity |
| `update any {plugin_id} relationship` | Edit any relationship entity |
| `update own {plugin_id} relationship` | Edit own relationship entity |
| `delete any {plugin_id} relationship` | Delete any relationship entity |
| `delete own {plugin_id} relationship` | Delete own relationship entity |
| `create {plugin_id} relationship` | Add an existing entity to the group |
| `view {plugin_id} entity` | View any entity in the group |
| `update any {plugin_id} entity` | Edit any entity in the group |
| `update own {plugin_id} entity` | Edit own entity in the group |
| `delete any {plugin_id} entity` | Delete any entity in the group |
| `delete own {plugin_id} entity` | Delete own entity in the group |
| `create {plugin_id} entity` | Create a new entity within the group |

For derived plugins (e.g., `group_node:article`), `{plugin_id}` becomes `group_node:article`.

## Scopes and Role Types

Roles in Group 4.x use a three-scope model:

```
outsider scope  → synchronized with global Drupal roles (authenticated, administrator, etc.)
                  Group adds permissions on top of the global role's capabilities
                  e.g.: group.role.project-outsider_authenticated.yml

insider scope   → synchronized with global Drupal roles, but only applies while the
                  user is a member of the group
                  e.g.: group.role.project-insider_authenticated.yml

individual scope → manually assigned to specific members within a group
                  These are what users typically call "group roles" (editor, manager, etc.)
                  e.g.: group.role.project-editor.yml
```

In v1 there were three hardcoded roles: `anonymous`, `outsider`, `member`. From v2 onward, these concepts are replaced by the scope system. Outsider and insider roles are configured through synchronized roles.

## Permission Calculation: Access Policy API

Group 4.x calculates a user's group permissions through Drupal core's **Access Policy API**. Each scope is handled by a service tagged `access_policy`:

| Scope | Access policy class | Service ID / priority |
|---|---|---|
| `individual` | `IndividualGroupRoleAccessPolicy` | `access_policy.individual_group_role` / -100 |
| `outsider`, `insider` | `SynchronizedGroupRoleAccessPolicy` | `access_policy.synchronized_group_role` / -50 |

`GroupPermissionCalculator::calculateFullPermissions()` asks core's `access_policy_processor` service to process each scope (`outsider`, `insider`, `individual`) and merges the results into a single `CalculatedPermissions` object. Each policy emits `CalculatedPermissionsItem` objects carrying the role's permissions, the admin flag, the scope, and the group ID (individual scope) or group-type ID (synchronized scopes).

To add a custom permission source, register a service tagged `access_policy` whose `applies()` method returns `TRUE` for the scope you target — the same way you would extend access policies for any core entity. The `group_permission.checker` service (`GroupPermissionChecker`) is the high-level entry point: `hasPermissionInGroup($permission, $account, $group)` checks the individual scope first, then the synchronized scope based on membership.

> **3.x:** Group 3.x used the contrib `flexible_permissions` module's chain calculator. It registered `IndividualGroupPermissionCalculator` (priority -100) and `SynchronizedGroupPermissionCalculator` (priority -50) as `flexible_permissions_calculator`-tagged services. In 4.x these became core access policies: the service tag changed from `flexible_permissions_calculator` to `access_policy`, and any custom calculators must be re-implemented as `AccessPolicyBase` subclasses.

## Role ID Convention

Role IDs follow the pattern `{group_type_id}-{role_suffix}`. Because GroupType IDs have a 22-character maximum (leaving room for `-anonymous` to stay under the 32-char config limit), keep group type IDs short.

## Checking Permissions

```php
// On a Group entity (most common).
if ($group->hasPermission('publish article', $account)) {
  // ...
}

// Via the permission checker service (inject GroupPermissionCheckerInterface).
if ($this->permissionChecker->hasPermissionInGroup('publish article', $account, $group)) {
  // ...
}

// Via GroupAccessResult for cacheable access checks.
use Drupal\group\Access\GroupAccessResult;
$access = GroupAccessResult::allowedIfHasGroupPermission($group, $account, 'view group');
$access = GroupAccessResult::allowedIfHasGroupPermissions($group, $account, ['edit group', 'administer group'], 'OR');
```

## Route Access Requirements

Group provides several custom access checks for routing:

| `requirements` key | Class | Checks |
|---|---|---|
| `_group_permission: 'some permission'` | `GroupPermissionAccessCheck` | User has permission in the group from route context |
| `_group_member: TRUE` | `GroupMemberAccessCheck` | User is a member of the group |
| `_group_installed_content: 'plugin_id'` | `GroupInstalledContentAccessCheck` | Plugin is installed on the group type |
| `_group_owns_content: TRUE` | `GroupOwnsContentAccessCheck` | User owns the group content |
| `_group_relationship_create_access: 'plugin_id'` | `GroupRelationshipCreateAccessCheck` | User can create a relationship of this type |

```yaml
# routing.yml example
mymodule.group.custom_page:
  path: '/group/{group}/my-page'
  defaults:
    _controller: '\Drupal\mymodule\Controller\MyController::page'
  requirements:
    _group_permission: 'manage features'
```

## Cache Context: `user.group_permissions`

Any render array or response that varies based on group permissions must add the `user.group_permissions` cache context. Group does this automatically for its own access checks. If you are checking group permissions manually in a controller, preprocess function, or block, you must add it yourself:

```php
$build['#cache']['contexts'][] = 'user.group_permissions';
```

## Common Mistakes

- Not adding `user.group_permissions` cache context when rendering group-permission-dependent content. This causes stale cached output to be served to users with different group permissions.
- Using Drupal's standard `AccessResult::allowedIfHasPermission()` for group permissions. It checks global Drupal permissions, not group-level permissions. Use `GroupAccessResult` instead.
- Setting scope but not `global_role` on outsider/insider roles. Both fields are required for those scopes. Individual roles must NOT have `global_role`.

## See Also

- [Access Control](access-control.md)
- [Caching](caching.md)
- Reference: `web/modules/contrib/group/src/Access/GroupAccessResult.php`
