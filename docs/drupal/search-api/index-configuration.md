---
description: Search API index entity — properties, datasource selection, key methods, and cron_limit tuning
tldr: "Use this when creating or configuring a Search API index — the central entity defining what gets indexed, how it's processed, and where it's stored."
drupal_version: "11.x"
---

# Index Configuration

## When to Use

> Use this when creating or configuring a Search API index — the central entity defining what gets indexed, how it's processed, and where it's stored.

## Decision

| Property | Config Key | Default | Purpose |
|---|---|---|---|
| Server | `server` | — | Which server to index to |
| Datasources | `datasource_settings` | — | What to index (content entities) |
| Fields | `field_settings` | — | Which fields to index |
| Processors | `processor_settings` | — | Processing pipeline |
| Index directly | `options.index_directly` | TRUE | Index immediately on save |
| Cron batch size | `options.cron_limit` | 50 | Items per cron run |
| Track references | `options.track_changes_in_references` | TRUE | Reindex when referenced entities change |
| Delete on fail | `options.delete_on_fail` | TRUE | Remove unloadable items |

## Pattern

**Index directly vs queue:**

| Setting | Behavior | Best For |
|---|---|---|
| `index_directly: TRUE` | Items indexed immediately after entity save | Small sites, real-time search |
| `index_directly: FALSE` | Items queued for cron/drush indexing | Large sites, high-traffic, complex entities |

**Datasource selection** — ContentEntity datasource auto-derives per entity type:
- `entity:node`, `entity:taxonomy_term`, `entity:user`, `entity:media`
- Multiple datasources on a single index are supported
- Each entity creates one index item **per language**

**Key index methods:**

| Method | Purpose |
|---|---|
| `getDatasources()` | Get datasource plugins |
| `getFields()` | Get indexed field instances |
| `getProcessors()` | Get processor plugins |
| `indexItems()` | Trigger indexing |
| `isFullyIndexed()` | All items indexed? |
| `getRemainingItems($limit)` | Get unindexed items |

## Common Mistakes

- **Wrong**: Indexing too many entity types → **Right**: Only index entities users will search for. Don't add paragraphs, blocks, or admin entities.
- **Wrong**: `cron_limit` too high → **Right**: Complex entities can consume 200MB+ per batch. Start with 50, reduce if you see memory issues.
- **Wrong**: Not enabling `track_changes_in_references` → **Right**: Referenced taxonomy term label changes won't trigger reindex without this.

## See Also

- [Fields & Data Types](fields-data-types.md)
- [Processor Architecture](processor-architecture.md)
- [Indexing Lifecycle](indexing-lifecycle.md)
- Reference: `web/modules/contrib/search_api/src/Entity/Index.php`
