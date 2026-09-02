---
description: Search API relevance tuning — field boosts, HTML element boosts, type boost, and Views relevance sort
tldr: "Use this when tuning search result relevance — making the most relevant results appear first."
drupal_version: "11.x"
---

# Relevance & Boosting

## When to Use

> When tuning search result relevance — making the most relevant results appear first.

## Decision: Boost Mechanisms

| Mechanism | Where | Effect |
|---|---|---|
| **Field boost** | Index → Fields tab | Per-field weight multiplier |
| **HTML element boost** | HTML Filter processor settings | Boost by H1, H2, H3, strong, em tags |
| **Type boost** | Type Boost processor | Boost entire entity types/bundles |
| **Number field boost** | Number Field Boost processor | Boost by a numeric field value |
| **Views sort** | Views sort criteria | Sort by "Search: Relevance" |

## Pattern: Field Boost Configuration

Set in the index Fields tab — each fulltext field has a "Boost" value:
- 1.0 = normal weight (default)
- 2.0 = double weight
- 0.5 = half weight
- 21.0 = maximum (for title fields)

## Pattern: HTML Filter Element Boosts

In the HTML Filter processor settings:
| Element | Recommended Boost | Rationale |
|---|---|---|
| H1 | 5 | Page title (if in rendered HTML) |
| H2 | 3 | Section headings |
| H3 | 2 | Sub-headings |
| Strong / B | 2 | Emphasized text |
| Em / I | 1.5 | Italicized text |

## Pattern: Rendered HTML vs Individual Fields

If using both a Rendered HTML Output field AND individual fields (title, body):
- Set Rendered HTML boost to **0.5 or lower**
- Set Title boost to **13-21x**
- This prevents the rendered output from diluting the title boost

## Decision: Views Sort

**Always sort by "Search: Relevance" descending** for search results. Views does NOT default to relevance sort — you must add it explicitly.

## Common Mistakes

- **Not sorting by relevance** — Default Views sort is not relevance. Without it, results appear in arbitrary order.
- **Over-boosting one field** — A title at 21x with body at 1x means a partial title match outweighs a perfect body match. Balance boosts.
- **Ignoring HTML filter** — The HTML filter processor can boost by element tags inside the rendered HTML, giving heading text more weight without separate fields.

## See Also

- [Fields & Data Types](fields-data-types.md) — field configuration
- [Processor Recommendations](processor-recommendations.md) — processor setup
