---
description: Breadcrumb cache metadata — contexts, tags, applies() merging, and Drupal 12 signature changes
tldr: "Breadcrumbs render via BigPipe (the `SystemBreadcrumbBlock` uses `createPlaceholder(): true`). Cache metadata on the `Breadcrumb` object directly controls invalidation."
drupal_version: "11.x"
---

# Caching

## When to Use

> Breadcrumbs are rendered inside the `SystemBreadcrumbBlock`, which uses `createPlaceholder(): true` — meaning the block renders via BigPipe as a placeholder that resolves after the initial page response. Cache metadata on the `Breadcrumb` object directly controls invalidation.

## Decision

| Cache concern | Mechanism | How to apply |
|---|---|---|
| Vary by current URL path | `url.path.parent` context | Core does this automatically; add it in your builder |
| Vary by whether on front page | `url.path.is_front` context | Core does this automatically |
| Vary by route (for route-specific builders) | `route` context | Add in both `applies()` and `build()` (legacy) or just `applies()` (Drupal 12+) |
| Invalidate when node changes | Entity cache tag (`node:42`) | `$breadcrumb->addCacheableDependency($node)` |
| Invalidate when config changes | Config cache tag | `$breadcrumb->addCacheableDependency($config)` |
| Vary by user (access checks) | `addCacheableDependency($access)` | `PathBasedBreadcrumbBuilder` does this per segment |
| Vary by language | `languages` context | Easy Breadcrumb adds this; add it in multilingual custom builders |
| Never cache | `max-age: 0` | `$breadcrumb->mergeCacheMaxAge(0)` — use only when unavoidable |

## Pattern

The `Breadcrumb` class extends `RefinableCacheableDependencyTrait`. All three cache metadata properties are available:

```php
$breadcrumb = new Breadcrumb();

// Cache contexts — who/what makes the output vary
$breadcrumb->addCacheContexts(['route', 'url.path.parent', 'languages']);

// Cache tags — what entity changes invalidate this
$breadcrumb->addCacheableDependency($node);   // adds node:NID tag
$breadcrumb->addCacheableDependency($config); // adds config:name tag

// Access result — varies output AND invalidates when access policies change
$access = $this->accessManager->check($route_match, $this->currentUser, NULL, TRUE);
$breadcrumb->addCacheableDependency($access);
```

**`applies()` metadata merging:** Starting in Drupal 10.4, the `BreadcrumbManager` collects a shared `CacheableMetadata` object and passes it to each builder's `applies()` call. After the winning builder runs, the shared metadata is merged into the returned `Breadcrumb`. This means:
- Add to `$cacheable_metadata` in `applies()` anything the applicability check depends on
- The `build()` method automatically inherits this; do not double-add it

**Drupal 12 signature change (issue #3459277):** The `applies()` signature will become:
```php
public function applies(RouteMatchInterface $route_match, CacheableMetadata $cacheable_metadata): bool;
```
The parameter will be mandatory (not optional). Current best practice: always use the null-safe operator `$cacheable_metadata?->addCacheContexts(...)` for forward compatibility.

**Easy Breadcrumb cache contexts:** The module adds `['route', 'url.path', 'languages']` and also adds the module config as a cacheable dependency — so any config change clears all its breadcrumb caches.

## Common Mistakes

- Omitting `url.path.parent` in a custom builder — the same builder result gets served for all paths, causing wrong breadcrumbs on unrelated pages
- Not adding entity dependencies — if a node title changes, the cached breadcrumb still shows the old title; `addCacheableDependency($node)` ensures invalidation
- Using `max-age: 0` because "breadcrumbs are complex" — this breaks Drupal's render cache for the entire block; use proper cache contexts/tags instead
- Missing the `languages` cache context on multilingual sites — the same crumb is served for all languages

## See Also

- Custom builder cache setup → [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Block uses BigPipe → [Block Placement](block-placement.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/Breadcrumb.php`
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbManager.php`
