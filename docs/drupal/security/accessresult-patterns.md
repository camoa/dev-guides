---
description: Returning access decisions using AccessResult objects with proper cache metadata, combining logic, and conditional methods.
---

# AccessResult Patterns

## When to Use
Returning access decisions from custom access checks, entity access handlers, or any code that determines access.

## Items

### AccessResult::allowed()
**Description:** Explicitly grant access.
**When to Use:** Condition is met and access should be granted.
**Pattern:**
```php
// Conditional access grant
if ($node->isPublished() && $account->hasPermission('view content')) {
  return AccessResult::allowed()->cachePerPermissions()->addCacheableDependency($node);
}
```
**Gotcha:** NEVER return `allowed()` unconditionally -- always condition it on something.

### AccessResult::forbidden()
**Description:** Explicitly deny access (overrides allowed from other checks).
**When to Use:** Condition actively prohibits access (e.g., banned user, locked content).
**Pattern:**
```php
// Explicitly forbid based on account state
if ($account->isBlocked()) {
  return AccessResult::forbidden('Account is blocked')->cachePerUser();
}
```
**Gotcha:** Forbidden is contagious -- ANY forbidden result denies access regardless of other allowed results.

### AccessResult::neutral()
**Description:** No opinion (neither allow nor deny).
**When to Use:** This check doesn't apply, or can't make a decision.
**Pattern:**
```php
// Neutral when conditions don't apply
if (!$node instanceof NodeInterface) {
  return AccessResult::neutral('Not a node');
}
// Continue checking...
```
**Gotcha:** Multiple neutrals = denied. Access only granted if at least one allowed and zero forbidden.

### AccessResult::allowedIf($condition)
**Description:** Shorthand for conditional allow/neutral.
**When to Use:** Simple boolean condition determines access.
**Pattern:**
```php
// Simple conditional
return AccessResult::allowedIf($account->isAuthenticated())
  ->addCacheContexts(['user.roles:authenticated']);
```
**Gotcha:** Returns neutral (not forbidden) when false. Use `forbiddenIf()` for active denial.

### AccessResult::forbiddenIf($condition)
**Description:** Shorthand for conditional forbid/neutral.
**When to Use:** Condition should actively block access.
**Pattern:**
```php
// Block access based on condition
return AccessResult::forbiddenIf($node->get('field_locked')->value)
  ->addCacheableDependency($node);
```

### AccessResult::allowedIfHasPermission($account, $permission)
**Description:** Check single permission with automatic cache context.
**When to Use:** Access depends solely on one permission.
**Pattern:**
```php
return AccessResult::allowedIfHasPermission($account, 'administer nodes');
// Automatically adds 'user.permissions' cache context
```

### AccessResult::allowedIfHasPermissions($account, $permissions, $conjunction)
**Description:** Check multiple permissions with AND/OR logic.
**Parameters:**
- `$permissions`: Array of permission strings
- `$conjunction`: 'AND' (default) or 'OR'

**Pattern:**
```php
// User must have ALL permissions
return AccessResult::allowedIfHasPermissions(
  $account,
  ['edit content', 'use admin toolbar'],
  'AND'
);

// User must have ANY permission
return AccessResult::allowedIfHasPermissions(
  $account,
  ['administer nodes', 'bypass node access'],
  'OR'
);
```

## Cache Metadata Methods
| Method | Purpose | Example |
|---|---|---|
| `cachePerPermissions()` | Vary by user permissions | Permission-based access |
| `cachePerUser()` | Vary by user ID | Ownership checks |
| `addCacheContexts($contexts)` | Custom cache contexts | `['url.path', 'languages']` |
| `addCacheTags($tags)` | Invalidate when entity changes | `$node->getCacheTags()` |
| `setCacheMaxAge($seconds)` | Time-based expiry | Time-sensitive access |
| `addCacheableDependency($object)` | Inherit another object's cacheability | Entities, config |

## Combining Results
```php
// AND logic: both must allow
$result1 = AccessResult::allowed();
$result2 = AccessResult::allowed();
$combined = $result1->andIf($result2); // allowed

// OR logic: either can allow
$result1 = AccessResult::neutral();
$result2 = AccessResult::allowed();
$combined = $result1->orIf($result2); // allowed

// Forbidden always wins
$result1 = AccessResult::allowed();
$result2 = AccessResult::forbidden();
$combined = $result1->orIf($result2); // forbidden
```

## Common Mistakes
- Returning `allowed()` without cache metadata -- Performance killer, check runs every request
- Using neutral when forbidden needed -- Access may leak if another check allows
- Not adding cacheability from checked entities -- Stale access when entity updates
- Chaining too many andIf/orIf -- Hard to debug; create separate check
- Forgetting that multiple requirements = AND -- Can't do OR in routing.yml, needs custom check

## See Also
- Reference: `/core/lib/Drupal/Core/Access/AccessResult.php`
- [Route Access Checks](route-access-checks.md) for usage context
- [Entity Access Control](entity-access-control.md) for entity-specific patterns
