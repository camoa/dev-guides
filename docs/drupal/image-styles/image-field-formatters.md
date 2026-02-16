---
description: Configure image, image_url, and responsive_image field formatters with settings for lazy loading, linking, and style selection
---

# Image Field Formatters

## When to Use

> Use this when you need to configure how image fields display in view modes.

## Formatters Catalog

### image

**Description:** Standard image formatter. Displays single derivative from image style.

**Configuration Schema:**
```yaml
settings:
  image_style: ''          # Image style machine name or empty for original
  image_link: ''           # 'content', 'file', or empty
  image_loading:
    attribute: 'lazy'      # 'lazy', 'eager', or empty
```

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `image_style` | string | `''` | Image style ID. Empty = original image |
| `image_link` | string | `''` | Link destination. Options: `'content'` (node), `'file'` (image file), `''` (no link) |
| `image_loading.attribute` | string | `'lazy'` | Native lazy loading. `'lazy'` (load on scroll), `'eager'` (immediate), `''` (no attribute) |

**Usage Example:**
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

**Gotchas:**
- `image_link: 'file'` links to derivative, not original → unexpected for lightbox modules expecting full-size
- Lazy loading on above-fold images → delayed LCP, poor Core Web Vitals
- Empty `image_style` serves original → massive files for user-uploaded images

### image_url

**Description:** Outputs image URL as plain text (no `<img>` tag). Useful for background images, meta tags.

**Configuration Schema:**
```yaml
settings:
  image_style: ''  # Image style machine name or empty for original
```

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `image_style` | string | `''` | Image style ID. Empty = original image URL |

**Usage Example:**
```yaml
field_background:
  type: image_url
  settings:
    image_style: hero_large
  label: hidden
```

**Gotchas:**
- Outputs URL only, no alt text → inaccessible if used for visible images
- No lazy loading support → all URLs generated immediately
- Doesn't trigger derivative generation → URL may 404 if derivative not yet created

### responsive_image

**Description:** Responsive image formatter. Uses responsive image style to generate picture element or img with srcset.

**Configuration Schema:**
```yaml
settings:
  responsive_image_style: ''  # Responsive image style machine name
  image_link: ''              # 'content', 'file', or empty
  image_loading:
    attribute: 'lazy'         # 'lazy', 'eager', or empty
```

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `responsive_image_style` | string | `''` | Responsive image style ID (required) |
| `image_link` | string | `''` | Link destination. Options: `'content'`, `'file'`, `''` |
| `image_loading.attribute` | string | `'lazy'` | Native lazy loading |

**Usage Example:**
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

**Gotchas:**
- Missing responsive_image_style → No image rendered, blank output
- Using on small thumbnails → Overkill, generates many unnecessary derivatives
- Lazy loading on hero images → Delays LCP, poor performance scores
- `image_link: 'file'` links to fallback image style, not original

## Formatter Selection Decision

| If displaying... | Use formatter... | Why |
|---|---|---|
| Fixed-size thumbnail or UI element | `image` | Simple, predictable output, minimal overhead |
| Full-width content images | `responsive_image` | Bandwidth optimization, DPR support |
| Hero/banner images above fold | `responsive_image` with `image_loading: eager` | Performance, avoid LCP delay |
| Background images via CSS | `image_url` | Need URL string, not markup |
| Meta tags (og:image, twitter:image) | `image_url` | Need absolute URL for external services |
| User avatars | `image` | Consistent size, no responsive needed |
| Gallery/lightbox images | `image` with `image_link: file` | Link to full-size for lightbox JS |

## Common Mistakes

- Using `responsive_image` for all images → Over-engineering, storage bloat, processing overhead
- Lazy loading above-fold images → Poor LCP, failed Core Web Vitals
- `image_url` for visible images → No alt text, accessibility violation
- Not setting `image_style` on user-uploaded images → Serving multi-MB originals
- `image_link: 'file'` expecting original size → Gets derivative URL instead
- Using `eager` loading on below-fold images → Wastes bandwidth, delays critical resources

## See Also

- [Image System Overview](image-overview.md)
- [Best Practices & Patterns](best-practices.md) (lazy loading)
- Reference: core/modules/image/src/Plugin/Field/FieldFormatter/ImageFormatter.php
- Reference: core/modules/responsive_image/src/Plugin/Field/FieldFormatter/ResponsiveImageFormatter.php
