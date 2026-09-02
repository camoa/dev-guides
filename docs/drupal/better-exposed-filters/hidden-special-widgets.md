---
description: "BEF hidden, single checkbox, and number widgets — plugin IDs, applicability, and treat_as_false behavior"
tldr: "Use hidden, single checkbox, or number widgets to hide a filter from the user, render a boolean as a single checkbox, or constrain a numeric input."
drupal_version: "11.x"
---

# Hidden & Special Widgets

## When to Use

> When you need to hide a filter from the user, render a boolean as a single checkbox, or constrain a numeric input.

## Decision: Hidden Widget (`bef_hidden`)

| Property | Value |
|---|---|
| Plugin ID | `bef_hidden` |
| Class | `Hidden` |
| Template | `bef-hidden.html.twig` (multi-value only) |

**Behavior:**
- Single-value: converts to `#type => 'hidden'` — standard hidden input
- Multi-value: uses `bef_hidden` theme — renders multiple hidden inputs with selected values

**Applicability:** All filters that match base `FilterWidgetBase::isApplicable()`, plus Date filters.

**Use case:** Pre-set filter values via URL parameters or defaults, without showing the filter to the user.

## Decision: Single On/Off Checkbox (`bef_single`)

| Property | Value |
|---|---|
| Plugin ID | `bef_single` |
| Class | `Single` |
| Config | `treat_as_false` (default: FALSE) |

**Applicability:** `BooleanOperator` filters, or grouped filters with exactly 1 group item.

**Behavior:**
- Converts the filter to a single checkbox (`#type => 'checkbox'`)
- Adds a hidden fallback input (`#type => 'hidden'`, value 0) so unchecked state is submitted
- **treat_as_false:** When FALSE (default), unchecked = "ANY" (show all). When TRUE, unchecked = FALSE (filter to false values).

**The checkbox problem:** In HTML, unchecked checkboxes are not included in form submissions. BEF adds a hidden input with the same `name` and value `0` to ensure the unchecked state is always submitted.

## Decision: Number Widget (`bef_number`)

| Property | Value |
|---|---|
| Plugin ID | `bef_number` |
| Class | `Number` |
| Template | `bef-number.html.twig` |
| Config | `min` (NULL), `max` (NULL) |

**Applicability:** `NumericFilter` only.

**Behavior:** Converts text inputs to `<input type="number">` with optional HTML5 `min` and `max` attributes. For "between" operators, converts both min and max fields.

## Common Mistakes

- **Hidden filter not filtering** — Hidden filters still need a default value or URL parameter to be effective. A hidden filter with no value does nothing.
- **Single checkbox always checked** — This is a known complexity. BEF handles the checkbox state via user input parsing, not the default value. If it seems stuck, check the form state logic.
- **Number min/max vs slider min/max** — The Number widget uses HTML5 `min`/`max` attributes (browser validation only). The Slider widget uses noUiSlider (visual constraint). Different mechanisms.

## See Also

- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md) — for multi-value boolean filters
- [Sliders Widget](sliders-widget.md) — for visual numeric ranges
