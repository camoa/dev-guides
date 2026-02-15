---
description: Choose the right Drupal form base class to honor LSP behavioral contracts
drupal_version: "11.x"
---

# Form Hierarchy - Liskov Substitution (LSP)

## When to Use

Drupal form base classes follow LSP -- extend the right base for your use case. ConfigFormBase adds config-specific behavior; SettingsForm adds protected config behavior.

## Decision

| Form type | Extend | When to use |
|---|---|---|
| Basic form | FormBase | Contact forms, filters, non-config forms |
| Config form | ConfigFormBase | Editable config (my_module.settings) |
| Settings form | SettingsForm | Protected config (settings that affect multiple modules) |
| Entity form | EntityForm | Adding/editing entities |
| Custom | FormInterface | Need full control, multiple form objects |

## Pattern

**GOOD: Following form LSP**

```php
// ConfigFormBase extends FormBase - honors parent contract plus config-specific behavior
class MySettingsForm extends ConfigFormBase {
  protected function getEditableConfigNames() {
    return ['mymodule.settings'];
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // ConfigFormBase contract: save to config
    $this->config('mymodule.settings')
      ->set('api_key', $form_state->getValue('api_key'))
      ->save();
    parent::submitForm($form, $form_state);  // Honor parent behavior
  }
}
```

**BAD: Violating form LSP**

```php
// Extending ConfigFormBase but not using config
class MyForm extends ConfigFormBase {
  protected function getEditableConfigNames() {
    return [];  // Empty - why extend ConfigFormBase?
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Not saving to config violates ConfigFormBase contract
    \Drupal::state()->set('value', $form_state->getValue('value'));
    // Not calling parent::submitForm() breaks cache clearing
  }
}
```

Reference:

- `/core/lib/Drupal/Core/Form/FormBase.php` -- base contract
- `/core/lib/Drupal/Core/Form/ConfigFormBase.php` -- config-specific contract

## Common Mistakes

- Extending ConfigFormBase for non-config forms -- extend FormBase. **WHY:** ConfigFormBase expects config operations; violating this breaks config validation
- Not calling parent::submitForm() -- always call parent. **WHY:** Parent clears form cache, triggers post-save hooks, handles redirects
- Overriding methods without preserving behavior -- honor parent contracts. **WHY:** buildForm() signature must match; changing return type breaks form system
- Using wrong form base (e.g., FormBase for entity forms) -- use EntityForm. **WHY:** EntityForm provides entity-specific validation, access control, routing

## See Also

- [Entity Hierarchy](entity-hierarchy-lsp.md) for entity LSP patterns
- [Access Results](access-results-lsp.md) for access LSP patterns
