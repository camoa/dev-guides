---
description: Admin route configuration - use admin theme and integrate with Drupal's administrative UI patterns
drupal_version: "11.x"
---

# Admin Route Configuration

## When to Use

> Use when creating administrative interfaces that should use the admin theme and integrate with Drupal's admin UI patterns.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Admin configuration page | `_admin_route: TRUE` | Uses admin theme, proper styling |
| Admin menu landing page | `SystemController::systemAdminMenuBlockPage` | Shows child menu items automatically |
| Admin tabs/local tasks | Separate routes + `*.links.task.yml` | Standard multi-tab interface |
| Admin breadcrumbs | `_admin_route: TRUE` | Triggers admin breadcrumb builder |

## Pattern

```yaml
# Admin landing page (shows child menu items)
my_module.admin:
  path: '/admin/config/workflow/my-module'
  defaults:
    _controller: '\Drupal\system\Controller\SystemController::systemAdminMenuBlockPage'
    _title: 'My Module'
  requirements:
    _permission: 'administer my module'
  options:
    _admin_route: TRUE

# Admin configuration form
my_module.settings:
  path: '/admin/config/workflow/my-module/settings'
  defaults:
    _form: '\Drupal\my_module\Form\SettingsForm'
    _title: 'Settings'
  requirements:
    _permission: 'administer my module'
  options:
    _admin_route: TRUE
```

Reference: `core/modules/system/system.routing.yml`, `core/modules/node/node.routing.yml`

## Common Mistakes

- **Wrong**: Forgetting `_admin_route: TRUE` → **Right**: Always set for admin pages
- **Wrong**: Not using `SystemController::systemAdminMenuBlockPage` → **Right**: Use for parent admin pages
- **Wrong**: Inconsistent admin path structure → **Right**: Follow `/admin/[section]/[subsection]` pattern
- **Wrong**: Missing admin permission prefix → **Right**: Use "administer" prefix for admin permissions
- **Wrong**: Admin routes without proper option → **Right**: Broken breadcrumbs and theme without `_admin_route`

## See Also

- [Route Parameters](route-parameters.md)
- [Dynamic Routes](dynamic-routes.md)
- Reference: `core/lib/Drupal/Core/Routing/RouteSubscriberBase.php`
