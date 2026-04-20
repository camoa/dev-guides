---
description: Breadcrumb cache metadata — contexts, tags, applies() merging, and Drupal 12 signature changes
tldr: "Breadcrumbs render via BigPipe (the `SystemBreadcrumbBlock` uses `createPlaceholder(): true`). Cache metadata on the `Breadcrumb` object directly controls invalidation."
drupal_version: "11.x"
---

# Caching

## When to Use

> Breadcrumbs render via BigPipe (the `SystemBreadcrumbBlock` uses `createPlaceholder(): true`). Cache metadata on the `Breadcrumb` object directly controls invalidation. Missing cache metadata causes wrong breadcrumbs served across routes or stale titles after content changes.

## Decision

| Cache concern | Mechanism | How to apply |
|---|---|---|
| Vary by current URL path | `url.path.parent` context | Core does this automatically; add it in your builder |
| Vary by route (route-specific builders) | `route` context | Add in `applies()` (Drupal 10.4+) or both `applies()` and `build()` (legacy) |
| Invalidate when node changes | Entity cache tag (`node:42`) | `$breadcrumb->addCacheableDependency($node)` |
| Invalidate when config changes | Config cache tag | `$breadcrumb->addCacheableDependency($config)` |
| Vary by user (access checks) | `addCacheableDependency($access)` | `PathBasedBreadcrumbBuilder` does this per segment |
| Vary by language | `languages` context | Easy Breadcrumb adds this; add it in multilingual custom builders |
| Never cache | `max-age: 0` | `$breadcrumb->mergeCacheMaxAge(0)` — avoid; breaks page caching |

## Pattern

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

**`applies()` metadata merging (Drupal 10.4+):** The `BreadcrumbManager` passes a shared `CacheableMetadata` object to each builder's `applies()`. After the winning builder runs, the shared metadata is merged into the returned `Breadcrumb`.
- Add to `$cacheable_metadata` in `applies()` anything the applicability check depends on
- `build()` automatically inherits this; do not double-add

**Drupal 12 signature change (issue #3459277):**
```php
// Future mandatory signature
public function applies(RouteMatchInterface $route_match, CacheableMetadata $cacheable_metadata): bool;
```
Current best practice: use the null-safe operator `$cacheable_metadata?->addCacheContexts(...)` for forward compatibility.

## Common Mistakes

- **Wrong**: Omitting `url.path.parent` in a custom builder → **Right**: The same cached result gets served for all paths; breadcrumbs appear wrong on unrelated pages
- **Wrong**: Not adding `addCacheableDependency($node)` → **Right**: When a node title changes, the cached breadcrumb still shows the old title
- **Wrong**: Using `max-age: 0` because "breadcrumbs are complex" → **Right**: This prevents the entire block from caching; use proper cache contexts/tags instead
- **Wrong**: Missing the `languages` cache context on multilingual sites → **Right**: The same crumb is served for all languages

## See Also

- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- [Block Placement](block-placement.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/Breadcrumb.php`
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbManager.php`
