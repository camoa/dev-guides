---
description: BEF vs core exposed filters — capabilities, architecture, and when to use Better Exposed Filters
drupal_version: "11.x"
---

# Overview

## When to Use

> Use Better Exposed Filters when you need more control over how Views exposed filters are rendered — replacing default select dropdowns with checkboxes, radio buttons, links, sliders, date pickers, or other widgets. Use core exposed filters when default select dropdowns are sufficient.

## Decision

| Feature | Core Exposed Filters | Better Exposed Filters |
|---|---|---|
| Select dropdowns | Yes | Yes (default) |
| Checkboxes / radio buttons | No (must write custom code) | Yes — `bef` widget |
| Clickable links | No | Yes — `bef_links` widget |
| Range sliders | No | Yes — `bef_sliders` widget (noUiSlider) |
| HTML5 date pickers | No | Yes — `bef_datepicker` widget |
| Hidden filters | Partially (manual form alter) | Yes — `bef_hidden` widget |
| Single on/off checkbox | No | Yes — `bef_single` widget |
| Number input with min/max | No | Yes — `bef_number` widget |
| Auto-submit on change | No (requires custom JS) | Yes — built-in with debounce |
| Secondary options panel | No | Yes — collapsible details element |
| Select all/none | No | Yes — for checkboxes and links |
| Soft limit (show more/less) | No | Yes — JS-based truncation |
| Option rewriting | No | Yes — find/replace labels |
| Option sorting | Views sort order only | Alphabetical, by key, natural sort |
| Hierarchical/nested display | Flat only | Yes — nested `<ul>` for taxonomy |
| Sort combine | No | Yes — merge sort_by + sort_order |

## Pattern

BEF replaces the Views exposed form handler with its own plugin (`bef`), which extends `InputRequired`. Three plugin types:

1. **Filter widgets** — Alter how individual exposed filters render
2. **Sort widgets** — Alter how exposed sort controls render
3. **Pager widgets** — Alter how exposed pager controls render

**Services:**
- `better_exposed_filters.bef_helper` — Static utility methods
- `plugin.manager.better_exposed_filters_filter_widget` — Filter widget manager
- `plugin.manager.better_exposed_filters_sort_widget` — Sort widget manager
- `plugin.manager.better_exposed_filters_pager_widget` — Pager widget manager

**Main plugin:** `BetterExposedFilters` (ID: `bef`) at `src/Plugin/views/exposed_form/BetterExposedFilters.php`

## Common Mistakes

- **Wrong**: Using BEF without first exposing filters in the View → **Right**: BEF only enhances filters already exposed in the View. Expose the filter in Views UI first.
- **Wrong**: Using BEF for sliders without the noUiSlider library → **Right**: Sliders require `drupal/nouislider_js`; verify files exist at `/libraries/nouislider/`.
- **Wrong**: Confusing BEF with Facets → **Right**: BEF enhances Views exposed forms. Facets is a separate system for Search API. They can work together but serve different purposes.

## See Also

- [Installation & Setup](installation-setup.md)
- [General Settings](general-settings.md)
- [Integration Patterns](integration-patterns.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/views/exposed_form/BetterExposedFilters.php`
