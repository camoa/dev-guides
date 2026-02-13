---
description: Pre-completion checklist for ECA plugins — all rules are MANDATORY, not optional
drupal_version: "11.x"
---

# Mandatory Rules

## When to Use

> Use this checklist before completing ANY ECA plugin. These are not optional - violating these rules will cause bugs or break your plugin.

## Decision

Every rule below is MANDATORY. Check each one before considering your plugin complete.

## Pattern

**create() Method Rules:**

- ALWAYS call `parent::create()` first
- NEVER use `new static()` when base class has dependencies
- ONLY inject services that are NEW to your plugin
- NEVER list parent's services (entity_type.manager, eca.token_services, etc.)

```php
// Correct pattern
public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): static {
  $instance = parent::create($container, $configuration, $plugin_id, $plugin_definition);
  $instance->myNewService = $container->get('my.new.service');
  return $instance;
}
```

**Configuration Method Rules:**

- `defaultConfiguration()` → ALWAYS merge: `return [...] + parent::defaultConfiguration()`
- `buildConfigurationForm()` → ALWAYS call `parent::buildConfigurationForm()` LAST
- `submitConfigurationForm()` → ALWAYS call `parent::submitConfigurationForm()`
- `access()` → ALWAYS call `parent::access()` after your checks

```php
// defaultConfiguration - merge
public function defaultConfiguration(): array {
  return ['my_field' => ''] + parent::defaultConfiguration();
}

// buildConfigurationForm - call parent LAST
public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
  $form['my_field'] = [...];
  return parent::buildConfigurationForm($form, $form_state);
}

// submitConfigurationForm - call parent
public function submitConfigurationForm(array &$form, FormStateInterface $form_state): void {
  $this->configuration['my_field'] = $form_state->getValue('my_field');
  parent::submitConfigurationForm($form, $form_state);
}

// access - call parent after checks
public function access($object, ?AccountInterface $account = NULL, $return_as_object = FALSE) {
  if (!$this->isValid()) {
    return $return_as_object ? AccessResult::forbidden('Invalid.') : FALSE;
  }
  return parent::access($object, $account, $return_as_object);
}
```

**Token Integration Rules:**

- Add `#eca_token_replacement => TRUE` to text fields that should process tokens
- Add `#eca_token_reference => TRUE` to fields that define token names
- Use `tokenService->getOrReplace()` in `execute()`, NEVER direct config access
- Call `parent::buildConfigurationForm()` LAST to include token browser

**Condition Rules:**

- ALWAYS wrap evaluate() result with `negationCheck()`
- NEVER override `StringComparisonBase::evaluate()` (it's FINAL)
- Override `getLeftValue()` and `getRightValue()` instead for comparisons
- Return bool from `evaluate()`, never NULL

**Attribute Rules:**

- BOTH `#[Action]` AND `#[EcaAction]` required for actions
- BOTH `#[EcaEvent]` and deriver required for events
- `#[EcaCondition]` required for conditions
- Include `version_introduced` in ECA attributes

**Pre-Completion Checklist:**

1. No parent constructor parameters duplicated in child
2. Child only injects its OWN new dependencies
3. All overridden methods call their parent
4. `StringComparisonBase::evaluate()` is NOT overridden
5. All text fields have appropriate `#eca_token_*` attributes
6. `execute()` uses `tokenService->getOrReplace()` for config values
7. Conditions wrap result with `negationCheck()`
8. Both required attributes present

## Common Mistakes

Every item in [Common Pitfalls](common-pitfalls.md) violates one of these mandatory rules. Review that section for examples of what NOT to do.

## See Also

- [Common Pitfalls](common-pitfalls.md) for mistake examples
- [Service Injection](service-injection.md) for create() details
- [String Comparison Conditions](string-comparison-conditions.md) for StringComparisonBase rules

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/EcaPluginBase.php` (FINAL constructor)
