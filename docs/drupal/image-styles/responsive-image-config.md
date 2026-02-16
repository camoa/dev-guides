---
description: Complete YAML schema for responsive_image.styles.*.yml with breakpoint mappings, sizes attributes, and image style references
---

# Responsive Image Style Config

## When to Use

> Use this when you need to configure a responsive image style that maps breakpoints to image styles for adaptive image delivery.

## Schema Structure

**Config entity type**: `responsive_image.styles.*`

**File location**: `config/sync/responsive_image.styles.{machine_name}.yml`

### Schema Definition

From `core/modules/responsive_image/config/schema/responsive_image.schema.yml`:

```yaml
responsive_image.styles.*:
  type: config_entity
  mapping:
    id:
      type: machine_name
    label:
      type: required_label
    image_style_mappings:
      type: sequence
      sequence:
        mapping:
          image_mapping_type:
            type: string  # 'sizes' or 'image_style'
          image_mapping:
            type: responsive_image.image_mapping_type.[%parent.image_mapping_type]
          breakpoint_id:
            type: string  # Must match a breakpoint in breakpoint_group
          multiplier:
            type: string  # '1x', '2x', '3x', etc.
    breakpoint_group:
      type: string  # Machine name of breakpoint group
    fallback_image_style:
      type: string  # Image style machine name
```

## Complete Config Example - Image Style Mapping

```yaml
langcode: en
status: true
dependencies:
  config:
    - image.style.hero_small
    - image.style.hero_medium
    - image.style.hero_large
id: hero
label: 'Hero Responsive'
breakpoint_group: olivero
fallback_image_style: hero_small
image_style_mappings:
  - image_mapping_type: image_style
    image_mapping: hero_small
    breakpoint_id: olivero.sm
    multiplier: 1x
  - image_mapping_type: image_style
    image_mapping: hero_medium
    breakpoint_id: olivero.md
    multiplier: 1x
  - image_mapping_type: image_style
    image_mapping: hero_large
    breakpoint_id: olivero.lg
    multiplier: 1x
```

## Complete Config Example - Sizes Attribute Mapping

```yaml
langcode: en
status: true
dependencies:
  config:
    - image.style.max_325x325
    - image.style.max_650x650
    - image.style.max_1300x1300
    - image.style.max_2600x2600
id: wide
label: Wide
breakpoint_group: responsive_image
fallback_image_style: max_325x325
image_style_mappings:
  - image_mapping_type: sizes
    image_mapping:
      sizes: '(min-width: 1290px) 1290px, 100vw'
      sizes_image_styles:
        - max_2600x2600
        - max_1300x1300
        - max_650x650
        - max_325x325
    breakpoint_id: responsive_image.viewport_sizing
    multiplier: 1x
```

## Key Properties

| Property | Type | Required | Description |
|---|---|---|---|
| `id` | machine_name | Yes | Machine name for responsive image style |
| `label` | required_label | Yes | Human-readable name |
| `breakpoint_group` | string | Yes | Must match a declared breakpoint group |
| `fallback_image_style` | string | Yes | Image style for no-JS or unsupported browsers |
| `image_style_mappings` | sequence | No | List of breakpoint-to-image-style mappings |
| `image_style_mappings.*.image_mapping_type` | string | Yes | `'image_style'` or `'sizes'` |
| `image_style_mappings.*.image_mapping` | string or mapping | Yes | Image style ID (if type=image_style) or sizes config (if type=sizes) |
| `image_style_mappings.*.breakpoint_id` | string | Yes | Must exist in breakpoint_group |
| `image_style_mappings.*.multiplier` | string | Yes | Pixel density: `'1x'`, `'2x'`, `'3x'` |

## Sizes Attribute Mapping Schema

When `image_mapping_type: sizes`:

```yaml
image_mapping:
  sizes: '(min-width: 1290px) 1290px, 100vw'
  sizes_image_styles:
    - image_style_id_1
    - image_style_id_2
```

| Property | Type | Description |
|---|---|---|
| `sizes` | string | CSS sizes attribute value (media queries + dimensions) |
| `sizes_image_styles` | sequence | List of image style IDs for srcset generation |

## Common Mistakes

- Using `sizes` mapping type with multipliers other than `1x` → Invalid HTML, browser ignores sizes attribute
- Missing fallback_image_style → Broken images for no-JS users, accessibility failure
- Breakpoint ID doesn't exist in declared breakpoint_group → Config validation error
- Not declaring dependencies on referenced image styles → Broken config on style deletion
- Mixing image_style and sizes mapping types on same breakpoint → Last mapping wins, confusing output
- Sizes attribute lists image styles in wrong order → Browser picks suboptimal size, bandwidth waste

## See Also

- [Breakpoint Configuration](breakpoint-configuration.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/modules/responsive_image/config/schema/responsive_image.schema.yml
- Reference: core/modules/responsive_image/src/Entity/ResponsiveImageStyle.php
