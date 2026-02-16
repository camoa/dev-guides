---
description: Complete YAML schema for image.style.*.yml config files including all required fields and effect structure
---

# Image Style Config Schema

## When to Use

> Use this when you need to write or validate image.style.*.yml config files manually.

## Schema Structure

**Config entity type**: `image.style.*`

**File location**: `config/sync/image.style.{machine_name}.yml`

### Schema Definition

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

### Complete Config File Example

```yaml
langcode: en
status: true
dependencies: { }
name: hero_large
label: 'Hero Large (1920x800)'
effects:
  1cfec298-8620-4749-b100-ccb6c4500779:
    uuid: 1cfec298-8620-4749-b100-ccb6c4500779
    id: image_scale_and_crop
    weight: 0
    data:
      width: 1920
      height: 800
      anchor: center-center
  c4eb9942-2c9e-4a81-949f-6161a44b6559:
    uuid: c4eb9942-2c9e-4a81-949f-6161a44b6559
    id: image_convert_avif
    weight: 2
    data:
      extension: webp
```

### Key Properties

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

- Missing UUID for effect → Config import fails with schema validation error
- Duplicate UUIDs across effects → Only first effect executes, silent failure on others
- Wrong effect plugin ID → "Plugin does not exist" error on style load
- Omitting `data` key when effect requires config → Uses defaults, may not match expectations
- Not setting weight correctly → Effects execute in wrong order (e.g., crop before scale)

## See Also

- [Core Image Effects](core-image-effects.md) (for effect-specific schemas)
- [Creating Image Styles via Config](creating-styles-config.md) (for workflow)
- Reference: core/modules/image/config/schema/image.schema.yml
