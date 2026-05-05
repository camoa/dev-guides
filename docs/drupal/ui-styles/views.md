---
description: Style Views display wrapper, pager, and exposed filter form via UI Styles instead of preprocess hooks.
tldr: Enable ui_styles_views; each Views display configuration gains UI Styles fieldsets for the display wrapper, pager, and exposed form. Display-level styles target the outer View wrapper — per-row styling still requires template overrides or field formatters.
drupal_version: "11.x"
---

# Integration: Views

## When to Use

> Use this guide when styling the wrapper of a Views display, the pager, or the exposed-filter form via curated class options instead of preprocess hooks.

## Decision

| Style location | Applies to |
|---|---|
| Display | Outer wrapper — grid/list layout switches, max-width, padding |
| Pager | Pager-specific spacing, alignment |
| Exposed form | Filter form layout (horizontal vs stacked) |

## Pattern

Enable `ui_styles_views`. Each Views display configuration form gains UI Styles fieldsets for:

- **Display wrapper** — outer `<div>` of the View
- **Pager** — pager element
- **Exposed form** — the filter form wrapper

Selections are stored on the Views display configuration.

## Common Mistakes

- **Applying display styles to fix per-row issues** → Per-row styling needs a Views row template override or field formatter, not display-level classes

## See Also

- [Integration: Block Layout](block-layout.md)
- [Anti-Patterns](anti-patterns.md)
- Reference: `modules/ui_styles_views/` in the UI Styles module
