---
description: Validation architecture — three-tier system, execution order, error methods
drupal_version: "11.x"
---

# Validation Architecture

## When to Use

> Use element validation for single field checks. Use form validation for cross-field logic. ConfigFormBase gets automatic typed config validation.

## Decision

| Validation Need | Level | Where |
|----------------|-------|-------|
| Single field format/range | Element | #element_validate property |
| Cross-field validation | Form | validateForm() method |
| Business logic | Form | validateForm() method |
| ConfigFormBase constraints | Typed config | schema.yml |

## Three-Tier Validation System

```
1. Element-level (#element_validate)
   - Per-element basis
   - Format, range, pattern validation
   - Runs first

2. Form-level (validateForm(), #validate)
   - Cross-field validation
   - Business logic
   - Runs second

3. Typed config (ConfigFormBase only)
   - Schema constraint validation
   - Runs automatically from config schema
   - Runs third
```

Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php` lines 94-126

## Validation Execution Order

**Complete Chain:**
```
1. CSRF token validation (failure stops all processing)
2. Element validators (depth-first tree traversal)
   - #element_validate callbacks
   - Built-in element type validation
3. Form validators (#validate array)
4. Form class validateForm() method
5. Typed config validators (ConfigFormBase only)
6. If any errors: redisplay form, no submit handlers run
```

Reference: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 180-237

## Error Setting Methods

**By Element Name (Preferred):**
```php
$form_state->setErrorByName('field_name', $this->t('Error message'));
```

**By Element Reference:**
```php
$form_state->setError($form['field_name'], $this->t('Error message'));
```

**Error Checking:**
```php
if ($form_state->hasAnyErrors()) { /* ... */ }
$errors = $form_state->getErrors(); // Associative array
$form_state->clearErrors(); // Reset all
```

## Validation Patterns

**Element Validation:**
```php
'#element_validate' => ['::validateEmail'],

public static function validateEmail($element, FormStateInterface $form_state) {
  $value = $element['#value'];
  if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
    $form_state->setError($element, t('Invalid email address.'));
  }
}
```

**Form Validation:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $start = $form_state->getValue('start_date');
  $end = $form_state->getValue('end_date');

  if ($end < $start) {
    $form_state->setErrorByName('end_date',
      $this->t('End date must be after start date.'));
  }
}
```

## Common Mistakes

- **Wrong**: Setting errors in buildForm() (wrong phase) → **Right**: Use validateForm()
- **Wrong**: Using element validation for cross-field checks → **Right**: Use form validation
- **Wrong**: Not translating error messages → **Right**: Use $this->t()
- **Wrong**: Forgetting to check for existing errors → **Right**: Use hasAnyErrors()

## See Also

- [Partial Validation](validation-partial.md)
- [Form State Methods](form-state-methods.md)
- [Typed Data Constraints](https://www.drupal.org/project/drupal/issues/2971727)
- Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php`
