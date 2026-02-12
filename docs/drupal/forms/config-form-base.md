---
description: ConfigFormBase — module settings forms that save to config
drupal_version: "11.x"
---

# ConfigFormBase

## When to Use

> Use ConfigFormBase when your form saves settings to Drupal configuration (e.g., API keys, feature toggles, display options). Use FormBase if the form processes input but doesn't store config.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Module settings page | ConfigFormBase | Auto-loads/saves config, provides `getEditableConfigNames()` |
| Admin toggle or option | ConfigFormBase | Settings belong in config system |
| User-submitted data (contact, search) | FormBase | Not config — process and discard or store in DB |
| Entity edit form | EntityForm | Not a standalone form |

## Pattern

```php
namespace Drupal\my_module\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class SettingsForm extends ConfigFormBase {

  protected function getEditableConfigNames() {
    return ['my_module.settings'];
  }

  public function getFormId() {
    return 'my_module_settings';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('my_module.settings');

    $form['api_key'] = [
      '#type' => 'textfield',
      '#title' => $this->t('API Key'),
      '#default_value' => $config->get('api_key'),
      '#required' => TRUE,
    ];

    return parent::buildForm($form, $form_state);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config('my_module.settings')
      ->set('api_key', $form_state->getValue('api_key'))
      ->save();

    parent::submitForm($form, $form_state);
  }

}
```

## Common Mistakes

- **Wrong**: Extending `FormBase` for settings (you lose config auto-handling)
- **Wrong**: Forgetting `parent::buildForm()` (no Save button rendered)
- **Wrong**: Using `\Drupal::config()` instead of `$this->config()` (bypasses editability)
- **Right**: Always call `parent::submitForm()` to get the status message

## Route

```yaml
my_module.settings:
  path: '/admin/config/system/my-module'
  defaults:
    _form: '\Drupal\my_module\Form\SettingsForm'
    _title: 'My Module Settings'
  requirements:
    _permission: 'administer site configuration'
```

## See Also

- [FormBase](form-base.md) — for non-config forms
- [Validation](validation.md) — adding validation to any form
