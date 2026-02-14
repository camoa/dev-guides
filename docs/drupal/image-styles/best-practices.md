---
description: Follow naming conventions and performance patterns
drupal_version: "11.x"
---

# Best Practices & Patterns

## When to Use

> Use this for guidance on naming conventions, standard sizes, performance optimization, and lazy loading patterns.

## Naming Conventions

**Image styles:**
- **Pattern:** `{purpose}_{size_descriptor}` or `{context}_{dimensions}`
- **Examples:** `thumbnail`, `hero_large`, `card_image_16x9`, `author_avatar`
- **Avoid:** Non-descriptive names like `style_1`, `new_style`, `test`

**Responsive image styles:**
- **Pattern:** `{context}_responsive` or just `{context}`
- **Examples:** `hero`, `content_responsive`, `gallery_item`

## Standard Image Style Sizes

**Recommended size ladder** (power of 2 or common breakpoints):

| Name | Width | Height | Use Case |
|---|---|---|---|
| `thumbnail` | 100 | 100 | User avatars, small icons |
| `small` | 240 | 240 | Card images, listings |
| `medium` | 480 | 480 | Sidebar images, small content |
| `large` | 960 | 960 | Main content images |
| `xlarge` | 1920 | 1920 | Full-width hero images |

**Aspect ratio variants:**

| Name | Dimensions | Ratio | Use Case |
|---|---|---|---|
| `card_4x3` | 480x360 | 4:3 | Card grids |
| `hero_16x9` | 1920x1080 | 16:9 | Hero banners |
| `square_small` | 320x320 | 1:1 | Social thumbnails |

## Performance Patterns

**1. Lazy loading strategy:**

| Image type | Loading attribute | Why |
|---|---|---|
| Above-fold hero | `eager` | Avoid LCP delay |
| Below-fold content | `lazy` | Save bandwidth, faster initial load |
| User avatars | `lazy` | Often numerous, non-critical |
| Background images | N/A (CSS) | Use Intersection Observer if critical |

**2. Derivative generation:**
- **Lazy generation (default):** Derivatives created on first request. Good: no wasted processing. Bad: first-user delay.
- **Pre-generation:** Generate derivatives via cron/script. Good: no user-facing delay. Bad: storage bloat if images unused.

**3. Image style reuse:**
```yaml
# DON'T create near-duplicate styles
image.style.content_large_1920: { width: 1920 }
image.style.content_large_1900: { width: 1900 }

# DO reuse with minor differences handled in CSS
image.style.content_large: { width: 1920 }
```

## Breakpoint Alignment

Align image breakpoints with CSS breakpoints:

```yaml
# olivero.breakpoints.yml
olivero.md:
  label: Medium
  mediaQuery: 'all and (min-width: 700px)'

# Should match SCSS
$breakpoint-md: 700px;
```

## Config Organization

```
my_theme/
├── config/
│   └── install/
│       ├── image.style.hero_large.yml
│       ├── image.style.hero_medium.yml
│       ├── responsive_image.styles.hero.yml
│       └── core.entity_view_display.node.article.default.yml
└── my_theme.breakpoints.yml
```

## Common Mistakes

- **Wrong**: Not aligning image breakpoints with CSS → **Right**: Match breakpoints exactly (images switch at different viewport widths than layout)
- **Wrong**: Creating too many image styles → **Right**: Keep to 5-10 styles (storage bloat, confusing UI, maintenance burden)
- **Wrong**: Inconsistent naming → **Right**: Follow naming patterns (hard to remember, unclear purpose)
- **Wrong**: Using eager loading everywhere → **Right**: Eager for above-fold only (wastes bandwidth, slower page loads)
- **Wrong**: Not reusing image styles → **Right**: Reuse across contexts (duplication, config bloat)

## See Also

- [WebP & AVIF Optimization](webp-avif-optimization.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.specbee.com/blogs/optimize-images-in-drupal-for-core-web-vitals
