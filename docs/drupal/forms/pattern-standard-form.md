---
description: FormBase — general-purpose forms for custom business logic
drupal_version: "11.x"
---

# Pattern: Standard Form (FormBase)

## When to Use

> Use FormBase for general-purpose forms. Use ConfigFormBase for admin settings. Use ConfirmFormBase for delete confirmations.

## Decision

| Use Case | Form Type | Why |
|----------|-----------|-----|
| Custom business logic | FormBase | General purpose |
| API integration | FormBase | Custom processing |
| Configuration management | ConfigFormBase | Auto config sync |
| Entity create/edit | EntityForm | Entity operations |
| Confirmation dialogs | ConfirmFormBase | Delete/confirm pattern |

## Pattern

```php
<?php

namespace Drupal\mymodule\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

class MyForm extends FormBase {

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

## Value Storage

```php
// Build phase: set default value
$form['field']['#default_value'] = $initial_value;

// Submit phase: get submitted value
$value = $form_state->getValue('field');

// Cross-rebuild: persist data
$form_state->set('stored_data', $data);
```

## Common Mistakes

- **Wrong**: Not implementing `getFormId()` with unique ID → **Right**: Return unique machine name
- **Wrong**: Using `$_POST` instead of `$form_state->getValue()` → **Right**: Use FormState API
- **Wrong**: Forgetting to call `parent::buildForm()` when needed → **Right**: Call parent when overriding
- **Wrong**: Not using dependency injection for services → **Right**: Inject via `create()` method

## See Also

- [Validation Architecture](validation-architecture.md)
- [Submission Architecture](submission-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormBase.php`
