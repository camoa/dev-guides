---
description: Form validation — validateForm, element validation, constraints
drupal_version: "11.x"
---

# Validation

## When to Use

> Add validation when form input needs checks beyond `#required`. Use `validateForm()` for cross-field logic. Use `#element_validate` for single-field rules.

## Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Field must not be empty | `#required => TRUE` | Built-in, no custom code |
| Field must match a pattern | `#element_validate` | Single-field, reusable |
| Two fields must be consistent | `validateForm()` | Cross-field logic |
| Complex business rules | `validateForm()` | Full access to all values |

## Pattern: validateForm()

```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $email = $form_state->getValue('email');
  if ($email && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $form_state->setErrorByName('email', $this->t('Invalid email address.'));
  }

  $start = $form_state->getValue('start_date');
  $end = $form_state->getValue('end_date');
  if ($start && $end && $start > $end) {
    $form_state->setErrorByName('end_date', $this->t('End date must be after start date.'));
  }
}
```

## Pattern: #element_validate

```php
$form['port'] = [
  '#type' => 'number',
  '#title' => $this->t('Port'),
  '#element_validate' => [[$this, 'validatePort']],
];

public function validatePort(array &$element, FormStateInterface $form_state) {
  $value = $element['#value'];
  if ($value < 1 || $value > 65535) {
    $form_state->setError($element, $this->t('Port must be between 1 and 65535.'));
  }
}
```

## Key Methods

| Method | Purpose |
|--------|---------|
| `setErrorByName($name, $message)` | Error on a named field |
| `setError($element, $message)` | Error on an element reference |
| `getErrors()` | Check existing errors |

## Common Mistakes

- **Wrong**: Validating in `submitForm()` (too late, form already submitted)
- **Wrong**: Using `setErrorByName()` with wrong field name (error shows but field not highlighted)
- **Wrong**: Not checking if value exists before validating (fails on optional empty fields)
- **Right**: Use `#required` for simple presence checks, custom validation for logic

## See Also

- [FormBase](form-base.md) — base form pattern
- [AJAX](ajax.md) — real-time validation with AJAX
