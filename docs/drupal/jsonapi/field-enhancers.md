---
description: "Transform field values during normalization (entity to JSON) and denormalization (JSON to entity). Requires jsonapi_extras module."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Field Enhancers

### When to Use

Transform field values during normalization (entity to JSON) and denormalization (JSON to entity). Requires `jsonapi_extras` module.

### Items

#### DateTimeEnhancer

**Description:** Format date/time fields.

**Configuration:**
- Format: Custom date format string (e.g., `Y-m-d H:i:s`)

**Usage Example:**
```
Input (stored): 2026-02-13T14:30:00+00:00
Output (enhanced): 2026-02-13 14:30:00
```

**Gotchas:**
- Format must be valid PHP date format
- Timezone handling depends on site configuration

#### DateTimeFromStringEnhancer

**Description:** Convert string to date object during denormalization.

**Configuration:**
- Input format string

**Usage Example:**
```
Input (JSON): "2026-02-13"
Output (stored): DateTimeInterface object
```

**Gotchas:**
- Input must match configured format exactly
- Validation errors if format mismatch

#### JSONFieldEnhancer

**Description:** Parse JSON string fields into objects/arrays.

**Configuration:**
- None required

**Usage Example:**
```
Input (stored): '{"key": "value"}'
Output (enhanced): { "key": "value" }
```

**Gotchas:**
- Only works on text fields containing JSON
- Invalid JSON causes errors

#### ListFieldEnhancer

**Description:** Transform list field values (allowed values to labels).

**Configuration:**
- None required

**Usage Example:**
```
Input (stored): "option_1"
Output (enhanced): "Option 1 Label"
```

**Gotchas:**
- Only works with fields using allowed values
- Returns NULL if key not in allowed values

#### SingleNestedEnhancer

**Description:** Extract single property from complex field value.

**Configuration:**
- Property name to extract (e.g., `value`, `uri`)

**Usage Example:**
```
Input (stored): { "value": "Text content", "format": "html" }
Output (enhanced): "Text content"
```

**Gotchas:**
- Loses other properties (format, summary)
- Denormalization may require full object

#### UrlLinkEnhancer

**Description:** Generate absolute URLs for link fields.

**Configuration:**
- None required

**Usage Example:**
```
Input (stored): { "uri": "internal:/node/1", "title": "Link" }
Output (enhanced): { "url": "https://example.com/node/1", "title": "Link" }
```

**Gotchas:**
- Requires valid base URL configuration
- External links pass through unchanged

#### UuidLinkEnhancer

**Description:** Transform entity UUIDs into full resource links.

**Configuration:**
- Target entity type

**Usage Example:**
```
Input (stored): "a3b2c1d0-..."
Output (enhanced): { "href": "https://example.com/jsonapi/node/article/a3b2c1d0-..." }
```

**Gotchas:**
- Requires entity type configuration
- Only works with valid UUIDs

### Custom Enhancer Example

**Create custom enhancer:**
```php
// mymodule/src/Plugin/jsonapi/FieldEnhancer/UppercaseEnhancer.php
namespace Drupal\mymodule\Plugin\jsonapi\FieldEnhancer;

use Drupal\jsonapi_extras\Plugin\ResourceFieldEnhancerBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;

/**
 * Uppercase text transformation.
 *
 * @ResourceFieldEnhancer(
 *   id = "uppercase",
 *   label = @Translation("Uppercase Text"),
 *   description = @Translation("Converts text to uppercase.")
 * )
 */
class UppercaseEnhancer extends ResourceFieldEnhancerBase {

  /**
   * {@inheritdoc}
   */
  protected function doUndoTransform($data, Context $context) {
    // Transform incoming data (JSON to entity)
    return strtolower($data);
  }

  /**
   * {@inheritdoc}
   */
  protected function doTransform($value, Context $context) {
    // Transform outgoing data (entity to JSON)
    return strtoupper($value);
  }
}
```

**Apply enhancer via UI:**
1. Visit `/admin/config/services/jsonapi/resource_types`
2. Edit resource type (e.g., `node--article`)
3. Configure field
4. Select "Uppercase Text" enhancer
5. Save

### Common Mistakes

**Using enhancers for validation:** Enhancers transform data, not validate. WHY: Validation happens elsewhere. Use entity validation constraints instead.

**Not accounting for denormalization:** `doUndoTransform()` must reverse `doTransform()`. WHY: POST/PATCH use denormalization. Asymmetric transforms break writes.

**Enhancing computed fields:** Computed fields aren't stored. WHY: Enhancers work on stored data. Computed fields are read-only.

**Over-transforming data:** Making data unrecognizable from original. WHY: Debugging becomes difficult. Keep transformations minimal and logical.

**Forgetting enhancer applies to all instances:** Field enhancer affects all entities of that bundle. WHY: Configuration is per field per bundle, not per entity. Can't have entity-specific enhancers.

### See Also
- [JSON:API Extras Customization](jsonapi-extras-customization.md)
- [Core Architecture](core-architecture.md) (Normalization System)
- [Code Reference Map](code-reference-map.md) (`modules/contrib/jsonapi_extras/src/Plugin/jsonapi/FieldEnhancer/`)
