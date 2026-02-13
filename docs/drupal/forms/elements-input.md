---
description: Input form elements - text, numeric, password, and date/time fields
drupal_version: "11.x"
---

# Form Elements: Input Elements

## When to Use

> Choose specific input types for HTML5 validation and mobile keyboard hints. Use textfield for generic text, email for emails, number for numeric input.

## Decision

| Data Type | Element | Why |
|-----------|---------|-----|
| Short text | textfield | Generic text input |
| Multi-line text | textarea | Long descriptions, messages |
| Email addresses | email | Automatic @ validation, email keyboard |
| Phone numbers | tel | Mobile keyboard hint |
| URLs | url | Protocol validation, URL keyboard |
| Search queries | search | Browser styling/history |
| Numeric values | number | Spinner controls, validation |
| Slider range | range | Visual slider UI |
| Passwords | password | No display, no default value |
| Password + confirm | password_confirm | Automatic matching validation |
| Date only | date | Date picker |
| Date + time | datetime | Date and time picker |
| Date dropdowns | datelist | Granular control, old browsers |

## Text Input Pattern

```php
$form['name'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Name'),
  '#maxlength' => 255,
  '#required' => TRUE,
];

$form['description'] = [
  '#type' => 'textarea',
  '#title' => $this->t('Description'),
  '#rows' => 5,
];

$form['email'] = [
  '#type' => 'email', // HTML5 email validation
  '#title' => $this->t('Email'),
];
```

## Numeric Input Pattern

```php
$form['quantity'] = [
  '#type' => 'number',
  '#title' => $this->t('Quantity'),
  '#min' => 0,
  '#max' => 100,
  '#step' => 1, // Integers only
];

$form['rating'] = [
  '#type' => 'range',
  '#title' => $this->t('Rating'),
  '#min' => 1,
  '#max' => 5,
  '#step' => 1,
];
```

## Password Pattern

```php
$form['password'] = [
  '#type' => 'password_confirm', // Dual fields with matching
  '#title' => $this->t('Password'),
  '#required' => TRUE,
];

// Security: Never set #default_value on password fields
// Security: Never log password values
```

## Date Pattern

```php
$form['start_date'] = [
  '#type' => 'date', // Modern browsers, simple date
  '#title' => $this->t('Start Date'),
  '#date_date_format' => 'Y-m-d',
];

$form['event_time'] = [
  '#type' => 'datetime', // Date + time
  '#title' => $this->t('Event Time'),
];
```

## Common Mistakes

- **Wrong**: Using textfield for dates → **Right**: Use date element (accessibility)
- **Wrong**: No #maxlength on textfields → **Right**: Set appropriate limits
- **Wrong**: Not setting #date_date_format → **Right**: Specify format

## See Also

- [Selection Elements](elements-selection.md)
- [Element Validation](validation-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/Textfield.php`
