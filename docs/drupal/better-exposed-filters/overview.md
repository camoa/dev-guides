---
description: "BEF vs core exposed filters — capabilities, architecture, and when to use Better Exposed Filters"
tldr: "Use Better Exposed Filters when you need more control over how Views exposed filters are rendered — replacing default select dropdowns with checkboxes, radio buttons, links, sliders, date pickers, or other widgets."
drupal_version: "11.x"
---

# Overview

## When to Use

> When you need more control over how Views exposed filters are rendered — replacing default select dropdowns with checkboxes, radio buttons, links, sliders, date pickers, or other widgets.

## Decision: BEF vs Core Exposed Filters

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

## Pattern: Architecture

BEF replaces the Views exposed form handler with its own plugin (`bef`), which extends `InputRequired`. It uses a **three-type plugin system**:

1. **Filter widgets** — Alter how individual exposed filters render
2. **Sort widgets** — Alter how exposed sort controls render
3. **Pager widgets** — Alter how exposed pager controls render

Each type has its own plugin manager service and widget base class. Widgets are discovered via PHP 8.1 Attributes (Drupal 11) with legacy Annotation fallback.

**Services:**
- `better_exposed_filters.bef_helper` — Static utility methods
- `plugin.manager.better_exposed_filters_filter_widget` — Filter widget manager
- `plugin.manager.better_exposed_filters_sort_widget` — Sort widget manager
- `plugin.manager.better_exposed_filters_pager_widget` — Pager widget manager

**Main plugin:** `BetterExposedFilters` (ID: `bef`) at `src/Plugin/views/exposed_form/BetterExposedFilters.php` — extends `InputRequired`, orchestrates all widget plugins.

## Common Mistakes

- **Expecting BEF to work without exposed filters** — BEF only enhances filters that are already exposed in the View. You must first expose the filter in Views UI.
- **Forgetting the noUiSlider library** — Sliders require the `drupal/nouislider_js` library. Composer installs it, but the JS library files must be in `/libraries/nouislider/`.
- **Confusing BEF with Facets** — BEF enhances Views exposed forms. Facets is a separate system for Search API. They can work together but serve different purposes.

## See Also

- [Installation & Setup](installation-setup.md) — getting BEF running
- [General Settings](general-settings.md) — global BEF configuration
- [Integration Patterns](integration-patterns.md) — BEF with AJAX, Facets, Search API
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/views/exposed_form/BetterExposedFilters.php`
