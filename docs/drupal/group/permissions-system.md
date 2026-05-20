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

## Pattern

```php
// Define in mymodule.group.permissions.yml:
// publish article:
//   title: 'Publish article nodes'
//   allowed for: [member]

// Check permission (most common).
if ($group->hasPermission('publish article', $account)) {
  // ...
}

// Cacheable access check.
use Drupal\group\Access\GroupAccessResult;
$access = GroupAccessResult::allowedIfHasGroupPermission($group, $account, 'view group');
$access = GroupAccessResult::allowedIfHasGroupPermissions(
  $group, $account, ['edit group', 'administer group'], 'OR'
);

// Add cache context when checking group permissions manually.
$build['#cache']['contexts'][] = 'user.group_permissions';
```

Route access requirement:

```yaml
mymodule.group.custom_page:
  path: '/group/{group}/my-page'
  requirements:
    _group_permission: 'manage features'
```

**4.x permission calculation services:**

| Scope | Access policy class | Tag / priority |
|---|---|---|
| `individual` | `IndividualGroupRoleAccessPolicy` | `access_policy` / -100 |
| `outsider`, `insider` | `SynchronizedGroupRoleAccessPolicy` | `access_policy` / -50 |

## Common Mistakes

- **Wrong**: Using `AccessResult::allowedIfHasPermission()` for group permissions → **Right**: Use `GroupAccessResult::allowedIfHasGroupPermission()`. The former checks global Drupal permissions only.
- **Wrong**: Not adding `user.group_permissions` cache context when rendering group-permission-dependent content → **Right**: Always add it or use `GroupAccessResult` which adds it automatically.
- **Wrong**: Setting scope without `global_role` on outsider/insider roles → **Right**: Outsider and insider roles require `global_role`. Individual roles must NOT have `global_role`.
- **Wrong**: Registering a `flexible_permissions_calculator`-tagged service in 4.x → **Right**: Re-implement as an `AccessPolicyBase` subclass tagged `access_policy`.

## See Also

- [Access Control](access-control.md)
- [Caching](caching.md)
- Reference: `web/modules/contrib/group/src/Access/GroupAccessResult.php`
