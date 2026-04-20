---
description: Search API indexing lifecycle — tracking, indexing steps, deletion, reindex flow, and reference tracking
tldr: "Use this when you need to understand how content gets tracked, indexed, and maintained in the search engine."
drupal_version: "11.x"
---

# Indexing Lifecycle

## When to Use

> Use this when you need to understand how content gets tracked, indexed, and maintained in the search engine.

## Decision

| Setting | When Items Are Indexed | Best For |
|---|---|---|
| `index_directly: TRUE` | Immediately after entity save (in same request) | Real-time search, small sites |
| `index_directly: FALSE` | Next cron run or drush command | High-traffic sites, complex entities |

## Pattern

**Lifecycle steps:**
```
1. ENTITY SAVED
   → Tracker records item as "needs indexing"

2. INDEXING TRIGGERED (cron or drush)
   → Tracker::getRemainingItems($limit) returns unindexed items
   → Datasource::loadMultiple() loads entities
   → IndexingItemsEvent dispatched
   → ALTER_ITEMS processors (filter unpublished, etc.)
   → PREPROCESS_INDEX processors (transform values)
   → Backend::indexItems() stores in search engine
   → ItemsIndexedEvent dispatched
   → Tracker marks as indexed

3. ENTITY DELETED
   → Backend::deleteItems() removes from search engine

4. REINDEX REQUESTED
   → Tracker marks all items as "needs indexing"
   → Re-processed on next indexing run
```

**Reference tracking:** When `track_changes_in_references: TRUE` (default), changes to referenced entities trigger reindexing. Editing a taxonomy term name → all nodes referencing it are queued for reindexing.

**Tracker methods:**

| Method | Purpose |
|---|---|
| `getRemainingItems($limit)` | Get items needing indexing |
| `getTotalItemsCount()` | Total tracked items |
| `getIndexedItemsCount()` | Successfully indexed count |
| `rebuildTrackingInfo()` | Rebuild from scratch |

## Common Mistakes

- **Wrong**: Not reindexing after processor changes → **Right**: Processor changes only affect future indexing. Existing indexed items keep old values until reindexed.
- **Wrong**: Disabling `track_changes_in_references` → **Right**: Referenced entity changes (e.g., taxonomy term labels) become invisible to the index.
- **Wrong**: Tracker out of sync after direct database deletes → **Right**: Use `drush sapi-rt` to rebuild tracking.

## See Also

- [Indexing Performance](indexing-performance.md)
- [Index Configuration](index-configuration.md)
- Reference: `web/modules/contrib/search_api/src/Tracker/`
