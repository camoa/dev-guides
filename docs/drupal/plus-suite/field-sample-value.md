---
description: "Field Sample Value — built-in generators, per-field configuration, prevent_save validation, and creating custom sample value generator plugins"
tldr: "Configure placeholder content that appears when new blocks are placed, or create custom sample value generators for specific field types."
drupal_version: "11.x"
---

# Field Sample Value

## When to Use

> When configuring placeholder content that appears when new blocks are placed, or creating custom sample value generators for specific field types.

## How It Works

When a block is placed via Plus Suite, the `Dropzones` service calls `SampleValueEntityGenerator::populateWithSampleValues()` on the new block_content entity. Each field's configured generator creates realistic placeholder content.

## Built-in Generators

| Generator | ID | Field Types | Description |
|---|---|---|---|
| Default | `default` | All (weight -10) | Calls field's native `generateSampleItems()` |
| Random Text | `random_text` | text, text_long, text_with_summary | Generates random paragraphs with configurable count and format |
| Entity Reference | `entity_reference` | entity_reference | Selects random published entity matching handler settings |

## Configuration Per Field

On **Manage Fields → [Field] → Edit**, under the sample value section:

| Setting | Purpose |
|---|---|
| Generator | Which plugin generates sample values |
| Configuration | Generator-specific settings (count, format, etc.) |
| Prevent save | Block entity save if sample value unchanged |

Stored as third-party settings:

```yaml
third_party_settings:
  field_sample_value:
    id: random_text
    configuration:
      prevent_save: false
      count: '1'
      filter_format: full_html
```

## Prevent Save Validation

When `prevent_save: true`, the `SampleValueConstraint` validator:
1. Stores original generated value in `$entity->_sampleValues[$field_name]`
2. On entity validation, compares current value with stored sample
3. If unchanged, adds constraint violation: "The %name field contains automatically generated sample values."
4. Prevents accidental saving of placeholder content

## Pattern: Creating a Custom Generator

```php
namespace Drupal\my_module\Plugin\Field\SampleValueGenerator;

use Drupal\field_sample_value\Annotation\SampleValueGenerator;
use Drupal\field_sample_value\SampleValueGeneratorBase;
use Drupal\Core\Field\FieldItemListInterface;

/**
 * @SampleValueGenerator(
 *   id = "lorem_ipsum",
 *   title = @Translation("Lorem Ipsum"),
 *   field_types = {"text", "text_long", "text_with_summary"},
 *   weight = 10,
 * )
 */
class LoremIpsum extends SampleValueGeneratorBase {

  public function generateSampleValue(FieldItemListInterface $field): void {
    $field->setValue([
      'value' => 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
      'format' => 'full_html',
    ]);
  }
}
```

## Generator Discovery

`SampleValueGeneratorManager` discovers generators:
- Namespace: `Plugin/Field/SampleValueGenerator`
- Annotation: `@SampleValueGenerator`
- Alter hook: `hook_sample_value_generator_info_alter()`
- `getApplicableGenerators($field_type)` returns applicable plugin IDs sorted by weight (highest first)

## Decision

| Field Type | Recommended Generator | Config |
|---|---|---|
| Body / formatted text | `random_text` | count: 1-3, format: full_html |
| Title / plain text | `default` | Uses core's random text |
| Image | `default` | Core generates placeholder image |
| Entity reference | `entity_reference` | Selects random published entity |
| Custom field type | Create custom generator | Match your content model |

## Alternative: PlaceBlockEvent with block_serialized

For cases where Field Sample Value generators aren't enough (e.g., setting select list defaults, configuring label display, or modifying block content fields before placement), use a `PlaceBlockEvent` subscriber to manipulate the block directly:

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\lb_plus\Event\PlaceBlockEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class PlaceBasicBlock implements EventSubscriberInterface {

  public function onPrePlaceBlockFormBuild(PlaceBlockEvent $event): void {
    if ($event->getBlockPluginId() !== 'inline_block' || $event->getBundle() !== 'basic') {
      return;
    }

    $block_plugin = $event->getBlockPlugin();
    $configuration = $block_plugin->getConfiguration();

    // Set label configuration.
    $configuration['label_display'] = 'visible';
    $configuration['label_tag'] = 'h2';
    $configuration['label'] = $block_plugin->label();

    // Modify block content fields via block_serialized.
    $block_content = unserialize($configuration['block_serialized']);
    $block_content->set('field_my_select_list', 'option_42');
    $configuration['block_serialized'] = serialize($block_content);

    $block_plugin->setConfiguration($configuration);
  }

  public static function getSubscribedEvents(): array {
    return [PlaceBlockEvent::class => ['onPrePlaceBlockFormBuild']];
  }
}
```

**When to use `block_serialized` vs Field Sample Value:**
- Use **Field Sample Value generators** for standard field content (text, images, references)
- Use **`block_serialized` in PlaceBlockEvent** for non-field configuration (label display, label tag, select list defaults, view mode)

## Common Mistakes

- **Do not** set `prevent_save: true` on fields where sample content is acceptable (like demo sites).
- **Do not** create generators that make external API calls — they're called on every block placement.

## See Also

- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Custom Block Types](custom-block-types.md)
- [End-to-End Component Creation](end-to-end-component.md)
- Reference: `field_sample_value/src/SampleValueGeneratorManager.php`
