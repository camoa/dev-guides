---
description: ConfigFormBase — admin settings forms with automatic config sync
drupal_version: "11.x"
---

# Pattern: Configuration Form (ConfigFormBase)

## When to Use

> Use ConfigFormBase for admin settings. Use #config_target (10.2+) for declarative binding. Use FormBase for non-config data.

## Decision

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| #config_target | Simple config mapping | Low |
| #config_target + ConfigTarget | Need transformations | Medium |
| Manual get/set | Complex logic, conditional saving | High |

## Pattern

**Modern (#config_target - Drupal 10.2+):**

```php
<?php

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
    $form['api_key'] = [
      '#type' => 'textfield',
      '#title' => $this->t('API Key'),
      '#config_target' => 'mymodule.settings:api_key',
    ];

    return parent::buildForm($form, $form_state);
  }
}
```

**Traditional (Manual sync):**

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $config = $this->config('mymodule.settings');

  $form['api_key'] = [
    '#type' => 'textfield',
    '#title' => $this->t('API Key'),
    '#default_value' => $config->get('api_key'),
  ];

  return parent::buildForm($form, $form_state);
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $this->config('mymodule.settings')
    ->set('api_key', $form_state->getValue('api_key'))
    ->save();

  parent::submitForm($form, $form_state);
}
```

Reference: `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php` lines 106-120

## Required Configuration Files

1. `config/install/mymodule.settings.yml` - Default values
2. `config/schema/mymodule.schema.yml` - Typed data definition

## Benefits of #config_target

- Less code (no manual get/set in submit)
- Automatic validation from schema constraints
- Works outside forms (recipes, programmatic config)

## Common Mistakes

- **Wrong**: Forgetting `getEditableConfigNames()` implementation → **Right**: Return array of config names
- **Wrong**: Not creating schema file (validation won't work) → **Right**: Define schema for validation
- **Wrong**: Using ConfigFormBase for non-config storage → **Right**: Use FormBase for non-config data
- **Wrong**: Hardcoding config names instead of constants → **Right**: Define config name constants

## See Also

- [Validation Architecture](validation-architecture.md)
- [Typed Data Constraints](https://www.drupal.org/project/drupal/issues/2971727)
- Documentation: [#config_target](https://www.drupal.org/node/3373502)
- Reference: `/modules/contrib/ai_provider_anthropic/src/Form/AnthropicConfigForm.php`
