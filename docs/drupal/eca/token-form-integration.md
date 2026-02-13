---
description: Add token replacement, reference, and selection to ECA form fields
drupal_version: "11.x"
---

# Token Form Integration

## When to Use

> Add token integration to form fields whenever users need to reference dynamic values from the workflow. Tokens enable accessing event data, global values, and previous action results.

## Decision

| Form Attribute | Purpose | When to Use |
|----------------|---------|-------------|
| `#eca_token_replacement` | Enable token replacement | Any text field that should process tokens |
| `#eca_token_reference` | Show in token browser | Fields that define token names for storage |
| `#eca_token_select_option` | Add "Defined by token" option | Select/radio fields where options can come from tokens |

## Pattern

```php
public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
  // Text field with token replacement
  $form['input_value'] = [
    '#type' => 'textfield',
    '#title' => $this->t('Input value'),
    '#default_value' => $this->configuration['input_value'],
    '#description' => $this->t('Use tokens like [entity:title].'),
    '#eca_token_replacement' => TRUE,  // Process tokens in this field
  ];

  // Token name field (for storing results)
  $form['result_token'] = [
    '#type' => 'textfield',
    '#title' => $this->t('Result token name'),
    '#default_value' => $this->configuration['result_token'],
    '#description' => $this->t('Name to store results under.'),
    '#eca_token_reference' => TRUE,  // Show in token browser
  ];

  // Select field with token option
  $form['operation'] = [
    '#type' => 'select',
    '#title' => $this->t('Operation'),
    '#options' => ['add' => 'Add', 'remove' => 'Remove'],
    '#default_value' => $this->configuration['operation'],
    '#eca_token_select_option' => TRUE,  // Add "Defined by token" option
  ];

  // CRITICAL: Call parent LAST to add token browser
  return parent::buildConfigurationForm($form, $form_state);
}

public function execute(): void {
  // Process tokens using tokenService
  $input = $this->tokenService->getOrReplace($this->configuration['input_value']);

  // Get token data directly
  $token_data = $this->tokenService->getTokenData('my_token');

  // Store results for downstream actions
  $this->tokenService->addTokenData($this->configuration['result_token'], $result);
}
```

## Common Mistakes

- **Wrong**: Not calling `parent::buildConfigurationForm()` → **Right**: Token browser missing (call it LAST)
- **Wrong**: Missing `#eca_token_replacement` → **Right**: Tokens appear as literal text `[entity:title]`
- **Wrong**: Using `$this->configuration['field']` directly in `execute()` → **Right**: Use `tokenService->getOrReplace()`
- **Wrong**: No description mentioning tokens → **Right**: Users don't know they can use tokens
- **Wrong**: Wrong attribute on wrong field type → **Right**: Token features won't work properly

## See Also

- [Complex Token Structures](complex-token-structures.md) for structured data
- [Action Plugin Basics](action-plugin-basics.md) for complete action example
- [Condition Plugin Basics](condition-plugin-basics.md) for condition token usage

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/EcaPluginBase.php` (buildConfigurationForm)
- Documentation: https://ecaguide.org/ (Token system)
