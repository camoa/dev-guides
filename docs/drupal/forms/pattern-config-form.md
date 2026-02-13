---
description: ConfigFormBase pattern with #config_target for automatic configuration sync
drupal_version: "11.x"
---

# Pattern: Configuration Form (ConfigFormBase)

## When to Use

> Use ConfigFormBase for admin settings and system configuration. Use FormBase for non-configuration data or temporary workflow data.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Admin settings, module config | ConfigFormBase | Auto sync, schema validation |
| Non-configuration data | FormBase + custom storage | Full control |
| Entity configuration | EntityForm | Entity-specific features |
| Temporary workflow | FormBase with FormState | No config overhead |

## Pattern

Modern pattern with #config_target (Drupal 10.2+):

```php
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
    $form['api_key'] = [
      '#type' => 'textfield',
      '#title' => $this->t('API Key'),
      '#config_target' => 'mymodule.settings:api_key', // Auto sync
    ];

    $form['timeout'] = [
      '#type' => 'number',
      '#title' => $this->t('Timeout (seconds)'),
      '#config_target' => 'mymodule.settings:timeout',
    ];

    return parent::buildForm($form, $form_state);
  }
  // submitForm() not needed - automatic save
}
```

## Required Configuration Files

1. `config/install/mymodule.settings.yml` - Default values
2. `config/schema/mymodule.schema.yml` - Typed data definition

## Decision: #config_target vs Manual

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| #config_target | Simple config mapping | Low |
| #config_target + ConfigTarget | Need transformations | Medium |
| Manual get/set | Complex logic, conditional saving | High |

## Common Mistakes

- **Wrong**: No `getEditableConfigNames()` → **Right**: Required for override detection
- **Wrong**: No schema file → **Right**: Required for #config_target validation
- **Wrong**: ConfigFormBase for non-config data → **Right**: Use FormBase
- **Wrong**: Hardcoded config names → **Right**: Use constants

## See Also

- [Configuration API Guide](https://www.drupal.org/docs/drupal-apis/configuration-api)
- [#config_target Documentation](https://www.drupal.org/node/3373502)
- [QED42 Tutorial](https://www.qed42.com/insights/exploring-the-new-config-target-option-in-drupal-10)
- Reference: `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php`
