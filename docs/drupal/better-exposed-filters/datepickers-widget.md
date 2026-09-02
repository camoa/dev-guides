---
description: "BEF date picker widget — HTML5 date input conversion, between operators, date offset handling"
tldr: "Use this widget when you have a date filter and want HTML5 <input type=\"date\"> instead of a text field. The date input always uses YYYY-MM-DD; grouped date filters cannot use this widget."
drupal_version: "11.x"
---

# Date Pickers Widget

## When to Use

> When you have a date filter and want HTML5 `<input type="date">` instead of a text field.

## Decision: Plugin Details

| Property | Value |
|---|---|
| Plugin ID | `bef_datepicker` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\DatePickers` |
| Attribute | `#[FiltersWidget(id: 'bef_datepicker', title: 'Date Picker')]` |
| Library | `better_exposed_filters/datepickers` |

## Decision: Applicability

- `Date` filter — Yes
- Filters with `$filter->date_handler` — Yes
- Grouped filters — No

## Pattern: How It Works

The widget converts date text fields to HTML5 `<input type="date">` elements:

```php
$element['value']['#type'] = 'date';
$element['value']['#attributes']['class'][] = 'bef-datepicker';
$element['value']['#attributes']['autocomplete'] = 'off';
```

For "between" operators, both min and max fields are converted:
```php
$element['min']['#type'] = 'date';
$element['max']['#type'] = 'date';
```

**Date offset handling:** When the filter uses relative date offsets (e.g., "+7 days"), BEF converts them to actual dates for the date picker default values via `convertOffsets()`.

## Common Mistakes

- **Date format mismatch** — The HTML5 date input always uses `YYYY-MM-DD` format. If your filter expects a different format, the values may not match. BEF stores the original `#date_format` in drupalSettings.
- **No grouped filter support** — Grouped date filters cannot use the date picker widget. Use the default widget instead.
- **Browser differences** — HTML5 date inputs render differently across browsers. The date picker is the native browser implementation, not a custom widget.

## See Also

- [Hidden & Special Widgets](hidden-special-widgets.md) — hiding date filters
- [Auto-Submit](auto-submit.md) — auto-submit with date inputs (debounced)
