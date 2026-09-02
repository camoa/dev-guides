---
description: Search API indexing lifecycle — tracking, indexing steps, deletion, reindex flow, and reference tracking
tldr: "Use this when you need to understand how content gets tracked, indexed, and maintained in the search engine."
drupal_version: "11.x"
---

# Indexing Lifecycle

## When to Use

> When you need to understand how content gets tracked, indexed, and maintained in the search engine.

## Decision: Lifecycle Steps

```
1. ENTITY SAVED
   → ContentEntityDatasourceHooks detects change
   → Index::trackItemsInserted() or trackItemsUpdated()
   → Tracker records item as "needs indexing"

2. INDEXING TRIGGERED (cron or drush)
   → Tracker::getRemainingItems($limit) returns unindexed items
   → Datasource::loadMultiple() loads entities
   → IndexingItemsEvent dispatched
   → Processors: STAGE_ALTER_ITEMS (filter unpublished, etc.)
   → Processors: STAGE_PREPROCESS_INDEX (transform values)
   → Backend::indexItems() stores in search engine
   → ItemsIndexedEvent dispatched
   → Tracker::trackItemsIndexed() marks as indexed

3. ENTITY DELETED
   → Index::trackItemsDeleted()
   → Backend::deleteItems() removes from search engine
   → Tracker removes records

4. REINDEX REQUESTED
   → ReindexScheduledEvent dispatched
   → Tracker marks all items as "needs indexing"
   → Items re-processed on next indexing run
```

## Decision: Index Directly vs Cron

| Setting | When Items Are Indexed | Best For |
|---|---|---|
| `index_directly: TRUE` | Immediately after entity save (in same request) | Real-time search, small sites |
| `index_directly: FALSE` | Next cron run or drush command | High-traffic sites, complex entities |

## Pattern: Tracker

The Basic tracker (default, only built-in option) uses a database table to track:
- Which items exist in each datasource
- Which items have been indexed
- Which items need (re)indexing

**Tracker methods:**
| Method | Purpose |
|---|---|
| `getRemainingItems($limit)` | Get items needing indexing |
| `getTotalItemsCount()` | Total tracked items |
| `getIndexedItemsCount()` | Successfully indexed count |
| `rebuildTrackingInfo()` | Rebuild from scratch |

## Pattern: Reference Tracking

When `options.track_changes_in_references` is TRUE (default), changes to referenced entities trigger reindexing. For example:
- Editing a taxonomy term name → all nodes referencing that term are queued for reindexing
- Changing an author's display name → all their content is queued

## Common Mistakes

- **Not reindexing after processor changes** — Changing processors only affects future indexing. Existing indexed items keep old values until reindexed.
- **Entity reference changes not detected** — If `track_changes_in_references` is disabled, referenced entity changes are invisible to the index.
- **Tracker out of sync** — If items are deleted directly from the database (not through Drupal), use `drush sapi-rt` to rebuild tracking.

## See Also

- [Indexing Performance](indexing-performance.md) — optimizing indexing speed
- [Index Configuration](index-configuration.md) — index_directly setting
