---
description: BEF integration patterns — Views AJAX, Facets, Search API, Select2, Chosen, and companion contrib modules
drupal_version: "11.x"
---

# Integration Patterns

## When to Use

> Use this guide when combining BEF with other Drupal modules — Views AJAX, Facets, Search API, Select2, or Chosen.

## Decision

**BEF + Views AJAX:**

| Aspect | Behavior |
|---|---|
| Auto-submit | Works — submits via AJAX instead of page reload |
| Links widget | Auto-adds `bef-links-use-ajax` class when View has AJAX |
| Sliders | Work — slider values trigger AJAX submit |
| Focus restoration | After AJAX refresh, BEF refocuses the last-triggered element |

Enable: Views UI → Advanced → Use AJAX: Yes. BEF detects this automatically.

**BEF + Facets:** Requires the `facets_exposed_filters` sub-module as a bridge. BEF explicitly supports `FacetsFilter` in its `isApplicable()` logic.

**BEF + Search API:** `SearchApiFulltext` filters work with BEF widgets. Other Search API filters that extend standard Views filter classes also work.

**BEF + Select2 / Chosen:** Auto-submit JS excludes `.select2-search__field` and `.chosen-search-input` to prevent double-submission.

**Companion contrib modules:**

| Module | Integration |
|---|---|
| [Select2](https://www.drupal.org/project/select2) | Additional widget options for exposed filters |
| [Selective BEF](https://www.drupal.org/project/selective_better_exposed_filters) | Show only filter options that have results |
| [Views Dependent Filters](https://www.drupal.org/project/views_dependent_filters) | Show/hide filters based on other filter values |
| [Token](https://www.drupal.org/project/token) | Token replacement in filter descriptions |

## Pattern

```
# Enabling AJAX on a View (BEF detects it automatically):
Views UI → Advanced → Use AJAX → Yes

# BEF + Facets setup:
1. Enable facets_exposed_filters sub-module
2. Configure Facets sources as Views exposed filters
3. BEF can then render those as checkboxes, links, etc.
```

## Common Mistakes

- **Wrong**: Trying to use BEF widgets on Facets without `facets_exposed_filters` → **Right**: Facets uses its own rendering. The bridge sub-module is required.
- **Wrong**: Older Select2 versions conflicting with auto-submit → **Right**: Older Select2 may trigger change events that confuse auto-submit. Update to latest versions.
- **Wrong**: AJAX + exposed form as block expecting no layout issues → **Right**: When the form is a block and the View uses AJAX, layout jumps can occur. AJAX commands target the View's wrapper correctly, but test the UX.

## See Also

- [Overview](overview.md)
- [Auto-Submit](auto-submit.md)
- Reference: https://www.drupal.org/project/better_exposed_filters
