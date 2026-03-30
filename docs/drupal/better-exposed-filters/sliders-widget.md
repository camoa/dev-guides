---
description: BEF sliders widget — noUiSlider configuration, applicable filter types, validation rules, and drupalSettings structure
drupal_version: "11.x"
---

# Sliders Widget

## When to Use

> Use this widget when you have a numeric filter (price, quantity, rating) and want a visual range slider instead of text inputs. Use the number widget for simple min/max inputs without visual slider.

## Decision

| Property | Value |
|---|---|
| Plugin ID | `bef_sliders` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\Sliders` |
| Library | `better_exposed_filters/sliders` (depends on `better_exposed_filters/nouislider`) |

**Applicable filter types:**

| Filter | Supported |
|---|---|
| `NumericFilter` | Yes (except Date filters) |
| `Range` (Range module) | Yes |
| `Date` filter | No — use date picker widget |
| Grouped filters | No |

**Slider configuration:**

| Option | Config Key | Default | Purpose |
|---|---|---|---|
| Min | `min` | 0 | Minimum slider value |
| Max | `max` | 99999 | Maximum slider value |
| Step | `step` | 1 | Increment between values |
| Orientation | `orientation` | 'horizontal' | 'horizontal' or 'vertical' |
| Tooltips | `enable_tooltips` | FALSE | Show value tooltips on handles |
| Tooltip prefix | `tooltips_value_prefix` | '' | Text before value (e.g., '$') |
| Tooltip suffix | `tooltips_value_suffix` | '' | Text after value (e.g., ' USD') |

**Validation:** `(max - min) / step` must be a whole number. Step can have at most 5 decimal places.

## Pattern

```javascript
// drupalSettings structure for slider
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

- **Wrong**: Using the slider without `/libraries/nouislider/nouislider.min.js` in place → **Right**: Verify the library files exist. `drupal/nouislider_js` installs them but some deployment setups strip `/libraries/`.
- **Wrong**: Setting `(max - min) / step` with a remainder → **Right**: Adjust min, max, or step so the range is evenly divisible by the step.
- **Wrong**: Trying to use sliders on date filters → **Right**: BEF explicitly excludes `Date` filters from the slider widget. Use `bef_datepicker` instead.
- **Wrong**: Hard-coding slider min/max in Views UI for dynamic content → **Right**: Use `hook_better_exposed_filters_options_alter()` to set slider range dynamically.

## See Also

- [Hooks & Alter Functions](hooks-alter.md)
- [JavaScript Behaviors](javascript-behaviors.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/filter/Sliders.php`
- Reference: https://www.drupal.org/project/nouislider_js
