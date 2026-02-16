---
description: Naming conventions, standard sizes, lazy loading strategies, and performance patterns for image style configuration and deployment
---

# Best Practices & Patterns

## When to Use

> Use this when you need guidance on naming conventions, standard sizes, performance optimization, and lazy loading patterns.

## Naming Conventions

**Image styles:**
- **Pattern:** `{purpose}_{size_descriptor}` or `{context}_{dimensions}`
- **Examples:**
  - `thumbnail` (generic, 100x100)
  - `hero_large` (purpose + size)
  - `card_image_16x9` (purpose + aspect ratio)
  - `author_avatar` (purpose, implies square)
- **Avoid:** Non-descriptive names like `style_1`, `new_style`, `test`

**Responsive image styles:**
- **Pattern:** `{context}_responsive` or just `{context}`
- **Examples:**
  - `hero` (implies responsive)
  - `content_responsive`
  - `gallery_item`

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

### 1. Lazy loading strategy

| Image type | Loading attribute | Why |
|---|---|---|
| Above-fold hero | `eager` | Avoid LCP delay |
| Below-fold content | `lazy` | Save bandwidth, faster initial load |
| User avatars | `lazy` | Often numerous, non-critical |
| Background images | N/A (CSS) | Use Intersection Observer if critical |

### 2. Derivative generation

- **Lazy generation (default):** Derivatives created on first request. Good: no wasted processing. Bad: first-user delay.
- **Pre-generation:** Generate derivatives via cron/script. Good: no user-facing delay. Bad: storage bloat if images unused.

### 3. CDN integration

```php
// Let CDN handle image derivatives
$config['image.settings']['allow_insecure_derivatives'] = TRUE;
$config['image.settings']['suppress_itok_output'] = TRUE;
```
Only if CDN provides security (signed URLs, origin restrictions).

### 4. Image style reuse

```yaml
# DON'T create near-duplicate styles
image.style.content_large_1920:
  effects: { width: 1920 }
image.style.content_large_1900:
  effects: { width: 1900 }

# DO reuse with minor differences handled in CSS
image.style.content_large:
  effects: { width: 1920 }
```

## Breakpoint Alignment

**Align image breakpoints with CSS breakpoints:**

```yaml
# olivero.breakpoints.yml (theme breakpoints)
olivero.md:
  label: Medium
  mediaQuery: 'all and (min-width: 700px)'

# Should match SCSS breakpoints
$breakpoint-md: 700px;
```

## Config Organization

**Module/theme structure:**
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

- Not aligning image breakpoints with CSS → Images switch at different viewport widths than layout
- Creating too many image styles → Storage bloat, confusing UI, maintenance burden
- Inconsistent naming → Hard to remember, unclear purpose
- Using eager loading everywhere → Wastes bandwidth, slower page loads
- Not reusing image styles → Duplication, config bloat
- Generating derivatives for unused view modes → Wasted storage, processing

## See Also

- [WebP & AVIF Optimization](webp-avif-optimization.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.specbee.com/blogs/optimize-images-in-drupal-for-core-web-vitals
