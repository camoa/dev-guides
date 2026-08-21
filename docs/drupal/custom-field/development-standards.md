---
description: "Drupal coding standards and API best practices for Custom Field -- dependency injection, field API usage, config-first fields, and empty checks."
tldr: "Inject services instead of static \\Drupal:: calls, use isEmpty() instead of checking individual sub-field properties, and deploy schema changes only through custom_field.update_manager in a hook_update_N() -- never raw SQL."
drupal_version: "11.x"
---

# Development Standards

## When to Use

You want to follow Drupal coding standards and API best practices when working with Custom Field programmatically.

## Best Practices

**Dependency injection** (not static calls):

```php
// GOOD: Inject services in custom plugins
class MyCustomType extends CustomFieldTypeBase {
  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected EntityTypeManagerInterface $entityTypeManager,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('entity_type.manager'),
    );
  }
}

// BAD: Static service calls
$entity = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
```

**Proper API usage**:

```php
// GOOD: Use field methods
$values = [];
foreach ($node->field_custom as $delta => $item) {
  $values[] = $item->street;
}

// BAD: Direct property access
$values = $node->field_custom->getValue(); // Bypasses field logic
```

**Configuration-first approach**:

- Create fields via UI or config YAML, not code
- Code-based fields harder to maintain, translate, export
- Use update hooks to modify field config, not programmatic creation

**Empty checks**:

```php
// GOOD: Use field isEmpty() method
if (!$node->field_custom->isEmpty()) {
  $value = $node->field_custom->street;
}

// BAD: Checking individual properties
if ($node->field_custom->street) { // May fail on 0, '0', FALSE
```

**Multi-value iteration**:

```php
// GOOD: Iterate properly
foreach ($node->field_custom as $delta => $item) {
  if (!$item->isEmpty()) {
    $output[] = $item->street;
  }
}

// BAD: Assume single value
$street = $node->field_custom->street; // Only gets delta 0
```

**Update hooks for schema changes**:

```php
function my_module_update_N() {
  /** @var \Drupal\custom_field\Service\UpdateManagerInterface $updateManager */
  $updateManager = \Drupal::service('custom_field.update_manager');

  // Add a new 'country' column to the `custom` field field_address on node.
  $updateManager->addColumn('node', 'field_address', 'country', 'string');

  return t('Added country column to field_address');
}
```

## Anti-Patterns

**Never do these**:

- Modify field schema directly in database -- always use the `custom_field.update_manager` service (`addColumn()` / `removeColumn()`). Schema changes without the update service break field property definitions and cause SQL errors
- Store sensitive data (passwords, API keys) in custom fields -- use State API or Key module. Field data ends up in exports, backups, and databases without encryption
- Create entity references to deleted entities -- validate entity exists before saving. Deleted references create orphaned IDs that break displays
- Use @extend in SCSS for custom field styling -- creates selector explosion. Use mixins or utility classes instead
- Assume field exists -- check field definition exists before accessing. Missing field access throws fatal errors
- Hard-code field names -- use constants or config for field name references. Hard-coded names break when fields are renamed

## Common Mistakes

- **Using static calls in OOP code** -- Inject dependencies via DI; improves testability
- **Not type-hinting** -- Use proper type hints for parameters and return values
- **Forgetting access checks** -- Always check entity and field access before displaying
- **Modifying fields without update hooks** -- Schema changes must go through the `custom_field.update_manager` service in a `hook_update_N()`

## See Also

- Drupal coding standards: https://www.drupal.org/docs/develop/standards
- PHP-FIG PSR-12: https://www.php-fig.org/psr/psr-12/
- [Best Practices: Performance & Security](best-practices-performance.md)
