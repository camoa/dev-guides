---
description: Control block visibility based on permissions, roles, or custom logic
drupal_version: "11.x"
---

# Block Access Control

## When to Use

Controlling whether a block should be displayed based on user permissions, roles, or custom logic.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 1 (access check) | Based on permission | Use `AccessResult::allowedIfHasPermission()` |
| Step 1 (access check) | Based on role | Check `$account->hasRole()`, add `user.roles` context |
| Step 1 (access check) | Based on content/entity | Add cache tags for that entity |
| Step 2 (return) | Access changes frequently | Use `forbidden()` sparingly; it's uncacheable |
| Step 3 (caching) | User-dependent | Add `user` or `user.roles` cache context |

## Pattern

Common access patterns:

```php
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Session\AccountInterface;

// Permission-based
protected function blockAccess(AccountInterface $account) {
  return AccessResult::allowedIfHasPermission($account, 'access content');
}

// Role-based with cache context
protected function blockAccess(AccountInterface $account) {
  return AccessResult::allowedIf($account->hasRole('premium_member'))
    ->addCacheContexts(['user.roles']);
}

// Anonymous users only
protected function blockAccess(AccountInterface $account) {
  return AccessResult::allowedIf($account->isAnonymous())
    ->addCacheContexts(['user.roles:anonymous']);
}

// Complex logic with multiple cache metadata
protected function blockAccess(AccountInterface $account) {
  $node = \Drupal::routeMatch()->getParameter('node');
  $access = AccessResult::allowedIf(
    $node && $node->bundle() === 'article' && $account->hasPermission('view articles')
  );
  return $access->addCacheContexts(['route', 'user.permissions'])
                ->addCacheTags($node ? $node->getCacheTags() : []);
}
```

**AccessResult options:**
- `allowed()` — Show the block
- `forbidden()` — Hide the block (uncacheable)
- `neutral()` — No opinion (default to other checks)

**Reference:** `core/modules/user/src/Plugin/Block/UserLoginBlock.php` (lines 85-92)

## Common Mistakes

- **Wrong**: Using `forbidden()` when `neutral()` is appropriate → **Right**: `forbidden()` prevents caching; use `neutral()` to defer to other systems
- **Wrong**: Forgetting cache contexts on dynamic access → **Right**: Block will show incorrectly for different users
- **Wrong**: Checking access in `build()` instead of `blockAccess()` → **Right**: Bypasses access control system and caching
- **Wrong**: Not returning `AccessResult` object → **Right**: Must return `AccessResult`, not boolean
- **Wrong**: Using `allowed()` when should use `allowedIf($condition)` → **Right**: `allowed()` always grants access regardless of condition

## See Also

- [Block Caching Strategies](block-caching.md)
- [Visibility Conditions](visibility-conditions.md)
- Reference: https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/access-checking-on-routes
