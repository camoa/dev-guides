---
description: Understand the difference between image styles (single derivative) and responsive images (multiple derivatives for different contexts)
---

# Image System Overview

## When to Use

> Use image styles for fixed-size images. Use responsive image styles when you need different sizes for different devices/viewports.

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

- Using responsive images when a single image style suffices → Adds complexity and generates unnecessary derivatives, increases storage/processing
- Not setting a fallback_image_style → Breaks display when JavaScript disabled or responsive_image module missing
- Creating separate image styles for every breakpoint instead of reusing → Bloats config, makes maintenance harder
- Using image styles for full-width hero images without responsive variants → Wastes bandwidth on mobile devices

## See Also

- [Creating Image Styles via Config](creating-styles-config.md)
- [Responsive Image Style Config](responsive-image-config.md)
- [Art Direction vs Resolution Switching](art-direction-resolution.md)
- Reference: core/modules/image/src/Entity/ImageStyle.php
- Reference: core/modules/responsive_image/src/Entity/ResponsiveImageStyle.php
