---
description: "How to render image props correctly in Canvas SDC components using the canvas:image built-in component — the real src-based signature, not an image object."
tldr: "Use this when your SDC component has an image prop and needs to render it via canvas:image. canvas:image takes `src` at the top level, not an `image` object — spread the prop with |merge or the strict-typed getWidth() throws a TypeError."
drupal_version: "11.x"
---

# SDC Image Handling

## When to Use

> Use this when your SDC component has an image prop (using `$ref: 'json-schema-definitions://canvas.module/image'`) and you need to render it in the Twig template correctly — with responsive images, lazy loading, performance attributes, and proper alt text.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Above-the-fold / hero image (LCP candidate) | `loading: 'eager'` + `attributes: create_attribute({fetchpriority: 'high'})` | Prioritizes the largest contentful paint |
| Below-the-fold images | `loading: 'lazy'` (the default) | Defers network requests until needed |
| Multiple images on a page | Only ONE with `fetchpriority: high` | Multiple high-priority images defeat the purpose |

## Pattern

Always use Canvas's built-in `canvas:image` component to render image props. Do not build your own `<img>` tag from the image prop object.

**The critical detail: `canvas:image` takes `src` at the top level, not an `image` object.** Its first line is `{% set width = width ?? src|getWidth %}`, and `getWidth()` is declared `public function getWidth(string $src)` in a `declare(strict_types=1)` file. Pass `{image: image}` and `src` is undefined, so `getWidth(null)` raises a `TypeError` — the component blows up at render and the editor gets a broken-component box.

So **spread** your image object into the include context:

```twig
{# The pattern Canvas's own components use.
   `image` is your $ref'd image prop; `sizes` and `loading` here are props of
   the *outer* component, so the editor can tune them per placement. #}
{% if image %}
  {% include 'canvas:image' with image|merge({
    loading,
    sizes,
    class: 'card__image',
    attributes: create_attribute({'data-testid': 'card-image'}),
  }|filter((value) => value is not null)) only %}
{% endif %}

{# For above-the-fold / hero images: eager. #}
{% if hero_image %}
  {% include 'canvas:image' with hero_image|merge({
    loading: 'eager',
    class: 'hero__image',
  }|filter((value) => value is not null)) only %}
{% endif %}
```

The `|filter((value) => value is not null)` is not decoration: it drops unset keys so `canvas:image`'s own `??` fallbacks can fire instead of receiving an explicit `null`.

**canvas:image parameters** (from `components/image/image.component.yml` and `image.twig`):

| Parameter | Type | Effective default | Purpose |
|---|---|---|---|
| `src` | string (`format: uri-reference`, `contentMediaType: image/*`) | — | **Required.** Relative/absolute URL, or a stream-wrapper URI (`public://…`) — `file_url()` resolves it |
| `alt` | string | none (attribute omitted) | Alt text |
| `width` | integer | derived from `src` via `\|getWidth` | Intrinsic width |
| `height` | integer | derived from `src` via `\|getHeight` | Intrinsic height |
| `sizes` | string | `auto 100vw` | `sizes` attribute, emitted only when a `srcset` was produced |
| `loading` | string, enum `lazy`/`eager` | `lazy` | `lazy` below-fold; `eager` above-fold |
| `class` | string | `image` | Class attribute. **Undeclared in the YAML but read by the Twig** — it works |
| `attributes` | Attribute | none | Extra attributes, rendered at the end of the tag. Also undeclared in the YAML but read by the Twig |

Notes on what is *not* there:

- **No `fetchpriority` parameter.** `image.twig` never reads it — put it in `attributes`: `attributes: create_attribute({fetchpriority: 'high'})`
- **No `image_attributes` parameter.** The key is `attributes`
- **`srcset` is computed, not passed.** `image.twig` derives it from `src|toSrcSet(width)`. There is no `srcset` prop and no `image.srcset` value

`canvas:image` is itself a worked example of the defaults rule: its YAML says `default: lazy` on `loading`, Canvas ignores that, and the `lazy` you actually get comes from `loading ?? 'lazy'` on the last line of `image.twig`.

## Common Mistakes

- **Wrong**: `{% include 'canvas:image' with {image: image} only %}` → **Right**: the killer mistake. `canvas:image` reads `src`, so this throws a `TypeError` under strict types. Spread with `image|merge({...})`
- **Wrong**: `<img src="{{ image }}">` → **Right**: the image prop is an object, not a URL string; this outputs nothing or breaks
- **Wrong**: `<img src="{{ image.url }}">` → **Right**: `image.url` does not exist — the key is `image.src`, and building your own tag still bypasses srcset and stream-wrapper URL resolution; use `canvas:image`
- **Wrong**: Passing `fetchpriority:` or `image_attributes:` → **Right**: neither is a `canvas:image` parameter; use `attributes: create_attribute({...})`
- **Wrong**: Using `{% embed 'canvas:image' %}` → **Right**: `canvas:image` must be included with `{% include ... only %}`, not embedded
- **Wrong**: Setting `fetchpriority="high"` on every image → **Right**: only the LCP image should have this
- **Wrong**: Missing `{% if image %}` guard → **Right**: the prop can be empty if the editor hasn't uploaded an image yet

## See Also

- [SDC Props Reference](sdc-props-reference.md) for image prop definition
- Canvas SDC Images docs: https://project.pages.drupalcode.org/canvas/sdc-components/image/
- Canvas Code Component responsive images: https://project.pages.drupalcode.org/canvas/code-components/responsive-images/
- Dripyard article on handling images across Drupal and Canvas: https://dripyard.com/blog/handling-images-drupal-and-canvas-same-component
