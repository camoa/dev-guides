---
description: Avoid critical ECA plugin mistakes — parent::create pattern, token attributes, negationCheck
drupal_version: "11.x"
---

# Common Pitfalls

## When to Use

> Review this section before completing any ECA plugin to avoid the most common mistakes that break plugins or cause maintenance problems.

## Decision

All pitfalls listed here are MANDATORY to avoid. They are not suggestions.

## Pattern

**Constructor and Service Injection:**

**DON'T:**
```php
// Using new static() - breaks when parent changes
public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
  return new static(
    $configuration,
    $plugin_id,
    $plugin_definition,
    $container->get('entity_type.manager'),
    $container->get('eca.token_services'),
    // ... listing all parent services
  );
}
```

**DO:**
```php
// Use parent::create() - resilient to parent changes
public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
  $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
  $instance->myCustomService = $container->get('my_module.custom_service');
  return $instance;
}
```

**Configuration Methods:**

**DON'T:**
```php
// Missing parent call
public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
  $form['field'] = [...];
  return $form;  // Token browser won't appear!
}
```

**DO:**
```php
// Call parent LAST
public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
  $form['field'] = [...];
  return parent::buildConfigurationForm($form, $form_state);
}
```

**Token Integration:**

**DON'T:**
```php
// Missing token attributes
$form['field'] = [
  '#type' => 'textfield',
  '#description' => $this->t('Enter value'),
];

// Direct config access in execute()
$value = $this->configuration['field_name'];
```

**DO:**
```php
// Proper token attributes
$form['field'] = [
  '#type' => 'textfield',
  '#eca_token_replacement' => TRUE,
  '#eca_token_reference' => TRUE,
  '#description' => $this->t('Enter value. Use tokens like [entity:title].'),
];

// Token-aware value retrieval
$value = $this->tokenService->getOrReplace($this->configuration['field_name']);
```

**Condition Evaluation:**

**DON'T:**
```php
// Missing negationCheck()
public function evaluate(): bool {
  return $this->checkCondition();  // Negation won't work!
}
```

**DO:**
```php
// Always wrap with negationCheck()
public function evaluate(): bool {
  $result = $this->checkCondition();
  return $this->negationCheck($result);
}
```

**StringComparisonBase:**

**DON'T:**
```php
// Overriding final method
public function evaluate(): bool {
  // Fatal error - evaluate() is FINAL!
}
```

**DO:**
```php
// Override these instead
protected function getLeftValue(): string {
  return $this->tokenService->getOrReplace($this->configuration['left']);
}

protected function getRightValue(): string {
  return $this->tokenService->getOrReplace($this->configuration['right']);
}
```

**Attributes:**

**DON'T:**
```php
// Missing EcaAction attribute
#[Action(
  id: 'my_action',
  label: new TranslatableMarkup('My Action'),
)]
class MyAction extends ConfigurableActionBase {
  // Won't register properly!
}
```

**DO:**
```php
// Both attributes required
#[Action(
  id: 'my_action',
  label: new TranslatableMarkup('My Action'),
)]
#[EcaAction(
  description: new TranslatableMarkup('What it does.'),
  version_introduced: '1.0.0',
)]
class MyAction extends ConfigurableActionBase {
}
```

## Common Mistakes

- Using `new static()` in `create()` → Breaks when parent constructor changes
- Not calling `parent::buildConfigurationForm()` → Missing token browser
- Accessing `$this->configuration` directly in `execute()` → Ignores token replacement
- Missing `#eca_token_replacement` → Tokens appear as literal text
- Missing `negationCheck()` in conditions → Negation toggle doesn't work
- Overriding `StringComparisonBase::evaluate()` → Fatal error (method is FINAL)
- Missing `#[EcaAction]` attribute → Plugin doesn't register
- Not calling parent methods → Breaks base class functionality

## See Also

- [Mandatory Rules](mandatory-rules.md) for enforcement checklist
- [Service Injection](service-injection.md) for create() patterns
- [String Comparison Conditions](string-comparison-conditions.md) for StringComparisonBase

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/EcaPluginBase.php`
