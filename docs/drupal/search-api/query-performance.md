---
description: Search API query performance — MySQL InnoDB COUNT problem, Highlight latency, mini pager, Solr index-only mode, and cache warming
tldr: "Use this when optimizing search query speed and reducing server load."
drupal_version: "11.x"
---

# Query Performance

## When to Use

> When optimizing search query speed and reducing server load.

## Decision: Performance Strategies

| Strategy | Impact | Applies To |
|---|---|---|
| Whole words only matching | Significant speedup | Database backend |
| Skip result count query | Major speedup on MySQL InnoDB | Database backend |
| Mini pager | Avoids COUNT query | All backends |
| Skip entity loads (Solr index-only) | Eliminates DB queries | Solr backend |
| Highlight processor skip | 10x latency reduction | All backends |
| Cache warming | Faster repeated queries | All backends |

## Pattern: MySQL InnoDB COUNT Problem

MySQL InnoDB COUNT queries are extremely slow on large tables. Two mitigations:

1. **Use Mini pager** in Views instead of Full pager — Mini pager doesn't need total count
2. **Enable "Skip result count query"** in Views query settings

## Pattern: Highlight Performance

The Highlight processor can add 10x latency on complex queries. Options:
- Disable globally if excerpts aren't needed
- Skip for specific pages via query tag:
```php
$query->addTag('search_api_skip_processor_highlight');
```

## Pattern: Cache Warming

For high-traffic search pages:
1. Identify popular search terms from analytics
2. Create a cron job that pre-executes popular queries
3. This warms Drupal's render cache and the backend's query cache

For Solr: configure autowarming in `solrconfig.xml` for filter cache, query result cache, and document cache.

## Common Mistakes

- **Using AJAX on search results Views** — Breaks unique URLs, harms UX and analytics. Does not improve performance.
- **Partial matching on DB backend** — "Partial matching" is much slower than "Whole words only." Only use partial if required.

## See Also

- [Indexing Performance](indexing-performance.md) — indexing-side optimization
- [Solr Best Practices](solr-best-practices.md) — Solr-specific performance
