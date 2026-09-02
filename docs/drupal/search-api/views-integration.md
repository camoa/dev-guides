---
description: Search API Views integration — plugin mapping, creating a search View, display types, fulltext filter configuration
tldr: "Use this when building search pages using Views — the most common approach for Search API."
drupal_version: "11.x"
---

# Views Integration

## When to Use

> When building search pages using Views (the most common approach).

## Decision: Views Plugin Mapping

| Views Component | Search API Plugin | Purpose |
|---|---|---|
| Query plugin | `SearchApiQuery` | Translates Views config to Search API queries |
| Field plugins | `SearchApiStandard`, `SearchApiText`, `SearchApiNumeric`, etc. | Display indexed fields |
| Filter plugins | Per-field type | Map to Search API conditions |
| Sort plugin | `SearchApiSort` | Map to Search API sorts |
| Argument plugins | `SearchApiStandard`, `SearchApiFulltext`, `SearchApiTerm` | Contextual filters |
| Row plugin | Rendered item | Display entity rendering |

## Pattern: Creating a Search View

1. Add View → Show: "Index: [your_index_name]"
2. Add a "Fulltext search" exposed filter (if needed)
3. Add fields or use "Rendered entity" row display
4. **Add sort: "Search: Relevance" (Descending)** — this is critical
5. Add pagination
6. Optionally add facets via Facets Exposed Filters

## Pattern: Views Display Types

| Display | Facet Source ID | Facets Support |
|---|---|---|
| Page | `search_api:views_page__{view}__{display}` | Yes |
| Block | `search_api:views_block__{view}__{display}` | Yes |
| REST export | `search_api:views_rest_export__{view}__{display}` | Yes (via facets_rest) |
| Attachment | Via parent display | Yes |

## Pattern: Fulltext Search Filter

Add "Search: Fulltext search" as an exposed filter. Configure:
- **Operator**: "Contains any of these words" (most common)
- **Searched fields**: Select which fulltext fields to search (or leave empty for all)
- **Min characters**: Set minimum search length

## Common Mistakes

- **Not sorting by relevance** — The #1 most common mistake. Add "Search: Relevance" sort descending.
- **Using "Use AJAX" on search Views** — Breaks unique URLs, harms UX and analytics. Use normal page loads.
- **Not exposing the fulltext search filter** — Without it, the View shows all indexed content unfiltered.

## See Also

- [Facets Integration](facets-integration.md) — adding facets to search Views
- [Query Performance](query-performance.md) — Views performance tips
