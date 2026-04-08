---
description: Field Sample Value — built-in generators, per-field configuration, prevent_save validation, and creating custom sample value generator plugins
drupal_version: "11.x"
---

# Field Sample Value

## When to Use

> Configure field sample value generators for every field on every block content type. Without them, blocks appear empty on placement, defeating Plus Suite's "drop and see" UX.

## Decision

| Field Type | Recommended Generator | Config |
|------------|--------------------- |--------|
| Body / formatted text | `random_text` | count: 1-3, format: full_html |
| Title / plain text | `default` | Uses core's random text |
| Image | `default` | Core generates placeholder image |
| Entity reference | `entity_reference` | Selects random published entity |
| Custom field type | Create custom generator | Match your content model |

## Pattern

**Built-in generators:**

| Generator | ID | Field Types |
|-----------|----|-------------|
| Default | `default` | All (weight -10) — calls native `generateSampleItems()` |
| Random Text | `random_text` | text, text_long, text_with_summary |
| Entity Reference | `entity_reference` | entity_reference — selects random published entity |

**Per-field config** (stored as third-party settings):

```yaml
third_party_settings:
  field_sample_value:
    id: random_text
    configuration:
      prevent_save: false
      count: '1'
      filter_format: full_html
```

**Custom generator:**

```php
/**
 * @SampleValueGenerator(
 *   id = "lorem_ipsum",
 *   title = @Translation("Lorem Ipsum"),
 *   field_types = {"text", "text_long"},
 *   weight = 10,
 * )
 */
class LoremIpsum extends SampleValueGeneratorBase {

  public function generateSampleValue(FieldItemListInterface $field): void {
    $field->setValue([
      'value' => 'Lorem ipsum dolor sit amet.',
      'format' => 'full_html',
    ]);
  }
}
```

**Discovery:** Namespace `Plugin/Field/SampleValueGenerator`, annotation `@SampleValueGenerator`.

**Prevent save:** When `prevent_save: true`, `SampleValueConstraint` blocks entity save if field value equals the generated sample — prevents accidental publishing of placeholder content.

## Common Mistakes

- **Wrong**: Setting `prevent_save: true` on demo/placeholder sites → **Right**: Only use on production sites where sample content must be replaced
- **Wrong**: Creating generators that make external API calls → **Right**: Generators run on every block placement; keep them fast and local

## See Also

- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Custom Block Types](custom-block-types.md)
- [End-to-End Component Creation](end-to-end-component.md)
- Reference: `field_sample_value/src/SampleValueGeneratorManager.php`
