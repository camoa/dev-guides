---
description: Common Drupal routing pitfalls - avoid site crashes and security vulnerabilities
drupal_version: "11.x"
---

# Common Pitfalls

## When to Use

> Reference this before committing routing YAML or when debugging routing issues. These are real-world errors that crash sites or create security vulnerabilities.

## Decision

| If you see | The problem is | Fix with |
|-----------|---------------|----------|
| `\\\\` in controller definition | Double backslash escaping | Change to single `\` in single quotes |
| Path without leading `/` | Invalid path pattern | Add leading slash: `/admin/config` |
| Underscores in URL path | Non-standard URL format | Use hyphens: `/my-module/my-page` |
| Missing `_admin_route: TRUE` | Wrong theme on admin page | Add option to route definition |
| Non-existent permission | Access always denied | Define in `permissions.yml` |
| Route parameter without validation | Security vulnerability | Add `requirements` regex validation |
| Missing entity type in parameters | String instead of entity object | Define `type: entity:node` in options |
| RouteSubscriber without service tag | Subscriber never runs | Add `event_subscriber` tag in services.yml |
| Custom access without cache metadata | Performance degradation | Add cache contexts/tags to AccessResult |

## Pattern

```yaml
# WRONG: Multiple critical errors
my_module.bad_route:
  path: 'admin/my_module/items/{id}'  # Missing leading slash
  defaults:
    _controller: '\\Drupal\\my_module\\Controller\\Bad::view'  # Double backslashes
  requirements:
    _permission: 'fake permission'  # Non-existent permission
  # Missing: parameter validation, parameter type, admin_route option

# CORRECT: All issues fixed
my_module.good_route:
  path: '/admin/my-module/items/{id}'  # Leading slash, hyphens
  defaults:
    _controller: '\Drupal\my_module\Controller\Good::view'  # Single backslashes
    _title_callback: '\Drupal\my_module\Controller\Good::getTitle'
  requirements:
    _permission: 'administer my module'  # Exists in permissions.yml
    id: '\d+'  # Parameter validation
  options:
    _admin_route: TRUE  # Admin theme
    parameters:
      id:
        type: integer  # Parameter type
```

## Common Mistakes

- **CRITICAL**: Double backslash issue causes site crashes during cache rebuild
- **SECURITY**: Missing parameter validation is a security risk - allows unexpected input
- **THEME**: Missing `_admin_route` causes theme confusion and broken breadcrumbs
- **ACCESS**: Not defining permissions before using them causes fatal errors

## See Also

- [Testing and Debugging](testing-and-debugging.md)
- [Security Best Practices](security-best-practices.md)
- Reference: All previous routing guides for detailed explanations
