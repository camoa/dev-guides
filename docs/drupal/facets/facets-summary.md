---
description: "The facets_summary sub-module for displaying active facet selections as removable breadcrumbs"
tldr: "Use this guide when you want to display active facet selections as removable breadcrumbs — 'Color: Blue (x) | Size: Large (x) | Reset all'. The maintainers recommend views_filters_summary as a broader replacement."
drupal_version: "11.x"
---

# Facets Summary

## When to Use

> When you want to display active facet selections as removable breadcrumbs — "Color: Blue (x) | Size: Large (x) | Reset all".

## Decision: Facets Summary Sub-Module

**Module:** `facets_summary`
**Entity:** `FacetsSummary` (config entity)
**Admin:** `/admin/config/search/facets/facet-summary/add`

## Decision: Summary Processors

| ID | Title | Purpose |
|---|---|---|
| `show_summary_processor` | Show a summary of active items | Display selected filter values |
| `show_count_processor` | Show result count | Display total results matching filters |
| `show_text_when_empty_processor` | Show text when empty | Message when no filters are active |
| `reset_facets_processor` | Reset all filters | Add a "Reset all" link |

## Pattern: Setup

```bash
drush en facets_summary
```

1. Go to `/admin/config/search/facets`
2. Click "Add facet summary"
3. Select the facet source
4. Enable processors (show summary, reset, etc.)
5. Place the summary block in your layout

## Pattern: Alternative — views_filters_summary

The Facets docs recommend `views_filters_summary` as a replacement for `facets_summary`. It works with any Views filter (not just facets) and integrates with the exposed filters approach.

## Common Mistakes

- **Building a custom breadcrumb solution from scratch** — Use `facets_summary`, or `views_filters_summary` if you need it to cover non-facet Views filters too.

## See Also

- [Facets Exposed Filters](facets-exposed-filters.md) — using with exposed filters
- [Overview](overview.md) — sub-module overview
- Reference: `modules/facets_summary/`, https://www.drupal.org/project/views_filters_summary
