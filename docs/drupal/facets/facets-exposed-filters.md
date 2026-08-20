---
description: "Integrating facets into the Views exposed form via facets_exposed_filters — the recommended approach in Facets 3.x"
tldr: "Use facets_exposed_filters when you want facets integrated into the Views exposed form — the recommended 3.x approach. Gives native Views AJAX, BEF widget support, and simpler configuration than block-based facets."
drupal_version: "11.x"
---

# Facets Exposed Filters

## When to Use

> When you want facets integrated into the Views exposed form — the recommended approach in Facets 3.x. This gives you native Views AJAX, BEF widget support, and simpler configuration.

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

## Pattern

```bash
drush en facets_exposed_filters better_exposed_filters
```

1. Create a View using a Search API index
2. **Save the View** (critical — source must exist before facets can find it)
3. In the View, add a Filter Criteria → look for the "Facets" category
4. Select the field you want to facet on
5. Configure the facet processors in the filter settings
6. Optionally: change the View's exposed form style to "Better Exposed Filters"
7. Configure BEF widgets per filter (checkboxes, links, etc.)

**New in 3.0.4**, the facet filter settings dialog also carries:
- **Ensure that only one result can be displayed** — once an option is selected, only that option stays visible until it is deselected
- **Depends on exposed filter** — only render and apply this facet after the selected exposed filter has an active value; when that filter changes, this facet is cleared before the form is submitted (client side, via the `facets_exposed_filters/dependent_filters` library)

`facets_exposed_filters` provides:
- `FacetsFilter` — a Views filter plugin (`src/Plugin/views/filter/FacetsFilter.php`) that appears in the Views UI as a standard filter but internally creates and manages a Facets facet entity
- `ViewsDefault` — Search API display plugin for Views defaults
- `ViewsAttachment` — Search API display for View attachments
- `ExposedRangeSliderProcessor` — **new in 3.0.4.** A facets processor (id `exposed_range_slider`, running at `pre_query` and `post_query`, weight 60) that supplies min/max range data to an exposed numeric facet. Only applies to facets whose source offers a `range` query type
- `ExposedRangeSlider` — **new in 3.0.4.** A Better Exposed Filters widget plugin (`#[FiltersWidget(id: 'facets_exposed_range_slider')]`, extending BEF's `Sliders`) that renders such a facet as a noUiSlider range slider. Becomes applicable only once the `exposed_range_slider` processor is enabled on the filter
- `FacetsExposedFiltersHelper` — **new in 3.0.4.** Request-scoped helper shared by the module's hook classes

With BEF as the exposed form style, facet filters render as BEF widgets (checkboxes, radio buttons, links, sliders), auto-submit works, secondary options/collapsible work, and soft limit works. Without BEF, facet filters render as standard dropdowns with no auto-submit or enhanced widgets.

## Common Mistakes

- **Wrong**: Adding facet filter criteria before saving the View → **Right**: The facet source doesn't exist until the View is saved — you'll get a warning otherwise.
- **Wrong**: Expecting to place exposed-filter facets in arbitrary regions → **Right**: With exposed filters, facets are part of the form, not blocks. Use `configurable_views_filter_block` if you need block placement.
- **Wrong**: Assuming overridden display filters work → **Right**: The module docs explicitly state overridden display filters are not (yet) supported.

## See Also

- [Overview](overview.md) — choosing between approaches
- [Widgets](widgets.md) — note: BEF widgets replace Facets widgets in this mode
- Reference: `modules/facets_exposed_filters/`
