---
description: Search API indexing performance — batch size tuning, cron vs Drush, search_api_fast for large sites, and Solr index-only mode
drupal_version: "11.x"
---

# Indexing Performance

## When to Use

> Use this when optimizing how fast content gets indexed, especially for large sites or initial indexing.

## Decision

| Scenario | Recommended Batch Size | Why |
|---|---|---|
| Simple nodes (title + body) | 100-200 | Low memory per item |
| Complex nodes (paragraphs, many references) | 10-25 | High memory per item (200MB+ per batch) |
| Initial full index | Use drush, not cron | More control over duration |
| Ongoing incremental | 50-100 via cron | Balance freshness vs load |

**Cron vs Drush:**

| Method | Use Case | Command |
|---|---|---|
| Cron | Incremental indexing | Automatic (set cron_limit on index) |
| Drush | Initial indexing, reindexing, bulk | `drush sapi-i --batch-size=50 --time-limit=300` |
| search_api_fast | Large sites (10K+ items) | Spawns parallel workers |

## Pattern

```bash
# Index all pending items
drush sapi-i

# With batch size and time limit
drush sapi-i --batch-size=25 --time-limit=600

# Mark everything for reindex
drush sapi-r my_index

# Clear index completely
drush sapi-c my_index
```

**search_api_fast** — for 10K+ nodes:
```bash
composer require drupal/search_api_fast
drush search-api-fast:index my_index --workers=4
```

**Cron frequency by site size:**

| Site Size | Cron Interval | Batch Size |
|---|---|---|
| Small (<10K items) | 15 minutes | 100 |
| Medium (10K-100K) | 5 minutes | 50 |
| Large (100K+) | 1-2 minutes | 25 |

## Common Mistakes

- **Wrong**: `cron_limit = -1` on large indexes → **Right**: Indexes all items at once. Causes memory exhaustion on complex entities.
- **Wrong**: `cron_limit = 0` → **Right**: Disables cron indexing entirely. Items never get indexed via cron.
- **Wrong**: Using cron for initial indexing → **Right**: Use drush with `--time-limit` for controlled batch indexing of large datasets.

## See Also

- [Indexing Lifecycle](indexing-lifecycle.md)
- [Query Performance](query-performance.md)
- Reference: https://www.drupal.org/project/search_api_fast
