---
description: Write a custom BreadcrumbBuilderInterface implementation — applies(), build(), service registration, and priority guidance
tldr: "Use a custom builder when breadcrumbs must be driven by entity relationships (not URL structure), or when you need different logic for specific routes. Use `hook_system_breadcrumb_alter()` instead for minor adjustments."
drupal_version: "11.x"
---

# Custom Breadcrumb Builder

## When to Use

> Use a custom builder when breadcrumbs must be driven by entity relationships (not URL structure), or when you need different logic for specific routes. Use `hook_system_breadcrumb_alter()` instead for minor adjustments.

## Decision

| In `applies()`... | Do... | Because... |
|---|---|---|
| Check route name | `$route_match->getRouteName() === 'entity.node.canonical'` | Cheapest check; do this first |
| Check a route parameter type | `$node instanceof NodeInterface` | Verify the parameter before accessing it |
| Check a route parameter value | `$node->bundle() === 'article'` | Use the already-loaded param converter entity |
| Add cache context | `$cacheable_metadata?->addCacheContexts(['route'])` | Vary cache by route so this result is not reused across routes |

**Priority guidance:**

| Priority range | Use |
|---|---|
| 1–99 | Minor overrides, before core builders |
| 100–999 | Standard custom builders |
| 1000–1002 | Run before Easy Breadcrumb for specific routes |
| 1003+ | Only to override Easy Breadcrumb for all routes |

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
    return $breadcrumb;
  }
}
```

Service registration in `my_module.services.yml`:

```yaml
services:
  my_module.article_breadcrumb_builder:
    class: Drupal\my_module\Breadcrumb\ArticleBreadcrumbBuilder
    arguments: ['@entity_type.manager', '@current_user', '@access_manager']
    tags:
      - { name: breadcrumb_builder, priority: 100 }
```

## Common Mistakes

- **Wrong**: `public function applies(RouteMatchInterface $route_match): bool` → **Right**: Declare `?CacheableMetadata $cacheable_metadata = NULL` as the second parameter (Drupal 11.x signature; required for Drupal 12 compatibility)
- **Wrong**: Not calling `$cacheable_metadata?->addCacheContexts(['route'])` in `applies()` → **Right**: Without it, `BreadcrumbManager` may reuse the wrong builder result across routes
- **Wrong**: Adding entity cache tags in `applies()` but skipping `addCacheableDependency($entity)` in `build()` → **Right**: `applies()` metadata is merged in, but entities loaded in `build()` must be added there
- **Wrong**: Returning a truthy non-`TRUE` value from `applies()` → **Right**: Return type is `bool`; return `TRUE` or `FALSE` explicitly

## See Also

- [Altering Breadcrumbs](altering-breadcrumbs.md)
- [Caching](caching.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbBuilderInterface.php`
- Reference: `core/modules/taxonomy/src/TermBreadcrumbBuilder.php` (real-world example)
