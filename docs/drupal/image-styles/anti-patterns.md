---
description: Avoid common mistakes
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Use this to understand what NOT to do and WHY to avoid costly mistakes.

## Over-Engineering with Responsive Images

**Wrong:** Using responsive image styles for small, fixed-size UI elements.

**Why it's wrong:** Responsive images generate multiple derivatives per breakpoint. For a 64x64 avatar that never changes size, this creates 5-10 unnecessary derivatives, wastes storage, and adds config complexity with zero UX benefit.

**Right:**
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

## Lazy Loading Above-Fold Images

**Wrong:** Setting `image_loading: lazy` on hero images or above-fold content.

**Why it's wrong:** Lazy loading defers image load until browser determines it's in viewport. For above-fold images, this delays Largest Contentful Paint (LCP), tanks Core Web Vitals scores, and makes the page feel slower.

**Right:**
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
```

## Missing Fallback Image Style

**Wrong:** Responsive image style without `fallback_image_style` set.

**Why it's wrong:** No-JS browsers, crawlers, and RSS readers use the fallback. If omitted, they get blank images or broken display. Accessibility failure, SEO harm, broken email notifications.

**Right:**
```yaml
# BAD: No fallback
id: hero
fallback_image_style: ''

# GOOD: Fallback set
id: hero
fallback_image_style: hero_small
```

## Creating Image Styles Programmatically

**Wrong:** Using `ImageStyle::create()` in hooks or services.

**Why it's wrong:** Config created in code isn't exported, isn't tracked in version control, breaks on config import, and causes "config overridden" warnings.

**Right:**
```php
// BAD: Programmatic creation
function my_module_install() {
  $style = ImageStyle::create(['name' => 'custom']);
  $style->save();  // Not exportable
}

// GOOD: YAML config
// config/install/image.style.custom.yml
```

## Upscaling Small Images

**Wrong:** Setting `upscale: true` on large image styles.

**Why it's wrong:** Upscaling a 400px source image to 1920px derivative creates a massive, blurry, pixelated file that's 10x the size with 1/10 the quality. Wastes bandwidth, looks terrible.

**Right:**
```yaml
# BAD: Upscale enabled
data:
  width: 1920
  upscale: true  # 400px becomes 1920px blurry mess

# GOOD: No upscaling
data:
  width: 1920
  upscale: false  # Small sources stay small, sharp
```

## Mixing Sizes Attribute with Multiple Multipliers

**Wrong:** Using `image_mapping_type: sizes` with `multiplier: 2x`.

**Why it's wrong:** The HTML5 spec forbids mixing `sizes` attribute with multiplier-based srcset. Browsers ignore the sizes attribute, pick wrong images, waste bandwidth.

**Right:**
```yaml
# BAD: Sizes with 2x
image_style_mappings:
  - image_mapping_type: sizes
    multiplier: 2x  # INVALID HTML

# GOOD: Sizes with 1x only
image_style_mappings:
  - image_mapping_type: sizes
    multiplier: 1x
```

## Converting Format Before Scaling

**Wrong:** Placing `image_convert` effect before `image_scale` in weight order.

**Why it's wrong:** Converts the full-size original image, then scales it. Wastes CPU, memory, and time. Some toolkits reconvert after scale, causing double conversion quality loss.

**Right:**
```yaml
# BAD: Convert before scale
effects:
  uuid-1:
    id: image_convert
    weight: 0  # Converts 5000px image
  uuid-2:
    id: image_scale
    weight: 1  # Scales 5000px WebP

# GOOD: Scale before convert
effects:
  uuid-1:
    id: image_scale
    weight: 0  # Scales 5000px to 800px
  uuid-2:
    id: image_convert
    weight: 1  # Converts 800px image
```

## Using image_url for Visible Images

**Wrong:** Using `image_url` formatter for images displayed via `<img>` tags.

**Why it's wrong:** `image_url` outputs a URL string only, no alt text, no accessibility attributes. Screen readers can't describe the image. WCAG violation.

**Right:**
```yaml
# BAD: image_url for content
field_photo:
  type: image_url  # No alt text

# GOOD: image formatter
field_photo:
  type: image  # Includes alt text
```

## Summary Table

| Mistake | Impact | Fix |
|---|---|---|
| Responsive images for fixed UI | Storage bloat | Use single image style |
| Lazy above-fold images | Poor LCP | Use `eager` loading |
| Missing fallback style | Broken no-JS display | Always set fallback |
| Programmatic style creation | Not exportable | Use YAML config |
| Upscaling small images | Pixelated, huge files | Use `upscale: false` |
| Sizes with 2x multiplier | Invalid HTML | Sizes only with 1x |
| Convert before scale | Wasted processing | Scale first, convert last |
| image_url for visible images | Accessibility violation | Use image formatter |

## See Also

- [Best Practices & Patterns](best-practices.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html
