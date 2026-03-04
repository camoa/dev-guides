---
description: Map front-end image craft into Drupal's pipeline — responsive image styles, focal point, WebP/AVIF conversion, and media library guidance
drupal_version: "11.x"
---

# Drupal Media Pipeline

## When to Use

> Use responsive image styles (not image styles) for any image that appears at different sizes across breakpoints. Use focal point module on any editorial site where editors upload images at multiple aspect ratios. Add WebP conversion via core effect or ImageAPI Optimize AVIF & WebP module.

## Decision

| If you need... | Use... | Config location |
|---|---|---|
| Fixed-size image (avatar, thumbnail) | Image style | `image.style.{name}.yml` |
| Same image at multiple viewport sizes | Responsive image style | `responsive_image.styles.{name}.yml` |
| Different crops per breakpoint (art direction) | Responsive image style + `<picture>` mapping | Art direction type in style config |
| Format conversion (WebP, AVIF) | Core WebP effect OR ImageAPI Optimize pipeline | Image effect or pipeline on every style |
| Editorial photo in body content | Responsive image style via CKEditor | Media embed + responsive image formatter |

**What Drupal gives you out of the box (Drupal 10/11)**:

| Feature | Module | Status |
|---|---|---|
| Image styles (derivatives) | `image` (core) | Enabled by default |
| Responsive image styles | `responsive_image` (core) | Enable manually |
| WebP conversion effect | `image` (core) | Built-in effect in image styles |
| Media entity types | `media` (core) | Enable manually |
| Focal point cropping | `focal_point` (contrib) | Install separately |
| AVIF + WebP pipeline | `imageapi_optimize_avif_webp` (contrib) | Install separately |

## Pattern

**Responsive image style config** (mapping breakpoints to image styles):
```yaml
# config/sync/responsive_image.styles.card_image.yml
id: card_image
label: 'Card Image'
breakpoint_group: mytheme
fallback_image_style: card_medium
image_style_mappings:
  - breakpoint_id: mytheme.xs
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_small   # 400px wide
  - breakpoint_id: mytheme.md
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_medium  # 600px wide
  - breakpoint_id: mytheme.lg
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: card_large   # 500px wide (3-column grid)
```

**Focal point crop effect** in image style config:
```yaml
effects:
  uuid-1:
    id: focal_point_crop
    weight: 0
    data:
      width: 800
      height: 600
      crop_type: focal_point
```

**WebP options**:
- **Option 1 (core, Drupal 10.3+)**: Add `Convert to WebP` effect to each image style. Serves WebP when browser supports it via `Accept` header. No extra modules.
- **Option 2 (contrib, for AVIF)**: Install `imageapi_optimize` + `imageapi_optimize_avif_webp`. Create pipeline with AVIF (quality 68) and WebP (quality 82) processors. Requires PHP 8.1+ with ImageMagick with AVIF support.

**Breakpoint-to-image-style mapping workflow**:
1. Identify image contexts: hero (full-bleed), card grid (33–50% wide), sidebar (25% wide)
2. For each context, define image widths at each layout breakpoint
3. Create image styles for each distinct width across all contexts
4. Create a responsive image style per context, mapping breakpoints to image styles
5. Set `sizes` hints in responsive image style config

## Common Mistakes

- **Wrong**: using image styles for editorial content → **Right**: use responsive image styles; image styles generate one size only
- **Wrong**: editors uploading pre-resized originals → **Right**: Drupal generates derivatives from source; pre-resized uploads prevent proper responsive derivative generation. Set a minimum upload size requirement
- **Wrong**: missing `width`/`height` on responsive image template output → **Right**: Drupal 10.3+ outputs these by default; verify your template doesn't strip them
- **Wrong**: new image styles without WebP effect → **Right**: add the convert effect or attach an ImageAPI Optimize pipeline on every new style
- **Wrong**: focal point not planned for on existing uploads when installing the module → **Right**: existing images fall back to center crop; plan a content update workflow

## See Also

- `drupal-image-styles.md` — complete image style and responsive image style config reference
- `drupal-media.md` → `responsive-image-strategy` — connecting media view modes to responsive image styles
- `drupal-media.md` → `focal-point-crop-integration` — focal point module config details
- Reference: [Drupal Responsive Image module documentation](https://www.drupal.org/docs/core-modules-and-themes/core-modules/responsive-image-module)
- Reference: [ImageAPI Optimize AVIF & WebP on drupal.org](https://www.drupal.org/project/imageapi_optimize_avif_webp)
- Reference: [Focal Point module on drupal.org](https://www.drupal.org/project/focal_point)
