---
description: "BEF theming — available templates, theme suggestions by view/display/field, preprocess functions, and nested hierarchy rendering"
tldr: "Use this guide when you need to customize the HTML output of BEF widgets in your theme."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> When you need to customize the HTML output of BEF widgets in your theme.

## Decision: Available Templates

| Template | Theme Hook | Used By |
|---|---|---|
| `bef-checkboxes.html.twig` | `bef_checkboxes` | Checkboxes widget (multi-select) |
| `bef-radios.html.twig` | `bef_radios` | Radio buttons widget (single-select) |
| `bef-links.html.twig` | `bef_links` | Links widget |
| `bef-hidden.html.twig` | `bef_hidden` | Hidden widget (multi-value) |
| `bef-number.html.twig` | `bef_number` | Number widget |
| `bef-nested-elements.html.twig` | N/A | Included template for hierarchical rendering |

## Pattern: Template Suggestions

BEF adds view-specific, display-specific, and field-specific suggestions via `hook_theme_suggestions_alter()`:

```
bef_checkboxes__VIEW_ID
bef_checkboxes__VIEW_ID__FIELD_NAME
bef_checkboxes__VIEW_ID__DISPLAY_ID
bef_checkboxes__VIEW_ID__DISPLAY_ID__FIELD_NAME
```

Same pattern for `bef_radios`, `bef_links`, `bef_hidden`, `bef_number`, and `form_element`.

**Requirement:** The element must have `#context.#plugin_type === 'bef'` — which BEF adds via `addContext()`.

## Pattern: Preprocess Functions

| Function | Template | Key Variables |
|---|---|---|
| `template_preprocess_bef_checkboxes()` | bef-checkboxes | `children`, `show_select_all_none`, `show_select_all_none_nested`, `display_inline`, `is_nested`, `depth`, `wrapper_attributes` |
| `template_preprocess_bef_radios()` | bef-radios | `children`, `display_inline`, `is_nested`, `depth`, `wrapper_attributes` |
| `template_preprocess_bef_links()` | bef-links | `links`, `children`, `selected`, `hiddens`, `is_nested` |
| `template_preprocess_bef_hidden()` | bef-hidden | `is_multiple`, `selected`, `hidden_elements` |
| `template_preprocess_bef_number()` | bef-number | `children`, `display_inline` |
| `better_exposed_filters_preprocess_views_exposed_form()` | views-exposed-form | Token replacement in filter descriptions (requires Token module) |

## Pattern: Nested Elements

Hierarchical taxonomy filters render as nested `<ul>` lists. The `_bef_preprocess_nested_elements()` function:

1. Sets `$variables['is_nested'] = TRUE`
2. Calculates `$variables['depth']` — number of leading hyphens stripped from each option's title
3. The template uses `bef-nested-elements.html.twig` (included) to recursively render levels

## Common Mistakes

- **Template override not applying** — Check the template suggestion name. Use Twig debug to see available suggestions: `{{ dump(_context) }}`.
- **Missing wrapper_attributes** — Checkboxes and radios have `wrapper_attributes` separate from element `attributes`. Use both in custom templates.
- **Breaking nested rendering** — When overriding bef-checkboxes or bef-radios, preserve the `is_nested` / `depth` logic or hierarchical filters will render flat.

## See Also

- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md) — template variable details
- [Links Widget](links-widget.md) — links template variables
- Reference: `web/modules/contrib/better_exposed_filters/templates/`
- Reference: `web/modules/contrib/better_exposed_filters/includes/better_exposed_filters.theme.inc`
