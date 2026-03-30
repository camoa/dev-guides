---
description: BEF date picker widget — HTML5 date input conversion, between operators, date offset handling
drupal_version: "11.x"
---

# Date Pickers Widget

## When to Use

> Use this widget when you have a date filter and want HTML5 `<input type="date">` instead of a text field. Use the hidden widget for date filters you want to set programmatically without user input.

## Decision

| Property | Value |
|---|---|
| Plugin ID | `bef_datepicker` |
| Class | `Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\DatePickers` |
| Library | `better_exposed_filters/datepickers` |

**Applicable filter types:**

| Filter | Supported |
|---|---|
| `Date` filter | Yes |
| Filters with `$filter->date_handler` | Yes |
| Grouped filters | No |

## Pattern

```php
// Single date filter
$element['value']['#type'] = 'date';
$element['value']['#attributes']['class'][] = 'bef-datepicker';
$element['value']['#attributes']['autocomplete'] = 'off';

// "Between" operators — both min and max are converted
$element['min']['#type'] = 'date';
$element['max']['#type'] = 'date';

// Date offset handling:
// When filter uses relative date offsets (e.g., "+7 days"),
// BEF converts them to actual dates for picker defaults via convertOffsets()
```

## Common Mistakes

- **Wrong**: Expecting the date picker to accept non-ISO formats → **Right**: HTML5 date input always uses `YYYY-MM-DD`. Configure the date filter to match or accept ISO format.
- **Wrong**: Using the date picker widget for grouped date filters → **Right**: Grouped date filters cannot use the date picker widget. Use the default widget instead.
- **Wrong**: Expecting consistent visual appearance across browsers → **Right**: HTML5 date inputs render as the native browser implementation. This is not a custom widget; appearance varies.

## See Also

- [Hidden & Special Widgets](hidden-special-widgets.md)
- [Auto-Submit](auto-submit.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/better_exposed_filters/filter/DatePickers.php`
