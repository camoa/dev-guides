---
description: Group security — trust model, permission escalation risks, config wrapper security, cache poisoning, and anonymous user cache tags
drupal_version: "11.x"
---

# Security

## When to Use

> Review this before deploying a Group-based site to production to understand the trust model and potential vulnerabilities.

## Decision

| Permission | Risk level | Guidance |
|---|---|---|
| `administer group` (global) | Critical | Full control over all groups, types, and roles. Treat like site admin. |
| `administer members` (group permission) | High | Can add/remove members, change roles. Can grant admin-level group roles. |
| `admin: true` role | Critical | Bypasses all permission checks. Assign with extreme caution. |
| `edit group` | Medium | Allows editing the group entity itself. Review what fields are exposed. |
| Outsider anonymous role | High (if misconfigured) | Applies to all unauthenticated users. Default to `view group` only for public groups. |

## Pattern

Minimal secure outsider role for a public group:

```yaml
# group.role.project-outsider_anonymous.yml
scope: outsider
global_role: anonymous
permissions:
  - 'view group'
  # Do NOT grant create/update/delete permissions to anonymous
```

Cache poisoning protection — the `user.group_permissions` hash:

```php
// The hash is generated as:
hash('sha256', $private_key . $hash_salt . $data)
// SHA-256 + site private key + hash salt = unforgeable from outside the application
```

SQL injection protection — always validate plugin IDs before passing to storage:

```php
// Wrong: pass unsanitized user input
$storage->loadByPluginId($request->query->get('plugin'));

// Right: validate against known plugin IDs first
$allowed = $this->pluginManager->getDefinitions();
if (!isset($allowed[$plugin_id])) { throw new AccessDeniedHttpException(); }
$storage->loadByPluginId($plugin_id);
```

## Common Mistakes

- **Wrong**: Giving outsider roles too many permissions during development → **Right**: Lock down outsider permissions before going live. Outsider permissions apply to ALL authenticated non-member users.
- **Wrong**: Using a single group type for all use cases → **Right**: Groups with different trust requirements should use different group types with separate role configurations.
- **Wrong**: Deploying config without reviewing group role permissions → **Right**: Export and review `group.role.*` config files before each deployment.

## See Also

- [Permissions System](permissions-system.md)
- [Access Control](access-control.md)
- [When to Use Group](when-to-use-group.md)
- Reference: `web/modules/contrib/group/src/Access/`
