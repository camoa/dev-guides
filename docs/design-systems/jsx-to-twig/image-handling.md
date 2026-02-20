---
description: Convert React image patterns (<img>, Next.js Image, picture/srcset, SVG) to Drupal Twig equivalents
drupal_version: "11.x"
---

## Image Handling

### When to Use
When converting React image components (`<img>`, Next.js `<Image>`, `<picture>` / srcset, CSS background-image, inline SVG) to Drupal Twig equivalents using managed media, image styles, and the Drupal file/media entity system.

### Decision

| React / JSX Pattern | Drupal / Twig Equivalent | Why |
|---|---|---|
| `<img src={src} alt={alt}>` (unmanaged) | `<img src="{{ uri }}" alt="{{ alt }}">` where `uri` from preprocess | Only for non-managed images; use preprocess to prepare URI |
| Next.js `<Image src={…} width height>` with CDN optimization | `{{ content.field_image }}` with Responsive Image style configured | Drupal generates srcset via breakpoint-aware image styles |
| `<picture>` / `srcset` | Responsive image style + `{{ content.field_image }}` formatter | Drupal builds `<picture>` / `srcset` HTML automatically |
| CSS `background-image: url(image.jpg)` | Inline style with preprocess-prepared `{{ bg_image_url }}` | Background images bypass render pipeline; prepare in preprocess |
| Inline `<svg>...</svg>` | `{% include '@my_theme/icons/name.svg' %}` or `{{ drupal_icon('name') }}` | SVG as Twig template include or Icon API |
| `<img>` with specific transform / crop | `{{ image_style_url('style_name', node.field_image.entity.fileUri) }}` | Drupal image styles handle server-side transforms |
| Image from media entity (media reference field) | `{{ content.field_media }}` with Image formatter | Media formatter traverses to file entity with correct cache tags |

### Pattern

**Preferred — rendered field with formatters (cache-safe):**
```twig
{# Renders with all formatters, srcset if Responsive Image style configured,
   and correct cache metadata. Always prefer this for display. #}
{{ content.field_image }}
```

**Responsive image via render array (in preprocess or template):**
```twig
{# When you need explicit control over the image style #}
{% set image = {
  '#theme': 'image_style',
  '#style_name': 'hero_large',
  '#uri': node.field_image.entity.fileUri,
  '#alt': node.field_image.alt,
} %}
{{ image }}
```

**The `theme: image` render array (used in UI Suite DaisyUI .story.yml stories):**
```twig
{# In Twig, build a theme image render array for slots that expect an image #}
{% set image = {
  '#theme': 'image',
  '#uri': image_uri,
  '#alt': alt_text,
  '#width': width,
  '#height': height,
} %}
{{ image }}
```
In `.story.yml`, the equivalent slot value is `theme: image` with `uri`, `alt`, `width`, `height` keys.

**Raw URI access — only from preprocess-prepared variables:**
```twig
{# ONLY safe when hero_image_url was prepared in preprocess with cache bubbling.
   See: drupal/twig/accessing-field-values — Cache Invalidation Warning #}
{% if hero_image_url %}
  <img src="{{ hero_image_url }}" alt="{{ hero_image_alt }}">
{% endif %}
```

**SVG via Twig include:**
```twig
{# SVG as a Twig template — scoped to theme namespace #}
{% include '@my_theme/icons/logo.svg' %}

{# SVG via Icon API (drupal/icons module) #}
{{ drupal_icon('arrow-right') }}
```

### Cache Invalidation Warning

`{{ content.field_image }}` bubbles the file entity's cache tags automatically — pages invalidate when the image is replaced.

Accessing `node.field_image.entity.fileUri` directly in Twig **does not** bubble the file's cache tags. The page caches fine initially, then serves the stale image after the file is replaced. Move entity traversal to preprocess and call `$cache->addCacheableDependency($file)` for every file/media entity loaded.

See: [Accessing Field Values — Cache Invalidation Warning](../../drupal/twig/accessing-field-values.md) and [Entity Reference Traversal](../../drupal/twig/entity-reference-traversal.md).

### Common Mistakes

- **Wrong**: Using `node.field_image.entity.fileUri` directly as `src` in Twig → **Right**: Move to preprocess to avoid bypassing file cache tags
- **Wrong**: Forgetting `file_url()` wrapper around a URI → **Right**: Wrap raw URIs or you'll output `public://path/file.jpg` instead of a web URL
- **Wrong**: Applying Drupal image styles to SVG files → **Right**: Image styles only process raster formats; SVGs pass through unchanged but may error
- **Wrong**: Assuming Next.js `<Image>` lazy-resize-on-the-fly behavior exists in Drupal → **Right**: Configure image styles and responsive image styles upfront
- **Wrong**: Rendering media entity images with `node.field_media.entity.field_media_image.entity.fileUri` chain → **Right**: Use `{{ content.field_media }}` with the Image formatter instead

## See Also

- [Conditional Rendering](conditional-rendering.md) — checking field emptiness before image output
- [Props to Twig Variables](props-to-twig.md) — passing image data as SDC props
- Reference: [Drupal Responsive Image — drupal.org](https://www.drupal.org/docs/8/mobile-guide/responsive-images-in-drupal-8)
- Reference: [Drupal twig/accessing-field-values](../../drupal/twig/accessing-field-values.md)
