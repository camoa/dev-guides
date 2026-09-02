---
description: "BEF sliders widget — noUiSlider configuration, applicable filter types, validation rules, and drupalSettings structure"
tldr: "Use this widget when you have a numeric filter (price, quantity, rating) and want a visual range slider instead of text inputs. The step must evenly divide the (max - min) range or the configuration form rejects it."
drupal_version: "11.x"
---

# Sliders Widget

## When to Use

> When you have a numeric filter (price, quantity, rating) and want a visual range slider instead of text inputs.

## Decision: Plugin Details

| Property | Value |
|---|---|
| Plugin ID | `bef_sliders` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\Sliders` |
| Attribute | `#[FiltersWidget(id: 'bef_sliders', title: 'Sliders')]` |
| Library | `better_exposed_filters/sliders` (depends on `better_exposed_filters/nouislider`) |

## Decision: Applicability

- `NumericFilter` — Yes (except Date filters)
- `Range` (from Range module) — Yes
- `Date` filter — No (excluded explicitly)
- Grouped filters — No

The key check: `($is_numeric_filter || $is_range_filter) && !$is_date_filter && !$filter->isAGroup()`

## Decision: Slider Configuration

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Min | `min` | 0 | Minimum slider value |
| Max | `max` | 99999 | Maximum slider value |
| Step | `step` | 1 | Increment between values (max 5 decimal places) |
| Animation | `animate` | 0 (none) | Slide animation: 0, 200 (fast), 400 (normal), 600 (slow), 'custom' |
| Custom animation ms | `animate_ms` | 0 | Custom animation duration |
| Orientation | `orientation` | 'horizontal' | 'horizontal' or 'vertical' |
| Tooltips | `enable_tooltips` | FALSE | Show value tooltips on handles |
| Tooltip prefix | `tooltips_value_prefix` | '' | Text before value (e.g., '$') |
| Tooltip suffix | `tooltips_value_suffix` | '' | Text after value (e.g., ' USD') |
| Placement | `placement_location` | 'end' | Where slider appears: 'start', 'middle', 'end' |

## Pattern: Validation Rules

- Max must be greater than min
- Step can have at most 5 decimal places
- `(max - min) / step` must be a whole number (range evenly divisible by step)

## Pattern: drupalSettings

```javascript
drupalSettings.better_exposed_filters.slider_options[field_id] = {
  min: 0,
  max: 99999,
  step: 1,
  animate: 0,
  orientation: 'horizontal',
  placement_location: 'end',
  id: 'unique-id',
  dataSelector: 'field-id',
  viewId: 'form-id',
  tooltips: false,
  tooltips_value_prefix: '',
  tooltips_value_suffix: ''
};
```

## Common Mistakes

- **Slider shows but doesn't work** — Check that noUiSlider library files exist at `/libraries/nouislider/`. The `drupal/nouislider_js` package should handle this.
- **Range not evenly divisible** — If `(max - min) / step` has a remainder, the configuration form will reject it. Adjust min, max, or step.
- **Using sliders for date filters** — BEF explicitly excludes Date filters from the slider widget. Use the date picker widget instead.
- **Alter hook for dynamic min/max** — Use `hook_better_exposed_filters_options_alter()` to set slider min/max dynamically based on content.

## See Also

- [Hooks & Alter Functions](hooks-alter.md) — dynamically setting slider range
- [JavaScript Behaviors](javascript-behaviors.md) — bef_sliders.js behavior
- Reference: https://www.drupal.org/project/nouislider_js
