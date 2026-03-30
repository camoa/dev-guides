---
description: Facets built-in widgets — links, checkbox, dropdown, array — configuration options, data attributes, and rendering
drupal_version: "11.x"
---

# Widgets

## When to Use

> Use this guide when choosing how facet results should be rendered to the user.

## Decision

| ID | Class | Template Suffix | Features | Best For |
|---|---|---|---|---|
| `links` | LinksWidget | `--links` | Soft limit, reset link, AJAX-ready | Default, most use cases |
| `checkbox` | CheckboxWidget | `--checkbox` | Extends links with checkbox UI | Multi-select with visual checkboxes |
| `dropdown` | DropdownWidget | `--dropdown` | HTML `<select>` element | Space-constrained UI, single-select |
| `array` | ArrayWidget | — | Returns PHP array (no HTML) | REST API, programmatic use |

**LinksWidget configuration:**

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Soft limit | `soft_limit` | 0 | Show N items with "Show more" toggle |
| Show more label | `soft_limit_settings.show_more_label` | 'Show more' | Expand link text |
| Show less label | `soft_limit_settings.show_less_label` | 'Show fewer' | Collapse link text |
| Show reset link | `show_reset_link` | FALSE | "Show all" link to clear facet |
| Hide reset when no selection | `hide_reset_when_no_selection` | FALSE | Only show reset when active |
| Reset text | `reset_text` | 'Show all' | Reset link label |

## Pattern

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

**Data attributes on widget container:**

| Attribute | Value | Purpose |
|---|---|---|
| `data-drupal-facet-id` | Facet machine name | JS targeting |
| `data-drupal-facet-alias` | URL alias | URL parameter mapping |
| `data-drupal-facet-filter-key` | Filter key (e.g., 'f') | URL query param name |

## Common Mistakes

- **Wrong**: Expecting CheckboxWidget to use HTML form checkboxes natively → **Right**: `CheckboxWidget` extends `LinksWidget`. It renders as links with checkbox styling. Actual form checkboxes require JavaScript.
- **Wrong**: Using dropdown with Views AJAX without verifying JS behavior → **Right**: The dropdown widget uses JS to trigger navigation on change. With AJAX views, this works via the `dropdown-widget.js` behavior.
- **Wrong**: Setting `soft_limit: 0` expecting it to be hidden → **Right**: Zero means "show all items." Set a positive number to enable show more/less.

## See Also

- [Range Slider Widget](range-slider.md) — for numeric ranges
- [Theming & Templates](theming-templates.md) — customizing widget output
- Reference: `web/modules/contrib/facets/src/Plugin/facets/widget/`
