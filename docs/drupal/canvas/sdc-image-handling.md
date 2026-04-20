---
description: How to render image props correctly in Canvas SDC components using the canvas:image built-in component.
tldr: "Use this when your SDC component has an image prop (using `$ref: 'json-schema-definitions://canvas.module/image'`) and you need to render it correctly in the Twig template — with responsive images, lazy loading, performance attributes, and…"
drupal_version: "11.x"
---

# SDC Image Handling

## When to Use

> Use this when your SDC component has an image prop (using `$ref: 'json-schema-definitions://canvas.module/image'`) and you need to render it correctly in the Twig template — with responsive images, lazy loading, performance attributes, and proper alt text.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Above-the-fold / hero image (LCP candidate) | `loading: eager` + `fetchpriority: high` | Prioritizes the largest contentful paint |
| Below-the-fold images | `loading: lazy` (default) + `fetchpriority: auto` | Defers network requests until needed |
| Multiple images on a page | Only ONE with `fetchpriority: high` | Multiple high-priority images defeat the purpose |

## Pattern

Always use Canvas's built-in `canvas:image` component to render image props. Do not build your own `<img>` tag from the image prop object.

```twig
{# Recommended: include canvas:image for all image rendering #}
{% if image %}
  {% include 'canvas:image' with {
    image: image,
    loading: 'lazy',
    fetchpriority: 'auto',
  } only %}
{% endif %}

{# For above-the-fold / hero images: eager + high priority #}
{% if hero_image %}
  {% include 'canvas:image' with {
    image: hero_image,
    loading: 'eager',
    fetchpriority: 'high',
  } only %}
{% endif %}
```

**canvas:image parameters:**

| Parameter | Type | Default | Purpose |
|---|---|---|---|
| `image` | object | — | The image prop value from your component (required) |
| `loading` | string | `lazy` | `lazy` for below-fold; `eager` for above-fold |
| `fetchpriority` | string | `auto` | `high` for LCP candidate images; `auto` or `low` otherwise |
| `image_attributes` | Attribute object | — | Merge additional HTML attributes onto the `<img>` tag |

## Common Mistakes

- **Wrong**: `<img src="{{ image }}">` — the image prop is an object, not a URL string; this outputs nothing or breaks → **Right**: Use `canvas:image`
- **Wrong**: `<img src="{{ image.url }}">` — works but bypasses srcset, lazy loading, and responsive image styles → **Right**: Use `canvas:image`
- **Wrong**: Using `{% embed 'canvas:image' %}` → **Right**: Canvas:image must be included with `{% include ... only %}`, not embedded
- **Wrong**: Setting `fetchpriority: high` on every image → **Right**: Only the LCP image should have this; others get `auto`
- **Wrong**: Missing `{% if image %}` guard → **Right**: The prop can be empty if the editor hasn't uploaded an image yet

## See Also

- [SDC Props Reference](sdc-props-reference.md) for image prop definition
- Canvas SDC Images docs: https://project.pages.drupalcode.org/canvas/sdc-components/image/
- Canvas Code Component responsive images: https://project.pages.drupalcode.org/canvas/code-components/responsive-images/
- Dripyard article on handling images across Drupal and Canvas: https://dripyard.com/blog/handling-images-drupal-and-canvas-same-component
