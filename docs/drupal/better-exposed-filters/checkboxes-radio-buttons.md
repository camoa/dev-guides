---
description: BEF checkboxes and radio buttons widget — plugin ID, applicable filter types, soft limit, select all/none, and nested hierarchy
tldr: "Use this widget when you want to replace a select dropdown with checkboxes (multi-select) or radio buttons (single-select) on an exposed filter. Use the Links widget when you want clickable URL-based navigation instead."
drupal_version: "11.x"
---

# Checkboxes & Radio Buttons Widget

## When to Use

> Use this widget when you want to replace a select dropdown with checkboxes (multi-select) or radio buttons (single-select) on an exposed filter. Use the Links widget when you want clickable URL-based navigation instead.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Multi-select filter | Checkboxes | "Allow multiple selections" is on — BEF renders `checkboxes` |
| Single-select filter | Radio buttons | "Allow multiple selections" is off — BEF renders `radios` |
| Taxonomy hierarchy | Checkboxes with `#bef_nested` | Adds `<ul>` nesting via `_bef_preprocess_nested_elements()` |

**Plugin details:**

| Property | Value |
|---|---|
| Plugin ID | `bef` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\RadioButtons` |
| Template (multi) | `bef-checkboxes.html.twig` |
| Template (single) | `bef-radios.html.twig` |

**Applicable filter types:** `InOperator`, `StringFilter` (in/or/and/not operators), `BooleanOperator`, `TaxonomyIndexTid` (select type only), grouped filters, `SearchApiFulltext`, `FacetsFilter`

**Widget-specific configuration:**

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Select all/none | `select_all_none` | FALSE | Adds "Select All / None" links (requires "Allow multiple selections") |
| Nested all/none | `select_all_none_nested` | FALSE | Parent checkbox toggles all children (requires hierarchy + multiple) |
| Display inline | `display_inline` | FALSE | Render options horizontally |
| Soft limit | `soft_limit` | 0 | Show only N items, with "Show more" link |

## Pattern

```php
// Multi-select → checkboxes
$form[$field_id]['#theme'] = 'bef_checkboxes';
$form[$field_id]['#type'] = 'checkboxes';

// Single-select → radio buttons
$form[$field_id]['#theme'] = 'bef_radios';
$form[$field_id]['#type'] = 'radios';

// Hierarchical taxonomy
$form[$field_id]['#bef_nested'] = TRUE; // triggers nested <ul> rendering
```

## Common Mistakes

- **Wrong**: Enabling "Select all/none" without "Allow multiple selections" on the filter → **Right**: Edit the filter, check "Allow multiple selections" first.
- **Wrong**: Enabling "Nested all/none" on non-hierarchical filters → **Right**: Requires both "Allow multiple selections" AND "Show hierarchy in dropdown" on the filter.
- **Wrong**: Expecting soft limit to work without the JS library → **Right**: Soft limit requires `better_exposed_filters/soft_limit` library. Check browser console for JS errors.

## See Also

- [Theming & Templates](theming-templates.md)
- [Option Rewriting & Sorting](option-rewriting-sorting.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/filter/RadioButtons.php`
