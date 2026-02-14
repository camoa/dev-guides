---
description: Set up a responsive image style with breakpoints
drupal_version: "11.x"
---

# Responsive Image Style Config

## When to Use

> Use this when configuring a responsive image style that maps breakpoints to image styles for adaptive image delivery.

## Pattern - Image Style Mapping

```yaml
# responsive_image.styles.hero.yml
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

## Pattern - Sizes Attribute Mapping

```yaml
# responsive_image.styles.wide.yml
langcode: en
status: true
dependencies:
  config:
    - image.style.max_325x325
    - image.style.max_650x650
    - image.style.max_1300x1300
id: wide
label: Wide
breakpoint_group: responsive_image
fallback_image_style: max_325x325
image_style_mappings:
  - image_mapping_type: sizes
    image_mapping:
      sizes: '(min-width: 1290px) 1290px, 100vw'
      sizes_image_styles:
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
| `image_style_mappings.*.image_mapping_type` | string | Yes | `'image_style'` or `'sizes'` |
| `image_style_mappings.*.breakpoint_id` | string | Yes | Must exist in breakpoint_group |
| `image_style_mappings.*.multiplier` | string | Yes | Pixel density: `'1x'`, `'2x'`, `'3x'` |

## Common Mistakes

- **Wrong**: Using `sizes` mapping type with multipliers other than `1x` → **Right**: Sizes only with 1x multiplier (invalid HTML, browser ignores sizes attribute)
- **Wrong**: Missing fallback_image_style → **Right**: Always set fallback (broken images for no-JS users, accessibility failure)
- **Wrong**: Breakpoint ID doesn't exist in declared breakpoint_group → **Right**: Use valid breakpoint IDs (config validation error)
- **Wrong**: Not declaring dependencies on referenced image styles → **Right**: Declare all dependencies (broken config on style deletion)
- **Wrong**: Sizes attribute lists image styles in wrong order → **Right**: List largest to smallest (browser picks suboptimal size, bandwidth waste)

## See Also

- [Breakpoint Configuration](breakpoint-configuration.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/modules/responsive_image/config/schema/responsive_image.schema.yml
- Reference: core/modules/responsive_image/src/Entity/ResponsiveImageStyle.php
