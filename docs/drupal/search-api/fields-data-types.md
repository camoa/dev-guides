---
description: Search API field data types — choosing Fulltext vs String vs Integer, what to index, boost values, and rendered HTML strategy
tldr: "Use this when adding fields to a Search API index and choosing the correct data type for each."
drupal_version: "11.x"
---

# Fields & Data Types

## When to Use

> When adding fields to a Search API index and choosing the correct data type for each.

## Decision: Data Types

| Type | Plugin ID | Indexing Behavior | Use For |
|---|---|---|---|
| **Fulltext** | `text` | Tokenized, analyzed, supports fulltext search | Title, body, description — fields users will search |
| **String** | `string` | Exact match only, not tokenized | Taxonomy term names (for facets), status values |
| **Integer** | `integer` | Numeric | Entity IDs, counts, numeric fields |
| **Decimal** | `decimal` | Floating point | Prices, ratings |
| **Boolean** | `boolean` | TRUE/FALSE | Published status, promoted, sticky |
| **Date** | `date` | Timestamp | Created, changed, event dates |

## Decision: What to Index

| Field | Data Type | Boost | Purpose |
|---|---|---|---|
| Title | Fulltext | 13-21x | Primary search target |
| Body / Description | Fulltext | 1x | Full content search |
| Rendered HTML (search view mode) | Fulltext | 0.5-1x | Catches nested content (paragraphs, references) |
| Content type | String | — | Faceting, filtering |
| Taxonomy terms | String | — | Faceting |
| Author | String | — | Faceting, filtering |
| Created date | Date | — | Sorting, date facets |
| Changed date | Date | — | Sorting |
| Status | Boolean | — | Filter to published only |
| URL | String | — | Display in results |

## Pattern: Rendered HTML Strategy

The "Rendered item" processor adds a field that renders the entity through a view mode. This catches content from paragraphs, nested entity references, layout builder sections — anything visible in the render.

**Best practice:**
1. Create a "Search index" view mode at `/admin/structure/types/manage/{type}/display`
2. Include only search-relevant fields in this view mode
3. Add the "Rendered HTML output" field to the index
4. Set its boost lower than the Title field (0.5-1x vs 13-21x)

## Pattern: Field Boost Values

| Content | Recommended Boost |
|---|---|
| Title | 13-21x |
| H1 elements (via HTML filter) | 5x |
| H2 elements | 3x |
| H3 elements | 2x |
| Strong/bold text | 2x |
| Body / rendered HTML | 1x (base) |

**Important:** If using Rendered HTML Output alongside individual fields, set the Rendered HTML Output boost to 0 or low. It indexes everything and dilutes individual field boosts.

## Common Mistakes

- **Using Fulltext for facet fields** — Fulltext fields are tokenized. A taxonomy term "Web Development" becomes two tokens: "web" and "development". Use String type for facets.
- **Indexing everything** — Only index fields relevant to search. Admin fields, revision logs, layout data waste index space.
- **Not using a dedicated search view mode** — The default "Full content" view mode includes navigation, sidebars, and irrelevant markup.

## See Also

- [Relevance & Boosting](relevance-boosting.md) — detailed boost strategy
- [Processor Architecture](processor-architecture.md) — how fields are processed
