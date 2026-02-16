---
description: Optimize image delivery with WebP and AVIF formats using image_convert effects with PHP/GD support checks and fallback strategies
---

# WebP & AVIF Optimization

## When to Use

> Use this when you need to optimize image delivery with modern formats (WebP, AVIF) while maintaining fallback for older browsers.

## Steps

### 1. Check PHP/GD support

```bash
# Check GD WebP support (requires libwebp)
drush php-eval "print_r(gd_info());"

# Check for AVIF support (requires PHP 8.1+ with libavif)
drush php-eval "var_dump(function_exists('imageavif'));"
```

### 2. Add conversion effect to image styles

**For WebP (universal support):**
```yaml
effects:
  uuid-1:
    id: image_scale
    weight: 0
    data:
      width: 1200
      height: 800
  uuid-2:
    id: image_convert
    weight: 1
    data:
      extension: webp
```

**For AVIF with WebP fallback (recommended):**
```yaml
effects:
  uuid-1:
    id: image_scale
    weight: 0
    data:
      width: 1200
      height: 800
  uuid-2:
    id: image_convert_avif
    weight: 1
    data:
      extension: webp  # Fallback if AVIF unsupported
```

### 3. Flush existing derivatives to regenerate with new format

```bash
# Flush specific style
drush image:flush large

# Flush all styles
drush image:flush --all
```

## Format Comparison

| Format | File Size | Browser Support | Use Case |
|---|---|---|---|
| JPEG | Baseline (100%) | Universal | Fallback only |
| PNG | 26% larger than WebP lossless | Universal | Transparency fallback |
| WebP | 25-34% smaller than JPEG | 96%+ (2025) | Primary optimization target |
| AVIF | 50% smaller than JPEG | 80%+ (2025) | Cutting edge optimization |

## Decision Points

| If... | Use... | Why |
|---|---|---|
| Site targets modern browsers only | `image_convert_avif` with WebP fallback | Best compression, future-proof |
| Need maximum compatibility | `image_convert` to WebP only | Near-universal support, good compression |
| Server lacks AVIF support (PHP < 8.1) | `image_convert` to WebP | AVIF requires newer PHP |
| Serving to legacy IE11 users | No conversion (JPEG/PNG) | WebP unsupported in IE |
| Transparency required | PNG or WebP | JPEG loses transparency |
| Photo content | AVIF > WebP > JPEG | Lossy compression benefits |
| Icons/diagrams | WebP lossless or PNG | Sharp edges preserved |

## Browser Support Strategy

**AVIF with fallback (best):**
```yaml
# Image style with AVIF attempt
effects:
  uuid-1:
    id: image_convert_avif
    weight: 0
    data:
      extension: webp
```

If AVIF unsupported by PHP, generates WebP. Browsers that don't support WebP will fall back via `<picture>` or UA sniffing (requires contrib module).

**WebP only (safe):**
```yaml
effects:
  uuid-1:
    id: image_convert
    weight: 0
    data:
      extension: webp
```

## Performance Impact

**Bandwidth savings** (source: Specbee research 2025):
- WebP vs JPEG: 25-34% reduction
- AVIF vs JPEG: 50% reduction
- Properly sized responsive images: ~30% additional reduction

**LCP improvement:**
- Smaller files → faster download → better LCP
- Target: LCP < 2.5s (Core Web Vitals)

## Common Mistakes

- Assuming AVIF works without checking PHP version → Silent fallback to fallback format, no error
- Converting all images to WebP without testing transparency → Lost alpha channel on PNGs converted to WebP in some GD versions
- Not flushing derivatives after adding convert effect → Old JPEG derivatives served until cache expires
- Using AVIF without fallback → Broken images if PHP lacks AVIF support
- Converting before scaling → Wasted processing, convert after final dimensions
- Setting convert effect weight before crop/scale → May get reconverted by toolkit, quality loss

## See Also

- [Core Image Effects](core-image-effects.md) (image_convert, image_convert_avif)
- [Best Practices & Patterns](best-practices.md) (performance)
- Reference: https://www.specbee.com/blogs/optimize-images-in-drupal-for-core-web-vitals
- Reference: https://www.drupal.org/project/imageapi_optimize_avif_webp
