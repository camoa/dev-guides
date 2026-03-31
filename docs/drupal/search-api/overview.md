---
description: Search API vs core Search — architecture, 7 plugin types, config entities, and key services
drupal_version: "11.x"
---

# Overview

## When to Use

> Use Search API when you need flexible, backend-agnostic search for Drupal. Always use Search API over core Search — uninstall the core `search` module, it performs redundant indexing.

## Decision

| Feature | Core Search | Search API |
|---|---|---|
| Backend | Database only | Pluggable (DB, Solr, ES, Typesense, Meilisearch) |
| Entity types | Nodes + users only | Any entity type |
| Faceted search | No | Yes (via Facets module) |
| Views integration | Limited | Full |
| Autocomplete | No | Yes (via search_api_autocomplete) |
| Field-level control | No | Yes — choose exactly what to index |
| Relevance tuning | Minimal | Field boosts, HTML element boosts, type boosts |
| Processors | Basic | 23+ built-in, extensible |
| Performance at scale | Poor | Excellent with Solr/ES |

## Pattern

Search API uses **7 plugin types** in a layered pipeline:

```
Datasource (where items come from — content entities)
  → Tracker (tracks which items need indexing)
    → Processors: ALTER_ITEMS → PREPROCESS_INDEX
      → Backend (stores & searches — DB, Solr, ES)
        → Processors: PREPROCESS_QUERY → [backend executes] → POSTPROCESS_QUERY
          → Display (Views page, block, REST)
```

**Plugin types:** Backend, Datasource, Processor, Tracker, Data Type, Parse Mode, Display

**Config entities:**
- `search_api.server.*` — Server (backend configuration)
- `search_api.index.*` — Index (fields, processors, datasources, options)

**Key services:**
- `search_api.query_helper` — Query building
- `plugin.manager.search_api.processor` — Processor plugin manager
- `search_api.index_task_manager` — Indexing task management

## Common Mistakes

- **Wrong**: Keeping core Search module enabled → **Right**: `drush pm:uninstall search` — it causes redundant indexing.
- **Wrong**: Using Database backend for production at scale → **Right**: DB backend is for development and small sites (<50K items). Use Solr for production.
- **Wrong**: Not creating a dedicated "Search index" view mode → **Right**: Index only what matters for search, not the full rendered entity.

## See Also

- [Backend Comparison](backend-comparison.md)
- [Installation & Setup](installation-setup.md)
- [Recommended Module Stacks](recommended-module-stacks.md)
- Reference: `web/modules/contrib/search_api/`
