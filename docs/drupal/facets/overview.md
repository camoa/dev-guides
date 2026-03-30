---
description: Facets vs BEF vs core exposed filters — architecture, sub-modules, and when to use each approach
drupal_version: "11.x"
---

# Overview

## When to Use

> Use Facets when you need faceted search navigation with result counts, narrowing behavior, and hierarchical filtering — and you are using Search API. Use Better Exposed Filters when you want enhanced widgets for any Views exposed form without Search API. Use core exposed filters when default select dropdowns are sufficient.

## Decision

| Feature | Core Exposed Filters | Better Exposed Filters | Facets |
|---|---|---|---|
| Backend | Views (any) | Views (any) | Search API required |
| Result counts | No | No | Yes — shows (42) next to each option |
| Narrowing behavior | No | No | Yes — only shows options with results |
| Hierarchical facets | No | Basic nesting | Full hierarchy with expand/collapse |
| Widget variety | Select only | Checkboxes, radio, links, sliders | Links, checkboxes, dropdown, range slider |
| AND/OR operators | Limited | Limited | Full AND/OR per facet |
| Summary/breadcrumbs | No | No | Yes — via facets_summary |
| AJAX support | Views AJAX | Views AJAX | Block: No / Exposed filter: Yes |
| Works without Search API | Yes | Yes | No — requires Search API |

## Pattern

Facets uses a multi-plugin layered architecture:

```
Facet Source (where data comes from)
    → Query Type (how to query the backend)
        → Processors: PRE_QUERY → backend executes → POST_QUERY → BUILD → SORT
            → Widget (how to render)
                → URL Processor (how URLs work)
```

**Six plugin types:**
1. **Facet Source** — Connects to Search API displays (Views pages, blocks, REST)
2. **Query Type** — Translates selections to search queries (string, date, range, granular)
3. **Processor** — 25 built-in processors across 4 stages (pre_query, post_query, build, sort)
4. **Widget** — Renders results (links, checkbox, dropdown, array)
5. **URL Processor** — Manages URL parameters (query string by default)
6. **Hierarchy** — Builds parent-child trees (taxonomy, dates)

**Sub-modules:**

| Module | Purpose |
|---|---|
| `facets_exposed_filters` | Use facets as Views exposed filters (integrates with BEF) |
| `facets_summary` | Show active selections as removable breadcrumbs |
| `facets_range_widget` | Range slider widget for numeric facets |
| `facets_searchbox_widget` | Searchbox to filter within facet item lists |
| `facets_rest` | Expose facets in REST API responses |

## Common Mistakes

- **Wrong**: Using Facets without Search API → **Right**: Facets requires Search API. It does not work with core Views database queries.
- **Wrong**: Expecting AJAX on facet blocks → **Right**: Block-based facets do NOT support AJAX. Use `facets_exposed_filters` for AJAX support.
- **Wrong**: Not indexing fields before adding facets → **Right**: A field must be added to the Search API index before it can be used as a facet.
- **Wrong**: Treating Facets 2.x and 3.x as equivalent → **Right**: Facets 3.x shifts toward exposed filters as the primary approach. Blocks still work but are secondary.

## See Also

- [Installation & Setup](installation-setup.md)
- [Facets Exposed Filters](facets-exposed-filters.md) — the recommended approach in 3.x
- [SEO & Bot Protection](seo-bot-protection.md) — preventing crawl bloat
- Reference: `web/modules/contrib/facets/`
