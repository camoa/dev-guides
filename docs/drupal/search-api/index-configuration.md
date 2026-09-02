---
description: Search API index entity — properties, datasource selection, key methods, and cron_limit tuning
tldr: "Use this when creating or configuring a Search API index — the central entity defining what gets indexed, how it's processed, and where it's stored."
drupal_version: "11.x"
---

# Index Configuration

## When to Use

> When creating or configuring a Search API index — the central entity that defines what gets indexed, how it's processed, and where it's stored.

## Decision: Index Entity Properties

| Property | Config Key | Default | Purpose |
|---|---|---|---|
| Machine name | `id` | — | Unique identifier |
| Name | `name` | — | Human-readable label |
| Server | `server` | — | Which server to index to |
| Datasources | `datasource_settings` | — | What to index (content entities) |
| Fields | `field_settings` | — | Which fields to index |
| Processors | `processor_settings` | — | Processing pipeline |
| Tracker | `tracker_settings` | Basic | How to track items |
| Read only | `read_only` | FALSE | Prevent writes |
| Index directly | `options.index_directly` | TRUE | Index immediately on save |
| Cron batch size | `options.cron_limit` | 50 | Items per cron run |
| Track references | `options.track_changes_in_references` | TRUE | Reindex when referenced entities change |
| Delete on fail | `options.delete_on_fail` | TRUE | Remove unloadable items |

## Decision: Index Directly vs Queue

| Setting | Behavior | Best For |
|---|---|---|
| `index_directly: TRUE` | Items indexed immediately after entity save | Small sites, real-time search |
| `index_directly: FALSE` | Items queued for cron/drush indexing | Large sites, high-traffic, complex entities |

## Pattern: Datasource Selection

The ContentEntity datasource auto-derives per entity type:
- `entity:node` — Content (nodes)
- `entity:taxonomy_term` — Taxonomy terms
- `entity:user` — Users
- `entity:media` — Media entities
- `entity:commerce_product` — Commerce products (if installed)

You can select multiple datasources on a single index. Each entity creates one index item per language.

## Pattern: Index Key Methods

| Method | Purpose |
|---|---|
| `getDatasources()` | Get datasource plugins |
| `getFields()` | Get indexed field instances |
| `getField($id)` | Get specific field |
| `setField($id, $field)` | Add/update field |
| `getProcessors()` | Get processor plugins (sorted by stage) |
| `getTrackerInstance()` | Get tracker plugin |
| `getServerInstance()` | Get server entity |
| `indexItems()` | Trigger indexing |
| `isFullyIndexed()` | All items indexed? |
| `getRemainingItems($limit)` | Get unindexed items |

## Common Mistakes

- **Indexing too many entity types** — Only index entities users will search for. Don't add paragraphs, blocks, or admin entities.
- **cron_limit too high** — Complex entities with many references can consume 200MB+ per batch. Start with 50, reduce if you see memory issues.
- **Not enabling track_changes_in_references** — If a referenced taxonomy term label changes, content referencing it won't reindex unless this is enabled.

## See Also

- [Fields & Data Types](fields-data-types.md) — adding fields
- [Processor Architecture](processor-architecture.md) — configuring processors
- [Indexing Lifecycle](indexing-lifecycle.md) — how indexing works
- Reference: `web/modules/contrib/search_api/src/Entity/Index.php`
