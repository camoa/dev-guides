---
description: FormBase — general-purpose forms for custom business logic
drupal_version: "11.x"
---

# Pattern: Standard Form (FormBase)

## When to Use

> Use FormBase for general-purpose forms with custom business logic. Use ConfigFormBase for admin settings. Use ConfirmFormBase for confirmation dialogs.

## Decision

| Use Case | Form Type | Why |
|----------|-----------|-----|
| Custom business logic | FormBase | General purpose with DI |
| API integration | FormBase | Custom processing needs |
| Administrative operations | FormBase | Non-config operations |
| Configuration management | ConfigFormBase | Automatic config sync |
| Entity create/edit | EntityForm | Entity operations |
| Confirmation dialogs | ConfirmFormBase | Delete/confirm pattern |

## Pattern

```php
<?php

namespace Drupal\mymodule\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class MyForm extends FormBase {

  public static function create(ContainerInterface $container) {
    return new static(
      // Inject services here
    );
  }

  public function getFormId() {
    return 'mymodule_my_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['field'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Field'),
      '#required' => TRUE,
    ];

    $form['actions']['submit'] = [
      '#type' => 'submit',
      '#value' => $this->t('Submit'),
    ];

    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $value = $form_state->getValue('field');
    // Process submission
    $form_state->setRedirect('route.name');
  }
}
```

Reference: `/web/core/modules/user/src/Form/UserLoginForm.php`

## Key Decisions

| Decision Point | Recommendation | Example |
|----------------|----------------|---------|
| Service injection | Use `create()` method | UserLoginForm lines 50-70 |
| Multiple validators | Add to `$form['#validate']` array | UserLoginForm lines 90-95 |
| Intermediate data | Use `$form_state->set()`/`get()` | Multi-step pattern |
| Post-submit routing | `$form_state->setRedirect()` | All submit handlers |

**Validation Chain:**
```
Element validators run first (#element_validate)
Then form validators ($form['#validate'] array)
Then class validateForm() method
Error on any → no submit handlers run
```

## Common Mistakes

- **Wrong**: Not implementing `getFormId()` with unique ID → **Right**: Return unique machine name
  - WHY BAD: Form ID collisions break form caching, alter hooks fail, form_build_id validation breaks
- **Wrong**: Using `$_POST` instead of `$form_state->getValue()` → **Right**: Use FormState API
  - WHY BAD: Bypasses CSRF protection, no sanitization, validation skipped, direct security vulnerability
- **Wrong**: Forgetting to call `parent::buildForm()` when needed → **Right**: Call parent when overriding
  - WHY BAD: Breaks form caching setup, CSRF token not added, form structure incomplete
- **Wrong**: Not using dependency injection for services → **Right**: Inject via `create()` method
  - WHY BAD: Can't unit test (mocking impossible), breaks service substitution, creates hidden dependencies

## See Also

- [Validation Architecture](validation-architecture.md)
- [Submission Architecture](submission-architecture.md)
- [Multi-Step Forms](multi-step-forms.md)
- Dependency Injection Guide
- Reference: `/web/core/lib/Drupal/Core/Form/FormBase.php`
