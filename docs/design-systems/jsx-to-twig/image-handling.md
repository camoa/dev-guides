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
| `<img loading="lazy">` | No action needed — Drupal image formatters add `loading="lazy"` automatically | Drupal injects the attribute via formatter; no Twig workaround required |
| `<figure><img><figcaption>` | `{{ include('ui_suite_daisyui:figure', ..., with_context: false) }}` | DaisyUI `figure` component handles semantic figure/figcaption structure |
| `<img className="rounded-full w-12 h-12">` (avatar) | `{{ include('ui_suite_daisyui:avatar', ..., with_context: false) }}` | DaisyUI `avatar` component — use component rather than Tailwind class workaround |
| `<img src="illustration.svg">` (SVG asset) | `{% include '@my_theme/icons/name.svg' %}` or `{{ drupal_icon('name') }}` | Twig include preserves SVG as code (styleable via CSS); file field serves it as binary |
| `<img className="w-48 h-32">` (Tailwind sizing) | Configure an image style with specific dimensions; use `{{ content.field_image }}` with that formatter | Twig width/height attributes don't resize the actual file — server-side image styles do |

### Pattern

**Preferred — rendered field with formatters (cache-safe):**

```jsx
// JSX: field value from CMS query result
const { fieldImage } = node;
return <img src={fieldImage.url} alt={fieldImage.alt} srcSet={fieldImage.srcSet} />;
```
```twig
{# Renders with all formatters, srcset if Responsive Image style configured,
   and correct cache metadata. Always prefer this for display. #}
{{ content.field_image }}
```

**Responsive image via render array (in preprocess or template):**

```jsx
// JSX: Next.js Image with explicit style and dimensions
return (
  <Image
    src={src}
    alt={alt}
    width={800}
    height={500}
  />
);
```
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

```jsx
// JSX: simple img with explicit dimensions
return <img src={uri} alt={alt} width={width} height={height} />;
```
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

```jsx
// JSX: image from component props
const { heroImageUrl, heroImageAlt } = props;
return heroImageUrl ? <img src={heroImageUrl} alt={heroImageAlt} /> : null;
```
```twig
{# ONLY safe when hero_image_url was prepared in preprocess with cache bubbling.
   See: drupal/twig/accessing-field-values — Cache Invalidation Warning #}
{% if hero_image_url %}
  <img src="{{ hero_image_url }}" alt="{{ hero_image_alt }}">
{% endif %}
```

**SVG via Twig include:**

```jsx
// JSX: import SVG as a React component
import Logo from './icons/logo.svg';
import ArrowRight from './icons/arrow-right.svg';

return (
  <>
    <Logo />
    <ArrowRight aria-label="Next" />
  </>
);
```
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

- **Wrong**: Using Tailwind sizing classes on `<img>` (`w-48 h-32`) to control image dimensions → **Right**: Configure an image style for server-side resizing; Tailwind classes only control CSS layout, not the actual file size
- **Wrong**: Building raw `srcset` strings manually in Twig → **Right**: Configure a Responsive Image style and use `{{ content.field_image }}` — Drupal generates the `<picture>` / `srcset` HTML automatically
- **Wrong**: `<img src="{{ file_url(node.field_image.entity.fileUri) }}">` directly in Twig → **Right**: Use `{{ content.field_image }}` with a formatter, or build a `#theme: 'image'` render array in preprocess — direct field traversal in Twig skips cache tags
- **Wrong**: Translating Next.js `<Image loader={customLoader}>` to a Drupal equivalent → **Right**: No direct equivalent — Drupal image styles are configured in admin UI; custom CDN integration goes in a preprocess function or image style effect

## See Also

- [Conditional Rendering](conditional-rendering.md) — checking field emptiness before image output
- [Props to Twig Variables](props-to-twig.md) — passing image data as SDC props
- [Styling Translation](styling.md) — converting Tailwind classes to SDC SCSS
- [Image Styles](../../drupal/image-styles/index.md) — configuring responsive image styles server-side
- Reference: [Drupal Responsive Image — drupal.org](https://www.drupal.org/docs/8/mobile-guide/responsive-images-in-drupal-8)
- Reference: [Drupal twig/accessing-field-values](../../drupal/twig/accessing-field-values.md)
