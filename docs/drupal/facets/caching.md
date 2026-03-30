---
description: Facets caching — facets_filter cache context, FacetManager in-memory cache, block cache, and debug mode
drupal_version: "11.x"
---

# Caching

## When to Use

> Use this guide when you need to understand or debug facet caching behavior, or when facets show stale data or wrong results after caching.

## Decision

| Component | Cache Mechanism | Purpose |
|---|---|---|
| Facet results | Cache metadata on render array | Vary by facet parameters |
| FacetManager | In-memory request cache | Prevent duplicate processing |
| Facet blocks | Block cache with facet context | Vary by active facet state |
| Config entities | Config cache | Facet/source configuration |

**`facets_filter` cache context** — A custom cache context that varies caching by active facet filter parameters. Ensures different filter combinations get different cached responses.

## Pattern

**Debug mode** — Enable cache metadata output in facet templates:

```php
// In settings.php or settings.local.php:
$settings['facets_debug_cacheable_metadata'] = TRUE;
```

This adds HTML comments to facet templates:
```html
<!-- cache_hash: abc123 -->
<!-- cache_contexts: facets_filter, url.query_args -->
<!-- cache_tags: config:facets.facet.category, search_api_list:index -->
<!-- cache_max_age: -1 -->
```

## Common Mistakes

- **Wrong**: Using block-based facets with Views cache enabled → **Right**: Block-based facets don't work with Views cache. Disable Views caching or switch to the exposed filters approach.
- **Wrong**: Stale facet counts after content changes → **Right**: If counts don't update after content changes, clear the search index cache and reindex (`drush sapi-r`).
- **Wrong**: Facets showing the same results regardless of selections → **Right**: The `facets_filter` cache context may not be applied. Check the block/View cache settings.

## See Also

- [Events](events.md) — cache-related events
- [Facets Exposed Filters](facets-exposed-filters.md) — better caching with exposed filters
