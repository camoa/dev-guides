---
description: Partial validation pattern with #limit_validation_errors for multi-step forms
drupal_version: "11.x"
---

# Validation: Partial Validation Pattern

## When to Use

> Use partial validation for multi-step forms with "Previous" buttons, "Save draft" vs "Publish" buttons, or progressive disclosure forms.

## Decision

| Situation | Use Partial Validation | Why |
|-----------|------------------------|-----|
| Multi-step "Previous" button | Yes | Don't validate when going back |
| "Save draft" vs "Publish" | Yes | Draft needs no validation |
| Progressive disclosure | Yes | Only validate visible sections |
| Simple single-step forms | No | Not needed |
| All fields always required | No | Full validation appropriate |

## Pattern

```php
// Multi-step form: Previous button (no validation)
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#limit_validation_errors' => [], // No validation
  '#submit' => ['::previousSubmit'],
];

// Multi-step form: Next button (validate current step only)
$form['actions']['next'] = [
  '#type' => 'submit',
  '#value' => $this->t('Next'),
  '#limit_validation_errors' => [['step1']], // Only validate step1
  '#submit' => ['::nextSubmit'],
];

// Save draft (no validation) vs Publish (full validation)
$form['actions']['draft'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save Draft'),
  '#limit_validation_errors' => [], // No validation
  '#submit' => ['::saveDraft'],
];

$form['actions']['publish'] = [
  '#type' => 'submit',
  '#value' => $this->t('Publish'),
  // No #limit_validation_errors = full validation
  '#submit' => ['::publishSubmit'],
];
```

## Syntax

```php
// Single element
'#limit_validation_errors' => [['field_name']]

// Nested element
'#limit_validation_errors' => [['container', 'field_name']]

// Multiple elements
'#limit_validation_errors' => [
  ['step1', 'name'],
  ['step1', 'email'],
]

// No validation
'#limit_validation_errors' => []
```

## How It Works

FormValidator checks button #limit_validation_errors. If present, only validates specified element paths. If absent, validates entire form. #required still enforced on specified paths.

## Common Mistakes

- **Wrong**: `'#limit_validation_errors' => 'field_name'` (string) → **Right**: `[['field_name']]` (array of arrays)
- **Wrong**: Missing parent elements in path → **Right**: Include full path `[['container', 'field']]`
- **Wrong**: Partial validation without #submit handler → **Right**: Always pair with #submit
- **Wrong**: Wrong element path → **Right**: Match form structure exactly

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [Submission Architecture](submission-architecture.md)
- [Button Elements](elements-grouping.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` lines 461-532
