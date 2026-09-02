---
description: "Drupal Form API overview - declarative render array system for building secure forms"
tldr: "Use Form API when you need user input with validation and CSRF protection. Use render arrays for display-only content."
drupal_version: "11.x"
---

# Form API Overview

## When to Use

> Use Form API when you need user input with validation and CSRF protection. Use render arrays for display-only content.

This guide provides architectural decision-making guidance for Drupal's Form API. It focuses on patterns, best practices, and references to core code implementations rather than step-by-step tutorials.

**Key Principle:** Form API is a declarative render array-based system that handles the complete form lifecycle: building, validation, submission, and security.

## Core Concepts

- Forms are controllers accessed via routes with `_form` parameter
- Forms implement FormInterface (or extend base classes)
- Lifecycle: Build → Validate → Submit → Redirect
- Security: CSRF tokens, input sanitization, access control
- State management: FormState object persists across rebuilds

## Decision: When to Use Forms

| Use Case | Form Type |
|----------|-----------|
| Admin settings | ConfigFormBase |
| Custom business logic | FormBase |
| Delete/confirm action | ConfirmFormBase |
| Entity create/edit | EntityForm (see Entity API guide) |
| Multi-step workflow | FormBase + setCached() |

## Pattern: A Minimal Form

Form API is declarative — you define structure, Drupal handles rendering and security.

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

## See Also

- [Entity API Guide](../entities/index.md) (for entity forms)
- [AJAX API Guide](../ajax/index.md) (for advanced AJAX patterns)
- [Security API Guide](../security/index.md) (for access control patterns)
- [Architecture: Core Form Classes](architecture-core-classes.md)
- [Architecture: Form Lifecycle](architecture-lifecycle.md)
- Reference: `/web/core/lib/Drupal/Core/Form/`
