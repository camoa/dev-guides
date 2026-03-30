---
description: Facets exposed filters — the recommended 3.x approach using Views filter criteria, native AJAX, and BEF widget integration
drupal_version: "11.x"
---

# Facets Exposed Filters

## When to Use

> Use facets_exposed_filters when you want facets integrated into the Views exposed form — the recommended approach in Facets 3.x. This gives you native Views AJAX, BEF widget support, and simpler configuration. Use block-based facets only when you need to place facets in arbitrary page regions (sidebar, Layout Builder).

## Decision

| Feature | Block-Based (2.x) | Exposed Filters (3.x) |
|---|---|---|
| AJAX support | No | Yes (native Views AJAX) |
| Configuration | Separate facet admin | Directly in Views UI |
| Multiple displays | Must recreate per display | Shared across displays |
| Widget control | Facets widgets only | BEF widgets (checkboxes, links, sliders) |
| Layout flexibility | Place blocks anywhere | In the exposed form area |
| Processors | Full processor support | Full processor support |
| Performance | Separate query overhead | Single Views query |

**BEF integration:**

| With BEF | Without BEF |
|---|---|
| BEF widgets (checkboxes, links, sliders) | Standard dropdowns |
| Auto-submit | No auto-submit |
| Soft limit, secondary panel | No enhanced widgets |

## Pattern

```bash
drush en facets_exposed_filters better_exposed_filters
```

1. Create a View using a Search API index
2. **Save the View** (critical — source must exist before facets can find it)
3. In the View, add a Filter Criteria → look for the "Facets" category
4. Select the field you want to facet on
5. Configure the facet processors in the filter settings
6. Optionally: Change the View's exposed form style to "Better Exposed Filters"
7. Configure BEF widgets per filter (checkboxes, links, etc.)

**Sub-module architecture — `facets_exposed_filters` provides:**
- `FacetsFilter` — A Views filter plugin (`src/Plugin/views/filter/FacetsFilter.php`)
- `ViewsDefault` — Search API display plugin for Views defaults
- `ViewsAttachment` — Search API display for View attachments

The `FacetsFilter` acts as a bridge: it appears in the Views UI as a standard filter but internally creates and manages a Facets facet entity.

## Common Mistakes

- **Wrong**: Creating facets before saving the View → **Right**: The facet source doesn't exist until the View is saved.
- **Wrong**: Trying to place exposed filter facets in arbitrary page regions → **Right**: With exposed filters, facets are part of the form. Use `configurable_views_filter_block` for arbitrary placement.
- **Wrong**: Using overridden display filters with facets_exposed_filters → **Right**: "Overridden display filters are not (yet) supported."

## See Also

- [Overview](overview.md) — choosing between approaches
- [Widgets](widgets.md) — note: BEF widgets replace Facets widgets in this mode
- Reference: `web/modules/contrib/facets/modules/facets_exposed_filters/src/Plugin/views/filter/FacetsFilter.php`
