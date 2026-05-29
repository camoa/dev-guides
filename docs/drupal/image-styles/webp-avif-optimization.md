---
description: Optimize image delivery with WebP and AVIF formats using image_convert effects with PHP/GD support checks and fallback strategies
tldr: "Use this when you need to optimize image delivery with modern formats (WebP, AVIF) while maintaining fallback for older browsers. AVIF is the Drupal 11 core default but is encoding-heavy; prefer WebP-only on shared/modest hosting."
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

**WebP (safe default — works on virtually any host):**
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

**AVIF with WebP fallback (the Drupal 11 core default):**
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
      extension: webp  # Server-side fallback when the toolkit can't produce AVIF
```

> **Hosting caveat:** Core 11 ships `image_convert_avif` in its default styles, and the effect degrades to the `extension` fallback on servers without AVIF support — so it is *safe* on unsupported hosts. The real cost is that AVIF **encoding is CPU- and memory-heavy and slow**; on shared/modest hosting, generating AVIF derivatives can hit PHP time/memory limits or noticeably delay first-request rendering. If you'd rather avoid that, swap `image_convert_avif` → `image_convert` with `extension: webp` in the affected styles (including the core defaults). WebP is the more conservative, widely-deployed choice.

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
| WebP | 25-34% smaller than JPEG | ~97% (2026) | Safe default optimization target |
| AVIF | 50% smaller than JPEG | ~93% (2026) | Best compression; Drupal 11 core default (with WebP fallback) |

## Decision Points

| If... | Use... | Why |
|---|---|---|
| Default / following core 11 | `image_convert_avif` with WebP fallback | Core default; best compression where the toolkit supports AVIF, safe webp fallback where it doesn't |
| Shared/modest hosting, want predictable generation cost | `image_convert` to WebP only | Avoids slow, memory-heavy AVIF encoding; near-universal browser support |
| Need maximum simplicity/compatibility | `image_convert` to WebP only | One format, widely deployed, good compression |
| Transparency required | WebP (or AVIF) — both support alpha | JPEG loses transparency |
| Photo content | AVIF > WebP > JPEG | Lossy compression benefits |
| Icons/diagrams | WebP lossless or PNG | Sharp edges preserved |

> The AVIF-vs-WebP choice here is about **server encoding cost**, not browser targeting — `image_convert_avif` already degrades to the fallback format on hosts without AVIF support. Per-browser format negotiation is a separate concern (needs `<picture>` `type` sources, contrib).

## Format Strategy

**AVIF with WebP fallback (Drupal 11 core default):**
```yaml
# Generates AVIF where the toolkit supports it, otherwise WebP
effects:
  uuid-1:
    id: image_convert_avif
    weight: 0
    data:
      extension: webp
```

The fallback is decided **server-side** by toolkit capability — if the server lacks AVIF, every derivative is WebP. It is **not** a per-browser fallback: where AVIF is generated, all visitors receive `.avif`. For true per-browser negotiation you need a `<picture>` element with `type`-based sources, which core's responsive image module does not emit on its own (use contrib such as ImageAPI Optimize WebP/AVIF).

**WebP only (conservative default for shared/modest hosting):**
```yaml
effects:
  uuid-1:
    id: image_convert
    weight: 0
    data:
      extension: webp
```

WebP avoids AVIF's heavy encoding cost while still cutting 25–34% off JPEG. Prefer this when derivative-generation time/memory is a concern.

## Performance Impact

**Bandwidth savings** (source: Specbee research 2025):
- WebP vs JPEG: 25-34% reduction
- AVIF vs JPEG: 50% reduction
- Properly sized responsive images: ~30% additional reduction

**LCP improvement:**
- Smaller files → faster download → better LCP
- Target: LCP < 2.5s (Core Web Vitals)

## Common Mistakes

- Assuming you're actually getting AVIF → `image_convert_avif` silently emits the fallback format when the toolkit lacks AVIF; verify the generated derivative's extension
- Ignoring AVIF encoding cost on shared hosting → slow derivative generation, possible PHP time/memory limits; use `image_convert` to WebP if this bites
- Converting all images to WebP without testing transparency → Lost alpha channel on PNGs converted to WebP in some GD versions
- Not flushing derivatives after adding convert effect → Old JPEG derivatives served until cache expires
- Using plain `image_convert` with `extension: avif` (no fallback) → Broken/failed derivatives where the toolkit lacks AVIF; use `image_convert_avif` so it falls back automatically
- Converting before scaling → Wasted processing, convert after final dimensions
- Setting convert effect weight before crop/scale → May get reconverted by toolkit, quality loss

## See Also

- [Core Image Effects](core-image-effects.md) (image_convert, image_convert_avif)
- [Best Practices & Patterns](best-practices.md) (performance)
- Reference: https://www.specbee.com/blogs/optimize-images-in-drupal-for-core-web-vitals
- Reference: https://www.drupal.org/project/imageapi_optimize_avif_webp
