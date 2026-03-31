---
description: Search API Views integration — plugin mapping, creating a search View, display types, fulltext filter configuration
drupal_version: "11.x"
---

# Views Integration

## When to Use

> Use this when building search pages using Views — the most common approach for Search API.

## Decision

| Views Component | Search API Plugin | Purpose |
|---|---|---|
| Query plugin | `SearchApiQuery` | Translates Views config to Search API queries |
| Field plugins | `SearchApiStandard`, `SearchApiText`, etc. | Display indexed fields |
| Filter plugins | Per-field type | Map to Search API conditions |
| Sort plugin | `SearchApiSort` | Map to Search API sorts |
| Argument plugins | `SearchApiFulltext`, `SearchApiTerm` | Contextual filters |

## Pattern

**Creating a search View:**
1. Add View → Show: "Index: [your_index_name]"
2. Add a "Fulltext search" exposed filter
3. Add fields or use "Rendered entity" row display
4. **Add sort: "Search: Relevance" (Descending)** — required
5. Add pagination
6. Optionally add facets via Facets Exposed Filters

**Facet source IDs by display type:**

| Display | Facet Source ID |
|---|---|
| Page | `search_api:views_page__{view}__{display}` |
| Block | `search_api:views_block__{view}__{display}` |
| REST export | `search_api:views_rest_export__{view}__{display}` |

**Fulltext search filter:** Add "Search: Fulltext search" as an exposed filter. Set operator to "Contains any of these words". Select which fulltext fields to search.

## Common Mistakes

- **Wrong**: Not sorting by relevance → **Right**: The #1 most common mistake. Add "Search: Relevance" sort descending.
- **Wrong**: Using "Use AJAX" on search Views → **Right**: Breaks unique URLs, harms UX and analytics. Use normal page loads.
- **Wrong**: Not exposing the fulltext search filter → **Right**: Without it, the View shows all indexed content unfiltered.

## See Also

- [Facets Integration](facets-integration.md)
- [Query Performance](query-performance.md)
- Reference: `web/modules/contrib/search_api/src/Plugin/views/`
