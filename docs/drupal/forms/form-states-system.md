---
description: Form states (#states) — client-side conditional field behavior
drupal_version: "11.x"
---

# Form States System (#states)

### Overview

**Purpose:** Client-side conditional field behavior (JavaScript)
**Use When:** Show/hide, enable/disable based on other field values
**Alternative:** AJAX (when server-side logic needed)

**Reference:**
- Documentation: [Conditional Form Fields](https://www.drupal.org/docs/drupal-apis/form-api/conditional-form-fields)
- Implementation: `/web/core/misc/states.js`

### Supported States

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

### Trigger Conditions

**Checkbox Conditions:**
| Condition | When True |
|-----------|-----------|
| `['checked' => TRUE]` | Checkbox is checked |
| `['unchecked' => TRUE]` | Checkbox is not checked |

**Value Conditions:**
| Condition | When True |
|-----------|-----------|
| `['value' => 'foo']` | Exact value match |
| `['value' => ['foo', 'bar']]` | Value in array |
| `['!value' => 'foo']` | Value NOT equal |

**State Conditions:**
| Condition | When True |
|-----------|-----------|
| `['empty' => TRUE]` | Field is empty |
| `['filled' => TRUE]` | Field has value |

### Basic Syntax

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

### Selector Syntax

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

### Complex Conditions

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

**Nested Logic (AND + OR):**
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

### Practical Examples

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

### States vs AJAX Decision

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

**Combine Both:**
```
#states for instant UI feedback
AJAX for data loading
Best user experience
```

### Common Mistakes

**Wrong Selector:**
```php
// WRONG - missing :input
'name="field"' => ['checked' => TRUE]

// CORRECT
':input[name="field"]' => ['checked' => TRUE]
```

**Nested Field Selector:**
```php
// WRONG - missing brackets
':input[name="container.field"]'

// CORRECT
':input[name="container[field]"]'
```

**OR Logic:**
```php
// WRONG - separate conditions = AND
'visible' => [
  ':input[name="a"]' => ['checked' => TRUE],
  ':input[name="b"]' => ['checked' => TRUE],
]

// CORRECT - array + 'or'
'visible' => [
  [':input[name="a"]' => ['checked' => TRUE]],
  'or',
  [':input[name="b"]' => ['checked' => TRUE]],
]
```

**See Also:**
- AJAX Forms (when states insufficient)
- Form Alter (adding states via hook)
- JavaScript API Guide
- Contributed module: [Conditional Fields](https://www.drupal.org/project/conditional_fields)
