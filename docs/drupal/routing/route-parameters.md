---
description: Drupal route parameters - dynamic URL segments with validation and entity auto-loading
drupal_version: "11.x"
---

# Route Parameters

## When to Use

> Use when routes need dynamic segments (e.g., node IDs, user IDs, custom identifiers). Parameters enable reusable routes for multiple entities or contexts.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Numeric ID | `{param}` with `\d+` requirement | Validates only digits |
| Entity object | `{entity_type}` with type parameter | Auto-loads entity, handles access |
| Alphanumeric slug | `{param}` with `[a-zA-Z0-9-]+` | URL-safe characters only |
| Optional parameter | Default value in controller | YAML doesn't support optional segments |

## Pattern

```yaml
# Numeric parameter with validation
my_module.item_view:
  path: '/items/{item_id}'
  defaults:
    _controller: '\Drupal\my_module\Controller\ItemController::view'
    _title_callback: '\Drupal\my_module\Controller\ItemController::getTitle'
  requirements:
    _permission: 'access content'
    item_id: '\d+'  # Only digits allowed
  options:
    parameters:
      item_id:
        type: integer

# Entity parameter (auto-loads node)
my_module.node_custom:
  path: '/node/{node}/custom-view'
  defaults:
    _controller: '\Drupal\my_module\Controller\NodeController::customView'
  requirements:
    _permission: 'access content'
    _entity_access: 'node.view'
  options:
    parameters:
      node:
        type: entity:node
```

Reference: `core/modules/node/node.routing.yml`

## Common Mistakes

- **Wrong**: Missing parameter validation in `requirements` → **Right**: Add regex validation for all parameters
- **Wrong**: Not defining parameter type in `options` → **Right**: Specify `type: integer` or `type: entity:node`
- **Wrong**: Using underscores in parameter names → **Right**: Use lowercase alphanumeric for consistency
- **Wrong**: Forgetting `_title_callback` for dynamic titles → **Right**: Add callback for context-specific titles
- **Wrong**: Missing entity access check → **Right**: Add `_entity_access` requirement

## See Also

- [Access Control Patterns](access-control-patterns.md)
- [Admin Route Configuration](admin-route-configuration.md)
- Reference: [Parameters in routes - Drupal.org](https://www.drupal.org/docs/8/api/routing-system/parameters-in-routes)
- Reference: [Route parameters - Drupal at your Fingertips](https://www.drupalatyourfingertips.com/links)
