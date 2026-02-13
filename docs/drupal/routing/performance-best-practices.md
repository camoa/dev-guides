---
description: Drupal routing performance - optimize route definitions, access checks, and dynamic route generation
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

> Use when routes are high-traffic, when using dynamic routes or custom access checkers, or when routes load significant data. Performance issues in routing affect every page load.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Static routes | YAML definitions | Parsed once, cached efficiently |
| Dynamic routes | `route_callbacks` with caching | Only regenerated when needed |
| Custom access checks | AccessResult with cache metadata | Prevents redundant access checks |
| Heavy data loading | Lazy loading in controller | Don't load data for access checks |
| Route-specific caching | Cache contexts/tags in access checks | Granular cache invalidation |

## Pattern

```php
// Custom access checker with proper caching
public function access(AccountInterface $account) {
  if ($this->performExpensiveCheck($account)) {
    return AccessResult::allowed()
      ->cachePerPermissions()  // Cache by permission changes
      ->cachePerUser();  // Cache per user
  }

  return AccessResult::forbidden()
    ->cachePerPermissions()
    ->cachePerUser();
}

// Route callback with caching
public function routes() {
  $cid = 'my_module:dynamic_routes';
  if ($cache = $this->cacheBackend->get($cid)) {
    return $cache->data;
  }

  $routes = $this->generateRoutes();
  $this->cacheBackend->set($cid, $routes, Cache::PERMANENT, ['my_module_routes']);
  return $routes;
}
```

## Performance Principles

### 1. Route Definition Performance

- Prefer static YAML routes - fastest, cached in compiled route table
- Use dynamic routes sparingly - overhead on route rebuild
- Limit total number of routes - router scales with route count
- Avoid complex regex in parameter validation - every request evaluates regex

### 2. Access Check Performance (CRITICAL)

- ALWAYS add cache metadata to custom AccessResult - without it, access checks run on EVERY request
- Use appropriate cache contexts (permissions, user, roles) - prevents stale access decisions
- Don't load entities in access checks - load in controller after access granted
- Layer cheap checks before expensive ones - fail fast on permission check before complex logic

### 3. Dynamic Route Performance

- Cache expensive route generation - don't rebuild routes on every request
- Use appropriate cache tags - invalidate only when source data changes
- Minimize routes generated dynamically - consider config entities with static routes
- Profile route generation time - if >100ms, optimize or reconsider approach

### 4. Controller Performance

- Don't load data until access granted - access checks run first, controller second
- Use lazy builders for expensive components - render arrays support lazy building
- Leverage entity query caching - entity queries cache automatically
- Consider BigPipe for slow components - render shell first, stream slow parts

## Common Mistakes

- **Wrong**: Custom access checks without cache metadata → **Right**: Add `->cachePerPermissions()` or equivalent
- **Wrong**: Loading entities in access checks → **Right**: Load in controller after access granted
- **Wrong**: Generating hundreds of dynamic routes → **Right**: Limit routes, consider alternatives
- **Wrong**: Complex regex in parameter requirements → **Right**: Use simple patterns, validate in code
- **Wrong**: Not profiling routing performance → **Right**: Profile and optimize before production
- **Wrong**: Dynamic routes without caching → **Right**: Cache route collections appropriately

## See Also

- [Security Best Practices](security-best-practices.md)
- Reference: Drupal caching documentation
- Reference: Core access check implementations in `core/lib/Drupal/Core/Access/`
