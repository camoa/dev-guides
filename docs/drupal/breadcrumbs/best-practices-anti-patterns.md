---
description: Security, performance, and development standards for Drupal breadcrumbs — access checks, entity loading, caching, and injection patterns
drupal_version: "11.x"
---

# Best Practices & Anti-Patterns

## When to Use

> Read this before writing any breadcrumb-related code. These are the patterns that cause production issues and the ones that solve them.

## Decision

| Concern | Anti-pattern | Correct pattern |
|---|---|---|
| XSS in titles | `new Link(Markup::create('<b>' . $node->getTitle() . '</b>'), $url)` | `new Link($node->getTitle(), $url)` — Twig escapes it |
| Access bypass | Custom builder creates links without checking access | Replicate `$this->accessManager->check()` per segment |
| Entity loading in `applies()` | `\Drupal::entityTypeManager()->getStorage('node')->load($nid)` | `$route_match->getParameter('node')` — param converter already loaded it |
| Static calls in a builder | `\Drupal::service(...)` in constructor logic | Inject services via `arguments:` in the service definition |
| Empty breadcrumb with no contexts | `return new Breadcrumb();` | Always add `addCacheContexts(['route'])` before returning |
| Priority collision | Priority 0 custom builder alongside `PathBasedBreadcrumbBuilder` | Use priority 1+ to guarantee ordering |

## Pattern

**Access check in custom builders:**
```php
$access = $this->accessManager->check($route_match, $this->currentUser, NULL, TRUE);
$breadcrumb->addCacheableDependency($access);
if ($access->isAllowed()) {
  $links[] = new Link($title, $url);
}
```

**Proper service injection:**
```yaml
# my_module.services.yml
services:
  my_module.product_breadcrumb:
    class: Drupal\my_module\Breadcrumb\ProductBreadcrumbBuilder
    arguments: ['@entity_type.manager', '@current_user', '@access_manager']
    tags:
      - { name: breadcrumb_builder, priority: 200 }
```

**Safe empty breadcrumb return:**
```php
$breadcrumb = new Breadcrumb();
$breadcrumb->addCacheContexts(['route']);
return $breadcrumb;
```

## Common Mistakes

- **Wrong**: Priority 0 custom builder that should run before `PathBasedBreadcrumbBuilder` → **Right**: Both are priority 0; use 1+ to guarantee ordering
- **Wrong**: `applies(RouteMatchInterface $route_match): bool` without the nullable `CacheableMetadata` parameter → **Right**: Declare `?CacheableMetadata $cacheable_metadata = NULL`; crashes on Drupal 10.4+ otherwise
- **Wrong**: Assuming `hook_system_breadcrumb_alter()` changes are reflected in Easy Breadcrumb's JSON-LD → **Right**: `EasyBreadcrumbStructuredDataJsonLd` calls `moduleHandler->alter()` itself, so the alter does run — but it is a separate call; verify behavior if you have both
- **Wrong**: Calling `$block->build()` in `hook_page_attachments` → **Right**: Renders the block outside the render pipeline and discards cache metadata

## When Not to Use Breadcrumbs

- Single-level sites (Home → page only) — the breadcrumb just shows "Home"; disable via `hide_single_home_item`
- Search results or Views with filters — breadcrumbs would show the filter path, which is meaningless to users
- Modal or AJAX-loaded content — breadcrumbs should reflect page hierarchy, not partial content state

## See Also

- [Caching](caching.md)
- [Core Breadcrumb Architecture](core-breadcrumb-architecture.md)
- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
