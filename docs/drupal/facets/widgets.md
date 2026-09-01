---
description: "Built-in facet widgets — links, checkbox, dropdown, array — and their configuration"
tldr: "Use this guide when choosing how facet results should be rendered to the user. Links is the default; checkbox extends it visually; dropdown suits space-constrained single-select; array returns raw PHP for REST."
drupal_version: "11.x"
---

# Widgets

## When to Use

> When choosing how facet results should be rendered to the user.

## Decision: Built-In Widgets

| ID | Class | Template Suffix | Features | Best For |
|---|---|---|---|---|
| `links` | LinksWidget | `--links` | Soft limit, reset link, AJAX-ready | Default, most use cases |
| `checkbox` | CheckboxWidget | `--checkbox` | Extends links with checkbox UI | Multi-select with visual checkboxes |
| `dropdown` | DropdownWidget | `--dropdown` | HTML `<select>` element | Space-constrained UI, single-select |
| `array` | ArrayWidget | — | Returns PHP array (no HTML) | REST API, programmatic use |

## Decision: LinksWidget Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Soft limit | `soft_limit` | 0 | Show N items with "Show more" toggle |
| Show more label | `soft_limit_settings.show_more_label` | 'Show more' | Expand link text |
| Show less label | `soft_limit_settings.show_less_label` | 'Show fewer' | Collapse link text |
| Show reset link | `show_reset_link` | FALSE | "Show all" link to clear facet |
| Hide reset when no selection | `hide_reset_when_no_selection` | FALSE | Only show reset when active |
| Reset text | `reset_text` | 'Show all' | Reset link label |

## Pattern: Widget Rendering

All widgets extend `WidgetPluginBase` which provides:

```php
// Build the facet render array
public function build(FacetInterface $facet): array {
  // Returns render array with:
  // - #theme: facets_item_list__WIDGET_TYPE
  // - #items: Rendered result items
  // - #attributes: data-drupal-facet-id, data-drupal-facet-alias, etc.
  // - #context: ['list_style' => 'links|checkbox|dropdown']
  // - #cache: Cache metadata from facet
}
```

## Pattern: Data Attributes on Widget Container

| Attribute | Value | Purpose |
|---|---|---|
| `data-drupal-facet-id` | Facet machine name | JS targeting |
| `data-drupal-facet-alias` | URL alias | URL parameter mapping |
| `data-drupal-facet-filter-key` | Filter key (e.g., 'f') | URL query param name |

## Common Mistakes

- **Checkbox widget is links underneath** — `CheckboxWidget` extends `LinksWidget`. It renders as links with checkbox styling. Actual form checkboxes require JavaScript.
- **Dropdown with AJAX** — The dropdown widget uses JS to trigger navigation on change. With AJAX views, this works via the `dropdown-widget.js` behavior.
- **Soft limit = 0** — Zero means "show all items." Set a positive number to enable show more/less.

## See Also

- [Range Slider Widget](range-slider.md) — for numeric ranges
- [Theming & Templates](theming-templates.md) — customizing widget output
- Reference: `src/Plugin/facets/widget/`
