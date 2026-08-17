---
description: "Facet cache architecture — the facets_filter cache context, debug mode, and common cache-related failure modes"
tldr: "Use this guide when you need to understand or debug facet caching behavior, or when facets show stale data or wrong results after caching. The facets_filter cache context varies by active filter parameters."
drupal_version: "11.x"
---

# Caching

## When to Use

> When you need to understand or debug facet caching behavior, or when facets show stale data.

## Decision

| Component | Cache Mechanism | Purpose |
|---|---|---|
| Facet results | Cache metadata on render array | Vary by facet parameters |
| FacetManager | In-memory request cache | Prevent duplicate processing |
| Facet blocks | Block cache with facet context | Vary by active facet state |
| Config entities | Config cache | Facet/source configuration |

`facets_filter` is a custom cache context that varies caching by active facet filter parameters, ensuring different filter combinations get different cached responses.

## Pattern

Enable debug output in facet templates:

```php
// In settings.php or settings.local.php:
$settings['facets_debug_cacheable_metadata'] = TRUE;
```

This adds cache metadata as HTML comments in facet templates:

```html
<!-- cache_hash: abc123 -->
<!-- cache_contexts: facets_filter, url.query_args -->
<!-- cache_tags: config:facets.facet.category, search_api_list:index -->
<!-- cache_max_age: -1 -->
```

## Common Mistakes

- **Wrong**: Leaving Views caching enabled on block-based facets → **Right**: Block-based facets don't work with Views cache. Disable Views caching or use the exposed filters approach.
- **Wrong**: Assuming counts are wrong forever after content changes → **Right**: If counts don't update, clear the search index cache and reindex.
- **Wrong**: Ignoring identical results across different selections → **Right**: If facets show the same results regardless of selections, the `facets_filter` cache context may be missing — check block/View cache settings.

## See Also

- [Events](events.md) — cache-related events
- [Facets Exposed Filters](facets-exposed-filters.md) — better caching with exposed filters
