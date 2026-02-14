---
description: Configure image field formatters
drupal_version: "11.x"
---

# Image Field Formatters

## When to Use

> Use this when configuring how image fields display in view modes.

## Decision

| If displaying... | Use formatter... | Why |
|---|---|---|
| Fixed-size thumbnail or UI element | `image` | Simple, predictable output, minimal overhead |
| Full-width content images | `responsive_image` | Bandwidth optimization, DPR support |
| Hero/banner images above fold | `responsive_image` with `image_loading: eager` | Performance, avoid LCP delay |
| Background images via CSS | `image_url` | Need URL string, not markup |
| Meta tags (og:image, twitter:image) | `image_url` | Need absolute URL for external services |
| User avatars | `image` | Consistent size, no responsive needed |
| Gallery/lightbox images | `image` with `image_link: file` | Link to full-size for lightbox JS |

## Pattern - image formatter

```yaml
# In view display config
field_image:
  type: image
  settings:
    image_style: large
    image_link: content
    image_loading:
      attribute: lazy
  label: hidden
  weight: 0
```

**Parameters:**

| Parameter | Options | Default | Description |
|---|---|---|---|
| `image_style` | Image style ID or `''` | `''` | Empty = original image |
| `image_link` | `'content'`, `'file'`, `''` | `''` | Link destination |
| `image_loading.attribute` | `'lazy'`, `'eager'`, `''` | `'lazy'` | Native lazy loading |

## Pattern - responsive_image formatter

```yaml
field_hero_image:
  type: responsive_image
  settings:
    responsive_image_style: hero
    image_link: ''
    image_loading:
      attribute: eager  # Above-fold hero image
  label: hidden
  weight: 0
```

**Parameters:**

| Parameter | Options | Default | Description |
|---|---|---|---|
| `responsive_image_style` | Responsive image style ID | `''` | Required |
| `image_link` | `'content'`, `'file'`, `''` | `''` | Link destination |
| `image_loading.attribute` | `'lazy'`, `'eager'`, `''` | `'lazy'` | Native lazy loading |

## Pattern - image_url formatter

```yaml
field_background:
  type: image_url
  settings:
    image_style: hero_large
  label: hidden
```

**Parameters:**

| Parameter | Options | Default | Description |
|---|---|---|---|
| `image_style` | Image style ID or `''` | `''` | Empty = original image URL |

## Common Mistakes

- **Wrong**: Using `responsive_image` for all images → **Right**: Use image for fixed-size elements (over-engineering, storage bloat, processing overhead)
- **Wrong**: Lazy loading above-fold images → **Right**: Use eager for above-fold (poor LCP, failed Core Web Vitals)
- **Wrong**: `image_url` for visible images → **Right**: Use image formatter (no alt text, accessibility violation)
- **Wrong**: Not setting `image_style` on user-uploaded images → **Right**: Always set image_style (serving multi-MB originals)
- **Wrong**: `image_link: 'file'` expecting original size → **Right**: Use image_url if you need original URL (gets derivative URL instead)

## See Also

- [Image System Overview](image-overview.md)
- [Best Practices & Patterns](best-practices.md)
- Reference: core/modules/image/src/Plugin/Field/FieldFormatter/ImageFormatter.php
- Reference: core/modules/responsive_image/src/Plugin/Field/FieldFormatter/ResponsiveImageFormatter.php
