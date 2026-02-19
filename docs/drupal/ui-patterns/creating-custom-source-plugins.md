---
description: Creating Custom Source Plugins — widget and context-aware source patterns, derivers
drupal_version: "11.x"
---

# Creating Custom Source Plugins

## When to Use

> Create a custom source plugin when no existing source exposes the Drupal API or external data you need, or when you need a specialized widget for a specific data entry pattern.

## Decision

| Pattern | Base Class | Use When |
|---------|-----------|----------|
| Widget (stores value in config) | `SourcePluginPropValueWidget` | Direct user input with a form widget |
| API source (pulls from Drupal) | `SourcePluginBase` | Data from Drupal services or context |
| Derived source (one per field/type) | Add `deriver:` to attribute | Need one plugin derivative per entity type/bundle/field |

## Pattern

### Minimal widget source

```php
#[Source(
  id: 'my_color_picker',
  label: new TranslatableMarkup('Color Picker'),
  prop_types: ['string'],
  tags: ['widget']
)]
class ColorPickerWidget extends SourcePluginPropValueWidget {

  public function settingsForm(array $form, FormStateInterface $form_state): array {
    $form = parent::settingsForm($form, $form_state);
    $form['value'] = [
      '#type' => 'color',
      '#default_value' => $this->getSetting('value') ?? '#000000',
    ];
    return $form;
  }

  public function getPropValue(): mixed {
    return $this->getSetting('value');
  }
}
```

### Context-aware API source

```php
#[Source(
  id: 'entity_created_date',
  label: new TranslatableMarkup('Created Date'),
  prop_types: ['string'],
  context_requirements: ['entity'],
  context_definitions: ['entity' => ['type' => 'entity']]
)]
class EntityCreatedDateSource extends SourcePluginBase {

  public function getPropValue(): mixed {
    $entity = $this->getContextValue('entity');
    if (!$entity || !method_exists($entity, 'getCreatedTime')) {
      return NULL;
    }
    return \Drupal::service('date.formatter')
      ->format($entity->getCreatedTime(), 'medium');
  }
}
```

### Source attribute properties

| Property | Purpose |
|----------|---------|
| `id` | Unique plugin ID |
| `prop_types` | Which prop types this source serves |
| `tags` | `widget`, `widget:dismissible` |
| `context_requirements` | Required context keys |
| `deriver` | Class for creating multiple derivatives |

### Key methods

| Method | Required | Purpose |
|--------|----------|---------|
| `getPropValue()` | Yes | Returns the raw prop value |
| `settingsForm()` | For widgets | Builds the configuration form |
| `defaultSettings()` | Optional | Default setting values |
| `alterComponent()` | Optional | Modify the entire component render array |
| `calculateDependencies()` | Optional | Declare config dependencies |

## Common Mistakes

- **Wrong**: Not declaring `prop_types` → **Right**: Without `prop_types`, the source matches all prop types, cluttering the source selector
- **Wrong**: Forgetting `context_requirements` for entity-dependent sources → **Right**: The source will appear in contexts where it cannot function, causing errors
- **Wrong**: Returning render arrays from `getPropValue()` for non-slot props → **Right**: Render arrays are only valid for slot prop types; props expect scalar/structured data
- **Wrong**: Not calling `$this->replaceTokens()` for string values → **Right**: Call it if the value may contain tokens; the base class provides token support

## See Also

- [Source Plugins](source-plugins.md)
- [Props System](props-system.md)
- Reference: [Source Plugins](https://project.pages.drupalcode.org/ui_patterns/3-devs/1-source-plugins/)
- Reference: `modules/contrib/ui_patterns/src/SourcePluginBase.php`
