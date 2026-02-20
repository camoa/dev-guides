---
description: Creating custom source plugins — widgets, API sources, and derivers
drupal_version: "10.3+ / 11"
---

## Creating Custom Source Plugins

### When to Create a Custom Source

Create a custom source plugin when:
- A Drupal API provides data that no existing source exposes
- You need a specialized widget for a specific data entry pattern
- An external system provides data that should be available in component forms

### Source Plugin Structure

A source plugin requires:
1. A class in `Plugin/UiPatterns/Source/` namespace
2. The `#[Source]` attribute with metadata
3. An implementation of `getPropValue()`

### Minimal Widget Source (Direct Input)

For sources that store a value directly in configuration, extend `SourcePluginPropValue` (or `SourcePluginPropValueWidget` for form widget sources):

```php
<?php

namespace Drupal\my_module\Plugin\UiPatterns\Source;

use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\ui_patterns\Attribute\Source;
use Drupal\ui_patterns\SourcePluginPropValueWidget;

#[Source(
  id: 'my_color_picker',
  label: new TranslatableMarkup('Color Picker'),
  description: new TranslatableMarkup('Select a color value.'),
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
    $this->addRequired($form['value']);
    return $form;
  }

  public function getPropValue(): mixed {
    return $this->getSetting('value');
  }

}
```

### Drupal API Source (Context-Aware)

For sources that pull data from Drupal APIs, extend `SourcePluginBase`:

```php
<?php

namespace Drupal\my_module\Plugin\UiPatterns\Source;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\ui_patterns\Attribute\Source;
use Drupal\ui_patterns\SourcePluginBase;

#[Source(
  id: 'entity_created_date',
  label: new TranslatableMarkup('Created Date'),
  description: new TranslatableMarkup('Entity creation date.'),
  prop_types: ['string'],
  context_requirements: ['entity'],
  context_definitions: [
    'entity' => ['type' => 'entity']
  ]
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

### Source Attribute Properties

| Property | Type | Purpose |
|---|---|---|
| `id` | string | Unique plugin ID |
| `label` | TranslatableMarkup | Human-readable name |
| `description` | TranslatableMarkup | Form description |
| `prop_types` | array | Which prop types this source serves (e.g., `['string', 'url']`) |
| `tags` | array | Categorization tags (`widget`, `widget:dismissible`) |
| `context_requirements` | array | Required context keys (`entity`, `field_granularity:item`) |
| `context_definitions` | array | Plugin context definitions for dependency injection |
| `deriver` | string | Deriver class for creating multiple derivatives |
| `metadata` | array | Arbitrary metadata accessible via `getCustomPluginMetadata()` |

### Key Methods to Implement

| Method | Required | Purpose |
|---|---|---|
| `getPropValue()` | Yes | Returns the raw prop value |
| `settingsForm()` | For widgets | Builds the configuration form |
| `defaultSettings()` | Optional | Default setting values |
| `alterComponent()` | Optional | Modify the entire component render array |
| `calculateDependencies()` | Optional | Declare config dependencies |
| `label()` | Optional | Override display label |

### Using Derivers

For sources that need one derivative per field, entity type, or other dynamic dimension, use a deriver. UI Patterns provides `EntityFieldSourceDeriverBase` as a base:

```php
#[Source(
  id: 'my_field_source',
  label: new TranslatableMarkup('My Field Source'),
  deriver: MyFieldSourceDeriver::class
)]
```

The deriver creates plugin definitions like `my_field_source:node:article:body`, `my_field_source:node:article:title`, etc.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Not declaring `prop_types` | Without `prop_types`, the source matches all prop types. This clutters the source selector for every prop. Always be explicit. |
| Forgetting `context_requirements` for entity-dependent sources | The source will appear in contexts where it cannot function (e.g., in a block without entity context), causing errors when it tries to access missing context. |
| Returning render arrays from `getPropValue()` for non-slot props | Props expect scalar/structured data matching their JSON Schema type. Render arrays are only valid for slot prop types. |
| Not calling `$this->replaceTokens()` for string values | If your source value may contain tokens, call `$this->replaceTokens($value)` to process them. The base class provides token support. |

### See Also

- [Source Plugins](#source-plugins)
- [Props System](#props-system)
- Drupal Services/DI Guide