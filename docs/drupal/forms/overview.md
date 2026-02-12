---
description: Form API overview — core concepts, lifecycle, form type selection
drupal_version: "11.x"
---

# Form API Overview

## When to Use

> Use this overview to understand Form API architecture and choose the right form approach.

## Core Concepts

- Forms are controllers accessed via routes with `_form` parameter
- Forms implement FormInterface (or extend base classes)
- Lifecycle: Build → Validate → Submit → Redirect
- Security: CSRF tokens, input sanitization, access control
- State management: FormState object persists across rebuilds

## Decision

| Use Case | Form Type | Why |
|----------|-----------|-----|
| Admin settings | ConfigFormBase | Automatic config sync |
| Custom business logic | FormBase | General purpose |
| Delete/confirm action | ConfirmFormBase | Confirmation dialog |
| Entity create/edit | EntityForm | Entity operations |
| Multi-step workflow | FormBase + setCached() | State persistence |

## Pattern

Form API is a declarative render array-based system:

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['field'] = [
    '#type' => 'textfield',
    '#title' => $this->t('Label'),
    '#required' => TRUE,
  ];
  return $form;
}
```

Forms handle the complete lifecycle: building, validation, submission, and security.

## Common Mistakes

- **Wrong**: Choosing EntityForm for simple admin settings → **Right**: Use ConfigFormBase
- **Wrong**: Using FormBase for confirmation dialogs → **Right**: Use ConfirmFormBase
- **Wrong**: Building multi-step forms without setCached() → **Right**: Always enable caching for multi-step

## See Also

- [Architecture: Core Classes](architecture-core-classes.md)
- [Architecture: Lifecycle](architecture-lifecycle.md)
- [Decision Trees](decision-trees.md)
- Entity API Guide (for entity forms)
- AJAX API Guide (for advanced AJAX patterns)
- Security API Guide (for access control patterns)
