---
description: Map front-end image craft into Drupal's pipeline — responsive image styles, focal point, WebP/AVIF conversion, and media library guidance
tldr: "Use responsive image styles (not image styles) for any image that appears at different sizes across breakpoints. Use focal point module on any editorial site where editors upload images at multiple aspect ratios."
drupal_version: "11.x"
---

# Drupal Media Pipeline

## When to Use

> Mapping the front-end image craft from this guide into Drupal's configuration layer. Start here when implementing responsive images, format conversion, or focal point in a Drupal project.

## What Drupal Gives You Out of the Box (Drupal 10/11)

| Feature | Module | Status |
|---|---|---|
| Image styles (derivatives) | `image` (core) | Enabled by default |
| Responsive image styles | `responsive_image` (core) | Enable manually |
| WebP conversion effect | `image` (core) | Built-in effect in image styles |
| Media entity types | `media` (core) | Enable manually |
| Media Library | `media_library` (core) | Enable manually |
| Focal point cropping | `focal_point` (contrib) | Install separately |
| AVIF + WebP pipeline | `imageapi_optimize_avif_webp` (contrib) | Install separately |

## Image Styles vs Responsive Image Styles Decision

| If you need... | Use... | Config location |
|---|---|---|
| Fixed-size image (avatar, thumbnail) | Image style | `image.style.{name}.yml` |
| Same image at multiple viewport sizes | Responsive image style | `responsive_image.styles.{name}.yml` |
| Different crops per breakpoint (art direction) | Responsive image style + `<picture>` mapping | Art direction type in style config |
| Format conversion (WebP, AVIF) | Image style effect OR ImageAPI Optimize pipeline | Image effect on every style |
| Editorial photo in body content | Responsive image style applied via CKEditor | Media embed + responsive image formatter |

For configuration details, see `drupal-image-styles.md`. For media entity setup, see `drupal-media.md`.

## Focal Point Module — Why It Matters

Without focal point, Drupal's scale-and-crop centers the crop region. For user-uploaded portraits, this frequently crops the subject's face. Focal point:

1. Adds a draggable focal point to image upload in Media Library
2. Stores the focal point as x/y percentages on the file entity
3. Focal point crop effect uses those coordinates when generating derivatives
4. CKEditor5 Focal Point module integrates it into embedded media

**When to use focal point**: Any site where editors upload images that will be displayed at multiple aspect ratios (hero, card, thumbnail). This is essentially every editorial site.

```yaml
# Image style using focal point crop instead of standard crop
effects:
  uuid-1:
    id: focal_point_crop
    weight: 0
    data:
      width: 800
      height: 600
      crop_type: focal_point
```

See `drupal-image-styles.md` → `core-image-effects` for the full effect configuration schema.

## Mapping Design Breakpoints to Responsive Image Styles

Design breakpoints (where layout changes) are not image breakpoints (where image file sizes change). The workflow:

1. **Identify image contexts**: Hero (full-bleed), card grid (33–50% wide), sidebar (25% wide), full content (content column width). When the source design system declares image use cases as named typed atoms (see [Atom Recognition → Media Atoms](../../design-systems/recognition/atom-recognition.md)), this step becomes a 1:1 read of those declarations rather than inference from page measurements — each declared atom (`name`, `aspectRatio`, `maxWidth`) maps to one Drupal responsive image style.
2. **For each context, define image widths at each layout breakpoint**: At 320px viewport, a card is 300px wide. At 768px, it's 360px. At 1280px, it's 390px.
3. **Create image styles** for each distinct width needed across all contexts
4. **Create a responsive image style** per context, mapping breakpoints to image styles
5. **Set `sizes` hints** in the responsive image style config to tell browsers the rendered width

```yaml
# config/sync/responsive_image.styles.card_image.yml
id: card_image
label: 'Card Image'
breakpoint_group: mytheme
fallback_image_style: card_medium
image_style_mappings:
  # Mobile: full-width card
  - breakpoint_id: mytheme.xs
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_small  # 400px wide
  # Tablet: 2-column grid
  - breakpoint_id: mytheme.md
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_medium  # 600px wide
  # Desktop: 3-column grid
  - breakpoint_id: mytheme.lg
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_large   # 500px wide (column is narrower at 3-up)
```

## WebP and AVIF in Drupal

**Option 1: Core WebP conversion** (Drupal 10.3+ core):
Add a `Convert to WebP` effect to each image style. Core serves WebP automatically when browser supports it (detected via `Accept` header). Simple; no additional modules needed.

**Option 2: ImageAPI Optimize AVIF & WebP** (contrib, for AVIF support):
Install `imageapi_optimize` + `imageapi_optimize_avif_webp`. Create a pipeline with both processors. Attach the pipeline to image styles. Generates `.avif` and `.webp` derivatives alongside the original derivative.

**Use Option 2 when AVIF savings matter** (editorial photo sites, high-traffic). The module requires PHP 8.1+ with `php-gd` or ImageMagick with AVIF support compiled in.

```
Pipeline: image_optimize_pipeline
  Processor 1: AVIF (quality 68)
  Processor 2: WebP (quality 82)
  Processor 3: [optional] jpegoptim or mozjpeg for JPEG fallback
```

## Media Library UX — What Editors Need

Editors using Media Library need to know:
- **Alt text is required** — enforce via field validation, not just guidance
- **Upload large originals** — Drupal generates derivatives; uploading a pre-cropped 400px image prevents proper responsive derivative generation
- **Focal point sets the crop anchor** — clicking in the focal point widget sets where crops are centered; default is center
- **Reusable media** — the same media entity can be referenced from multiple nodes; editing the media entity's alt text updates it everywhere

## Common Mistakes

- **Not using responsive image styles for editorial content** — image styles generate one size; responsive image styles let the browser pick the right one. For any image that appears at different sizes across breakpoints, use responsive image styles
- **Uploading pre-resized originals** — CMS image handling generates derivatives from the source; if editors upload 600px images, the "large" derivative cannot exceed 600px. Set a minimum upload size requirement
- **Missing `width` and `height` on responsive image template output** — Drupal's responsive image field formatter outputs `width` and `height` by default in Drupal 10.3+. Verify your template doesn't strip these
- **Image styles without WebP effect** — new image styles get no WebP conversion by default; add the convert effect or attach an ImageAPI Optimize pipeline
- **Focal point not set on existing uploads** — when installing focal point on a live site, existing images have no focal point data. Default behavior falls back to center crop. Plan a content update workflow

## See Also

- `drupal-image-styles.md` — complete image style and responsive image style config reference
- `drupal-media.md` → `responsive-image-strategy` — the connection between media view modes and responsive image styles
- `drupal-media.md` → `focal-point-crop-integration` — focal point module config details
- Reference: [Drupal Responsive Image module documentation](https://www.drupal.org/docs/core-modules-and-themes/core-modules/responsive-image-module)
- Reference: [ImageAPI Optimize AVIF & WebP on drupal.org](https://www.drupal.org/project/imageapi_optimize_avif_webp)
- Reference: [Focal Point module on drupal.org](https://www.drupal.org/project/focal_point)
