---
description: Image styles and responsive images — configuration-first approach to derivatives, effects, breakpoints, and modern format optimization.
guide-meta:
  concepts:
    - image styles
    - image effects
    - responsive image styles
    - breakpoint configuration
    - art direction
    - resolution switching
    - WebP
    - AVIF
    - image derivatives
  not:
    - Media Library (see drupal/media-system)
    - media source plugins (see drupal/media)
    - focal point cropping (see drupal/media-system)
  requires: []
  complements:
    - drupal/media-system
    - drupal/media
    - media/image-media-craft
  specializes: ""
  category: drupal
---

# Image Styles

**Philosophy**: Configuration over code. Image styles and responsive image styles are config entities defined via YAML. The preferred workflow is config management, export/import, and recipes.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand when to use image styles vs responsive images | [Image System Overview](image-overview.md) | Use image styles for fixed-size images. Use responsive image styles when you need different sizes for different devices/viewports. |
| Know the full YAML config schema for image styles | [Image Style Config Schema](image-style-schema.md) | Use this when you need to write or validate image.style.*.yml config files manually. |
| Configure resize, scale, crop, or conversion effects | [Core Image Effects](core-image-effects.md) | Use this when you need to configure specific image transformations in an image style. Drupal core provides 8 image effect plugins. |
| Create an image style via YAML config | [Creating Image Styles via Config](creating-styles-config.md) | Use this when you need to create an image style via YAML config for version control, recipes, or distribution. |
| Set up a responsive image style with breakpoints | [Responsive Image Style Config](responsive-image-config.md) | Use this when you need to configure a responsive image style that maps breakpoints to image styles for adaptive image delivery. |
| Define breakpoints in my theme | [Breakpoint Configuration](breakpoint-configuration.md) | Use this when you need to define breakpoints in your theme or module for responsive image style mappings. |
| Configure image field formatters | [Image Field Formatters](image-field-formatters.md) | Use this when you need to configure how image fields display in view modes. |
| Decide between art direction and resolution switching | [Art Direction vs Resolution Switching](art-direction-resolution.md) | Use this when you need to decide whether to use the sizes attribute (resolution switching) or distinct image styles per breakpoint (art direction). |
| Optimize images with WebP and AVIF | [WebP & AVIF Optimization](webp-avif-optimization.md) | Use this when you need to optimize image delivery with modern formats (WebP, AVIF) while maintaining fallback for older browsers. |
| Generate derivatives or create custom effects programmatically | [Programmatic Image Operations](programmatic-operations.md) | Use this when you need to load image styles, generate derivatives, flush caches, or create custom image effects programmatically. |
| Export image styles or create a recipe | [Config Export & Recipes](config-export-recipes.md) | Use this when you need to export image styles for version control or create a recipe to distribute image styles as reusable config. |
| Follow naming conventions and performance patterns | [Best Practices & Patterns](best-practices.md) | Use this when you need guidance on naming conventions, standard sizes, performance optimization, and lazy loading patterns. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns.md) | Use this when you need to understand what NOT to do and WHY to avoid costly mistakes. |
| Secure image derivatives and optimize performance | [Security & Performance](security-performance.md) | Use this when you need to secure image derivatives against attacks and optimize image delivery performance. |
| Find key classes and interfaces | [Code Reference Map](code-reference-map.md) |  |
| Check sources and version history | [Sources & Maintenance](sources-maintenance.md) |  |
