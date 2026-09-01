---
description: "The facets_searchbox_widget sub-module for type-to-filter facet item lists"
tldr: "Use this guide when a facet has many items and you want users to type-to-filter the visible options client-side via JavaScript."
drupal_version: "11.x"
---

# Searchbox Widget

## When to Use

> When a facet has many items and you want users to type-to-filter the visible options.

## Decision: Searchbox Sub-Module

**Module:** `facets_searchbox_widget`

**Widgets:**

| ID | Class | Purpose |
|---|---|---|
| `searchbox_links` | SearchboxLinksWidget | Links with search input above |
| `searchbox_checkbox` | SearchboxCheckboxWidget | Checkboxes with search input above |

Both widgets add a text input that filters the facet item list client-side via JavaScript.

## Pattern: Setup

```bash
drush en facets_searchbox_widget
```

Select "Searchbox Links" or "Searchbox Checkbox" as the widget in facet configuration.

## Common Mistakes

- **Expecting server-side filtering from the searchbox** — The searchbox filters the already-rendered item list client-side; it does not requery the backend.

## See Also

- [Widgets](widgets.md) — standard widgets
- Reference: `modules/facets_searchbox_widget/`
