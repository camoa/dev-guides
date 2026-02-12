---
description: Grouping and action elements — containers, fieldsets, buttons
drupal_version: "11.x"
---

# Form Elements: Grouping and Action Elements

## When to Use

> Use container for AJAX wrappers. Use details for collapsible sections. Use actions for button groups.

## Decision

| Purpose | Element | Why |
|---------|---------|-----|
| AJAX wrapper | container | Invisible, targetable |
| Related fields group | fieldset | Border + legend |
| Optional/advanced settings | details | Collapsible |
| Multiple setting groups | vertical_tabs | Tabbed interface |
| Form action buttons | actions | Standard wrapper |

## Grouping/Container Elements

**Layout Organization:**
| Element | Visual | Collapsible | When to Use |
|---------|--------|-------------|-------------|
| container | Invisible wrapper | No | Grouping for #states, AJAX wrapper |
| fieldset | Border + legend | No | Related fields group |
| details | Border + summary | Yes | Optional/advanced settings |
| vertical_tabs | Tabbed interface | Yes | Multiple setting groups |
| actions | Button wrapper | No | Form action buttons |

**Container Element:**
```php
$form['wrapper'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'ajax-wrapper'],
  '#tree' => TRUE,  // Nest values in FormState
];
```

**Details Element:**
```php
$form['advanced'] = [
  '#type' => 'details',
  '#title' => $this->t('Advanced settings'),
  '#open' => FALSE,  // Collapsed by default
];
```

Reference: `/web/core/lib/Drupal/Core/Render/Element/VerticalTabs.php`

## Action Elements (Buttons)

**Button Types:**
| Element | Purpose | Submits Form | Custom Handler |
|---------|---------|--------------|----------------|
| submit | Primary action | Yes | Optional #submit |
| button | Custom action | Optional | #executes_submit_callback, #ajax |
| image_button | Image submit | Yes | #src, #submit |

**Submit Button Properties:**
```php
$form['actions']['submit'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save'),
  '#submit' => ['::customSubmit'],  // Custom handler
  '#validate' => ['::customValidate'],  // Custom validation
  '#limit_validation_errors' => [['field']],  // Partial validation
];
```

## Multiple Submit Buttons Pattern

Different buttons trigger different handlers:
```php
$form['actions']['save'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save'),
  '#submit' => ['::saveSubmit'],
];

$form['actions']['save_continue'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save and Continue'),
  '#submit' => ['::saveContinueSubmit'],
];
```

**Priority order:**
1. Button #submit handlers (if that button triggered)
2. Form #submit handlers
3. Class submitForm() method

## Common Mistakes

- **Wrong**: Using button instead of submit (doesn't submit by default) → **Right**: Use submit element
- **Wrong**: Forgetting #executes_submit_callback on button elements → **Right**: Enable submission
- **Wrong**: Not using #limit_validation_errors on "Previous" buttons → **Right**: Skip validation for navigation
- **Wrong**: Creating custom buttons without AJAX for simple submits → **Right**: Use standard submit

## See Also

- [Submission Architecture](submission-architecture.md)
- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/Actions.php`
