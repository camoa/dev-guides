---
description: Image & Media Craft — front-end pipeline decisions for responsive images, format strategy, loading optimization, placeholders, video, SVG, effects, and Drupal integration
tracks: []
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

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose `<picture>` vs `srcset` vs `sizes` for responsive images | [Responsive Images Craft](responsive-images-craft.md) | Use `srcset`+`sizes` on `<img>` when serving the same crop at different sizes. Use `<picture>` with `<source media>` when you need different crops or compositions per breakpoint (art direction). |
| Pick the right image format (JPEG, WebP, AVIF, PNG, SVG) | [Image Format Strategy](image-format-strategy.md) | Use this when deciding what format to produce and serve. Choosing the wrong format is the single biggest avoidable image performance mistake. |
| Set `loading`, `decoding`, `fetchpriority` correctly for LCP | [Loading and Decode Craft](loading-and-decode-craft.md) | Use `fetchpriority="high"` on the one LCP image. Use `loading="lazy"` + `decoding="async"` on all below-fold images. |
| Show a placeholder while images load (blur-up, LQIP, skeleton) | [Placeholder Strategies](placeholder-strategies.md) | Use `width`/`height` attributes on every image to prevent CLS — this is non-negotiable. Add LQIP blur-up for editorial photos where perceived performance matters. |
| Lazy-load YouTube/Vimeo, handle video autoplay policies | [Video and Embed Craft](video-and-embed-craft.md) | Use the facade pattern for YouTube/Vimeo embeds on any performance-sensitive page — it saves ~500KB initial load. Use `<video autoplay muted loop playsinline>` for decorative background video. |
| Decide inline SVG vs img vs CSS mask-image for icons | [SVG Craft](svg-craft.md) | Use `css mask-image` for single-color icon systems — it separates shape from color and works with dark mode. Use inline `<svg>` with `currentColor` for multi-color icons or when you need animation. |
| Apply object-fit, image reveal, before/after slider, lightbox | [Image Effects Craft](image-effects-craft.md) | Use `object-fit: cover` with an explicit container height for card and hero images. Use `transform: scale(1.05)` for hover zoom — keep scale under 1.06. |
| Set up Sharp, CDN transforms, compression budgets | [Build Pipeline Optimization](build-pipeline-optimization.md) | Use Sharp for any Node.js build pipeline — it is the default choice. Use CDN transforms (Cloudinary, imgix) for user-uploaded CMS media where image dimensions are unpredictable. |
| Map design breakpoints to Drupal responsive image styles | [Drupal Media Pipeline](drupal-media-pipeline.md) | Use responsive image styles (not image styles) for any image that appears at different sizes across breakpoints. Use focal point module on any editorial site where editors upload images at multiple aspect ratios. |
