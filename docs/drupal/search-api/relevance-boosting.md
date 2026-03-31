---
description: Search API relevance tuning — field boosts, HTML element boosts, type boost, and Views relevance sort
drupal_version: "11.x"
---

# Relevance & Boosting

## When to Use

> Use this when tuning search result relevance — making the most relevant results appear first.

## Decision

| Mechanism | Where | Effect |
|---|---|---|
| **Field boost** | Index → Fields tab | Per-field weight multiplier |
| **HTML element boost** | HTML Filter processor settings | Boost by H1, H2, H3, strong, em tags |
| **Type boost** | Type Boost processor | Boost entire entity types/bundles |
| **Number field boost** | Number Field Boost processor | Boost by a numeric field value |
| **Views sort** | Views sort criteria | Sort by "Search: Relevance" |

## Pattern

**Field boost values:**

| Content | Recommended Boost |
|---|---|
| Title | 13-21x |
| H1 elements (via HTML filter) | 5x |
| H2 elements | 3x |
| H3 elements | 2x |
| Strong / bold text | 2x |
| Body / rendered HTML | 1x (base) |

**HTML Filter element boosts** (set in HTML Filter processor settings):
- H1: 5, H2: 3, H3: 2, Strong/B: 2, Em/I: 1.5

**If using Rendered HTML Output alongside individual fields:**
- Set Title boost to **13-21x**
- Set Rendered HTML boost to **0.5 or lower**
- This prevents rendered output from diluting the title boost

**Views sort:** Always add "Search: Relevance" sort descending. Views does NOT default to relevance sort — you must add it explicitly.

## Common Mistakes

- **Wrong**: Not sorting by relevance in Views → **Right**: Default Views sort is not relevance. Without it, results appear in arbitrary order.
- **Wrong**: Over-boosting one field → **Right**: A title at 21x with body at 1x means a partial title match outweighs a perfect body match. Balance boosts.
- **Wrong**: Ignoring HTML filter → **Right**: The HTML filter processor can boost by element tags inside rendered HTML, giving heading text more weight without separate fields.

## See Also

- [Fields & Data Types](fields-data-types.md)
- [Processor Recommendations](processor-recommendations.md)
