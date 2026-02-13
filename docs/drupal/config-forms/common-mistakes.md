---
description: Common configuration form mistakes and how to fix them
drupal_version: "11.x"
---

# Common Mistakes

## When to Use

> Reference when debugging form issues or reviewing code.

## Decision

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Config not saving | Forgot $config->save() | Call ->save() after ->set() |
| Operations not appearing | Missing parent::buildRow() | Add parent call |
| Dropbutton not styled | Missing library attachment | Attach library in form |
| FOUC on dropbuttons | Missing CSS visibility rules | Add FOUC prevention CSS |
| Validation not working | Missing #config_target | Add #config_target for Drupal 11+ |
| Form not submitting | Missing parent::buildForm() | Add parent call for submit button |
| Double-escaped HTML | Sanitizing on input | Sanitize on output only |
| Permission denied | Missing _permission in route | Add permission requirement |

## Pattern

**ConfigFormBase Issues**:
```php
// WRONG: Config not saved
$this->config('mymodule.settings')->set('key', $value);

// RIGHT: Config saved
$this->config('mymodule.settings')
  ->set('key', $value)
  ->save();
```

**ListBuilder Issues**:
```php
// WRONG: Operations missing
public function buildRow(EntityInterface $entity) {
  $row['label'] = $entity->label();
  return $row; // Missing operations!
}

// RIGHT: Operations included
public function buildRow(EntityInterface $entity) {
  $row['label'] = $entity->label();
  return $row + parent::buildRow($entity); // Adds operations
}
```

**FormBase Issues**:
```php
// WRONG: No submit button
public function buildForm(array $form, FormStateInterface $form_state) {
  // Build form...
  return $form; // Missing parent call!
}

// RIGHT: Submit button included
public function buildForm(array $form, FormStateInterface $form_state) {
  // Build form...
  return parent::buildForm($form, $form_state);
}
```

**Operations Issues**:
```php
// WRONG: Manual HTML
$row['operations'] = ['#markup' => '<a href="/edit">Edit</a>'];

// RIGHT: Operations render element
$row['operations'] = [
  '#type' => 'operations',
  '#links' => $operations,
];
```

**Validation Issues**:
```php
// WRONG: No validation (Drupal 11+)
$form['api_key'] = [
  '#type' => 'textfield',
  '#default_value' => $config->get('api_key'),
];

// RIGHT: With validation
$form['api_key'] = [
  '#type' => 'textfield',
  '#default_value' => $config->get('api_key'),
  '#config_target' => 'mymodule.settings:api_key', // Uses schema constraints
];
```

**DI Issues**:
```php
// WRONG: Static service call
$entities = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple($ids);

// RIGHT: Injected service
$entities = $this->entityTypeManager->getStorage('node')->loadMultiple($ids);
```

## Common Mistakes

- **Wrong**: Using FormBase for simple config → **Right**: Use ConfigFormBase, automatic save/load
- **Wrong**: Using ConfigFormBase for non-config data → **Right**: Use FormBase, config API inappropriate
- **Wrong**: Not checking if link template exists before using → **Right**: Fatal error on entity->toUrl()
- **Wrong**: Mixing routing defaults (_form vs _entity_list) → **Right**: Wrong handler invoked
- **Wrong**: Not attaching CSS library to prevent FOUC → **Right**: Ugly dropbutton flash
- **Wrong**: Forgetting config schema → **Right**: Strict validation failures in Drupal 11+

## See Also

- [ConfigFormBase Pattern](configformbase-pattern.md)
- [FormBase Pattern](formbase-pattern.md)
- [ListBuilder Pattern](listbuilder-pattern.md)
- [Operations Implementation](operations-implementation.md)
- Reference: Drupal API documentation, core examples
