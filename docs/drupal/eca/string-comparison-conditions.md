---
description: Compare values with StringComparisonBase — override getLeftValue/getRightValue, NOT evaluate
drupal_version: "11.x"
---

# String Comparison Conditions

## When to Use

> Use StringComparisonBase when comparing two values using standard operators (equals, contains, starts with, regex, etc.). The base class provides operator selection and comparison logic; you only implement value retrieval.

## Decision

**CRITICAL:** `StringComparisonBase::evaluate()` is FINAL. You CANNOT override it.

| Override Method | Purpose | Return Type |
|-----------------|---------|-------------|
| `getLeftValue()` | Retrieve left comparison value | `string` |
| `getRightValue()` | Retrieve right comparison value | `string` |

## Pattern

```php
#[EcaCondition(
  id: 'my_module_compare_values',
  label: new TranslatableMarkup('My Module: Compare Values'),
)]
class CompareValuesCondition extends StringComparisonBase {

  public function defaultConfiguration(): array {
    return [
      'left_value' => '',
      'right_value' => '',
    ] + parent::defaultConfiguration();
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form['left_value'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Left value'),
      '#default_value' => $this->configuration['left_value'],
      '#eca_token_replacement' => TRUE,
    ];

    $form['right_value'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Right value'),
      '#default_value' => $this->configuration['right_value'],
      '#eca_token_replacement' => TRUE,
    ];

    return parent::buildConfigurationForm($form, $form_state);
  }

  // REQUIRED: Override these, NOT evaluate()
  protected function getLeftValue(): string {
    return $this->tokenService->getOrReplace($this->configuration['left_value']);
  }

  protected function getRightValue(): string {
    return $this->tokenService->getOrReplace($this->configuration['right_value']);
  }
}
```

## Common Mistakes

- **Wrong**: Overriding `evaluate()` → **Right**: Fatal error (method is FINAL)
- **Wrong**: Not calling `parent::buildConfigurationForm()` → **Right**: Missing operator dropdown
- **Wrong**: Returning non-string from `getLeftValue()`/`getRightValue()` → **Right**: Type errors
- **Wrong**: Forgetting token replacement → **Right**: Comparing literal strings instead of values
- **Wrong**: Not handling NULL values → **Right**: Comparison failures

## See Also

- [Condition Plugin Basics](condition-plugin-basics.md) for general conditions
- [Token Form Integration](token-form-integration.md) for token replacement
- [Mandatory Rules](mandatory-rules.md) for inheritance rules

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/Condition/StringComparisonBase.php`
- Example: `/modules/contrib/eca/modules/base/src/Plugin/ECA/Condition/ScalarComparison.php`
