---
description: BEF hidden, single checkbox, and number widgets — plugin IDs, applicability, and treat_as_false behavior
drupal_version: "11.x"
---

# Hidden & Special Widgets

## When to Use

> Use the hidden widget to pre-set filter values without showing them to users. Use the single checkbox widget for boolean filters (on/off). Use the number widget to constrain numeric inputs with HTML5 min/max attributes.

## Decision

**Hidden widget (`bef_hidden`):**

| Property | Value |
|---|---|
| Plugin ID | `bef_hidden` |
| Template | `bef-hidden.html.twig` (multi-value only) |
| Applicable | All base-applicable filters, plus Date filters |

- Single-value: converts to `#type => 'hidden'` — standard hidden input
- Multi-value: uses `bef_hidden` theme — renders multiple hidden inputs

**Single on/off checkbox (`bef_single`):**

| Property | Value |
|---|---|
| Plugin ID | `bef_single` |
| Config | `treat_as_false` (default: FALSE) |
| Applicable | `BooleanOperator` filters, or grouped filters with exactly 1 group item |

| `treat_as_false` | Unchecked means |
|---|---|
| FALSE (default) | "ANY" — show all results |
| TRUE | FALSE — filter to false values |

BEF adds a hidden fallback input (value `0`) so unchecked state is always submitted (HTML unchecked checkboxes are not sent).

**Number widget (`bef_number`):**

| Property | Value |
|---|---|
| Plugin ID | `bef_number` |
| Template | `bef-number.html.twig` |
| Config | `min` (NULL), `max` (NULL) |
| Applicable | `NumericFilter` only |

Converts text inputs to `<input type="number">` with optional HTML5 `min` and `max` attributes. For "between" operators, converts both fields.

## Pattern

```php
// Hidden widget — set a default value via URL parameter:
// /view-path?field_status=1

// Single checkbox — treat_as_false = TRUE
// Unchecked = filter to items where boolean = FALSE
// Checked = filter to items where boolean = TRUE

// Number widget — HTML5 browser validation
// <input type="number" min="0" max="100">
```

## Common Mistakes

- **Wrong**: Using a hidden filter without a default value or URL parameter → **Right**: A hidden filter with no value does nothing. Set defaults or populate via URL.
- **Wrong**: Confusing Number widget min/max with Slider min/max → **Right**: Number widget uses HTML5 `min`/`max` (browser validation only). Slider uses noUiSlider (visual constraint). Different mechanisms.

## See Also

- [Checkboxes & Radio Buttons](checkboxes-radio-buttons.md)
- [Sliders Widget](sliders-widget.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/filter/`
