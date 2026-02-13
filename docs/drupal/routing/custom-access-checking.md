---
description: Custom access checking for routes - implement complex business logic beyond built-in permission checks
drupal_version: "11.x"
---

# Custom Access Checking

## When to Use

> Use when built-in access checks (`_permission`, `_role`, `_entity_access`) are insufficient. Complex business logic, multi-factor checks, or context-dependent access require custom checkers.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| AND logic for permissions | Custom access checker | Built-in only supports OR |
| Time-based access | Custom checker checking current time | No built-in time-based access |
| Entity relationship access | Custom checker with entity loading | Check ownership, references, etc. |
| Configuration-based access | Custom checker reading config | Access rules from admin settings |
| Complex multi-factor access | Custom checker with multiple conditions | Full control over access logic |

## Pattern

```php
// src/Access/CustomAccessChecker.php
namespace Drupal\my_module\Access;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Routing\Access\AccessInterface;
use Drupal\Core\Session\AccountInterface;

class CustomAccessChecker implements AccessInterface {

  public function access(AccountInterface $account) {
    // Custom logic here
    if ($account->hasPermission('access content')
        && $account->hasPermission('use admin toolbar')) {
      return AccessResult::allowed()->cachePerPermissions();
    }

    return AccessResult::forbidden()->cachePerPermissions();
  }
}
```

```yaml
# my_module.services.yml
services:
  my_module.custom_access_checker:
    class: Drupal\my_module\Access\CustomAccessChecker
    tags:
      - { name: access_check, applies_to: _custom_access_check }
```

```yaml
# my_module.routing.yml
my_module.custom_page:
  path: '/custom-page'
  defaults:
    _controller: '\Drupal\my_module\Controller\CustomController::build'
  requirements:
    _custom_access_check: 'TRUE'
```

Reference: `core/lib/Drupal/Core/Access/AccessInterface.php`, `core/modules/user/src/Access/`

## Common Mistakes

- **Wrong**: Not implementing cache metadata → **Right**: Add `->cachePerPermissions()` or appropriate cache context
- **Wrong**: Using `AccessResult::allowed()` without cache contexts → **Right**: Always specify cache metadata
- **Wrong**: Missing service tag `access_check` → **Right**: Add tag with `applies_to` parameter
- **Wrong**: Not injecting dependencies properly → **Right**: Use dependency injection, avoid static calls
- **Wrong**: Overly complex access logic → **Right**: Consider simplifying or using existing patterns
- **Wrong**: Forgetting to handle edge cases → **Right**: Test all access scenarios thoroughly

## See Also

- [Route Subscribers](route-subscribers.md)
- [Testing and Debugging](testing-and-debugging.md)
- Reference: [Custom route access checking - Drupal.org](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/custom-route-access-checking)
- Reference: [Advanced route access checking - Drupal.org](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/advanced-route-access-checking)
- Reference: [Custom access check - Axelerant](https://www.axelerant.com/blog/custom-access-check-routes-drupal-8)
- Reference: [Custom route access checker - Bhimmu](https://www.bhimmu.com/drupal10/custom-route-access-checks)
