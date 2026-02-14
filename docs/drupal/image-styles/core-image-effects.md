---
description: Configure resize, scale, crop, or conversion effects
drupal_version: "11.x"
---

# Core Image Effects

## When to Use

> Use this when you need to configure specific image transformations in an image style. Drupal core provides 8 image effect plugins.

## Decision

| Effect | Use When | Why |
|---|---|---|
| `image_scale` | Responsive images, maintaining aspect ratio | Most common, prevents distortion, handles one or both dimensions |
| `image_scale_and_crop` | Square thumbnails, fixed aspect ratios | Scales to fill then crops excess, no stretching |
| `image_resize` | Fixed-size placeholders where aspect doesn't matter | Forces exact dimensions, may distort |
| `image_crop` | Extract specific region, manual art direction | Cuts without scaling |
| `image_convert` | Format standardization, manual optimization | Converts to JPEG, PNG, WebP, GIF |
| `image_convert_avif` | Modern format optimization with fallback | Tries AVIF, falls back to specified format |
| `image_rotate` | Orientation correction, artistic effects | Rotates by degrees, can randomize |
| `image_desaturate` | Grayscale conversion | Full desaturation, no config needed |

## Pattern - Common Effects

**image_scale** (most common):
```yaml
data:
  width: 480
  height: 480
  upscale: false  # Don't enlarge small images
```

**image_scale_and_crop** (thumbnails):
```yaml
data:
  width: 400
  height: 300
  anchor: center-center  # left-top, center-top, right-top, etc.
```

**image_convert_avif** (optimization):
```yaml
data:
  extension: webp  # Fallback if AVIF unavailable
```

## Effect Chaining

Effects execute in weight order (lowest first). Each effect receives the output of the previous effect.

```yaml
effects:
  uuid-1:
    id: image_scale
    weight: 0
    data:
      width: 800
      height: 600
  uuid-2:
    id: image_desaturate
    weight: 1
    data: { }
  uuid-3:
    id: image_convert
    weight: 2
    data:
      extension: webp
```

## Common Mistakes

- **Wrong**: Using `image_resize` when `image_scale` intended → **Right**: Use image_scale for responsive images (distorts images, user complaints)
- **Wrong**: Setting `upscale: true` on large image styles → **Right**: Use `upscale: false` (massive derivatives from small sources, storage bloat)
- **Wrong**: Forgetting to set anchor on crop effects → **Right**: Explicitly set anchor (center-center default crops faces/text)
- **Wrong**: Converting to JPEG before rotate → **Right**: Rotate before format conversion (loses transparency fill areas become white)
- **Wrong**: Randomizing rotation in production → **Right**: Use fixed rotation (cache thrashing, inconsistent output across page loads)
- **Wrong**: Assuming AVIF works without checking PHP version → **Right**: Check PHP 8.1+ and libavif support (falls back to fallback format silently, no optimization gains)

## See Also

- [Image Style Config Schema](image-style-schema.md)
- [Creating Image Styles via Config](creating-styles-config.md)
- [WebP & AVIF Optimization](webp-avif-optimization.md)
- Reference: core/modules/image/src/Plugin/ImageEffect/
