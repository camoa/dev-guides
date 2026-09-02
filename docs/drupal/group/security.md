---
description: Group security — trust model, permission escalation risks, config wrapper security, role ID predictability, SQL injection, cache poisoning, and anonymous user cache tags
tldr: "Review this before deploying a Group-based site to production to understand the trust model and potential vulnerabilities. Anonymous is not its own scope — it is an outsider-scope role with global_role: anonymous."
drupal_version: "11.x"
---

# Security

## When to Use

> Review this before deploying a Group-based site to production to understand the trust model and potential vulnerabilities.

## Decision

| Permission | Risk |
|---|---|
| `administer group` (global) | Full control over all groups, group types, and roles. Treat like admin. |
| `administer members` (group permission) | Can add/remove members, change roles. Can be used to grant other members admin-level group roles. |
| `admin: true` role | Group admin role bypasses all permission checks. Assign with extreme caution. |
| `edit group` | Allows editing the group entity itself, potentially changing group type settings surfaced to users. |

Always configure the `outsider` (anonymous) role permissions conservatively. Anonymous users should generally only have `view group` if the group is public.

## Trust Model

Group operates on the principle of **explicit group-level override**: for any entity type with an active `entity_access: TRUE` plugin, Group either explicitly allows or explicitly forbids access. Returning `forbidden` is intentional — it means no other module can override Group's denial for a grouped entity.

This means: configure Group permissions carefully. If Group forbids access and the user does not have the right group role, no other module's `hook_entity_access()` implementation can grant access.

## Permission Escalation Risks

Anonymous is not a scope of its own. An anonymous group role is an **outsider**-scope role whose `global_role` is `anonymous` — that is exactly what `GroupRole::isAnonymous()` tests. `GroupRole::preSave()` rejects the insider equivalent, throwing `EntityMalformedException` ("Anonymous users cannot be members…") for `scope: insider` with `global_role: anonymous`. So every permission you hand anonymous users lands in the outsider scope and applies to every group of that type:

```yaml
# group.role.project-anonymous.yml
# The shape Group's own "add default roles" option produces for anonymous users.
id: project-anonymous
label: 'Anonymous'
scope: outsider
global_role: anonymous
group_type: project
permissions:
  - 'view group'
  # Do NOT grant create/update/delete relationship or entity permissions here.
```

## Config Wrapper Security

Group wraps config entities (via `group_config_wrapper`) to allow them to be related to groups. Config entities are typically admin-only. Exposing config entities through group relations to non-admin users requires carefully verifying that the config entity type does not expose sensitive data through its views or fields.

## Group Role ID Predictability

Group role IDs follow the pattern `{group_type_id}-{role_id}`. These are exposed in URLs (`/admin/group/types/manage/{group_type}/roles/{group_role}`). Do not use sensitive names as role IDs.

## Query Access and SQL Injection

Group's `EntityQueryAlter`, `GroupQueryAlter`, and `GroupRelationshipQueryAlter` classes add conditions to SQL queries using parameterized queries via Drupal's database API. There is no SQL injection risk from Group's own code. However:

- Never pass unsanitized user input as a `plugin_id` to `loadByPluginId()` or similar storage methods. Validate against known plugin IDs first.
- Views with exposed filters on `plugin_id` should use allowed-values constraints.

```php
// Wrong: pass unsanitized user input
$storage->loadByPluginId($request->query->get('plugin'));

// Right: validate against known plugin IDs first
$allowed = $this->pluginManager->getDefinitions();
if (!isset($allowed[$plugin_id])) { throw new AccessDeniedHttpException(); }
$storage->loadByPluginId($plugin_id);
```

## Cache Poisoning Risk

The `user.group_permissions` cache context hash includes serialized permission data. The hash uses SHA-256 with the site's private key and hash salt as a prefix (`hash('sha256', $private_key . $hash_salt . $data)`). This makes the hash unforgeable from outside the application. Do not expose the private key.

## Anonymous User Cache Tags

The `AnonymousUserResponseSubscriber` adds cache tags for anonymous group permissions to responses. If Varnish or another reverse proxy is configured to serve anonymous users, ensure your CDN respects `Cache-Control: no-store` for group-permission-dependent pages, or that it handles Drupal's cache tag invalidation headers (e.g., via the `purge` module).

## Common Mistakes

- Giving outsider roles too many permissions during development and forgetting to lock them down before going live. Outsider permissions apply to ALL authenticated non-member users, which can be a very large audience.
- Using a single group type for all use cases to save configuration time. Groups with different trust requirements should use different group types with separate role configurations.
- Deploying config without reviewing what permissions are being granted to outsider/insider roles. Export and review `group.role.*` config files before each deployment.

## See Also

- [Permissions System](permissions-system.md)
- [Access Control](access-control.md)
- [When to Use Group](when-to-use-group.md)
- Reference: `web/modules/contrib/group/src/Access/`
