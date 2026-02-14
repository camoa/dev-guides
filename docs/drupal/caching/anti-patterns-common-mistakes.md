---
description: Avoid common caching mistakes that cause bugs, stale content, and performance issues
---

# Anti-Patterns & Common Mistakes

## When to Use

When you need to avoid common caching mistakes that cause bugs, performance issues, or stale content.

## Decision

| Anti-pattern | Why it's wrong | Do this instead |
|---|---|---|
| Using `Cache::PERMANENT` without cache tags | Content never invalidates when source changes | Add cache tags for source data |
| Using `user` context for role-based content | Creates per-user cache entries (huge cache) | Use `user.roles` or `user.permissions:{permission}` |
| Manually copying cache metadata between arrays | Renderer does this automatically via bubbling | Let bubbling handle metadata propagation |
| Using `deleteAll()` to fix cache issues | Clears valid entries, expensive operation | Use targeted cache tag invalidation |
| Forgetting cache metadata on render arrays | Serves stale content, incorrect variations | Always set tags, contexts, max-age |
| Adding same tags on parent and child | Unnecessary duplication, metadata bubbles | Set tags on children only |
| Using per-request cache tags | Tags not reusable, cache never hits | Use reusable tags (entity ID, config name) |
| Storing objects in cache bins | Serialization overhead, version incompatibility | Store simple data structures |
| Not using DI for cache bins | Static calls harder to test, less flexible | Inject CacheBackendInterface via DI |
| Creating too many lazy builders | Each placeholder adds overhead | Use sparingly (2-5 per page) |

## Pattern

**Wrong: Manual metadata copying**
```php
// DON'T DO THIS
$child = ['#cache' => ['tags' => ['node:123']]];
$parent = [
  'child' => $child,
  '#cache' => ['tags' => ['node:123']],  // Duplicated, unnecessary
];
```

**Right: Let bubbling handle it**
```php
// DO THIS
$child = ['#cache' => ['tags' => ['node:123']]];
$parent = [
  'child' => $child,
  // Tags bubble automatically from child
];
```

**Wrong: Clearing entire bin**
```php
// DON'T DO THIS
\Drupal::cache('render')->deleteAll();  // Clears ALL render cache
```

**Right: Targeted tag invalidation**
```php
// DO THIS
\Drupal::service('cache_tags.invalidator')
  ->invalidateTags(['node:123']);  // Only clears affected entries
```

**Wrong: Per-user context for role-based content**
```php
// DON'T DO THIS
'contexts' => ['user']  // Separate cache per user
```

**Right: Role-based context**
```php
// DO THIS
'contexts' => ['user.roles']  // One cache per role combination
```

Reference: [Common caching mistakes](https://www.drupal.org/docs/drupal-apis/cache-api/cache-api#common-mistakes)

## Common Mistakes

- Over-caching with `Cache::PERMANENT` — Causes stale content; use appropriate max-age or rely on tags
- Under-caching with max-age 0 — Makes everything uncacheable; use placeholders for variable parts
- Not understanding cache context cardinality — `user` context creates thousands of cache entries
- Testing only as admin — Admin bypasses Page Cache and has different permissions; test as anonymous and authenticated

## See Also

- [Best Practices & Patterns](best-practices-patterns.md) — What to do instead
- [Security & Performance](security-performance.md) — Security implications of caching
