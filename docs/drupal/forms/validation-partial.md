---
description: "Partial validation pattern with #limit_validation_errors for multi-step forms"
tldr: "Use partial validation for multi-step forms with \"Previous\" buttons, \"Save draft\" vs \"Publish\" buttons, or progressive disclosure forms."
drupal_version: "11.x"
---

# Validation: Partial Validation Pattern

## When to Use

> Use partial validation for multi-step forms with "Previous" buttons, "Save draft" vs "Publish" buttons, or progressive disclosure forms.

**When to Use Partial Validation:**

- Multi-step forms with "Previous" button
- "Save draft" vs "Publish" buttons
- Progressive disclosure forms
- Forms with optional sections

**When NOT to Use:**

- Simple single-step forms
- All fields always required
- No multiple submit buttons

## Pattern: #limit_validation_errors

**#limit_validation_errors Property:**

```
Applied to: Button elements (submit, button)
Effect: Only validates specified form sections
Syntax: Array of arrays (element parents)
```

**Example - Multi-Step Form:**

```php
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#limit_validation_errors' => [['step1']], // Only validate step1
  '#submit' => ['::previousSubmit'],
];

$form['actions']['next'] = [
  '#type' => 'submit',
  '#value' => $this->t('Next'),
  '#limit_validation_errors' => [['step2']], // Only validate step2
  '#submit' => ['::nextSubmit'],
];
```

**Example - Save Draft:**

```php
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

## Reference: Syntax Details

**Single Element:**

```php
'#limit_validation_errors' => [['field_name']]
```

**Nested Element:**

```php
'#limit_validation_errors' => [['container', 'field_name']]
```

**Multiple Elements:**

```php
'#limit_validation_errors' => [
  ['step1', 'name'],
  ['step1', 'email'],
]
```

**No Validation:**

```php
'#limit_validation_errors' => []
```

## Reference: How It Works

**Internal Mechanism:**

```
FormValidator checks button #limit_validation_errors
If present: Only validates specified element paths
If absent: Validates entire form
#required still enforced on specified paths
```

**Reference:** `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` lines 461-532

## Common Mistakes

**Incorrect Path:**

```php
// WRONG - string instead of array
'#limit_validation_errors' => 'field_name'

// CORRECT
'#limit_validation_errors' => [['field_name']]
```

**Missing Parent Elements:**

```php
// If field is $form['container']['field']
// WRONG
'#limit_validation_errors' => [['field']]

// CORRECT
'#limit_validation_errors' => [['container', 'field']]
```

**Forgetting #submit Handler:**

```
Partial validation without custom submit handler is useless
Always pair #limit_validation_errors with #submit
```

## See Also

- [Multi-Step Form Pattern](multi-step-forms.md) (dedicated section)
- [Submission Architecture](submission-architecture.md) (dedicated section)
- [Button Elements](elements-grouping.md) (element reference)
