---
description: "BEF JavaScript libraries — auto_submit, sliders, select_all_none, soft_limit, links_use_ajax, and drupalSettings structure"
tldr: "Use this guide when you need to understand or customize BEF's client-side behavior — auto-submit, sliders, select all/none, soft limit, or link AJAX."
drupal_version: "11.x"
---

# JavaScript Behaviors

## When to Use

> When you need to understand or customize BEF's client-side behavior — auto-submit, sliders, select all/none, soft limit, or link AJAX.

## Decision: Library Reference

| Library | File | Behavior | Dependencies |
|---|---|---|---|
| `general` | `better_exposed_filters.js` | Checkbox highlighting, autosubmit exclusion, single checkbox fix | core/drupal, core/jquery, core/once |
| `auto_submit` | `auto_submit.js` | Debounced form auto-submission | core/drupal, core/once, core/drupal.debounce |
| `sliders` | `bef_sliders.js` | noUiSlider initialization and sync | core/drupal, core/drupalSettings, core/jquery, core/once, better_exposed_filters/nouislider |
| `datepickers` | `bef_datepickers.js` | HTML5 date input conversion | core/drupal, core/drupalSettings, core/jquery |
| `select_all_none` | `bef_select_all_none.js` | Select all/none checkbox behavior | core/drupal, core/jquery, core/once |
| `links_use_ajax` | `bef_links_use_ajax.js` | AJAX form submission for link filters | core/drupal, core/once |
| `soft_limit` | `bef_soft_limit.js` | Show more/less toggle | core/drupal, core/once, core/drupalSettings, core/jquery |
| `nouislider` | `/libraries/nouislider/nouislider.min.js` | External slider library | — |

## Pattern: auto_submit.js Key Behaviors

**`Drupal.behaviors.betterExposedFiltersAutoSubmit`:**

- Binds to `change` and `keyup` events on form elements
- `change` on non-date elements: submits immediately
- `change` on date inputs: debounced (prevents premature submit while typing)
- `keyup` on text/textarea: debounced by configurable delay
- Ignores navigation keys (arrows, tab, enter, esc, shift, ctrl, alt, etc.)
- Respects media query breakpoints
- Excludes `.select2-search__field` and `.chosen-search-input`
- Refocuses the last-triggered element after AJAX refresh

## Pattern: drupalSettings Structure

```javascript
drupalSettings.better_exposed_filters = {
  // Auto-submit
  auto_submit_sort_only: false,

  // Sliders
  slider: true,
  slider_options: {
    field_price_value: {
      min: 0, max: 1000, step: 10,
      animate: 0, orientation: 'horizontal',
      // ...
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

## Common Mistakes

- **jQuery dependency** — BEF still uses jQuery for several behaviors. Ensure `core/jquery` is available. In Drupal 11, jQuery is not loaded by default on all pages.
- **AJAX refresh breaks behaviors** — BEF uses `Drupal.behaviors` pattern, so behaviors re-attach after AJAX. If custom JS doesn't use behaviors, it will break.
- **Once library** — BEF uses `once()` to prevent duplicate event binding. Custom code interacting with BEF elements should also use `once()`.

## See Also

- [Auto-Submit](auto-submit.md) — auto-submit configuration
- [Sliders Widget](sliders-widget.md) — slider configuration
