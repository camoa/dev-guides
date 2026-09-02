---
description: Search API indexing performance — batch size tuning, cron vs Drush, Solr parallel indexing, search_api_fast for non-Solr backends
tldr: "Use this when optimizing how fast content gets indexed, especially for large sites or initial indexing."
drupal_version: "11.x"
---

# Indexing Performance

## When to Use

> When optimizing how fast content gets indexed, especially for large sites or initial indexing.

## Decision: Batch Size Tuning

| Scenario | Recommended Batch Size | Why |
|---|---|---|
| Simple nodes (title + body) | 100-200 | Low memory per item |
| Complex nodes (paragraphs, many references) | 10-25 | High memory per item (200MB+ per batch) |
| Initial full index | Use drush, not cron | More control over duration |
| Ongoing incremental | 50-100 via cron | Balance freshness vs load |

Set in Index → Edit → "Cron batch size" or via drush `--batch-size`.

## Decision: Cron vs Drush

| Method | Use Case | Command |
|---|---|---|
| **Cron** | Incremental indexing of content changes | Automatic (set cron_limit on index) |
| **Drush** | Initial indexing, reindexing, bulk operations | `drush sapi-i --batch-size=50 --time-limit=300` |
| **Solr parallel indexing** | Large sites (10K+ items) on Solr | `drush search-api-solr:index-parallel --threads=8 --batch-size=100` |
| **search_api_fast** | Large sites (10K+ items) on a non-Solr backend | Spawns parallel workers across CPU cores |

## Pattern: Drush Indexing Commands

```bash
# Index all pending items
drush sapi-i

# Index specific index only
drush sapi-i my_index

# With batch size and time limit
drush sapi-i --batch-size=25 --time-limit=600

# Mark everything for reindex (doesn't delete from backend)
drush sapi-r my_index

# Clear index completely (deletes from backend)
drush sapi-c my_index

# Rebuild tracking info
drush sapi-rt my_index
```

## Pattern: Parallel Indexing

On Solr, use the parallel indexing command that ships with `search_api_solr` — no extra module:
```bash
drush search-api-solr:index-parallel my_index --threads=8 --batch-size=100
```

On a non-Solr backend, `search_api_fast` spawns parallel Drush workers:
```bash
composer require drupal/search_api_fast
drush search-api-fast:index my_index
# or with the alias:
drush sapi-fast my_index
```

Worker count is **configuration, not a command option** — there is no `--workers` flag. Set `index_workers` (default 8) in `search_api_fast.performance`:
```bash
drush config:set search_api_fast.performance index_workers 4
```

## Pattern: Solr Index-Only Mode

For maximum query performance on Solr, skip entity loads entirely:

1. Server config → Enable "Retrieve result data from Solr"
2. Views query settings → Enable "Skip item access checks" (only for fully public content)
3. Ensure all displayed fields are in the Search API index

Result: Solr returns field data directly — no database queries for entity loading.

## Pattern: Cron Frequency

| Site Size | Cron Interval | Batch Size |
|---|---|---|
| Small (<10K items) | 15 minutes | 100 |
| Medium (10K-100K) | 5 minutes | 50 |
| Large (100K+) | 1-2 minutes | 25 |

## Common Mistakes

- **cron_limit = -1 on large indexes** — Indexes all items at once. Causes memory exhaustion on complex entities.
- **cron_limit = 0** — Disables cron indexing entirely. Items never get indexed via cron.
- **Not using drush for initial indexing** — Cron indexing large datasets takes days. Use drush with --time-limit for controlled batch indexing.

## See Also

- [Indexing Lifecycle](indexing-lifecycle.md) — how indexing works
- [Query Performance](query-performance.md) — query-side optimization
