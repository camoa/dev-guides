---
description: Form states system - client-side conditional field behavior with #states
drupal_version: "11.x"
---

# Form States System (#states)

## When to Use

> Use #states for client-side show/hide and enable/disable. Use AJAX when server-side logic or dynamic options needed.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple show/hide logic | #states | Instant, client-side only |
| Field enable/disable | #states | No server call needed |
| Required status changes | #states | Client-side validation |
| Options must change | AJAX | Need server data |
| Need server-side data | AJAX | Complex logic |
| Need to load entities | AJAX | Server processing required |

## Supported States

**Visibility:** visible, invisible

**Interaction:** enabled, disabled, readonly

**Validation:** required, optional

**Special:** checked, unchecked (checkbox), expanded, collapsed (details)

## Basic Syntax

```php
// Show field when checkbox checked
$form['custom_value'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Custom Value'),
  '#states' => [
    'visible' => [
      ':input[name="use_custom"]' => ['checked' => TRUE],
    ],
    'required' => [
      ':input[name="use_custom"]' => ['checked' => TRUE],
    ],
  ],
];

// Show based on select value
$form['other_value'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Other'),
  '#states' => [
    'visible' => [
      'select[name="type"]' => ['value' => 'other'],
    ],
  ],
];

// Disable when another field empty
$form['dependent'] = [
  '#type' => 'textfield',
  '#states' => [
    'disabled' => [
      ':input[name="primary"]' => ['empty' => TRUE],
    ],
  ],
];
```

## Trigger Conditions

| Condition | When True |
|-----------|-----------|
| `['checked' => TRUE]` | Checkbox is checked |
| `['unchecked' => TRUE]` | Checkbox is not checked |
| `['value' => 'foo']` | Exact value match |
| `['value' => ['foo', 'bar']]` | Value in array |
| `['!value' => 'foo']` | Value NOT equal |
| `['empty' => TRUE]` | Field is empty |
| `['filled' => TRUE]` | Field has value |

## Selector Syntax

```php
// Simple field
':input[name="field_name"]'

// Nested field
':input[name="container[field]"]'

// Field API widget
':input[name="field[0][value]"]'

// Radio buttons
':input[name="field_name"]' => ['value' => 'option1']

// Select dropdown
'select[name="field_name"]' => ['value' => 'option1']

// Checkboxes group
':input[name="field_name[option1]"]' => ['checked' => TRUE]
```

## Complex Conditions

**AND (all must be true):**
```php
'#states' => [
  'visible' => [
    ':input[name="enable"]' => ['checked' => TRUE],
    ':input[name="role"]' => ['value' => 'admin'],
  ],
],
```

**OR (any can be true):**
```php
'#states' => [
  'visible' => [
    [':input[name="type"]' => ['value' => 'custom']],
    'or',
    [':input[name="type"]' => ['value' => 'advanced']],
  ],
],
```

**XOR (exactly one true):**
```php
'#states' => [
  'visible' => [
    [':input[name="option1"]' => ['checked' => TRUE]],
    'xor',
    [':input[name="option2"]' => ['checked' => TRUE]],
  ],
],
```

**Nested (AND + OR):**
```php
'#states' => [
  'visible' => [
    [':input[name="enable"]' => ['checked' => TRUE]],
    'and',
    [
      [':input[name="type"]' => ['value' => 'custom']],
      'or',
      [':input[name="type"]' => ['value' => 'advanced']],
    ],
  ],
],
```

## States vs AJAX Decision

**Use #states when:**
- Simple show/hide logic
- Field enable/disable
- Required status changes
- No server-side processing needed
- Performance important

**Use AJAX when:**
- Options must change (dependent dropdowns)
- Need server-side data
- Complex validation logic
- Field structure must change
- Need to load entities/data

**Combine both:**
- #states for instant UI feedback
- AJAX for data loading
- Best user experience

## Common Mistakes

- **Wrong**: Missing :input in selector → **Right**: Always use `:input[name="field"]`
- **Wrong**: Nested field with dot notation → **Right**: Use brackets `container[field]`
- **Wrong**: Separate conditions for OR → **Right**: Use array + 'or' operator
- **Wrong**: String instead of array → **Right**: `[['field' => 'value']]` not `'field' => 'value'`

## See Also

- [AJAX Forms](ajax-architecture.md)
- [Form Alter](form-alter-system.md)
- [JavaScript API](https://www.drupal.org/docs/develop/drupal-apis/javascript-api)
- Reference: [Conditional Form Fields](https://www.drupal.org/docs/drupal-apis/form-api/conditional-form-fields)
