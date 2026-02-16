---
description: Choose between sizes attribute (resolution switching) and picture element (art direction) for responsive images with config examples
---

# Art Direction vs Resolution Switching

## When to Use

> Use this when you need to decide whether to use the sizes attribute (resolution switching) or distinct image styles per breakpoint (art direction).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Same crop, different resolutions for DPR/viewport | Sizes attribute (resolution switching) | Browser picks best resolution, minimal config, fewer derivatives |
| Different crops for mobile vs desktop | Picture element (art direction) | Full control over which image shows at each breakpoint |
| Different aspect ratios per viewport | Picture element (art direction) | 16:9 on desktop, 1:1 on mobile, etc. |
| Same aspect ratio, automatic browser selection | Sizes attribute | Simpler config, browser optimizes based on viewport + DPR |
| Show different focal points (face on mobile, full body on desktop) | Picture element (art direction) | Manual control over important content visibility |

## Pattern - Resolution Switching (Sizes Attribute)

**When:** Same image crop, browser picks resolution based on viewport width and device pixel ratio.

**Config:**
```yaml
# responsive_image.styles.content.yml
id: content
label: 'Content Images'
breakpoint_group: responsive_image
fallback_image_style: medium
image_style_mappings:
  - image_mapping_type: sizes
    image_mapping:
      sizes: '(min-width: 1200px) 1200px, (min-width: 768px) 768px, 100vw'
      sizes_image_styles:
        - large        # 1200px
        - medium       # 768px
        - small        # 480px
        - thumbnail    # 240px
    breakpoint_id: responsive_image.viewport_sizing
    multiplier: 1x
```

**Output:**
```html
<img srcset="/styles/large/image.jpg 1200w,
             /styles/medium/image.jpg 768w,
             /styles/small/image.jpg 480w,
             /styles/thumbnail/image.jpg 240w"
     sizes="(min-width: 1200px) 1200px, (min-width: 768px) 768px, 100vw"
     src="/styles/medium/image.jpg" alt="...">
```

## Pattern - Art Direction (Picture Element)

**When:** Different crops/aspect ratios per breakpoint.

**Config:**
```yaml
# responsive_image.styles.hero.yml
id: hero
label: 'Hero Images'
breakpoint_group: olivero
fallback_image_style: hero_mobile
image_style_mappings:
  - image_mapping_type: image_style
    image_mapping: hero_mobile      # 1:1 square crop
    breakpoint_id: olivero.sm
    multiplier: 1x
  - image_mapping_type: image_style
    image_mapping: hero_tablet      # 4:3 crop
    breakpoint_id: olivero.md
    multiplier: 1x
  - image_mapping_type: image_style
    image_mapping: hero_desktop     # 16:9 crop
    breakpoint_id: olivero.lg
    multiplier: 1x
```

**Output:**
```html
<picture>
  <source media="(min-width: 1000px)" srcset="/styles/hero_desktop/image.jpg">
  <source media="(min-width: 700px)" srcset="/styles/hero_tablet/image.jpg">
  <source media="(min-width: 500px)" srcset="/styles/hero_mobile/image.jpg">
  <img src="/styles/hero_mobile/image.jpg" alt="...">
</picture>
```

## Sizes Attribute Syntax

**Format:** `(media-query) width, (media-query) width, default-width`

**Examples:**

```yaml
# Full viewport width on all screens
sizes: '100vw'

# Fixed width on desktop, full width on mobile
sizes: '(min-width: 1200px) 1200px, 100vw'

# Sidebar layout (main content is 75% on desktop, full on mobile)
sizes: '(min-width: 768px) 75vw, 100vw'

# Fixed max width with padding
sizes: '(min-width: 1400px) 1200px, calc(100vw - 2rem)'
```

## Common Mistakes

- Using sizes attribute with 2x/3x multipliers → Invalid HTML, browser ignores sizes
- Art direction when resolution switching suffices → Storage bloat, maintenance overhead
- Sizes attribute doesn't match CSS layout → Browser picks wrong image, wasted bandwidth
- Listing image styles in sizes_image_styles in wrong order → Browser confused about which to use
- Not providing fallback for `<picture>` → Broken images in old browsers
- Using art direction for minor crop differences → Over-engineering, user won't notice
- Sizes attribute missing default value → Last value should have no media query

## See Also

- [Responsive Image Style Config](responsive-image-config.md)
- [Breakpoint Configuration](breakpoint-configuration.md)
- Reference: https://www.drupal.org/docs/mobile-guide/responsive-images-in-drupal
- Reference: https://www.w3.org/html/wg/drafts/html/master/embedded-content.html#attr-img-sizes
