---
description: Ensure cache security against data leakage and optimize cache performance
---

# Security & Performance

## When to Use

When you need to ensure cache security and optimal performance. Caching affects both security (sensitive data leakage) and performance (cache hit rates, memory usage).

## Decision

**Security Concerns**:

| Risk | How it happens | Prevention |
|---|---|---|
| Sensitive data in anonymous Page Cache | Missing `user` or `user.permissions` context | Add appropriate contexts for permission-gated content |
| CSRF tokens cached | Token in cached render array | Use lazy builder for forms/tokens |
| Access-controlled content served to wrong users | Missing cache contexts or tags | Add `user.permissions:{permission}` context |
| Cache poisoning via query parameters | Using `url.query_args` without sanitization | Sanitize query params before using in cache keys |

**Performance Concerns**:

| Issue | Cause | Solution |
|---|---|---|
| Low cache hit rate | Too many contexts, per-user caching | Minimize contexts; use `user.roles` not `user` |
| Large cache size | List tags, too many variations | Use specific entity tags; reduce context cardinality |
| Slow cache backend | Database backend on high-traffic site | Use Redis or Memcache |
| Cache stampede | Many requests rebuild same cache simultaneously | Use lock system or stale-while-revalidate pattern |
| Memory exhaustion | Redis/Memcache without eviction policy | Set `maxmemory` and `maxmemory-policy` |

## Pattern

**Access-controlled content**:
```php
// WRONG: No access context
$build = [
  '#markup' => $sensitive_content,
  '#cache' => ['tags' => ['node:123']],
];
// Served from cache to users without permission

// RIGHT: Add permission context
$build = [
  '#markup' => $sensitive_content,
  '#cache' => [
    'tags' => ['node:123'],
    'contexts' => ['user.permissions:access content'],
  ],
];
```

**CSRF tokens (uncacheable)**:
```php
// WRONG: Token in cached array
$build = [
  '#markup' => '<form><input name="token" value="' . $token . '">',
  '#cache' => ['keys' => ['my_form']],
];

// RIGHT: Use lazy builder for token
$build = [
  '#lazy_builder' => ['MyController::buildFormWithToken', []],
  '#create_placeholder' => TRUE,
];
```

**Cache stampede prevention**:
```php
use Drupal\Core\Lock\LockBackendInterface;

$lock = \Drupal::lock();
$data = $cache->get($cid);

if (!$data) {
  if ($lock->acquire($cid . '_rebuild')) {
    $data = expensive_calculation();
    $cache->set($cid, $data, $expire, $tags);
    $lock->release($cid . '_rebuild');
  }
  else {
    // Another request is rebuilding; wait or serve stale
    $lock->wait($cid . '_rebuild');
    $data = $cache->get($cid, TRUE);  // allow_invalid = TRUE
  }
}
```

Reference: [OWASP Caching Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

## Common Mistakes

- Caching user-specific data without `user` context — Data leaks to other users
- Not checking access before caching — Permission-gated content served from cache to unauthorized users
- Caching CSRF tokens — Makes forms vulnerable to CSRF attacks
- Not rate-limiting cache invalidation — Mass tag invalidation can cause DoS
- Storing passwords or session data in cache — Even with encryption, cache is not secure storage

## See Also

- [Cache Contexts](cache-contexts.md) — Security-relevant contexts
- [Best Practices & Patterns](best-practices-patterns.md) — Safe caching patterns
- Reference: [Drupal security best practices](https://www.drupal.org/security/secure-configuration)
