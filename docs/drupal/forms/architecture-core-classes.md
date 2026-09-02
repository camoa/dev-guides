---
description: "Core Form API classes and interfaces - base classes, services, and selection criteria"
tldr: "Choose the appropriate base class based on your form's purpose. Use FormBase for general forms, ConfigFormBase for settings, ConfirmFormBase for confirmations."
drupal_version: "11.x"
---

# Architecture: Core Form Classes

## When to Use

> Choose the appropriate base class based on your form's purpose. Use FormBase for general forms, ConfigFormBase for settings, ConfirmFormBase for confirmations.

## Reference: Primary Interfaces

**FormInterface** - Base form contract

- Location: `/web/core/lib/Drupal/Core/Form/FormInterface.php`
- Methods: `getFormId()`, `buildForm()`, `validateForm()`, `submitForm()`
- When to implement: Custom form without base class benefits

**FormStateInterface** - State management contract

- Location: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php`
- Size: 1160+ lines defining all state operations
- Purpose: Value access, storage, control flags, error handling

**FormBuilderInterface** - Form building service contract

- Location: `/web/core/lib/Drupal/Core/Form/FormBuilderInterface.php`
- Service: `@form_builder`
- Use for: Programmatic form rendering, submission

## Reference: Base Form Classes

| Class | Purpose | Location |
|-------|---------|----------|
| FormBase | Standard forms with DI | `/web/core/lib/Drupal/Core/Form/FormBase.php` |
| ConfigFormBase | Config management | `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php` |
| ConfirmFormBase | Confirmation dialogs | `/web/core/lib/Drupal/Core/Form/ConfirmFormBase.php` |

## Reference: Core Services

| Service | Purpose | File |
|---------|---------|------|
| FormBuilder | Main building engine | `/web/core/lib/Drupal/Core/Form/FormBuilder.php` |
| FormValidator | Validation orchestration | `/web/core/lib/Drupal/Core/Form/FormValidator.php` |
| FormSubmitter | Submission handling | `/web/core/lib/Drupal/Core/Form/FormSubmitter.php` |

## Decision: Base Class Selection

```
Need config management? → ConfigFormBase
Need confirmation dialog? → ConfirmFormBase
Entity create/edit? → EntityForm (see Entity API guide)
Everything else? → FormBase
```

## Pattern: Extending a Base Class

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

## Common Mistakes

- Not using dependency injection via `create()` method
    - **WHY BAD:** Breaks unit testing (can't mock services), violates SOLID principles, prevents service substitution for testing/overrides
- Extending wrong base class (ConfigFormBase for non-config forms)
    - **WHY BAD:** ConfigFormBase expects config schema, requires getEditableConfigNames(), adds unnecessary overhead for non-config data
- Implementing FormInterface directly when base class would work
    - **WHY BAD:** Lose helper methods (t(), messenger(), config(), etc.), must implement all interface methods manually, harder to maintain

## See Also

- [Form Lifecycle](architecture-lifecycle.md) (next section)
- [Dependency Injection Guide](../services/index.md)
- [Configuration API Guide](../config-management/index.md)
- Reference: [Form API Overview](https://www.drupal.org/docs/drupal-apis/form-api)
