---
description: "Integrating facets into the Views exposed form via facets_exposed_filters — the recommended approach in Facets 3.x"
tldr: "Use facets_exposed_filters when you want facets integrated into the Views exposed form — the recommended 3.x approach. Gives native Views AJAX, BEF widget support, and simpler configuration than block-based facets."
drupal_version: "11.x"
---

# Facets Exposed Filters

## When to Use

> When you want facets integrated into the Views exposed form — the recommended approach in Facets 3.x. This gives you native Views AJAX, BEF widget support, and simpler configuration.

## Decision: Why Exposed Filters?

| Feature | Block-Based (2.x) | Exposed Filters (3.x) |
|---|---|---|
| AJAX support | No | Yes (native Views AJAX) |
| Configuration | Separate facet admin | Directly in Views UI |
| Multiple displays | Must recreate per display | Shared across displays |
| Widget control | Facets widgets only | BEF widgets (checkboxes, links, sliders) |
| Layout flexibility | Place blocks anywhere | In the exposed form area |
| Processors | Full processor support | Full processor support |
| Performance | Separate query overhead | Single Views query |

## Pattern: Setup

1. Enable modules:

```bash
drush en facets_exposed_filters better_exposed_filters
```

2. Create a View using a Search API index
3. **Save the View** (critical — source must exist before facets can find it)
4. In the View, add a Filter Criteria → Look for the "Facets" category
5. Select the field you want to facet on
6. Configure the facet processors in the filter settings
7. Optionally: Change the View's exposed form style to "Better Exposed Filters"
8. Configure BEF widgets per filter (checkboxes, links, etc.)

## Pattern: Filter Configuration

When you add a facet filter in Views:

- The facet entity is auto-created
- You configure processors directly in the filter settings dialog
- Widget type is controlled by BEF (not Facets widgets)
- AJAX is handled by Views AJAX setting

**New in 3.0.4**, the facet filter settings also carry:

- **Ensure that only one result can be displayed** — once an option is selected, only that option stays visible until it is deselected
- **Depends on exposed filter** — only render and apply this facet after the selected exposed filter has an active value; when that filter changes, this facet is cleared before the form is submitted (client side, via the `facets_exposed_filters/dependent_filters` library)

## Pattern: Sub-Module Architecture

**facets_exposed_filters** provides:

- `FacetsFilter` — A Views filter plugin (`src/Plugin/views/filter/FacetsFilter.php`)
- `ViewsDefault` — Search API display plugin for Views defaults
- `ViewsAttachment` — Search API display for View attachments
- `ExposedRangeSliderProcessor` — **New in 3.0.4.** A facets processor (id `exposed_range_slider`, running at `pre_query` and `post_query`, weight 60) that supplies min/max range data to an exposed numeric facet. It only supports facets whose source offers a `range` query type
- `ExposedRangeSlider` — **New in 3.0.4.** A *Better Exposed Filters* widget plugin (`#[FiltersWidget(id: 'facets_exposed_range_slider')]`, extending BEF's `Sliders`) that renders such a facet as a noUiSlider range slider. It becomes applicable only once the `exposed_range_slider` processor is enabled on the filter
- `FacetsExposedFiltersHelper` — **New in 3.0.4.** Request-scoped helper shared by the module's hook classes

The `FacetsFilter` acts as a bridge: it appears in the Views UI as a standard filter but internally creates and manages a Facets facet entity.

## Decision: BEF + Facets Exposed Filters

With BEF as the exposed form style:

- Facet filters render as BEF widgets (checkboxes, radio buttons, links, sliders)
- Auto-submit works for facet filters
- Secondary options/collapsible work for facet filters
- Soft limit works for facet filters

Without BEF (plain exposed form):

- Facet filters render as standard dropdowns
- No auto-submit
- No enhanced widgets

## Common Mistakes

- **Not saving the View first** — The facet source doesn't exist until the View is saved. You'll get a warning.
- **Expecting block-based features** — With exposed filters, facets are not blocks. They're part of the form. You can't place them in arbitrary page regions (use `configurable_views_filter_block` for that).
- **Overridden display filters not supported** — The docs explicitly state this: "Overridden display filters are not (yet) supported."

## See Also

- [Overview](overview.md) — choosing between approaches
- [Widgets](widgets.md) — note: BEF widgets replace Facets widgets in this mode
- Reference: `modules/facets_exposed_filters/`
