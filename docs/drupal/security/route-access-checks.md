---
description: Protecting routes from unauthorized access using permission checks, entity access, and custom access check services.
---

# Route Access Checks

## When to Use
Protecting routes (URLs) from unauthorized access before the controller executes.

## Steps
1. **Add access requirements to route definition**
   ```yaml
   # mymodule.routing.yml
   mymodule.node_edit:
     path: '/node/{node}/custom-edit'
     defaults:
       _controller: '\Drupal\mymodule\Controller\NodeController::edit'
     requirements:
       _entity_access: 'node.update'  # Check entity access
       _permission: 'edit content'     # Check permission (both required)
     options:
       parameters:
         node:
           type: 'entity:node'
   ```

2. **For custom logic, create access check service**
   ```php
   // src/Access/CustomCheck.php
   namespace Drupal\mymodule\Access;

   use Drupal\Core\Access\AccessResult;
   use Drupal\Core\Session\AccountInterface;

   class CustomCheck {
     public function access(AccountInterface $account) {
       // Custom logic
       $allowed = $account->id() > 0 && date('H') < 17;
       return AccessResult::allowedIf($allowed)
         ->cachePerUser()
         ->addCacheTags(['config:mymodule.settings']);
     }
   }
   ```

3. **Register in `mymodule.services.yml`**
   ```yaml
   services:
     mymodule.custom_access_check:
       class: Drupal\mymodule\Access\CustomCheck
       tags:
         - { name: access_check, applies_to: _custom_access }
   ```

4. **Use in routing.yml**
   ```yaml
   requirements:
     _custom_access: 'TRUE'
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Choosing check type | Simple permission | Use `_permission: 'permission name'` |
| Choosing check type | Entity operation | Use `_entity_access: 'entity_type.operation'` |
| Choosing check type | Complex logic | Create custom access check service |
| Combining checks | ALL must pass | List multiple in `requirements:` (AND logic) |
| Combining checks | ANY can pass | Separate with + in permission: `_permission: 'perm1+perm2'` (OR) |

## Common Mistakes
- No requirements key -- Route is public, including to anonymous
- Returning boolean from custom check -- Must return `AccessResult` object
- Not adding cache metadata -- Access check runs on every request, killing performance
- Using `_access: 'TRUE'` -- This means "always allow", extremely dangerous
- Forgetting to tag service -- Access check won't be discovered

## See Also
- Reference: `/core/lib/Drupal/Core/Access/AccessCheckInterface.php`
- [AccessResult Patterns](accessresult-patterns.md) for return value details
- Reference: https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes
