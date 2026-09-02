---
description: Integrating Facets with Search API — exposed filters approach, String field requirement, and setup pattern
tldr: "Use this when adding faceted search navigation to your Search API-powered search page. Facets 3.x only works with Search API, not core Views."
drupal_version: "11.x"
---

# Facets Integration

## When to Use

> When adding faceted search navigation to your Search API-powered search page.

## Decision: Facets Module Compatibility

Facets 3.x **only works with Search API**. It does not work with core Views database queries.

## Decision: Architecture Approach

| Approach | Module | AJAX | Recommended |
|---|---|---|---|
| **Exposed Filters** | `facets_exposed_filters` + BEF | Yes (native Views) | **Yes — for new projects** |
| **Blocks** | `facets` (core) | No | Legacy approach |

## Pattern: Setup with Exposed Filters (Recommended)

```bash
drush en facets facets_exposed_filters better_exposed_filters
```

1. Create View using Search API index
2. Save the View (required before adding facets)
3. Add Filter Criteria → select from "Facets" category
4. Configure facet processors in filter settings
5. Change exposed form style to "Better Exposed Filters"
6. Configure BEF widgets (checkboxes, links, etc.)

## Pattern: Key Integration Points

- Index the field as **String** type (not Fulltext) for faceting
- Enable `translate_entity` processor on the facet for entity reference fields
- Use `hide_non_narrowing_result_processor` for clean UX
- Exposed filter facets produce no crawlable URLs (SEO safe — see the [Drupal Facets guide](../facets/index.md))

## Common Mistakes

- **Using Fulltext type for facet fields** — Fulltext tokenizes values. "Web Development" becomes two facet items: "web" and "development". Use String type.
- **Facets on non-indexed fields** — The field must be in the Search API index.
- **Not saving the View first** — Facet source doesn't exist until the View is saved.

## See Also

- The dedicated **Drupal Facets Guide** covers facets comprehensively:
  - Facets overview and architecture
  - All processors, widgets, and hierarchy
  - SEO & bot protection (critical!)
  - BEF integration details
- [Drupal Facets guide](../facets/index.md)
