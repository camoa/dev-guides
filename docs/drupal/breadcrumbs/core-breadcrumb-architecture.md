---
description: How BreadcrumbManager dispatches to builders — the chain, priority system, and cache metadata merging
tldr: "Read this before writing any custom builder or alter hook. The `BreadcrumbManager` is the chain dispatcher; every breadcrumb request routes through it."
drupal_version: "11.x"
---

# Core Breadcrumb Architecture

## When to Use

> Read this before writing any custom builder or alter hook. The `BreadcrumbManager` is the chain dispatcher; every breadcrumb request routes through it.

## Decision

| Component | Role | Key method |
|---|---|---|
| `BreadcrumbBuilderInterface` | Contract all builders implement | `applies()`, `build()` |
| `BreadcrumbManager` | Chain dispatcher, sorted by priority | `build()` calls `getSortedBuilders()`, iterates, takes first `applies() === TRUE` |
| `Breadcrumb` | Value object: links + cache metadata | `addLink()`, `addCacheContexts()`, `addCacheableDependency()` |
| `BreadcrumbPreprocess` | Template preprocessor | Converts `Link` objects to `[text, url]` arrays for Twig |
| `hook_system_breadcrumb_alter` | Post-build hook | Fires after winning builder; receives `Breadcrumb`, `RouteMatchInterface`, `$context` |

## Pattern

```php
// BreadcrumbManager::build() — simplified
$cacheable_metadata = new CacheableMetadata();
$breadcrumb = new Breadcrumb();
foreach ($this->getSortedBuilders() as $builder) {
  if (!$builder->applies($route_match, $cacheable_metadata)) {
    continue;
  }
  $breadcrumb = $builder->build($route_match);
  $context['builder'] = $builder;
  break;
}
$breadcrumb->addCacheableDependency($cacheable_metadata); // merge applies() metadata
$this->moduleHandler->alter('system_breadcrumb', $breadcrumb, $route_match, $context);
return $breadcrumb;
```

Key behaviors:
- `Breadcrumb` uses `RefinableCacheableDependencyTrait` — cacheability added in `applies()` is automatically merged into the returned breadcrumb
- Builders are tagged with `breadcrumb_builder` in `*.services.yml`; the `RegisterBreadcrumbBuilderPass` compiler pass collects them by priority
- Higher priority number = checked first; only the first `applies() === TRUE` builder's `build()` is called

## Common Mistakes

- **Wrong**: Adding cache metadata in both `applies()` and `build()` → **Right**: `applies()` metadata is merged automatically; double-adding is redundant but harmless
- **Wrong**: Returning `NULL` from `build()` → **Right**: Always return a `Breadcrumb` instance; the manager throws `UnexpectedValueException` on `NULL`
- **Wrong**: Assuming all builders run → **Right**: Only the winning builder's `build()` is called; all other builders only have `applies()` checked

## See Also

- [Core Breadcrumb Builders](core-breadcrumb-builders.md)
- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Reference: `core/lib/Drupal/Core/Breadcrumb/BreadcrumbManager.php`
- Reference: `core/lib/Drupal/Core/Breadcrumb/Breadcrumb.php`
