---
description: Partial validation — #limit_validation_errors for multi-step forms
drupal_version: "11.x"
---

# Validation: Partial Validation Pattern

## When to Use

> Use partial validation for multi-step forms, "Previous" buttons, and "Save draft" vs "Publish" workflows.

## Decision

| Scenario | Pattern | Why |
|----------|---------|-----|
| Multi-step "Previous" | `#limit_validation_errors => []` | No validation |
| Multi-step "Next" | `#limit_validation_errors => [['step']]` | Only validate current step |
| Save draft | `#limit_validation_errors => []` | Skip validation |
| Publish | No limit | Full validation |

## Pattern

**Multi-Step Form:**
```php
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#limit_validation_errors' => [], // No validation
  '#submit' => ['::previousSubmit'],
];

$form['actions']['next'] = [
  '#type' => 'submit',
  '#value' => $this->t('Next'),
  '#limit_validation_errors' => [['step2']], // Only validate step2
  '#submit' => ['::nextSubmit'],
];
```

**Save Draft:**
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

## Syntax Details

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

## How It Works

```
FormValidator checks button #limit_validation_errors
If present: Only validates specified element paths
If absent: Validates entire form
#required still enforced on specified paths
```

Reference: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` lines 461-532

## Common Mistakes

- **Wrong**: `'#limit_validation_errors' => 'field_name'` (string) → **Right**: `[['field_name']]` (array of arrays)
- **Wrong**: Missing parent elements in path → **Right**: Include full element hierarchy
- **Wrong**: Forgetting #submit handler → **Right**: Always pair with custom submit
- **Wrong**: Wrong path for nested field → **Right**: Match form structure exactly

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [Submission Architecture](submission-architecture.md)
- [Validation Architecture](validation-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php`
