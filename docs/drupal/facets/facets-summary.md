---
description: Facets Summary sub-module — display active facet selections as removable breadcrumbs with processors and views_filters_summary alternative
tldr: "Use this guide when you want to display active facet selections as removable breadcrumbs — \"Color: Blue (x) | Size: Large (x) | Reset all\"."
drupal_version: "11.x"
---

# Facets Summary

## When to Use

> Use this guide when you want to display active facet selections as removable breadcrumbs — "Color: Blue (x) | Size: Large (x) | Reset all".

## Decision

**Module:** `facets_summary`
**Entity:** `FacetsSummary` (config entity)
**Admin:** `/admin/config/search/facets/facet-summary/add`

**Summary processors:**

| ID | Title | Purpose |
|---|---|---|
| `show_summary_processor` | Show a summary of active items | Display selected filter values |
| `show_count_processor` | Show result count | Display total results matching filters |
| `show_text_when_empty_processor` | Show text when empty | Message when no filters are active |
| `reset_facets_processor` | Reset all filters | Add a "Reset all" link |

**Alternative:** The Facets docs recommend `views_filters_summary` as a replacement for `facets_summary`. It works with any Views filter (not just facets) and integrates with the exposed filters approach.

## Pattern

```bash
drush en facets_summary
```

1. Go to `/admin/config/search/facets`
2. Click "Add facet summary"
3. Select the facet source
4. Enable processors (show summary, reset, etc.)
5. Place the summary block in your layout

## Common Mistakes

- **Wrong**: Using `facets_summary` with the exposed filters approach → **Right**: For exposed filters, prefer `views_filters_summary` — it integrates natively with the Views exposed form.

## See Also

- [Facets Exposed Filters](facets-exposed-filters.md) — using with exposed filters
- [Overview](overview.md) — sub-module overview
- Reference: `web/modules/contrib/facets/modules/facets_summary/`
