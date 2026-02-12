---
description: Form states (#states) — client-side conditional field behavior
drupal_version: "11.x"
---

# Form States System (#states)

## When to Use

> Use #states for client-side show/hide/enable/disable. Use AJAX when server-side data loading needed.

## Decision

| Need | Solution | Why |
|------|----------|-----|
| Show/hide fields | #states | Client-side, instant |
| Enable/disable fields | #states | No server call |
| Change required status | #states | Conditional validation |
| Dependent dropdowns | AJAX | Options from server |
| Load entities/data | AJAX | Server-side data |

## Supported States

**Visibility States:**
| State | Effect |
|-------|--------|
| visible | Show element when condition true |
| invisible | Hide element when condition true |

**Interaction States:**
| State | Effect |
|-------|--------|
| enabled | Enable input when condition true |
| disabled | Disable input when condition true |
| readonly | Make read-only when condition true |

**Validation States:**
| State | Effect |
|-------|--------|
| required | Mark required when condition true |
| optional | Mark optional when condition true |

**Special States:**
| State | Effect | Element Type |
|-------|--------|--------------|
| checked | Check checkbox when condition true | Checkbox |
| unchecked | Uncheck checkbox when condition true | Checkbox |
| expanded | Expand when condition true | Details |
| collapsed | Collapse when condition true | Details |

Reference: `/web/core/misc/states.js`

## Trigger Conditions

**Checkbox Conditions:**
```php
['checked' => TRUE]   // Checkbox is checked
['unchecked' => TRUE] // Checkbox is not checked
```

**Value Conditions:**
```php
['value' => 'foo']           // Exact value match
['value' => ['foo', 'bar']]  // Value in array
['!value' => 'foo']          // Value NOT equal
```

**State Conditions:**
```php
['empty' => TRUE]   // Field is empty
['filled' => TRUE]  // Field has value
```

## Basic Syntax

**Single Condition:**
```php
'#states' => [
  'visible' => [
    ':input[name="enable_feature"]' => ['checked' => TRUE],
  ],
],
```

**Multiple States (Same Element):**
```php
'#states' => [
  'visible' => [
    ':input[name="enable_feature"]' => ['checked' => TRUE],
  ],
  'required' => [
    ':input[name="enable_feature"]' => ['checked' => TRUE],
  ],
],
```

## Selector Syntax

**Input Name:**
```php
':input[name="field_name"]'           // Simple field
':input[name="container[field]"]'     // Nested field
':input[name="field[0][value]"]'      // Field API widget
```

**Radio Buttons:**
```php
':input[name="field_name"]' => ['value' => 'option1']
```

**Select Dropdowns:**
```php
'select[name="field_name"]' => ['value' => 'option1']
```

**Checkboxes (Group):**
```php
':input[name="field_name[option1]"]' => ['checked' => TRUE]
```

## Complex Conditions

**AND Conditions (All Must Be True):**
```php
'#states' => [
  'visible' => [
    ':input[name="enable_feature"]' => ['checked' => TRUE],
    ':input[name="user_role"]' => ['value' => 'admin'],
  ],
],
```

**OR Conditions (Any Can Be True):**
```php
'#states' => [
  'visible' => [
    [':input[name="type"]' => ['value' => 'custom']],
    'or',
    [':input[name="type"]' => ['value' => 'advanced']],
  ],
],
```

**XOR Conditions (Exactly One True):**
```php
'#states' => [
  'visible' => [
    [':input[name="option1"]' => ['checked' => TRUE]],
    'xor',
    [':input[name="option2"]' => ['checked' => TRUE]],
  ],
],
```

## Practical Examples

**Show Field When Checkbox Checked:**
```php
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
```

**Show Field Based on Select:**
```php
$form['other_value'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Other'),
  '#states' => [
    'visible' => [
      'select[name="type"]' => ['value' => 'other'],
    ],
  ],
];
```

**Disable Field When Another Empty:**
```php
$form['dependent'] = [
  '#type' => 'textfield',
  '#states' => [
    'disabled' => [
      ':input[name="primary"]' => ['empty' => TRUE],
    ],
  ],
];
```

## States vs AJAX Decision

**Use #states When:**
- Simple show/hide logic
- Field enable/disable
- Required status changes
- No server-side processing needed
- Performance important (client-side only)

**Use AJAX When:**
- Options must change (e.g., dependent dropdowns)
- Need server-side data
- Complex validation logic
- Field structure must change
- Need to load entities/data

## Common Mistakes

- **Wrong**: Missing :input in selector `'name="field"'` → **Right**: `:input[name="field"]`
- **Wrong**: Using dot notation for nested `'container.field'` → **Right**: `'container[field]'`
- **Wrong**: OR logic with separate conditions → **Right**: Use array + 'or' keyword
- **Wrong**: Not matching exact form structure → **Right**: Inspect form to get correct selector

## See Also

- [AJAX Forms](ajax-architecture.md)
- [Form Alter](form-alter-system.md)
- Documentation: [Conditional Form Fields](https://www.drupal.org/docs/drupal-apis/form-api/conditional-form-fields)
- Contrib: [Conditional Fields](https://www.drupal.org/project/conditional_fields)
- Reference: `/web/core/misc/states.js`
