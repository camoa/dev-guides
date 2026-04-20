---
description: BEF theming — available templates, theme suggestions by view/display/field, preprocess functions, and nested hierarchy rendering
tldr: "Use this guide when you need to customize the HTML output of BEF widgets in your theme."
drupal_version: "11.x"
---

# Theming & Templates

## When to Use

> Use this guide when you need to customize the HTML output of BEF widgets in your theme.

## Decision

| Template | Theme Hook | Used By |
|---|---|---|
| `bef-checkboxes.html.twig` | `bef_checkboxes` | Checkboxes widget (multi-select) |
| `bef-radios.html.twig` | `bef_radios` | Radio buttons widget (single-select) |
| `bef-links.html.twig` | `bef_links` | Links widget |
| `bef-hidden.html.twig` | `bef_hidden` | Hidden widget (multi-value) |
| `bef-number.html.twig` | `bef_number` | Number widget |
| `bef-nested-elements.html.twig` | N/A | Included for hierarchical rendering |

## Pattern

**Template suggestions** (BEF adds via `hook_theme_suggestions_alter()`):
```
bef_checkboxes__VIEW_ID
bef_checkboxes__VIEW_ID__FIELD_NAME
bef_checkboxes__VIEW_ID__DISPLAY_ID
bef_checkboxes__VIEW_ID__DISPLAY_ID__FIELD_NAME
```

Same pattern for `bef_radios`, `bef_links`, `bef_hidden`, `bef_number`, and `form_element`.

**Requirement:** Element must have `#context.#plugin_type === 'bef'` (added by BEF via `addContext()`).

**Preprocess functions and key variables:**

| Function | Template | Key Variables |
|---|---|---|
| `template_preprocess_bef_checkboxes()` | bef-checkboxes | `children`, `show_select_all_none`, `display_inline`, `is_nested`, `depth`, `wrapper_attributes` |
| `template_preprocess_bef_radios()` | bef-radios | `children`, `display_inline`, `is_nested`, `depth`, `wrapper_attributes` |
| `template_preprocess_bef_links()` | bef-links | `links`, `selected`, `hiddens`, `is_nested` |
| `template_preprocess_bef_hidden()` | bef-hidden | `is_multiple`, `selected`, `hidden_elements` |

**Nested hierarchy rendering:** `_bef_preprocess_nested_elements()` sets `is_nested = TRUE` and calculates `depth` (number of leading hyphens stripped from each option). The template uses `bef-nested-elements.html.twig` to render levels.

## Common Mistakes

- **Wrong**: Override not applying because template suggestion name is wrong → **Right**: Enable Twig debug and check available suggestions: `{{ dump(_context) }}`.
- **Wrong**: Custom template ignores `wrapper_attributes` → **Right**: Checkboxes and radios have `wrapper_attributes` separate from element `attributes`. Use both.
- **Wrong**: Custom template removes `is_nested` / `depth` logic → **Right**: Hierarchical filters will render flat without this logic.

## See Also

- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md)
- [Links Widget](links-widget.md)
- Reference: `web/modules/contrib/better_exposed_filters/templates/`
- Reference: `web/modules/contrib/better_exposed_filters/includes/better_exposed_filters.theme.inc`
