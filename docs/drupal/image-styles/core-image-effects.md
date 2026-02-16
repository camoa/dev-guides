---
description: Complete catalog of Drupal core's 8 image effect plugins with data schemas, use cases, and gotchas for each transformation type
---

# Core Image Effects

## When to Use

> Use this when you need to configure specific image transformations in an image style. Drupal core provides 8 image effect plugins.

## Effects Catalog

### image_resize

**Description:** Resize to exact dimensions. May stretch or shrink disproportionately.

**Data Schema:**
```yaml
data:
  width: 300      # Required, integer, min 1
  height: 200     # Required, integer, min 1
```

**Use Case:** Fixed-size elements where aspect ratio doesn't matter (e.g., placeholder images, strict design system constraints).

**Gotchas:**
- Does not maintain aspect ratio → can distort images severely
- Both width and height required → no partial resize

### image_scale

**Description:** Scale maintaining aspect ratio. If one dimension omitted, calculated automatically.

**Data Schema:**
```yaml
data:
  width: 480      # Optional, integer, min 1
  height: 480     # Optional, integer, min 1
  upscale: false  # Optional, boolean, default false
```

**Use Case:** Most common effect for responsive images. Maintains quality, prevents distortion.

**Gotchas:**
- At least one dimension required → config validation error if both empty
- `upscale: false` prevents enlarging small images → good for performance, bad for consistency
- `upscale: true` degrades quality on small source images → pixelation risk

### image_scale_and_crop

**Description:** Scale to fill target dimensions, then crop excess. Maintains aspect ratio, no stretching.

**Data Schema:**
```yaml
data:
  width: 400           # Required, integer, min 1
  height: 300          # Required, integer, min 1
  anchor: center-center  # Optional, string, default 'center-center'
```

**Anchor Options:**
- `left-top`, `center-top`, `right-top`
- `left-center`, `center-center`, `right-center`
- `left-bottom`, `center-bottom`, `right-bottom`

**Use Case:** Square thumbnails, hero images with fixed aspect ratios.

**Gotchas:**
- Default center-center anchor may crop important content → test with real images
- Crops whichever dimension is larger after scaling → may lose critical image areas

### image_crop

**Description:** Crop to dimensions without scaling. Cuts from anchor point.

**Data Schema:**
```yaml
data:
  width: 300           # Required, integer, min 1
  height: 300          # Required, integer, min 1
  anchor: center-center  # Optional, string, default 'center-center'
```

**Use Case:** Extract specific region from image, manual art direction.

**Gotchas:**
- No scaling → if source smaller than crop dimensions, crops to source size
- Anchor applies before crop → unexpected results if anchor misunderstood

### image_convert

**Description:** Convert image to a different format (JPEG, PNG, WebP).

**Data Schema:**
```yaml
data:
  extension: webp  # Required, string, must be toolkit-supported
```

**Valid Extensions:** Depends on image toolkit. GD toolkit typically supports: `jpeg`, `jpg`, `png`, `gif`, `webp` (PHP 7.0+).

**Use Case:** Format standardization, manual optimization, fallback for AVIF.

**Gotchas:**
- GD toolkit WebP support requires PHP compiled with libwebp → check `gd_info()` output
- Converting from PNG to JPEG loses transparency → background becomes white or black
- Extension must be in `ImageToolkitManager::getAllValidExtensions()` → unsupported format = config validation error

### image_convert_avif

**Description:** Convert to AVIF with fallback. If AVIF unsupported, uses fallback format.

**Data Schema:**
```yaml
data:
  extension: webp  # Required, string, fallback format if AVIF unavailable
```

**Use Case:** Modern format optimization with graceful degradation.

**Gotchas:**
- AVIF requires PHP 8.1+ with GD compiled with libavif → not universally available
- Falls back silently → check derivative extension to verify AVIF worked
- Fallback format still processes even if AVIF succeeds in config → no extra derivatives, just config declaration

### image_rotate

**Description:** Rotate image by degrees. Can randomize rotation.

**Data Schema:**
```yaml
data:
  degrees: 90        # Required, integer, positive = clockwise, negative = counter-clockwise
  bgcolor: '#FFFFFF' # Optional, color_hex, transparent if omitted and format supports
  random: false      # Optional, boolean, randomizes within +/- degrees
```

**Use Case:** Orientation correction, artistic effects.

**Gotchas:**
- Rotation increases canvas size to fit diagonal → derivative dimensions unpredictable
- `random: true` generates different output per derivative creation → breaks caching expectations
- Bgcolor required for formats without transparency (JPEG) → black corners if omitted

### image_desaturate

**Description:** Convert to grayscale. No configuration.

**Data Schema:**
```yaml
data: { }  # Or omit data key entirely
```

**Use Case:** Artistic effect, accessibility adjustments, print preparation.

**Gotchas:**
- No configuration options → always full desaturation, no partial grayscale
- Irreversible in effect chain → place last if combining with color-dependent effects

## Effect Chaining

Effects execute in weight order (lowest first). Each effect receives the output of the previous effect.

**Example**: Scale → Desaturate → Convert to WebP
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

- Using `image_resize` when `image_scale` intended → distorts images, user complaints
- Setting `upscale: true` on large image styles → massive derivatives from small sources, storage bloat
- Forgetting to set anchor on `image_crop` / `image_scale_and_crop` → center-center default crops faces/text
- Converting to JPEG before rotate → loses transparency fill areas become white
- Randomizing rotation in production → cache thrashing, inconsistent output across page loads
- Assuming AVIF works without checking PHP version → falls back to fallback format silently, no optimization gains

## See Also

- [Image Style Config Schema](image-style-schema.md) (for YAML structure)
- [Creating Image Styles via Config](creating-styles-config.md) (for workflow)
- [WebP & AVIF Optimization](webp-avif-optimization.md) (for format conversion best practices)
- Reference: core/modules/image/src/Plugin/ImageEffect/
