---
description: Optimize images with WebP and AVIF
drupal_version: "11.x"
---

# WebP & AVIF Optimization

## When to Use

> Use this when optimizing image delivery with modern formats (WebP, AVIF) while maintaining fallback for older browsers.

## Decision

| If... | Use... | Why |
|---|---|---|
| Site targets modern browsers only | `image_convert_avif` with WebP fallback | Best compression, future-proof |
| Need maximum compatibility | `image_convert` to WebP only | Near-universal support, good compression |
| Server lacks AVIF support (PHP < 8.1) | `image_convert` to WebP | AVIF requires newer PHP |
| Serving to legacy IE11 users | No conversion (JPEG/PNG) | WebP unsupported in IE |
| Transparency required | PNG or WebP | JPEG loses transparency |
| Photo content | AVIF > WebP > JPEG | Lossy compression benefits |
| Icons/diagrams | WebP lossless or PNG | Sharp edges preserved |

## Pattern

1. **Check PHP/GD support**

   ```bash
   drush php-eval "print_r(gd_info());"
   drush php-eval "var_dump(function_exists('imageavif'));"
   ```

2. **Add conversion effect**

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

   **For WebP only (safe):**
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

3. **Flush existing derivatives**

   ```bash
   drush image:flush large
   # or: drush image:flush --all
   ```

## Format Comparison

| Format | File Size | Browser Support | Use Case |
|---|---|---|---|
| JPEG | Baseline (100%) | Universal | Fallback only |
| PNG | 26% larger than WebP lossless | Universal | Transparency fallback |
| WebP | 25-34% smaller than JPEG | 96%+ (2025) | Primary optimization target |
| AVIF | 50% smaller than JPEG | 80%+ (2025) | Cutting edge optimization |

## Performance Impact

**Bandwidth savings:**
- WebP vs JPEG: 25-34% reduction
- AVIF vs JPEG: 50% reduction
- Properly sized responsive images: ~30% additional reduction

**LCP improvement:** Smaller files = faster download = better LCP (target: LCP < 2.5s)

## Common Mistakes

- **Wrong**: Assuming AVIF works without checking PHP version → **Right**: Check PHP 8.1+ and libavif support (silent fallback to fallback format, no error)
- **Wrong**: Converting all images to WebP without testing transparency → **Right**: Test PNG transparency conversion (lost alpha channel on PNGs in some GD versions)
- **Wrong**: Not flushing derivatives after adding convert effect → **Right**: Flush all derivatives (old JPEG derivatives served until cache expires)
- **Wrong**: Using AVIF without fallback → **Right**: Always set fallback extension (broken images if PHP lacks AVIF support)
- **Wrong**: Converting before scaling → **Right**: Scale first, convert last (wasted processing)

## See Also

- [Core Image Effects](core-image-effects.md)
- [Best Practices & Patterns](best-practices.md)
- Reference: https://www.specbee.com/blogs/optimize-images-in-drupal-for-core-web-vitals
- Reference: https://www.drupal.org/project/imageapi_optimize_avif_webp
