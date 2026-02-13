---
description: Three-tier validation architecture - element, form, and typed config validation
drupal_version: "11.x"
---

# Validation Architecture

## When to Use

> Use element-level validation for single-field checks, form-level for cross-field validation, typed config for automatic schema validation.

## Decision

| Validation Type | When to Use | Example |
|-----------------|-------------|---------|
| Element-level (#element_validate) | Single field format/range | Email format, number range |
| Form-level (validateForm()) | Cross-field validation | End date > start date |
| Typed config (ConfigFormBase) | Automatic from schema | Min/max constraints |

## Validation Execution Order

```
1. CSRF token validation (failure stops all processing)
2. Element validators (#element_validate)
   - Depth-first tree traversal
   - Built-in element type validation
3. Form validators (#validate array)
   - In order added via hook_form_alter or buildForm
4. Form class validateForm() method
5. Typed config validators (ConfigFormBase only)
6. If any errors: redisplay form, no submit handlers run
```

## Pattern

```php
// Element validation
$form['email']['#element_validate'] = [
  '::validateEmail',
];

public static function validateEmail(&$element, FormStateInterface $form_state, &$complete_form) {
  if (!filter_var($element['#value'], FILTER_VALIDATE_EMAIL)) {
    $form_state->setError($element, t('Invalid email.'));
  }
}

// Form validation
public function validateForm(array &$form, FormStateInterface $form_state) {
  $start = $form_state->getValue('start_date');
  $end = $form_state->getValue('end_date');

  if ($end < $start) {
    $form_state->setErrorByName('end_date', $this->t('End date must be after start date.'));
  }
}

// Typed config validation (automatic from schema)
// Define in config/schema/mymodule.schema.yml:
// mymodule.settings:
//   type: config_object
//   mapping:
//     api_key:
//       type: string
//       constraints:
//         NotBlank: []
//         Length:
//           min: 10
//           max: 255
```

## Error Setting Methods

```php
// By element name (preferred)
$form_state->setErrorByName('field_name', $this->t('Error message'));

// By element reference
$form_state->setError($form['field'], $this->t('Error message'));

// Check for errors
if ($form_state->hasAnyErrors()) {
  // Handle errors
}

// Get all errors
$errors = $form_state->getErrors();
```

## Common Mistakes

- **Wrong**: Setting errors in buildForm() → **Right**: Errors only in validateForm()
- **Wrong**: Element validation for cross-field checks → **Right**: Use form validation
- **Wrong**: Not translating error messages → **Right**: Use $this->t()
- **Wrong**: Generic setError() → **Right**: Use setErrorByName() (better UX, accessibility)

## See Also

- [Form State Methods](form-state-methods.md)
- [Partial Validation](validation-partial.md)
- [Typed Data Constraints](https://www.drupal.org/docs/drupal-apis/typed-data-api)
- Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php`
