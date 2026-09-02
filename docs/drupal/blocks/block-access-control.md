---
description: Control block visibility based on permissions, roles, or custom logic
tldr: "Use `blockAccess()` for programmatic access control tied to code logic. Use Visibility Conditions for UI-configurable per-placement access (pages, roles, content type)."
drupal_version: "11.x"
---

# Block Access Control

## When to Use

> Controlling whether a block should be displayed based on user permissions, roles, or custom logic.

## Steps

1. **Override blockAccess() method**
   ```php
   use Drupal\Core\Access\AccessResult;
   use Drupal\Core\Session\AccountInterface;

   protected function blockAccess(AccountInterface $account) {
     return AccessResult::allowedIfHasPermission($account, 'access content');
   }
   ```

2. **Return AccessResult object**
   - `AccessResult::allowed()` — Show the block
   - `AccessResult::forbidden()` — Hide the block (uncacheable)
   - `AccessResult::neutral()` — No opinion (default to other checks)

3. **Add cache metadata** for dynamic access
   ```php
   return AccessResult::allowedIfHasPermission($account, 'edit own content')
     ->addCacheContexts(['user']);
   ```

4. **Combine multiple conditions**
   ```php
   return AccessResult::allowedIf($condition1 && $condition2)
     ->addCacheTags(['node:1']);
   ```

## Decision Points

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

**Reference:** `core/modules/user/src/Plugin/Block/UserLoginBlock.php` (lines 85-92)

## Common Mistakes

- Using `forbidden()` when `neutral()` is appropriate → `forbidden()` prevents caching; use `neutral()` to defer to other systems
- Forgetting cache contexts on dynamic access → Block will show incorrectly for different users
- Checking access in `build()` instead of `blockAccess()` → Bypasses access control system and caching
- Not returning `AccessResult` object → Must return `AccessResult`, not boolean
- Using `allowed()` when should use `allowedIf($condition)` → `allowed()` always grants access regardless of condition

## See Also

- [Block Caching Strategies](block-caching.md)
- [Visibility Conditions](visibility-conditions.md) (for UI-configurable access)
- Reference: https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/access-checking-on-routes
