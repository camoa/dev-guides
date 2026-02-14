---
description: When restricting who can view a display based on permissions or roles.
drupal_version: "11.x"
---

## 14. Access Control

### When to Use
When restricting who can view a display based on permissions or roles.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Standard permission check | Permission access | Integrates with Drupal permission system |
| Role-based access | Role access | Direct role check, simpler than permission |
| Public access | None (unrestricted) | No access check, everyone can view |
| Custom access logic | Custom access plugin | Complex rules (e.g., time-based, entity ownership) |

### Access Types

#### Permission Access
```yaml
access:
  type: perm
  options:
    perm: 'access content'  # Machine name of permission
```

Checks if user has the specified permission. Permissions defined in `*.permissions.yml` files.

Reference: `core/modules/node/config/optional/views.view.content.yml` lines 332-335

#### Role Access
```yaml
access:
  type: role
  options:
    role:
      authenticated: authenticated
      administrator: administrator
```

Checks if user has any of the specified roles.

#### None (Unrestricted)
```yaml
access:
  type: none
  options: {}
```

No access check. Everyone can view.

### Pattern
Admin-only view with permission check:

```yaml
display:
  page_1:
    display_options:
      access:
        type: perm
        options:
          perm: 'administer nodes'
      path: admin/content/custom
```

Public REST export with authentication:

```yaml
rest_export_1:
  display_options:
    access:
      type: perm
      options:
        perm: 'access content'
    auth:
      - basic_auth
      - cookie
```

### Access vs Authentication (REST Export)
- **Access** (`access` option): Who can view results (based on Drupal permissions)
- **Authentication** (`auth` option): How users prove identity (cookie, basic_auth, oauth, etc.)

For REST exports, configure both:
1. `auth` → Forces authentication method
2. `access` → Checks permission after authentication

If authentication fails, user becomes anonymous. Access check then applies to anonymous user.

Reference: `core/modules/rest/src/Plugin/views/display/RestExport.php` lines 315-326

### Common Mistakes
- REST export without access control → Anonymous users can access all data; always set `access.type: perm`
- Using `access.type: none` on admin views → Anyone can view; use `perm: 'administer nodes'` or similar
- Permission name typo → Access silently fails (denies everyone); verify permission exists in `*.permissions.yml`
- Confusing role machine name vs label → Use machine name (`authenticated`), not label ("Authenticated user")
- Not considering anonymous access → Permission `access content` includes anonymous; use authenticated-only permission if needed

### See Also
- Section 6: REST Export Display — authentication configuration
- Section 31: Security & Performance — access control security
- Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 48-59
