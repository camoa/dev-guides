---
description: Common mistakes and anti-patterns to avoid when configuring image styles, responsive images, and format conversions
---

# Anti-Patterns & Common Mistakes

## When to Use

> Use this when you need to understand what NOT to do and WHY to avoid costly mistakes.

## Anti-Pattern: Over-Engineering with Responsive Images

**What:** Using responsive image styles for small, fixed-size UI elements.

**Why it's wrong:** Responsive images generate multiple derivatives per breakpoint. For a 64x64 avatar that never changes size, this creates 5-10 unnecessary derivatives, wastes storage, and adds config complexity with zero UX benefit.

**Correct approach:** Use single image style for fixed-size elements.

```yaml
# BAD: Responsive for avatar
field_avatar:
  type: responsive_image
  settings:
    responsive_image_style: avatar_responsive  # Generates 8 derivatives

# GOOD: Single style for avatar
field_avatar:
  type: image
  settings:
    image_style: avatar_64x64  # Generates 1 derivative
```

## Anti-Pattern: Lazy Loading Above-Fold Images

**What:** Setting `image_loading: lazy` on hero images or above-fold content.

**Why it's wrong:** Lazy loading defers image load until browser determines it's in viewport. For above-fold images, this delays Largest Contentful Paint (LCP), tanks Core Web Vitals scores, and makes the page feel slower. Browsers penalize this in performance metrics.

**Correct approach:** Use `eager` for above-fold, `lazy` for below-fold.

```yaml
# BAD: Lazy hero image
field_hero:
  settings:
    image_loading:
      attribute: lazy  # Delays LCP by 1-2s

# GOOD: Eager hero, lazy content
field_hero:
  settings:
    image_loading:
      attribute: eager

field_content_images:
  settings:
    image_loading:
      attribute: lazy
```

## Anti-Pattern: Missing Fallback Image Style

**What:** Responsive image style without `fallback_image_style` set.

**Why it's wrong:** No-JS browsers, crawlers, and RSS readers use the fallback. If omitted, they get blank images or broken display. Accessibility failure, SEO harm, broken email notifications.

**Correct approach:** Always set fallback to smallest acceptable size.

```yaml
# BAD: No fallback
id: hero
breakpoint_group: olivero
fallback_image_style: ''  # Blank

# GOOD: Fallback set
id: hero
breakpoint_group: olivero
fallback_image_style: hero_small
```

## Anti-Pattern: Creating Image Styles Programmatically

**What:** Using `ImageStyle::create()` in hooks or services.

**Why it's wrong:** Config created in code isn't exported, isn't tracked in version control, breaks on config import, and causes "config overridden" warnings. Update hooks run once, so style only exists on sites that ran the hook. Sites installed later never get it.

**Correct approach:** Always use YAML config in `config/install/`.

```php
// BAD: Programmatic creation
function my_module_install() {
  $style = ImageStyle::create(['name' => 'custom']);
  $style->save();  // Not exportable, not in version control
}

// GOOD: YAML config
// config/install/image.style.custom.yml
name: custom
label: 'Custom Style'
effects: { }
```

## Anti-Pattern: Upscaling Small Images

**What:** Setting `upscale: true` on large image styles.

**Why it's wrong:** Upscaling a 400px source image to 1920px derivative creates a massive, blurry, pixelated file that's 10x the size with 1/10 the quality. Wastes bandwidth, looks terrible, angers users. The browser could just scale the original CSS-side with same visual result and less data.

**Correct approach:** Use `upscale: false` (default) and handle small sources in CSS if needed.

```yaml
# BAD: Upscale enabled on large style
effects:
  uuid-1:
    id: image_scale
    data:
      width: 1920
      height: 1080
      upscale: true  # 400px source becomes 1920px blurry mess

# GOOD: No upscaling
effects:
  uuid-1:
    id: image_scale
    data:
      width: 1920
      height: 1080
      upscale: false  # Small sources stay small, sharp
```

## Anti-Pattern: Mixing Sizes Attribute with Multiple Multipliers

**What:** Using `image_mapping_type: sizes` with `multiplier: 2x`.

**Why it's wrong:** The HTML5 spec forbids mixing `sizes` attribute with multiplier-based srcset. Browsers ignore the sizes attribute, pick wrong images, waste bandwidth. Results in invalid markup like: `<source sizes="..." srcset="img.jpg 1x, img2.jpg 2x">` which browsers can't parse correctly.

**Correct approach:** Use sizes only with `1x` multiplier. For 2x, use image_style mapping type.

```yaml
# BAD: Sizes with 2x
image_style_mappings:
  - image_mapping_type: sizes
    image_mapping:
      sizes: '100vw'
      sizes_image_styles: [large, medium]
    breakpoint_id: responsive_image.viewport_sizing
    multiplier: 2x  # INVALID HTML

# GOOD: Sizes with 1x only
image_style_mappings:
  - image_mapping_type: sizes
    image_mapping:
      sizes: '100vw'
      sizes_image_styles: [large, medium]
    breakpoint_id: responsive_image.viewport_sizing
    multiplier: 1x
```

## Anti-Pattern: Converting Format Before Scaling

**What:** Placing `image_convert` effect before `image_scale` in weight order.

**Why it's wrong:** Converts the full-size original image, then scales it. For a 5000px source, this processes 5000px worth of data through format conversion, then throws away most of it in scaling. Wastes CPU, memory, and time. Worse, some toolkits reconvert after scale, causing double conversion quality loss.

**Correct approach:** Scale first (weight 0), convert last (weight 1+).

```yaml
# BAD: Convert before scale
effects:
  uuid-1:
    id: image_convert
    weight: 0  # Converts 5000px image
    data:
      extension: webp
  uuid-2:
    id: image_scale
    weight: 1  # Scales 5000px WebP to 800px
    data:
      width: 800

# GOOD: Scale before convert
effects:
  uuid-1:
    id: image_scale
    weight: 0  # Scales 5000px to 800px
    data:
      width: 800
  uuid-2:
    id: image_convert
    weight: 1  # Converts 800px image
    data:
      extension: webp
```

## Anti-Pattern: Using image_url for Visible Images

**What:** Using `image_url` formatter for images displayed via `<img>` tags.

**Why it's wrong:** `image_url` outputs a URL string only, no alt text, no accessibility attributes. Screen readers can't describe the image. WCAG violation, lawsuit risk, poor SEO. Images should always have alt text.

**Correct approach:** Use `image` or `responsive_image` formatter for visible images. Reserve `image_url` for CSS backgrounds or meta tags.

```yaml
# BAD: image_url for content image
field_photo:
  type: image_url
  # No alt text, screen reader says nothing

# GOOD: image formatter
field_photo:
  type: image
  # Includes alt text from field
```

## Common Mistakes Summary

| Mistake | Impact | Fix |
|---|---|---|
| Responsive images for fixed UI | Storage bloat, config complexity | Use single image style |
| Lazy above-fold images | Poor LCP, failed Core Web Vitals | Use `eager` loading |
| Missing fallback style | Broken no-JS/RSS display | Always set fallback |
| Programmatic style creation | Not exportable, breaks config sync | Use YAML config |
| Upscaling small images | Pixelated, huge files | Use `upscale: false` |
| Sizes with 2x multiplier | Invalid HTML, wrong images | Sizes only with 1x |
| Convert before scale | Wasted processing, quality loss | Scale first, convert last |
| image_url for visible images | Accessibility violation | Use image formatter |

## See Also

- [Best Practices & Patterns](best-practices.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html
