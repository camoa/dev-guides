---
description: Search API query performance — MySQL InnoDB COUNT problem, Highlight latency, mini pager, Solr index-only mode, and cache warming
tldr: "Use this when optimizing search query speed and reducing server load."
drupal_version: "11.x"
---

# Query Performance

## When to Use

> Use this when optimizing search query speed and reducing server load.

## Decision

| Strategy | Impact | Applies To |
|---|---|---|
| Whole words only matching | Significant speedup | Database backend |
| Skip result count query | Major speedup on MySQL InnoDB | Database backend |
| Mini pager | Avoids COUNT query | All backends |
| Skip entity loads (Solr index-only) | Eliminates DB queries | Solr backend |
| Highlight processor skip | 10x latency reduction | All backends |
| Cache warming | Faster repeated queries | All backends |

## Pattern

**MySQL InnoDB COUNT problem** — InnoDB COUNT queries are extremely slow on large tables:
1. Use **Mini pager** in Views instead of Full pager — Mini pager doesn't need total count
2. Enable **"Skip result count query"** in Views query settings

**Highlight processor latency** — can add 10x latency on complex queries:
```php
// Skip highlighting for specific queries
$query->addTag('search_api_skip_processor_highlight');
```

**Solr index-only mode** — for maximum query performance:
1. Server config → Enable "Retrieve result data from Solr"
2. Views query settings → Enable "Skip item access checks" (only for fully public content)
3. Ensure all displayed fields are in the Search API index
4. Result: Solr returns field data directly — no database queries for entity loading

## Common Mistakes

- **Wrong**: Using AJAX on search results Views → **Right**: Breaks unique URLs, harms UX and analytics. Does not improve performance.
- **Wrong**: "Partial matching" on DB backend → **Right**: Much slower than "Whole words only." Only use partial if required.
- **Wrong**: Using "Skip item access checks" on restricted sites → **Right**: This bypasses all access control. Restricted content becomes visible.

## See Also

- [Indexing Performance](indexing-performance.md)
- [Solr Best Practices](solr-best-practices.md)
- [Content Access & Security](content-access-security.md)
