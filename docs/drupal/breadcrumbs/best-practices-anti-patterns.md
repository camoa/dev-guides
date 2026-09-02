---
description: Security, performance, and development standards for Drupal breadcrumbs — access checks, entity loading, caching, and injection patterns
tldr: "Read this before writing any breadcrumb-related code. These are the patterns that cause production issues and the ones that solve them."
drupal_version: "11.x"
---

# Best Practices & Anti-Patterns

## When to Use

> Read this section before writing any breadcrumb-related code. These are the patterns that cause production issues and the ones that solve them.

## Security

**XSS in breadcrumb titles:** All text rendered through core's `Breadcrumb` + `BreadcrumbPreprocess` pipeline is automatically escaped via Twig's auto-escaping. The `EasyBreadcrumbBuilder` explicitly uses `Xss::filter()` on custom path titles and `Html::decodeEntities()` on resolved titles. Never bypass this by rendering raw HTML in a builder.

**Unsafe pattern:**
```php
// WRONG — raw HTML in a Link label
$links[] = new Link(Markup::create('<b>' . $node->getTitle() . '</b>'), $url);
```

**Safe pattern:**
```php
// CORRECT — plain text; Twig escapes it
$links[] = new Link($node->getTitle(), $url);
```

**Access bypass:** The `PathBasedBreadcrumbBuilder` checks access for each segment. Custom builders MUST replicate this. Never create links to paths the current user cannot access — that is an information disclosure vulnerability.

```php
$access = $this->accessManager->check($route_match, $this->currentUser, NULL, TRUE);
$breadcrumb->addCacheableDependency($access);
if ($access->isAllowed()) {
  $links[] = new Link($title, $url);
}
```

## Performance

**Builders run on every page request** (unless cached). Keep `applies()` cheap — check the route name string first, then check parameter types. Avoid database queries or entity loads in `applies()`.

**The entity load trap:** Never load an entity by ID in `applies()` when you can get it from the route parameters:
```php
// WRONG — loads entity unnecessarily
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);

// CORRECT — entity is already loaded by the param converter
$node = $route_match->getParameter('node');
```

**Custom path matching in Easy Breadcrumb** has O(n) cost for n configured custom paths — each path is checked via `preg_match()`. If you have 50+ custom paths, consider a custom builder with route-based routing instead of regex matching.

**`max-age: 0` kills page caching.** When a breadcrumb uses `max-age: 0`, the entire block cannot be cached. The BigPipe placeholder still renders every request. On high-traffic pages, use proper cache contexts/tags.

## Development Standards

**Use `RefinableCacheableDependencyInterface`** — `Breadcrumb` implements this, so call `addCacheableDependency()` for any entity, config, or access object the breadcrumb depends on. Do not manually pull tag/context strings from entities.

**Never use `\Drupal::` static calls in a builder** — inject services via the constructor. Breadcrumb builders are service-registered; static calls break testability and make swapping services impossible.

**Proper injection for a builder:**
```yaml
# my_module.services.yml
services:
  my_module.product_breadcrumb:
    class: Drupal\my_module\Breadcrumb\ProductBreadcrumbBuilder
    arguments: ['@entity_type.manager', '@current_user', '@access_manager']
    tags:
      - { name: breadcrumb_builder, priority: 200 }
```

**Avoid returning an empty breadcrumb with no cache contexts** — if your builder returns a `new Breadcrumb()` with no links and no cache metadata, the empty result is cached globally and may show on unrelated pages:
```php
// WRONG — returns empty breadcrumb, may be cached across routes
return new Breadcrumb();

// CORRECT — add contexts before returning empty
$breadcrumb = new Breadcrumb();
$breadcrumb->addCacheContexts(['route']);
return $breadcrumb;
```

## When Not to Use Breadcrumbs

Breadcrumbs are navigation tools for hierarchical structures. They are inappropriate for:
- Single-level sites (home → page only) — the breadcrumb just shows "Home"; disable via `hide_single_home_item` in Easy Breadcrumb
- User-generated path browsing (search results, Views with filters) — breadcrumbs would show the search path, which is meaningless
- Modal or AJAX-loaded content — breadcrumbs should reflect page hierarchy, not partial content state

## Common Mistakes

- **Wrong priority** — setting priority to 0 in a custom builder that should run before `PathBasedBreadcrumbBuilder` (also 0). Use priority 1+ to guarantee ordering
- **Not verifying the `$cacheable_metadata` parameter is nullable** — older custom builders crash on Drupal 10.4+ because `applies()` now passes the metadata object; declare `?CacheableMetadata $cacheable_metadata = NULL`
- **Assuming Easy Breadcrumb's breadcrumb and the JSON-LD breadcrumb are always identical** — `EasyBreadcrumbStructuredDataJsonLd` calls `EasyBreadcrumbBuilder::build()` directly (bypassing `BreadcrumbManager`), so `hook_system_breadcrumb_alter()` modifications are NOT reflected in the JSON-LD output unless the hook is explicitly invoked (it is — the service calls `moduleHandler->alter()` itself)
- **Calling `block->build()` in `hook_page_attachments`** — this renders the block outside the render pipeline and discards its cache metadata

## See Also

- All cache patterns → [Caching](caching.md)
- Core architecture → [Core Breadcrumb Architecture](core-breadcrumb-architecture.md)
- Custom builder template → [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
