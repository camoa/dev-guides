---
description: Creating custom source plugins — widgets, API sources, and derivers
tldr: "Creating custom source plugins — widgets, API sources, and derivers"
drupal_version: "11.x"
---

# Creating Custom Source Plugins

## When to Create a Custom Source

Create a custom source plugin when:
- A Drupal API provides data that no existing source exposes
- You need a specialized widget for a specific data entry pattern
- An external system provides data that should be available in component forms

## Source Plugin Structure

A source plugin requires:
1. A class in `Plugin/UiPatterns/Source/` namespace
2. The `#[Source]` attribute with metadata
3. An implementation of `getPropValue()`

## Minimal Widget Source (Direct Input)

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

## Drupal API Source (Context-Aware)

For sources that pull data from Drupal APIs, extend `SourcePluginBase`:

```php
<?php

namespace Drupal\my_module\Plugin\UiPatterns\Source;

use Drupal\Core\Plugin\Context\ContextDefinition;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\ui_patterns\Attribute\Source;
use Drupal\ui_patterns\SourcePluginBase;

#[Source(
  id: 'entity_created_date',
  label: new TranslatableMarkup('Created Date'),
  description: new TranslatableMarkup('Entity creation date.'),
  prop_types: ['string'],
  // Entity dependency is a context DEFINITION, not a context requirement.
  // Definitions must be ContextDefinition objects, never arrays.
  context_definitions: [
    'entity' => new ContextDefinition(
      'entity',
      label: new TranslatableMarkup('Entity'),
      required: TRUE
    ),
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

## Source Attribute Properties

| Property | Type | Purpose |
|---|---|---|
| `id` | string | Unique plugin ID |
| `label` | TranslatableMarkup | Human-readable name |
| `description` | TranslatableMarkup | Form description |
| `no_ui` | bool | Since 2.0.16+. Hides the source from the component configuration form; it stays usable programmatically |
| `prop_types` | array | Which prop types this source serves (e.g., `['string', 'url']`). **Omit it and the source matches every prop type** |
| `tags` | array | Categorization tags. Use the `SourceTags` enum (2.0.16+): `Widget`, `WidgetDismissible`, `ContextSwitcher`, `Field`, `EntityReferenced` |
| `context_requirements` | array | The rendering *situation* the source needs. Only these five are ever satisfied: `field_granularity:item`, `field_granularity:items`, `field_formatter`, `views:row`, `views:style` |
| `context_definitions` | array | `ContextDefinition` **objects**, keyed by context name. This is where an entity dependency belongs |
| `deriver` | string | Deriver class for creating multiple derivatives |
| `metadata` | array | Arbitrary metadata accessible via `getCustomPluginMetadata()` |

`no_ui` is declared as the **fourth positional parameter** of `#[Source]`, ahead of `prop_types`. Always pass source attribute arguments by name.

#### `context_requirements` is not "what data do I need"

`SourcePluginManager::processDefinition()` converts each `context_requirements` entry into a `RequirementsContextDefinition` that must be satisfied by a `context_requirements` context supplied at render time. The nine `RequirementsContext::addToContext()` call sites in the module supply only the five strings listed above. `context_requirements: ['entity']` compiles cleanly, produces no error, and yields a source that appears in **no** dropdown anywhere — the hardest possible thing to debug. Declare the entity through `context_definitions` instead, and read it with `$this->getContextValue('entity')`.

## Key Methods to Implement

| Method | Required | Purpose |
|---|---|---|
| `getPropValue()` | Yes | Returns the raw prop value |
| `settingsForm()` | For widgets | Builds the configuration form |
| `defaultSettings()` | Optional | Default setting values |
| `alterComponent()` | Optional | Modify the entire component render array |
| `calculateDependencies()` | Optional | Declare config dependencies |
| `label()` | Optional | Override display label |

## Using Derivers

For sources that need one derivative per field, entity type, or other dynamic dimension, use a deriver. UI Patterns provides `EntityFieldSourceDeriverBase` as a base:

```php
#[Source(
  id: 'my_field_source',
  label: new TranslatableMarkup('My Field Source'),
  deriver: MyFieldSourceDeriver::class
)]
```

The deriver creates plugin definitions like `my_field_source:node:article:body`, `my_field_source:node:article:title`, etc.

## Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Not declaring `prop_types` | `filterDefinitionsByPropType()` only filters when the array is non-empty, so an omitted `prop_types` makes the source match every prop type. That is deliberate for context switchers (`entity_field`, `entity_reference`); for anything else it clutters the selector on every prop. Be explicit. |
| Using `context_requirements: ['entity']` to declare an entity dependency | `context_requirements` names a rendering situation (field formatter, Views row, field granularity), and `entity` is never one of them. The source silently disappears from every form. Declare `context_definitions: ['entity' => new ContextDefinition('entity', required: TRUE)]` instead — `ComponentElementBuilder::buildSource()` catches the resulting `ContextException` and skips the prop when the context is absent. |
| Passing arrays as `context_definitions` | Core's `ContextHandler` calls methods such as `isRequired()` on each definition. An array fatals the first time a component form builds its source list. Every shipped source passes `new ContextDefinition(...)`. |
| Returning render arrays from `getPropValue()` for non-slot props | Props expect scalar/structured data matching their JSON Schema type. Render arrays are only valid for slot prop types. |
| Not calling `$this->replaceTokens()` for string values | If your source value may contain tokens, call `$this->replaceTokens($value)` to process them. The base class provides token support. |

## See Also

- [Source Plugins](source-plugins.md)
- [Props System](props-system.md)
- Drupal Services/DI Guide