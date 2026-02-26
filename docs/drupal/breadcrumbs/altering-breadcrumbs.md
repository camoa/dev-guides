---
description: Use hook_system_breadcrumb_alter to add, remove, or modify breadcrumb links after a builder runs
drupal_version: "11.x"
---

# Altering Breadcrumbs

## When to Use

> Use `hook_system_breadcrumb_alter()` for low-overhead adjustments after a builder runs: inserting a segment, removing a specific link, adding cache tags/contexts. For complex logic involving entity loading or routing, write a custom builder instead.

## Decision

| Situation | Approach |
|---|---|
| Remove a specific home link | `hook_system_breadcrumb_alter()` — filter `$breadcrumb->getLinks()` |
| Add one extra link at the end | `hook_system_breadcrumb_alter()` — `$breadcrumb->addLink()` |
| Build completely different trail based on entity type | Custom builder — the alter hook is not the place for routing logic |
| Know which builder won | `$context['builder']` is the winning builder instance |
| Clear the breadcrumb entirely | Replace `$breadcrumb` with a new empty `Breadcrumb` object |

## Pattern

```php
// my_module.module
use Drupal\Core\Breadcrumb\Breadcrumb;
use Drupal\Core\Link;
use Drupal\Core\Routing\RouteMatchInterface;

function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  if ($route_match->getRouteName() !== 'entity.node.canonical') {
    return;
  }
  // Always add cache context for any variation introduced by this alter.
  $breadcrumb->addCacheContexts(['route']);
  // addLink() is always safe — appends to the end.
  $breadcrumb->addLink(Link::createFromRoute('Section', 'my_route'));
}
```

**Clearing the breadcrumb entirely** — `setLinks()` throws `LogicException` if links are already set; replace the object instead:

```php
function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  if ($route_match->getRouteName() === 'commerce_checkout.form') {
    $breadcrumb = new Breadcrumb();
    $breadcrumb->addCacheContexts(['route']);
  }
}
```

## Common Mistakes

- **Wrong**: Calling `$breadcrumb->setLinks()` in the alter hook → **Right**: It throws `LogicException` if links exist; use `addLink()` to append or replace `$breadcrumb` with a fresh object
- **Wrong**: Not adding cache metadata in the alter → **Right**: If your alter varies by user role, add `user.roles` context; if it depends on config, add `addCacheableDependency($config)`
- **Wrong**: Using the alter for expensive operations like entity queries → **Right**: The alter runs on every page load; put expensive logic in a builder where it is cached per route

## See Also

- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- [Caching](caching.md)
- Reference: `core/lib/Drupal/Core/Menu/menu.api.php` — `hook_system_breadcrumb_alter` docblock
- API docs: https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Menu!menu.api.php/function/hook_system_breadcrumb_alter
