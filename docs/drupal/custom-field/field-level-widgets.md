---
description: Stacked and flexbox layout widgets for controlling how the entire custom field displays on the edit form. CustomFlexWidget ships its own CSS grid, not Bootstrap.
tldr: "You need to control how the entire custom field (all sub-fields together) is laid out on the edit form. CustomFlexWidget uses the module's own 12-column CSS grid, not Bootstrap -- works in any theme."
---

# Field-Level Widgets

## When to Use

You need to control how the entire custom field (all sub-fields together) is laid out on the edit form.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Vertical stacking (default) | CustomStackedWidget | Simplest layout, sub-fields stack vertically |
| Side-by-side columns | CustomFlexWidget | The module's own 12-column CSS flexbox grid, with an optional breakpoint below which columns stack. Theme-independent |

## CustomStackedWidget

Stacks sub-field widgets vertically (default field widget).

- **Plugin ID:** `custom_stacked`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| wrapper | string | `details` | Wrapper element around each delta |
| label_value | string | '' | Sub-field whose value is used as the delta label |
| label_limit | integer | 60 | Truncation length for that label |
| label_prefix | string | `Item` | Prefix when no `label_value` is set |
| auto_collapse | boolean | -- | Collapse a delta once it has a value |
| open | boolean | -- | Whether the wrapper starts expanded |
| fields | array | [] | Per-sub-field widget settings (inherited) |

**Layout:** Each sub-field renders full-width, one below the other

```yaml
# In field display config
type: custom_stacked
settings:
  fields:
    street:
      type: text
      weight: 0
    city:
      type: text
      weight: 1
```

**Gotchas:** Sub-field order controlled by weight in field settings. No responsive control.

## CustomFlexWidget

Lays sub-fields out side by side on a 12-column flexbox grid. **This is not Bootstrap.** The widget emits the module's own `custom-field-row` / `custom-field-col-N` classes and attaches the module's own `custom_field/custom-field-flex` library (`css/custom-field-flex.css`), so it works in any theme with no CSS framework installed.

- **Plugin ID:** `custom_flex`

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| columns | array | [] | Per-sub-field integer width on the 12-column grid |
| breakpoint | string | '' | Viewport below which columns stack. `''` = "Don't stack", `medium` = below 769px, `small` = below 601px |
| fields | array | [] | Per-sub-field widget settings (inherited) |

**Layout:** Wraps sub-fields in `.custom-field-row`, each sub-field in `.custom-field-col-{1..12}`

```yaml
type: custom_flex
settings:
  breakpoint: medium
  columns:
    first_name: 6
    last_name: 6
```

**Gotchas:** Widths are integers out of 12, not class names -- a sub-field left unset takes the full row. Choosing a `breakpoint` is what makes the layout responsive; with `''` the columns never stack.

## Common Mistakes

- **Setting `columns` values that don't sum to 12 per row** -- Sub-fields wrap to the next row; check the totals if the layout breaks unexpectedly
- **Leaving `breakpoint` at "Don't stack" on a narrow form** -- Columns stay side by side at every width, which squeezes sub-field widgets on mobile and in narrow sidebars
- **Looking for a gap or gutter setting** -- There is none; spacing comes from the module's stylesheet. Override it in your theme's CSS if you need different spacing

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/Field/FieldWidget/CustomFlexWidget.php`
- Reference: `/modules/contrib/custom_field/css/custom-field-flex.css` -- the grid the widget ships with
- Reference: `/modules/contrib/custom_field/templates/custom-field-flex-wrapper.html.twig`
