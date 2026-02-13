---
description: Drupal Form API overview - declarative render array system for building secure forms
drupal_version: "11.x"
---

# Form API Overview

## When to Use

> Use Form API when you need user input with validation and CSRF protection. Use render arrays for display-only content.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Admin settings | ConfigFormBase | Automatic config sync, schema validation |
| Custom business logic | FormBase | Full control, service injection |
| Delete/confirm action | ConfirmFormBase | Standard confirmation UI |
| Entity create/edit | EntityForm | Entity-specific features (see Entity API guide) |
| Multi-step workflow | FormBase + setCached() | State persistence across steps |

## Pattern

Form API is declarative - you define structure, Drupal handles rendering and security.

```php
class ExampleForm extends FormBase {
  public function getFormId() {
    return 'example_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['field'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Label'),
      '#required' => TRUE,
    ];
    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $value = $form_state->getValue('field');
    // Process submission
  }
}
```

## Core Concepts

**Lifecycle:** Build → Validate → Submit → Redirect

**Security:** Automatic CSRF tokens, input sanitization, access control

**State Management:** FormState persists across rebuilds (AJAX, multi-step)

**Forms as Controllers:** Accessed via routes with `_form` parameter

## Common Mistakes

- **Wrong**: Implementing FormInterface directly → **Right**: Extend FormBase (get helper methods)
- **Wrong**: Using `$_POST` directly → **Right**: Use `$form_state->getValue()` (sanitized, CSRF-checked)
- **Wrong**: Business logic in buildForm() → **Right**: buildForm() for UI only, submitForm() for logic

## See Also

- [FormBase Pattern](pattern-standard-form.md)
- [ConfigFormBase Pattern](pattern-config-form.md)
- [Form Lifecycle](architecture-lifecycle.md)
- Reference: `/web/core/lib/Drupal/Core/Form/`
