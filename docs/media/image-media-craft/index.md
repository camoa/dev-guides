---
description: Image & Media Craft — front-end pipeline decisions for responsive images, format strategy, loading optimization, placeholders, video, SVG, effects, and Drupal integration
guide-meta:
  concepts:
    - responsive images HTML
    - srcset sizes
    - picture element
    - image format strategy
    - loading decoding fetchpriority
    - LQIP blur-up
    - video embed lazy loading
    - SVG inline vs img
    - object-fit
    - build pipeline optimization
  not:
    - Drupal image styles config (see drupal/image-styles)
    - Drupal Media Library (see drupal/media-system)
  requires: []
  complements:
    - drupal/image-styles
    - drupal/media-system
    - css/css-craft
  specializes: ""
  category: media
---

# Image & Media Craft

| I need to... | Guide |
|---|---|
| Choose `<picture>` vs `srcset` vs `sizes` for responsive images | [Responsive Images Craft](responsive-images-craft.md) |
| Pick the right image format (JPEG, WebP, AVIF, PNG, SVG) | [Image Format Strategy](image-format-strategy.md) |
| Set `loading`, `decoding`, `fetchpriority` correctly for LCP | [Loading and Decode Craft](loading-and-decode-craft.md) |
| Show a placeholder while images load (blur-up, LQIP, skeleton) | [Placeholder Strategies](placeholder-strategies.md) |
| Lazy-load YouTube/Vimeo, handle video autoplay policies | [Video and Embed Craft](video-and-embed-craft.md) |
| Decide inline SVG vs img vs CSS mask-image for icons | [SVG Craft](svg-craft.md) |
| Apply object-fit, image reveal, before/after slider, lightbox | [Image Effects Craft](image-effects-craft.md) |
| Set up Sharp, CDN transforms, compression budgets | [Build Pipeline Optimization](build-pipeline-optimization.md) |
| Map design breakpoints to Drupal responsive image styles | [Drupal Media Pipeline](drupal-media-pipeline.md) |
