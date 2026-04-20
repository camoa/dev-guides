---
description: Integrating Facets with Search API — exposed filters approach, String field requirement, and setup pattern
tldr: "Use this when adding faceted search navigation to your Search API-powered search page."
drupal_version: "11.x"
---

# Facets Integration

## When to Use

> Use this when adding faceted search navigation to your Search API-powered search page.

## Decision

| Approach | Module | AJAX | Recommended |
|---|---|---|---|
| **Exposed Filters** | `facets_exposed_filters` + BEF | Yes (native Views) | Yes — for new projects |
| **Blocks** | `facets` (core) | No | Legacy approach |

## Pattern

```bash
drush en facets facets_exposed_filters better_exposed_filters
```

**Setup with exposed filters:**
1. Create View using Search API index
2. **Save the View** (required before adding facets)
3. Add Filter Criteria → select from "Facets" category
4. Configure facet processors in filter settings
5. Change exposed form style to "Better Exposed Filters"
6. Configure BEF widgets (checkboxes, links, etc.)

**Key integration points:**
- Index the field as **String** type (not Fulltext) for faceting
- Enable `translate_entity` processor on the facet for entity reference fields
- Use `hide_non_narrowing_result_processor` for clean UX
- Exposed filter facets produce no crawlable URLs (SEO safe)

## Common Mistakes

- **Wrong**: Using Fulltext type for facet fields → **Right**: Fulltext tokenizes values. "Web Development" becomes two facet items. Use String type.
- **Wrong**: Adding facets before saving the View → **Right**: Facet source doesn't exist until the View is saved.
- **Wrong**: Facets on non-indexed fields → **Right**: The field must be in the Search API index.

## See Also

- The dedicated **[Drupal Facets guide](../facets/index.md)** covers facets comprehensively — all processors, widgets, hierarchy, SEO & bot protection
- [Better Exposed Filters guide](../better-exposed-filters/index.md)
- Reference: https://www.drupal.org/project/facets
