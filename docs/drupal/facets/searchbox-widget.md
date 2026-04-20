---
description: Facets searchbox widget — facets_searchbox_widget sub-module for type-to-filter facet items client-side
tldr: "Use this guide when a facet has many items and you want users to type to filter the visible options client-side."
drupal_version: "11.x"
---

# Searchbox Widget

## When to Use

> Use this guide when a facet has many items and you want users to type to filter the visible options client-side.

## Decision

**Module:** `facets_searchbox_widget`

| ID | Class | Purpose |
|---|---|---|
| `searchbox_links` | SearchboxLinksWidget | Links with search input above |
| `searchbox_checkbox` | SearchboxCheckboxWidget | Checkboxes with search input above |

Both widgets add a text input that filters the facet item list client-side via JavaScript. The filtering is purely presentational — it does not trigger a new search query.

## Pattern

```bash
drush en facets_searchbox_widget
```

Select "Searchbox Links" or "Searchbox Checkbox" as the widget in facet configuration.

## Common Mistakes

- **Wrong**: Expecting the searchbox to search the full index → **Right**: The searchbox only filters the already-loaded list of facet items client-side. It does not query the search backend.

## See Also

- [Widgets](widgets.md) — standard widgets
- Reference: `web/modules/contrib/facets/modules/facets_searchbox_widget/`
