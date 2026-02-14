---
description: Full YAML config schema for image styles
drupal_version: "11.x"
---

# Image Style Config Schema

## When to Use

> Use this when writing or validating image.style.*.yml config files manually.

## Schema Definition

**Config entity type**: `image.style.*`

**File location**: `config/sync/image.style.{machine_name}.yml`

From `core/modules/image/config/schema/image.schema.yml`:

```yaml
image.style.*:
  type: config_entity
  label: 'Image style'
  mapping:
    name:
      type: machine_name
    label:
      type: required_label
    effects:
      type: sequence
      sequence:
        type: mapping
        mapping:
          uuid:
            type: uuid
          id:
            type: string  # Plugin ID: image_scale, image_crop, etc.
          weight:
            type: weight  # Integer for effect ordering
          data:
            type: image.effect.[%parent.id]  # Effect-specific config
```

## Complete Config Example

```yaml
langcode: en
status: true
dependencies: { }
name: thumbnail
label: 'Thumbnail (100x100)'
effects:
  1cfec298-8620-4749-b100-ccb6c4500779:
    uuid: 1cfec298-8620-4749-b100-ccb6c4500779
    id: image_scale
    weight: 0
    data:
      width: 100
      height: 100
      upscale: false
  c4eb9942-2c9e-4a81-949f-6161a44b6559:
    uuid: c4eb9942-2c9e-4a81-949f-6161a44b6559
    id: image_convert_avif
    weight: 2
    data:
      extension: webp
```

## Key Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | machine_name | Yes | Machine name, used in URLs |
| `label` | required_label | Yes | Human-readable name |
| `effects` | sequence | No | Ordered list of image effects |
| `effects.*.uuid` | uuid | Yes | Unique identifier for effect instance |
| `effects.*.id` | string | Yes | Effect plugin ID |
| `effects.*.weight` | weight | Yes | Integer controlling effect order (lower = earlier) |
| `effects.*.data` | mapping | Varies | Effect-specific configuration |

## Common Mistakes

- **Wrong**: Missing UUID for effect → **Right**: Generate UUID for every effect (config import fails with schema validation error)
- **Wrong**: Duplicate UUIDs across effects → **Right**: Unique UUID per effect (only first effect executes, silent failure on others)
- **Wrong**: Wrong effect plugin ID → **Right**: Use valid plugin ID from core or contrib ("Plugin does not exist" error on style load)
- **Wrong**: Omitting `data` key when effect requires config → **Right**: Always include data key with required properties (uses defaults, may not match expectations)
- **Wrong**: Not setting weight correctly → **Right**: Set weights in execution order (effects execute in wrong order, e.g., crop before scale)

## See Also

- [Core Image Effects](core-image-effects.md)
- [Creating Image Styles via Config](creating-styles-config.md)
- Reference: core/modules/image/config/schema/image.schema.yml
