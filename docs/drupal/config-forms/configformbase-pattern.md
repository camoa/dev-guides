---
description: Build module settings forms with ConfigFormBase
drupal_version: "11.x"
---

# ConfigFormBase Pattern

## When to Use

> Use ConfigFormBase when building a module settings page that stores configuration in the config system (database + YML export).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple module settings | ConfigFormBase | Automatic config loading/saving |
| Multiple config objects | ConfigFormBase with multiple getEditableConfigNames | Supports multiple configs |
| Config with validation constraints | ConfigFormBase + #config_target | Uses Drupal 11+ validation system |
| Non-config settings | FormBase + custom storage | ConfigFormBase is for config API only |

## Pattern

```php
namespace Drupal\mymodule\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class SettingsForm extends ConfigFormBase {

  protected function getEditableConfigNames() {
    return ['mymodule.settings'];
  }

  public function getFormId() {
    return 'mymodule_settings_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('mymodule.settings');

    $form['api_key'] = [
      '#type' => 'textfield',
      '#title' => $this->t('API Key'),
      '#default_value' => $config->get('api_key'),
      '#required' => TRUE,
      '#config_target' => 'mymodule.settings:api_key', // Drupal 11+ validation
    ];

    return parent::buildForm($form, $form_state);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config('mymodule.settings')
      ->set('api_key', $form_state->getValue('api_key'))
      ->save();

    parent::submitForm($form, $form_state);
  }
}
```

**Routing** (mymodule.routing.yml):
```yaml
mymodule.settings:
  path: '/admin/config/mymodule/settings'
  defaults:
    _form: '\Drupal\mymodule\Form\SettingsForm'
    _title: 'MyModule Settings'
  requirements:
    _permission: 'administer site configuration'
```

**Config Schema** (config/schema/mymodule.schema.yml):
```yaml
mymodule.settings:
  type: config_object
  label: 'MyModule settings'
  mapping:
    api_key:
      type: string
      label: 'API Key'
      constraints:
        NotBlank: []
        Length:
          max: 255
```

## Common Mistakes

- **Wrong**: Not implementing getEditableConfigNames() → **Right**: Required method, returns array of config names
- **Wrong**: Using $config->save() without setting values first → **Right**: No error but config not updated
- **Wrong**: Forgetting parent::buildForm() → **Right**: Loses submit button and CSRF token
- **Wrong**: Forgetting parent::submitForm() → **Right**: Loses status message and cache clear
- **Wrong**: Using FormBase::config() in ConfigFormBase → **Right**: Different behavior, disables overrides unexpectedly
- **Wrong**: Not defining config schema → **Right**: Strict validation fails in Drupal 11+

## See Also

- [FormBase vs ListBuilder](formbase-vs-listbuilder.md)
- [Configuration Schema](configuration-schema.md)
- [Dependency Injection](dependency-injection.md)
- Reference: [ConfigFormBase with Simple Configuration API](https://www.drupal.org/docs/drupal-apis/form-api/configformbase-with-simple-configuration-api)
- Reference: core/modules/system/src/Form/SiteInformationForm.php
