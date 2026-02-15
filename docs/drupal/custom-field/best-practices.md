---
description: Performance optimization, security hardening, dependency injection, and coding standards for custom field development.
---

# Best Practices

## Performance

**Single-table advantage**:

- Custom Field stores all sub-fields in one table row -- single query to load all data
- Paragraphs creates N entities -- N+1 query problem (1 parent + N children)
- For 10 sub-fields: Custom Field = 1 JOIN, Paragraphs = 10+ JOINs

**Optimization patterns**:

```php
// GOOD: Load entity once, access multiple sub-fields
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
$street = $node->field_address->street;
$city = $node->field_address->city;
$state = $node->field_address->state;

// BAD: Loading entity repeatedly
$street = Node::load($nid)->field_address->street;
$city = Node::load($nid)->field_address->city; // Redundant load
```

**Views performance**:

- All columns in same table -- no relationship needed
- Filter/sort on custom field columns = single table query
- vs Paragraphs: require relationships, multiple JOIN tables

**Field count limits**:

- MySQL row size limit: ~8KB per row
- Practical limit: ~50-100 sub-fields depending on types
- For 100+ fields: consider custom field type plugin instead

**Caching**:

- Field values cached with entity
- No special caching needed
- Clear entity cache when updating programmatically

## Security

**XSS prevention**:

```php
// GOOD: Use render arrays with automatic escaping
return [
  '#markup' => $this->t('Value: @value', ['@value' => $value]),
];

// BAD: Raw concatenation
return '<div>' . $value . '</div>'; // XSS vulnerability
```

**Entity reference access checks**:

```php
// GOOD: Check access before rendering
$entity = $storage->load($entity_id);
if ($entity && $entity->access('view')) {
  return $entity->toLink()->toRenderable();
}

// BAD: Assume access
return $storage->load($entity_id)->toLink(); // May expose restricted content
```

**File upload security**:

- Always validate file extensions in widget settings
- Use private:// scheme for sensitive files
- Configure upload_location to segregate files
- Set max_filesize to prevent DoS

**Link security**:

- Use noopener noreferrer for target="_blank"
- Validate external URLs with allowed protocols
- Built-in constraints: LinkExternalProtocolsConstraint, LinkAccessConstraint

**SQL injection prevention**:

- Custom Field uses Entity API -- parameterized queries automatic
- For custom queries, use query builders with placeholders
- Never concatenate user input into SQL

## Development Standards

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
function my_module_update_9001() {
  /** @var \Drupal\custom_field\CustomFieldUpdateManager $updateManager */
  $updateManager = \Drupal::service('custom_field.update_manager');

  $field_storage = FieldStorageConfig::loadByName('node', 'field_address');
  $columns = $field_storage->getSetting('columns');

  // Add new column
  $columns['country'] = [
    'name' => 'country',
    'type' => 'string',
    'length' => 2,
  ];

  $field_storage->setSetting('columns', $columns);
  $updateManager->updateFieldSchema($field_storage);

  return t('Added country column to field_address');
}
```

## Anti-Patterns

- Modify field schema directly in database -- always use CustomFieldUpdateManager
- Store sensitive data (passwords, API keys) in custom fields -- use State API or Key module
- Create entity references to deleted entities -- validate entity exists before saving
- Use @extend in SCSS for custom field styling -- creates selector explosion
- Assume field exists -- check field definition exists before accessing
- Hard-code field names -- use constants or config for field name references

## Common Mistakes

- **Loading entities in loops** -- Load once, access multiple times; or use loadMultiple()
- **Not sanitizing output in custom formatters** -- Use render arrays with #markup and placeholders, not raw concatenation
- **Exposing entity references without access checks** -- Always check $entity->access('view')
- **Public files for private data** -- Use private:// scheme and configure file access controls
- **Using static calls in OOP code** -- Inject dependencies via DI; improves testability
- **Modifying fields without update hooks** -- Schema changes must go through CustomFieldUpdateManager

## See Also

- OWASP: https://owasp.org/www-project-top-ten/
- Drupal security: https://www.drupal.org/security/secure-coding-practices
- Drupal coding standards: https://www.drupal.org/docs/develop/standards
