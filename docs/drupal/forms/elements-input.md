---
description: Input elements — text, numeric, password, date/time fields
drupal_version: "11.x"
---

# Form Elements: Input Elements

## When to Use

> Use semantic HTML5 input types for automatic validation and better mobile UX.

## Decision

| Data Type | Element | Why |
|-----------|---------|-----|
| Email addresses | email | Automatic @ validation, email keyboard |
| Phone numbers | tel | Mobile phone keyboard hint |
| Web addresses | url | Protocol validation |
| Short text | textfield | Generic input |
| Long text | textarea | Multi-line content |
| Numbers | number | Spinner controls, validation |
| Slider | range | Visual range selection |
| Password | password | Hidden input |
| Password + confirm | password_confirm | Dual fields, auto-matching |
| Date only | date | Date picker |
| Date + time | datetime | Date and time picker |
| Date dropdowns | datelist | Granular control, old browsers |

## Text Input Elements

| Element | HTML5 Type | Validation | Key Properties |
|---------|------------|------------|----------------|
| textfield | text | None | #maxlength, #size, #autocomplete_route_name |
| textarea | textarea | None | #rows, #cols, #resizable |
| email | email | Email format | #maxlength |
| tel | tel | None | #maxlength |
| url | url | URL format | #maxlength |
| search | search | None | #maxlength |

Reference: `/web/core/lib/Drupal/Core/Render/Element/Textfield.php`

## Numeric Input Elements

| Element | Purpose | Properties | Browser Behavior |
|---------|---------|------------|------------------|
| number | Numeric input | #min, #max, #step | Spinner controls |
| range | Slider | #min, #max, #step | Visual slider |

**Number Validation:**
```php
'#min' => 0,           // Minimum value
'#max' => 100,         // Maximum value
'#step' => 0.01,       // Increment (decimals)
```

## Password Elements

| Element | Purpose | Features |
|---------|---------|----------|
| password | Single password | #maxlength, #size, no #default_value |
| password_confirm | Password + confirm | Dual fields, automatic matching validation |

**Security Note:**
- Never set #default_value on password fields
- Never log password values
- Always use PasswordConfirm for user-facing password changes

Reference: `/web/core/lib/Drupal/Core/Render/Element/PasswordConfirm.php`

## Date/Time Elements

| Element | Interface | Format | Properties |
|---------|-----------|--------|------------|
| date | Date picker | Y-m-d | #date_date_format |
| datetime | Date + time | Y-m-d H:i:s | #date_time_format, #date_date_format |
| datelist | Dropdowns | Custom | #date_part_order, #date_year_range |

**Date Element Decision:**
```
Modern browser, single date? → date
Date and time needed? → datetime
Need granular control/old browsers? → datelist
Complex date logic? → Custom element
```

## Common Mistakes

- **Wrong**: Using textfield for dates (accessibility issue) → **Right**: Use date/datetime element
- **Wrong**: Not setting #date_date_format (uses site default) → **Right**: Set explicit format
- **Wrong**: Forgetting timezone handling → **Right**: Use Drupal DateTime API
- **Wrong**: Setting #default_value on password fields → **Right**: Never set password defaults

## See Also

- [Selection Elements](elements-selection.md)
- [Element Lifecycle](elements-lifecycle.md)
- [DateTime API](https://www.drupal.org/docs/drupal-apis/date-time-api)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/`
