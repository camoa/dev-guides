---
description: Element lifecycle callbacks - #process, #after_build, #pre_render, and validation callbacks
drupal_version: "11.x"
---

# Form Elements: Lifecycle Callbacks

## When to Use

> Use #process for adding child elements, #after_build for accessing complete tree, #pre_render for final display modifications.

## Decision

| Situation | Callback | Why |
|-----------|----------|-----|
| Add child elements dynamically | #process | During build, can modify structure |
| Access complete form tree | #after_build | Full tree exists |
| Final HTML modifications | #pre_render | Just before rendering |
| Per-element validation | #element_validate | Format/range checks |
| Custom value extraction | #value_callback | Complex value structure |

## Callback Execution Order

```
Build Phase:
1. #process - Can add children, modify structure
2. #after_build - Complete tree exists
3. #pre_render - Final modifications

Validation Phase:
1. #element_validate - Per-element
2. Form-level validation - Cross-field
3. Typed config validation - Schema constraints
```

## Pattern

```php
// Process callback
$form['custom']['#process'] = [
  '::processElement',
];

public static function processElement(&$element, FormStateInterface $form_state, &$complete_form) {
  // Add child elements
  $element['child'] = [
    '#type' => 'textfield',
    '#title' => t('Child Field'),
  ];
  return $element;
}

// Element validation
$form['email']['#element_validate'] = [
  '::validateEmail',
];

public static function validateEmail(&$element, FormStateInterface $form_state, &$complete_form) {
  if (!filter_var($element['#value'], FILTER_VALIDATE_EMAIL)) {
    $form_state->setError($element, t('Invalid email address.'));
  }
}
```

## When to Use Each

| Callback | Common Use |
|----------|------------|
| #process | Container elements, composite fields (e.g., password_confirm) |
| #after_build | Add form-wide dependencies, access siblings |
| #pre_render | Attach libraries, alter markup |
| #element_validate | Email format, number range, string length |
| #value_callback | Date elements (combine multiple inputs) |

## Security

FormBuilder maintains callback whitelist. Only approved callbacks run without token validation. Never use user input as callback names.

## Common Mistakes

- **Wrong**: Using #process for display-only changes → **Right**: Use #pre_render (more efficient)
- **Wrong**: Modifying values in #pre_render → **Right**: Use #process (too late in #pre_render)
- **Wrong**: Element validation needing form-level context → **Right**: Use form validation
- **Wrong**: Not understanding execution order → **Right**: Study callback phases

## See Also

- [Validation Architecture](validation-architecture.md)
- [Form Builder Service](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Form!FormBuilder.php/class/FormBuilder/11.x)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/FormElement.php`
