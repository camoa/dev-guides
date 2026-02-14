---
description: When to use image styles vs responsive images
drupal_version: "11.x"
---

# Image System Overview

## When to Use

> Use image styles when you need a single derivative at a fixed size. Use responsive images when you need different sizes for different devices/viewports.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Fixed-size image at one dimension | Image style | Single derivative, simple caching, minimal overhead |
| Different sizes for different devices/viewports | Responsive image style | Browser picks best derivative based on viewport/DPR |
| Art direction (different crops for mobile vs desktop) | Responsive image style with picture element | Full control over which image shows at which breakpoint |
| Format conversion (WebP, AVIF) | Image style with convert effects | Automatic format conversion with fallback |
| Same aspect ratio, different resolutions | Responsive image style with sizes attribute | Resolution switching via srcset, browser chooses |
| Thumbnails, user avatars, consistent UI elements | Image style | Predictable dimensions, simpler cache management |

## Pattern

**Image style**: Config entity that applies effects (resize, crop, convert) to generate a derivative.

```yaml
# config/sync/image.style.medium.yml
name: medium
label: 'Medium (220x220)'
effects:
  uuid-1:
    id: image_scale
    weight: 0
    data:
      width: 220
      height: 220
      upscale: false
```

**Responsive image style**: Maps breakpoints to image styles.

```yaml
# config/sync/responsive_image.styles.hero.yml
id: hero
label: 'Hero Image'
breakpoint_group: olivero
fallback_image_style: large
image_style_mappings:
  - breakpoint_id: olivero.lg
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: hero_large
```

## Common Mistakes

- **Wrong**: Using responsive images when a single image style suffices → **Right**: Use single image style for fixed-size elements (adds complexity and generates unnecessary derivatives, increases storage/processing)
- **Wrong**: Not setting a fallback_image_style → **Right**: Always set fallback to smallest acceptable size (breaks display when JavaScript disabled or responsive_image module missing)
- **Wrong**: Creating separate image styles for every breakpoint instead of reusing → **Right**: Reuse image styles across breakpoints (bloats config, makes maintenance harder)
- **Wrong**: Using image styles for full-width hero images without responsive variants → **Right**: Use responsive image style for full-width content (wastes bandwidth on mobile devices)

## See Also

- [Creating Image Styles via Config](creating-styles-config.md)
- [Responsive Image Style Config](responsive-image-config.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/modules/image/src/Entity/ImageStyle.php
- Reference: core/modules/responsive_image/src/Entity/ResponsiveImageStyle.php
