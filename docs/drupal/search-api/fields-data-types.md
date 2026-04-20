---
description: Search API field data types — choosing Fulltext vs String vs Integer, what to index, boost values, and rendered HTML strategy
tldr: "Use this when adding fields to a Search API index and choosing the correct data type for each."
drupal_version: "11.x"
---

# Fields & Data Types

## When to Use

> Use this when adding fields to a Search API index and choosing the correct data type for each.

## Decision

| Type | Plugin ID | Indexing Behavior | Use For |
|---|---|---|---|
| **Fulltext** | `text` | Tokenized, analyzed, supports fulltext search | Title, body, description — fields users will search |
| **String** | `string` | Exact match only, not tokenized | Taxonomy term names (for facets), status values |
| **Integer** | `integer` | Numeric | Entity IDs, counts, numeric fields |
| **Decimal** | `decimal` | Floating point | Prices, ratings |
| **Boolean** | `boolean` | TRUE/FALSE | Published status, promoted, sticky |
| **Date** | `date` | Timestamp | Created, changed, event dates |

## Pattern

**What to index:**

| Field | Data Type | Boost | Purpose |
|---|---|---|---|
| Title | Fulltext | 13-21x | Primary search target |
| Body / Description | Fulltext | 1x | Full content search |
| Rendered HTML (search view mode) | Fulltext | 0.5-1x | Catches paragraphs, nested references |
| Content type | String | — | Faceting, filtering |
| Taxonomy terms | String | — | Faceting |
| Status | Boolean | — | Filter to published only |
| Created date | Date | — | Sorting |

**Rendered HTML strategy:**
1. Create a "Search index" view mode at `/admin/structure/types/manage/{type}/display`
2. Include only search-relevant fields in this view mode
3. Add the "Rendered HTML output" field to the index
4. Set its boost to **0.5 or lower** — lower than individual field boosts

**If using both Rendered HTML AND individual fields:** Set Rendered HTML boost to 0 or very low. It indexes everything and dilutes individual field boosts.

## Common Mistakes

- **Wrong**: Using Fulltext for facet fields → **Right**: Fulltext is tokenized. "Web Development" becomes two tokens: "web" and "development". Use String type for facets.
- **Wrong**: Indexing everything → **Right**: Only index fields relevant to search. Admin fields, revision logs, layout data waste index space.
- **Wrong**: Not using a dedicated search view mode → **Right**: Default "Full content" view mode includes navigation, sidebars, and irrelevant markup.

## See Also

- [Relevance & Boosting](relevance-boosting.md)
- [Processor Architecture](processor-architecture.md)
- Reference: `web/modules/contrib/search_api/src/Plugin/search_api/processor/`
