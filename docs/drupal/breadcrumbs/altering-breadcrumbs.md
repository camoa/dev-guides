---
description: Use hook_system_breadcrumb_alter to add, remove, or modify breadcrumb links after a builder runs
tldr: "Use `hook_system_breadcrumb_alter()` for low-overhead adjustments after a builder runs: inserting a segment, removing a specific link, adding cache tags/contexts. For complex logic involving entity loading or routing, write a custom…"
drupal_version: "11.x"
---

# Altering Breadcrumbs

## When to Use

> Use `hook_system_breadcrumb_alter()` for low-overhead adjustments that apply after a builder runs. Good for: inserting a segment between existing links, removing a specific segment on certain routes, adding extra cache tags/contexts. For complex logic involving entity loading or routing, write a custom builder instead.

## Decision

| Situation | Approach |
|---|---|
| Remove a specific home link | `hook_system_breadcrumb_alter()` — modify `$breadcrumb->getLinks()` |
| Add one extra link at the end | `hook_system_breadcrumb_alter()` — `$breadcrumb->addLink()` |
| Build completely different trail based on entity type | Custom builder — the alter hook is not the place for routing logic |
| Know which builder won | `$context['builder']` is the winning builder instance |

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
  // Add cache context for any variation introduced by this alter.
  $breadcrumb->addCacheContexts(['route']);

  $links = $breadcrumb->getLinks();
  // Insert a "Blog" link after "Home".
  if (count($links) > 1) {
    array_splice($links, 1, 0, [Link::createFromRoute('Blog', 'view.blog.page_1')]);
    // Must rebuild — setLinks() throws if already set, use the internal pattern.
  }
}
```

**Important:** `Breadcrumb::setLinks()` throws `LogicException` if links were already set (prevents overwriting). To modify the links array, you must add individual links via `addLink()` or work with a new breadcrumb. The safe pattern for insertion is to build a new `Breadcrumb` with the modified links:

```php
function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  $breadcrumb->addCacheContexts(['route']);
  $breadcrumb->addLink(Link::createFromRoute('Section', 'my_route'));
  // addLink() is always safe — appends to the end.
}
```

## Common Mistakes

- Calling `$breadcrumb->setLinks()` in the alter hook — it throws if links exist; use `addLink()` or replace `$breadcrumb` entirely with a fresh one
- Not adding cache metadata in the alter — if your alter varies by user role, add `user.roles` context; if it depends on a config, add `addCacheableDependency($config)`
- Using the alter for expensive operations (entity queries, database lookups) — this runs on every page load; put expensive logic in a builder where it can be properly cached and separated by route

## See Also

- Writing a full builder → [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Cache metadata → [Caching](caching.md)
- Reference: `core/lib/Drupal/Core/Menu/menu.api.php` — `hook_system_breadcrumb_alter` docblock
- API docs: https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Menu!menu.api.php/function/hook_system_breadcrumb_alter
