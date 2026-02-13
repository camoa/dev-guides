---
description: Drupal route access control - permission, role, and custom access patterns to secure routes
drupal_version: "11.x"
---

# Access Control Patterns

## When to Use

> Use when restricting route access to specific users, roles, or custom conditions. Always define access requirements - never leave routes open.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Single permission | `_permission: 'permission name'` | Simplest, most common pattern |
| Multiple permissions (OR) | `_permission: 'perm1+perm2'` | User needs ANY listed permission |
| Role-based access | `_role: 'role_name'` | Less flexible than permissions, avoid unless necessary |
| Logged-in users only | `_user_is_logged_in: 'TRUE'` | No specific permission needed |
| Custom access logic | `_custom_access` | Complex conditions beyond permissions/roles |
| Entity access | `_entity_access: 'node.edit'` | Leverages entity access system |

## Pattern

```yaml
# Permission-based access
my_module.admin:
  path: '/admin/my-module'
  defaults:
    _form: '\Drupal\my_module\Form\AdminForm'
  requirements:
    _permission: 'administer my module'

# Multiple permissions (OR logic)
my_module.content:
  path: '/my-module/content'
  defaults:
    _controller: '\Drupal\my_module\Controller\ContentController::build'
  requirements:
    _permission: 'edit content+administer nodes'

# Custom access checker
my_module.custom:
  path: '/my-module/special'
  defaults:
    _controller: '\Drupal\my_module\Controller\SpecialController::build'
  requirements:
    _custom_access: '\Drupal\my_module\Access\CustomAccessChecker::access'
```

Reference: `core/modules/user/user.routing.yml`

## Common Mistakes

- **Wrong**: Using non-existent permissions → **Right**: Check `permissions.yml` before using
- **Wrong**: Forgetting to define custom permissions → **Right**: Add to `permissions.yml` before routing
- **Wrong**: Expecting AND logic for multiple permissions → **Right**: Use `_custom_access` for AND logic
- **Wrong**: Leaving routes without access requirements → **Right**: Always define access checks
- **Wrong**: Using `_role` instead of `_permission` → **Right**: Prefer permissions for flexibility

## See Also

- [Basic Route Structure](basic-route-structure.md)
- [Custom Access Checking](custom-access-checking.md)
- Reference: [Access checking on routes - Drupal.org](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes)
- Reference: [Custom route access checking - Drupal.org](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/custom-route-access-checking)
