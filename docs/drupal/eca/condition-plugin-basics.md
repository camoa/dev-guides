---
description: Create custom ECA Condition plugins with ConditionBase for business logic evaluation
drupal_version: "11.x"
---

# Condition Plugin Basics

## When to Use

> Create custom Condition plugins when you need to evaluate business logic that existing conditions don't support, such as checking external API state, validating complex data structures, or implementing domain-specific rules.

## Decision

| If you need... | Base Class | Why |
|----------------|------------|-----|
| General condition logic | `ConditionBase` | Full control over evaluation logic |
| Compare two values | `StringComparisonBase` | Built-in comparison operators (equals, contains, regex, etc.) |
| Check list contents | `ListContainsTrait` + `ConditionBase` | Reusable list checking logic |
| Negate condition | Any base (use `negationCheck()`) | All conditions support negation |

## Pattern

```php
#[EcaCondition(
  id: 'my_module_token_check',
  label: new TranslatableMarkup('My Module: Token Check'),
  description: new TranslatableMarkup('Checks if token meets criteria.'),
)]
class TokenCheckCondition extends ConditionBase {

  public function defaultConfiguration(): array {
    return [
      'token_name' => '',
    ] + parent::defaultConfiguration();
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form['token_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Token name'),
      '#default_value' => $this->configuration['token_name'],
      '#required' => TRUE,
      '#eca_token_reference' => TRUE,
    ];

    return parent::buildConfigurationForm($form, $form_state);
  }

  public function submitConfigurationForm(array &$form, FormStateInterface $form_state): void {
    $this->configuration['token_name'] = $form_state->getValue('token_name');
    parent::submitConfigurationForm($form, $form_state);
  }

  public function evaluate(): bool {
    $token_name = trim((string) $this->configuration['token_name']);

    if ($token_name === '') {
      return FALSE;
    }

    $token_data = $this->tokenService->getTokenData($token_name);
    $result = !empty($token_data);

    // CRITICAL: Always wrap result with negationCheck()
    return $this->negationCheck($result);
  }
}
```

## Common Mistakes

- **Wrong**: Missing `negationCheck()` wrapper in `evaluate()` → **Right**: Negation toggle won't work
- **Wrong**: Not calling `parent::buildConfigurationForm()` → **Right**: Missing negation checkbox
- **Wrong**: Returning NULL instead of bool → **Right**: Type errors in strict mode
- **Wrong**: Complex logic in `evaluate()` → **Right**: Should be in separate methods for testability
- **Wrong**: Not handling empty/null token values → **Right**: Unexpected failures

## See Also

- [String Comparison Conditions](string-comparison-conditions.md) for value comparison
- [Token Form Integration](token-form-integration.md) for accessing token data
- [Common Pitfalls](common-pitfalls.md) for negationCheck() errors

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/Condition/ConditionBase.php`
- Example: `/modules/contrib/eca/modules/base/src/Plugin/ECA/Condition/TokenExists.php`
