---
description: BEF JavaScript libraries — auto_submit, sliders, select_all_none, soft_limit, links_use_ajax, and drupalSettings structure
tldr: "Use this guide when you need to understand or customize BEF's client-side behavior — auto-submit, sliders, select all/none, soft limit, or link AJAX."
drupal_version: "11.x"
---

# JavaScript Behaviors

## When to Use

> Use this guide when you need to understand or customize BEF's client-side behavior — auto-submit, sliders, select all/none, soft limit, or link AJAX.

## Decision

| Library | File | Behavior | Key Dependencies |
|---|---|---|---|
| `general` | `better_exposed_filters.js` | Checkbox highlighting, autosubmit exclusion, single checkbox fix | jQuery, once |
| `auto_submit` | `auto_submit.js` | Debounced form auto-submission | once, drupal.debounce |
| `sliders` | `bef_sliders.js` | noUiSlider initialization and sync | drupalSettings, jQuery, once, nouislider |
| `datepickers` | `bef_datepickers.js` | HTML5 date input conversion | drupalSettings, jQuery |
| `select_all_none` | `bef_select_all_none.js` | Select all/none checkbox behavior | jQuery, once |
| `links_use_ajax` | `bef_links_use_ajax.js` | AJAX form submission for link filters | once |
| `soft_limit` | `bef_soft_limit.js` | Show more/less toggle | once, drupalSettings, jQuery |
| `nouislider` | `/libraries/nouislider/nouislider.min.js` | External slider library | — |

## Pattern

```javascript
// drupalSettings structure
drupalSettings.better_exposed_filters = {
  auto_submit_sort_only: false,

  // Sliders
  slider: true,
  slider_options: {
    field_price_value: {
      min: 0, max: 1000, step: 10,
      animate: 0, orientation: 'horizontal',
      tooltips: false,
      tooltips_value_prefix: '$',
      tooltips_value_suffix: ' USD'
    }
  },

  // Date pickers
  datepicker: true,
  datepicker_options: { dateformat: 'Y-m-d' },

  // Soft limit
  soft_limit: {
    field_category_target_id: {
      limit: 5,
      list_selector: '.bef-checkboxes',
      item_selector: '.js-form-type-checkbox',
      show_less: 'Show less',
      show_more: 'Show more'
    }
  }
};
```

**auto_submit.js key behaviors:**
- `change` on non-date elements: submits immediately
- `change` on date inputs: debounced
- `keyup` on text/textarea: debounced by configurable delay
- Ignores navigation keys (arrows, tab, enter, esc, shift, ctrl, alt, etc.)
- Respects `matchMedia()` for breakpoint guards
- Excludes `.select2-search__field` and `.chosen-search-input`
- Refocuses last-triggered element after AJAX refresh

## Common Mistakes

- **Wrong**: Assuming jQuery is always available in Drupal 11 → **Right**: Drupal 11 does not load jQuery by default on all pages. BEF still uses jQuery; it's loaded as a dependency via its libraries, but custom code must declare it explicitly.
- **Wrong**: Custom JS not re-attaching after AJAX refresh → **Right**: Wrap custom JS in `Drupal.behaviors` so it re-attaches after every AJAX response.
- **Wrong**: Double event binding on BEF elements → **Right**: BEF uses `once()` to prevent duplicate binding. Custom code interacting with BEF elements should also use `once()`.

## See Also

- [Auto-Submit](auto-submit.md)
- [Sliders Widget](sliders-widget.md)
- Reference: `web/modules/contrib/better_exposed_filters/js/`
