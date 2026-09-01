---
description: Search API indexing performance — batch size tuning, cron vs Drush, Solr parallel indexing, search_api_fast for non-Solr backends
tldr: "Use this when optimizing how fast content gets indexed, especially for large sites or initial indexing."
drupal_version: "11.x"
---

# Indexing Performance

## When to Use

> Use this when optimizing how fast content gets indexed, especially for large sites or initial indexing.

## Pattern: Solr Index-Only Mode

For maximum query performance on Solr, skip entity loads entirely:

1. Server config → Enable "Retrieve result data from Solr"
2. Views query settings → Enable "Skip item access checks" (only for fully public content)
3. Ensure all displayed fields are in the Search API index

Result: Solr returns field data directly — no database queries for entity loading.

## Decision

| Scenario | Recommended Batch Size | Why |
|---|---|---|
| Simple nodes (title + body) | 100-200 | Low memory per item |
| Complex nodes (paragraphs, many references) | 10-25 | High memory per item (200MB+ per batch) |
| Initial full index | Use drush, not cron | More control over duration |
| Ongoing incremental | 50-100 via cron | Balance freshness vs load |

**Cron vs Drush vs parallel:**

| Method | Use Case | Command |
|---|---|---|
| Cron | Incremental indexing | Automatic (set cron_limit on index) |
| Drush | Initial indexing, reindexing, bulk | `drush sapi-i --batch-size=50 --time-limit=300` |
| Solr parallel indexing | Large sites (10K+ items) on Solr | `drush search-api-solr:index-parallel` — ships with `search_api_solr`, no extra module |
| search_api_fast | Large sites (10K+ items) on a **non-Solr** backend | Spawns parallel Drush workers |

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

**Solr parallel indexing** — no extra module needed on Solr:
```bash
drush search-api-solr:index-parallel my_index --threads=8 --batch-size=100
```

**search_api_fast** — only when the backend is *not* Solr:
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
- **Wrong**: Passing `--workers=N` to `search-api-fast:index` → **Right**: There is no such flag. Set `index_workers` via `drush config:set search_api_fast.performance index_workers N`.
- **Wrong**: Reaching for `search_api_fast` on a Solr site → **Right**: Solr ships its own parallel indexing command (`search-api-solr:index-parallel`). Reserve `search_api_fast` for non-Solr backends.

## See Also

- [Indexing Lifecycle](indexing-lifecycle.md)
- [Query Performance](query-performance.md)
- Reference: https://www.drupal.org/project/search_api_fast
