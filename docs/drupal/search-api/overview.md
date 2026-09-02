---
description: Search API vs core Search — architecture, 7 plugin types, config entities, and key services
tldr: "Use Search API when you need flexible, backend-agnostic search for Drupal. Always use Search API over core Search — uninstall the core `search` module, it performs redundant indexing."
drupal_version: "11.x"
---

# Overview

## When to Use

> When you need a flexible, backend-agnostic search framework for Drupal. Search API provides the architecture — you choose the search engine (database, Solr, Elasticsearch, Typesense, Meilisearch) and build on top with Views, Facets, and autocomplete.

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
| Processors | Basic | 22 built-in, extensible |
| Performance at scale | Poor | Excellent with Solr/ES |

**Recommendation:** Always use Search API. Uninstall core `search` module — it performs redundant indexing.

## Pattern

Search API uses **7 plugin types** to create a flexible, layered search system:

```
Datasource (where items come from — content entities)
  → Tracker (tracks which items need indexing)
    → Processors: ALTER_ITEMS → PREPROCESS_INDEX
      → Backend (stores & searches — DB, Solr, ES)
        → Processors: PREPROCESS_QUERY → [backend executes] → POSTPROCESS_QUERY
          → Display (Views page, block, REST)
```

**Plugin types:**
1. **Backend** — Search engine adapter (Database, Solr, Elasticsearch, etc.)
2. **Datasource** — Data source (ContentEntity — auto-derives per entity type)
3. **Processor** — 22 built-in across 6 stages (add_properties, pre_index_save, alter_items, preprocess_index, preprocess_query, postprocess_query)
4. **Tracker** — Tracks item indexing state (Basic — FIFO database tracker)
5. **Data Type** — Field type definitions (string, text, integer, decimal, boolean, date)
6. **Parse Mode** — Search input parsing (Terms, Phrase, Direct, Complex)
7. **Display** — Search display representation (Views pages, blocks)

**Config entities:**
- `search_api.server.*` — Server (backend configuration)
- `search_api.index.*` — Index (fields, processors, datasources, options)

**Key services:**
- `facets.manager` / `search_api.query_helper` — Query building
- `plugin.manager.search_api.processor` — Processor plugin manager
- `search_api.index_task_manager` — Indexing task management
- `search_api.post_request_indexing` — Post-request indexing queue

## Common Mistakes

- **Keeping core Search module enabled** — Uninstall `search` module. It performs redundant indexing and hurts performance.
- **Using Database backend for production at scale** — DB backend is for development and small sites (<50K items). Use Solr for production.
- **Not creating a dedicated "Search index" view mode** — Index only what matters for search, not the full rendered entity.

## See Also

- [Backend Comparison](backend-comparison.md) — choosing the right search engine
- [Installation & Setup](installation-setup.md) — getting started
- [Recommended Module Stacks](recommended-module-stacks.md) — by site size
- Reference: `web/modules/contrib/search_api/`
