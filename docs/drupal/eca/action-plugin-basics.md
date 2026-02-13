---
description: Create custom ECA Action plugins with ConfigurableActionBase for user-configurable operations
drupal_version: "11.x"
---

# Action Plugin Basics

## When to Use

> Create custom Action plugins when you need to perform operations that existing ECA actions cannot handle, such as integrating with external APIs, processing custom data structures, or implementing specialized business logic.

## Decision

| If you need... | Use Base Class | Why |
|----------------|----------------|-----|
| User-configurable action | `ConfigurableActionBase` | Provides form building, token support, configuration storage |
| Simple action with no config | `ActionBase` | Minimal overhead for straightforward operations |
| Form field manipulation | `FormFieldActionBase` | Built-in form field lookup and modification logic |
| Key-value storage operations | `KeyValueStoreBase` | Integrated KV store access patterns |

## Pattern

```php
<?php
namespace Drupal\my_module\Plugin\Action;

use Drupal\Core\Action\Attribute\Action;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\eca\Attribute\EcaAction;
use Drupal\eca\Plugin\Action\ConfigurableActionBase;

#[Action(
  id: 'my_module_custom_action',
  label: new TranslatableMarkup('My Module: Custom Action'),
  type: 'entity'  // Optional: passes entity context
)]
#[EcaAction(
  description: new TranslatableMarkup('Performs custom business logic.'),
  version_introduced: '1.0.0',
)]
class CustomAction extends ConfigurableActionBase {

  public function defaultConfiguration(): array {
    return [
      'input_field' => '',
      'result_token' => '',
    ] + parent::defaultConfiguration();
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form['input_field'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Input value'),
      '#default_value' => $this->configuration['input_field'],
      '#eca_token_replacement' => TRUE,
      '#eca_token_reference' => TRUE,
    ];

    $form['result_token'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Result token name'),
      '#default_value' => $this->configuration['result_token'],
      '#required' => TRUE,
    ];

    return parent::buildConfigurationForm($form, $form_state);
  }

  public function submitConfigurationForm(array &$form, FormStateInterface $form_state): void {
    $this->configuration['input_field'] = $form_state->getValue('input_field');
    $this->configuration['result_token'] = $form_state->getValue('result_token');
    parent::submitConfigurationForm($form, $form_state);
  }

  public function execute(): void {
    $input = $this->tokenService->getOrReplace($this->configuration['input_field']);

    // Business logic
    $result = $this->performOperation($input);

    // Store result for downstream actions
    $this->tokenService->addTokenData($this->configuration['result_token'], $result);
  }
}
```

## Common Mistakes

- **Wrong**: Missing `parent::buildConfigurationForm()` call → **Right**: ALWAYS call parent LAST
- **Wrong**: Missing `#eca_token_replacement` attribute → **Right**: Add attribute to enable token replacement
- **Wrong**: Accessing `$this->configuration` directly in `execute()` → **Right**: Use `tokenService->getOrReplace()`
- **Wrong**: Using `new static()` in `create()` → **Right**: Use `parent::create()`
- **Wrong**: Missing both `#[Action]` and `#[EcaAction]` attributes → **Right**: Include both attributes

## See Also

- [Advanced Action Patterns](advanced-action-patterns.md) for API integration
- [Token Form Integration](token-form-integration.md) for comprehensive token support
- [Service Injection](service-injection.md) for adding custom services

**References:**
- Core: `/modules/contrib/eca/src/Plugin/Action/ConfigurableActionBase.php`
- Example: `/modules/contrib/eca_base/src/Plugin/Action/EcaStateWrite.php`
