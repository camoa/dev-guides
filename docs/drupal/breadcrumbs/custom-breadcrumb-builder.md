---
description: Write a custom BreadcrumbBuilderInterface implementation — applies(), build(), service registration, and priority guidance
tldr: "Use a custom builder when breadcrumbs must be driven by entity relationships (not URL structure), or when you need different logic for specific routes. Use `hook_system_breadcrumb_alter()` instead for minor adjustments."
drupal_version: "11.x"
---

# Custom Breadcrumb Builder

## When to Use

> Write a custom builder when:
> - You need breadcrumbs driven by entity relationships, not URL structure (e.g., a product variant always gets the parent product + category in the trail)
> - You need different breadcrumb logic for specific routes (e.g., a content type's canonical route)
> - Easy Breadcrumb's configuration cannot express your requirements
>
> Do NOT write a custom builder for minor adjustments — use `hook_system_breadcrumb_alter()` instead.

## Steps

1. **Create the builder class** — implement `BreadcrumbBuilderInterface` in `src/Breadcrumb/`

2. **Implement `applies()`** — check the route name and/or route parameters; add cache metadata for anything the check depends on

3. **Implement `build()`** — create links, add all cache metadata (entity tags, user-dependent contexts)

4. **Register as a service** with the `breadcrumb_builder` tag and a priority > 0

## Pattern

```php
namespace Drupal\my_module\Breadcrumb;

use Drupal\Core\Breadcrumb\Breadcrumb;
use Drupal\Core\Breadcrumb\BreadcrumbBuilderInterface;
use Drupal\Core\Cache\CacheableMetadata;
use Drupal\Core\Link;
use Drupal\Core\Routing\RouteMatchInterface;
use Drupal\node\NodeInterface;

class ArticleBreadcrumbBuilder implements BreadcrumbBuilderInterface {

  public function applies(RouteMatchInterface $route_match, ?CacheableMetadata $cacheable_metadata = NULL): bool {
    $cacheable_metadata?->addCacheContexts(['route']);
    $node = $route_match->getParameter('node');
    return $route_match->getRouteName() === 'entity.node.canonical'
      && $node instanceof NodeInterface
      && $node->bundle() === 'article';
  }

  public function build(RouteMatchInterface $route_match): Breadcrumb {
    $breadcrumb = new Breadcrumb();
    $node = $route_match->getParameter('node');
    $breadcrumb->addCacheableDependency($node);
    $breadcrumb->addCacheContexts(['route']);

    $breadcrumb->addLink(Link::createFromRoute($this->t('Home'), '<front>'));
    $breadcrumb->addLink(Link::createFromRoute($this->t('News'), 'view.news.page_1'));
    // Do not add current page — it is not a convention to link the current page
    return $breadcrumb;
  }
}
```

Service registration in `my_module.services.yml`:

```yaml
services:
  my_module.article_breadcrumb_builder:
    class: Drupal\my_module\Breadcrumb\ArticleBreadcrumbBuilder
    tags:
      - { name: breadcrumb_builder, priority: 100 }
```

**Priority guidance:**
- Priority 1–99: minor overrides, runs before core builders
- Priority 100–999: standard custom builders
- Priority 1000–1002: run before Easy Breadcrumb; use to handle routes Easy Breadcrumb would otherwise win
- Priority 1003+: only if intentionally overriding Easy Breadcrumb for all routes

**Autowiring:** If your builder depends on services, use constructor injection with type hints. The container resolves them automatically in Drupal 10+.

## Decision Points

| In `applies()`... | Do... | Because... |
|---|---|---|
| Check route name | `$route_match->getRouteName() === 'entity.node.canonical'` | Cheapest check; do this first |
| Check a route parameter type | `$node instanceof NodeInterface` | Verify the parameter before accessing it |
| Check a route parameter value | `$node->bundle() === 'article'` | Load as little as possible; use the already-loaded param |
| Add cache context | `$cacheable_metadata?->addCacheContexts(['route'])` | Vary cache by route so this result is not reused across routes |

## Common Mistakes

- Forgetting `?` in `?CacheableMetadata $cacheable_metadata = NULL` — this is the current Drupal 11.x signature; required for forward compatibility with Drupal 12
- Not calling `$cacheable_metadata?->addCacheContexts(['route'])` in `applies()` — the `BreadcrumbManager` will reuse the wrong builder across routes
- Adding entity cache tags in `applies()` but not `addCacheableDependency($entity)` in `build()` — tags from `applies()` metadata are merged in, but entity-loaded-in-build dependencies must be added there
- Returning a truthy value other than `TRUE` from `applies()` — the return type is `bool`, not `mixed`

## See Also

- After-build alterations → [Altering Breadcrumbs](altering-breadcrumbs.md)
- Cache metadata details → [Caching](caching.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbBuilderInterface.php`
- Reference: `core/modules/taxonomy/src/TermBreadcrumbBuilder.php` (real-world example)
