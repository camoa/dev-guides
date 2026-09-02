---
description: "BEF integration patterns — Views AJAX, Facets, Search API, Select2, Chosen, and companion contrib modules"
tldr: "Use this guide when combining BEF with other Drupal modules — Views AJAX, Facets, Search API, Select2, or Chosen."
drupal_version: "11.x"
---

# Integration Patterns

## When to Use

> When combining BEF with other Drupal modules — Views AJAX, Facets, Search API, Select2, or Chosen.

## Decision: BEF + Views AJAX

| Aspect | Behavior |
|---|---|
| Auto-submit | Works with AJAX — submits via AJAX instead of page reload |
| Links widget | Automatically adds `bef-links-use-ajax` class when View has AJAX enabled |
| Sliders | Work with AJAX — slider values trigger AJAX submit |
| Focus restoration | After AJAX refresh, BEF refocuses the last-triggered element |

**Enable:** Views UI → Advanced → Use AJAX: Yes. BEF detects this automatically.

## Decision: BEF + Facets

BEF explicitly supports `Drupal\facets_exposed_filters\Plugin\views\filter\FacetsFilter` in its `isApplicable()` logic. The Facets Exposed Filters sub-module bridges Facets with Views exposed forms, and BEF can then render those as checkboxes, links, etc.

## Decision: BEF + Search API

BEF supports `Drupal\search_api\Plugin\views\filter\SearchApiFulltext` — fulltext search filters from Search API work with BEF widgets. Other Search API filters that extend standard Views filter classes also work.

## Decision: BEF + Select2 / Chosen

Auto-submit JS explicitly excludes `.select2-search__field` and `.chosen-search-input` from triggering auto-submit. This prevents double-submission when these libraries fire change events during their own initialization.

## Decision: Integration Modules

| Module | Integration |
|---|---|
| [Select2](https://www.drupal.org/project/select2) | Additional widget options for exposed filters |
| [Selective BEF](https://www.drupal.org/project/selective_better_exposed_filters) | Show only filter options that have results |
| [Configurable Views Filter Block](https://www.drupal.org/project/configurable_views_filter_block) | Expose filters in configurable blocks |
| [Views Dependent Filters](https://www.drupal.org/project/views_dependent_filters) | Show/hide filters based on other filter values |
| [Token](https://www.drupal.org/project/token) | Token replacement in filter descriptions |

## Common Mistakes

- **BEF + Facets without facets_exposed_filters** — Facets uses its own rendering system. To use BEF with Facets, you need the `facets_exposed_filters` sub-module as a bridge.
- **Auto-submit + Select2 conflict** — Older versions of Select2 may trigger change events that confuse auto-submit. Update to latest versions.
- **AJAX + exposed form as block** — When the exposed form is a block and the View uses AJAX, the form and results may be in different DOM regions. AJAX commands target the View's wrapper, which works, but layout jumps can occur.

## See Also

- [Overview](overview.md) — BEF vs Facets distinction
- [Auto-Submit](auto-submit.md) — auto-submit with AJAX
