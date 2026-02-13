---
description: Filter ECA event triggers by entity type, bundle, or field with wildcard patterns
drupal_version: "11.x"
---

# Entity-Aware Events

## When to Use

> Use entity-aware events when you need to filter event triggers by entity type, bundle, or field name. This enables precise workflow targeting without evaluating every entity operation.

## Decision

| If you need... | Filtering Level | Wildcard Pattern |
|----------------|-----------------|------------------|
| All entity types | Type: ALL | `*` |
| Specific entity type | Type selection | `node` |
| Specific bundle | Type + Bundle | `node::article` |
| Specific field | Type + Bundle + Field | `node::article::field_tags` |

## Pattern

```php
public function defaultConfiguration(): array {
  return [
    'type' => ContentEntityTypes::ALL,
    'field_name' => '',  // For field-specific events
  ] + parent::defaultConfiguration();
}

public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
  $form['type'] = [
    '#type' => 'select',
    '#title' => $this->t('Type (and bundle)'),
    '#options' => $this->entityTypes->getTypesAndBundles(TRUE),
    '#default_value' => $this->configuration['type'],
  ];

  if (is_subclass_of($this->eventClass(), FieldSelectionBase::class)) {
    $form['field_name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Restrict by field (machine name)'),
      '#default_value' => $this->configuration['field_name'],
    ];
  }

  return parent::buildConfigurationForm($form, $form_state);
}

public function generateWildcard(string $eca_config_id, EcaEventObject $ecaEvent): string {
  $config = $ecaEvent->getConfiguration();
  $type = $config['type'] ?? ContentEntityTypes::ALL;

  if ($type === ContentEntityTypes::ALL) {
    return '*';
  }

  [$entityType, $bundle] = array_merge(explode(' ', $type), [ContentEntityTypes::ALL]);

  if ($bundle === ContentEntityTypes::ALL) {
    return $entityType;
  }

  $wildcard = $entityType . '::' . $bundle;

  // Add field filtering if configured
  if (!empty($config['field_name'])) {
    $wildcard .= '::' . $config['field_name'];
  }

  return $wildcard;
}

public static function appliesForWildcard(Event $event, string $event_name, string $wildcard): bool {
  if ($event instanceof ContentEntityEvent) {
    $entity = $event->getEntity();
    $candidates = [
      '*',
      $entity->getEntityTypeId(),
      $entity->getEntityTypeId() . '::' . $entity->bundle(),
    ];

    if ($event instanceof FieldEvent) {
      $field_name = $event->getFieldName();
      $candidates[] = $entity->getEntityTypeId() . '::' . $entity->bundle() . '::' . $field_name;
    }

    return in_array($wildcard, $candidates, TRUE);
  }

  return TRUE;
}
```

## Common Mistakes

- **Wrong**: Missing wildcard generation → **Right**: All events trigger regardless of config
- **Wrong**: Wrong wildcard format → **Right**: Use `entity_type::bundle::field` format
- **Wrong**: Not checking all candidate patterns in `appliesForWildcard()` → **Right**: Some valid matches fail
- **Wrong**: Forgetting ContentEntityTypes::ALL constant → **Right**: Can't select "all entities"
- **Wrong**: Missing field name validation → **Right**: Invalid field names cause silent failures

## See Also

- [Event Plugin Basics](event-plugin-basics.md) for base event structure
- [Token Form Integration](token-form-integration.md) for token data from entities
- [Reusable Traits](reusable-traits.md) for EntityApplianceTrait

**References:**
- Core: `/modules/contrib/eca/modules/content/src/Plugin/ECA/Event/ContentEntityEvent.php`
- Service: `/modules/contrib/eca/modules/content/src/Service/ContentEntityTypes.php`
