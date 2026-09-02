---
description: "BEF checkboxes and radio buttons widget — plugin ID, applicable filter types, soft limit, select all/none, and nested hierarchy"
tldr: "Use this widget when you want to replace a select dropdown with checkboxes (for multi-select) or radio buttons (for single-select) on an exposed filter."
drupal_version: "11.x"
---

# Checkboxes & Radio Buttons Widget

## When to Use

> When you want to replace a select dropdown with checkboxes (for multi-select) or radio buttons (for single-select) on an exposed filter.

## Decision: Plugin Details

| Property | Value |
|---|---|
| Plugin ID | `bef` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\RadioButtons` |
| Attribute | `#[FiltersWidget(id: 'bef', title: 'Checkboxes/Radio Buttons')]` |
| Template (multi) | `bef-checkboxes.html.twig` |
| Template (single) | `bef-radios.html.twig` |

## Decision: Applicability (isApplicable)

The widget is available for:
- `InOperator` filters with operators: in, or, and, not, empty, not empty
- `StringFilter` with operators: in, or, and, not, empty, not empty
- `BooleanOperator` filters
- `TaxonomyIndexTid` filters (only when type is 'select', not autocomplete)
- Grouped filters (`isAGroup()`)
- `SearchApiFulltext` filters
- `FacetsFilter` filters

## Decision: Widget-Specific Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Select all/none | `select_all_none` | FALSE | Adds "Select All / None" links (requires "Allow multiple selections") |
| Nested all/none | `select_all_none_nested` | FALSE | Parent checkbox toggles all children (requires hierarchy + multiple) |
| Display inline | `display_inline` | FALSE | Render options horizontally |
| Soft limit | `soft_limit` | 0 | Show only N items, with "Show more" link (values: 3, 5, 10, 15, 20, 30, 40, 50) |
| Show less label | `soft_limit_label_less` | 'Show less' | Custom text for collapse link |
| Show more label | `soft_limit_label_more` | 'Show more' | Custom text for expand link |

## Pattern: How It Renders

```
# Multi-select → checkboxes
$form[$field_id]['#theme'] = 'bef_checkboxes';
$form[$field_id]['#type'] = 'checkboxes';

# Single-select → radio buttons
$form[$field_id]['#theme'] = 'bef_radios';
$form[$field_id]['#type'] = 'radios';
```

For hierarchical taxonomy filters, adds `#bef_nested = TRUE` which triggers nested `<ul>` rendering via `_bef_preprocess_nested_elements()`.

## Pattern: Template Variables (bef-checkboxes)

| Variable | Type | Description |
|---|---|---|
| `element` | array | The form element |
| `children` | array | Child element keys |
| `show_select_all_none` | bool | Render select all/none links |
| `show_select_all_none_nested` | bool | Nested hierarchy select |
| `display_inline` | bool | Render items inline |
| `is_nested` | bool | Hierarchical rendering |
| `depth` | array | Nesting level per child |
| `wrapper_attributes` | Attribute | Wrapper HTML attributes |

## Common Mistakes

- **Select all/none disabled** — This option requires "Allow multiple selections" on the filter. Edit the filter and check that box first.
- **Nested all/none disabled** — Requires both "Allow multiple selections" AND "Show hierarchy in dropdown" enabled on the filter.
- **Soft limit not working** — Requires the `better_exposed_filters/soft_limit` library. Check browser console for JS errors.

## See Also

- [Theming & Templates](theming-templates.md) — overriding bef-checkboxes.html.twig
- [Option Rewriting & Sorting](option-rewriting-sorting.md) — rewriting checkbox labels
