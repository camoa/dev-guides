---
description: Core Form API classes and interfaces - base classes, services, and selection criteria
drupal_version: "11.x"
---

# Architecture: Core Form Classes

## When to Use

> Choose the appropriate base class based on your form's purpose. Use FormBase for general forms, ConfigFormBase for settings, ConfirmFormBase for confirmations.

## Decision

| Situation | Base Class | Why |
|-----------|------------|-----|
| Need config management | ConfigFormBase | Auto config sync, schema validation |
| Need confirmation dialog | ConfirmFormBase | Standard confirm UI, cancel link |
| Entity create/edit | EntityForm | Entity-specific features |
| Everything else | FormBase | General purpose, DI support |

## Pattern

All forms implement FormInterface or extend a base class.

```php
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

class MyForm extends FormBase {
  public function getFormId() {
    return 'my_module_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    // Define form structure
    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Process submission
  }
}
```

## Key Interfaces and Classes

| Component | Location | Purpose |
|-----------|----------|---------|
| FormInterface | `/web/core/lib/Drupal/Core/Form/FormInterface.php` | Core contract |
| FormStateInterface | `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` | State management (1160+ lines) |
| FormBase | `/web/core/lib/Drupal/Core/Form/FormBase.php` | Standard forms with DI |
| ConfigFormBase | `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php` | Config management |
| ConfirmFormBase | `/web/core/lib/Drupal/Core/Form/ConfirmFormBase.php` | Confirmation dialogs |

## Core Services

| Service | File | Purpose |
|---------|------|---------|
| FormBuilder | `/web/core/lib/Drupal/Core/Form/FormBuilder.php` | Main building engine |
| FormValidator | `/web/core/lib/Drupal/Core/Form/FormValidator.php` | Validation orchestration |
| FormSubmitter | `/web/core/lib/Drupal/Core/Form/FormSubmitter.php` | Submission handling |

## Common Mistakes

- **Wrong**: Not using dependency injection via `create()` → **Right**: Use `create()` method for testability
- **Wrong**: Extending ConfigFormBase for non-config forms → **Right**: ConfigFormBase only for config management
- **Wrong**: Implementing FormInterface directly → **Right**: Extend base class to get helper methods

## See Also

- [Form Lifecycle](architecture-lifecycle.md)
- [FormBase Pattern](pattern-standard-form.md)
- [ConfigFormBase Pattern](pattern-config-form.md)
- Reference: [Form API Overview](https://www.drupal.org/docs/drupal-apis/form-api)
