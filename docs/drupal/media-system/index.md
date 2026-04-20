---
description: Drupal Media System configuration guides — media types, view modes, display configuration, Media Library, responsive image delivery, and file storage.
guide-meta:
  concepts:
    - Media Library
    - media view modes
    - media display configuration
    - responsive image strategy
    - CKEditor media embedding
    - media reference fields
    - focal point
    - media file system
  not:
    - custom media source plugins (see drupal/media)
    - image style effects (see drupal/image-styles)
  requires: []
  complements:
    - drupal/media
    - drupal/image-styles
    - drupal/entities
    - media/image-media-craft
  specializes: ""
  category: drupal
---

# Media System

**Philosophy**: Configuration-first approach to Drupal's media subsystem. This guide covers media types, view modes, display configuration, Media Library, and the critical strategy connecting media display to responsive image delivery. For custom media source plugin development, see `drupal_media_types_guide.md`. For image style and responsive image configuration, see `drupal-image-styles.md`.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand when to use Media vs direct file/image fields | [Media System Overview](media-overview.md) | You're deciding whether to use the Media subsystem or direct file/image fields on your content types. |
| Know what core media types provide | [Core Media Types](core-media-types.md) | You need to understand what core provides before creating custom media types. |
| Create a custom media type via config | [Custom Media Type Configuration](custom-media-type-config.md) | Core media types don't fit your needs — you need a custom media type for a specific use case. |
| Configure source field and metadata mapping | [Media Fields & Field Mapping](media-fields-field-mapping.md) | You need to understand how source fields store media and how metadata maps to media entity fields. |
| Create view modes for different contexts (hero, card, thumbnail) | [Media View Modes](media-view-modes.md) | You need different displays per usage context: hero images, cards, thumbnails, embedded in text. |
| Configure display formatters per view mode | [Media Display Configuration](media-display-config.md) | You need to configure how media renders: image formatters, video players, file download links. |
| **Connect media view modes to responsive images** | **[The Responsive Image Strategy](responsive-image-strategy.md)** | You need to deliver optimized images across devices and screen densities. This pattern connects media display configuration to responsive image delivery. |
| Configure media upload forms | [Media Form Display](media-form-display.md) | You need to configure the media upload and edit form: field order, widgets, help text. |
| Use Media Library widget in entity reference fields | [Media Library Widget](media-library-widget.md) | You need to add a media reference field to a content type with the Media Library browser. |
| Customize the Media Library view | [Media Library Views](media-library-views.md) | You need to customize the Media Library browser: filters, sort order, fields displayed. |
| Enable and configure CKEditor media embedding | [CKEditor Media Embedding](ckeditor-media-embedding.md) | You need to let editors embed media (images, videos) directly in WYSIWYG content. |
| Control media access and permissions | [Media Access & Permissions](media-access-permissions.md) | You need to control who can create, edit, delete, and view media. |
| Configure media reference fields | [Media Reference Fields](media-reference-fields.md) | You need to add media reference fields to content types, paragraphs, or other entities. |
| Place media in Layout Builder | [Media in Layout Builder](media-layout-builder.md) | You need to place media in Layout Builder sections using inline blocks or custom blocks. |
| Display media in Views | [Media in Views](media-views.md) | You need to display collections of media: galleries, media listings, search results. |
| Integrate focal point and crop for smart cropping | [Focal Point & Crop Integration](focal-point-crop-integration.md) | You need smart cropping where editors specify the important area of an image (face, product) that must stay visible across all crops. |
| Configure file storage for media | [Media File System](media-file-system.md) | You need to configure where media files are stored: public vs private, directory structure, CDN integration. |
| Follow naming and configuration best practices | [Best Practices & Patterns](best-practices-patterns.md) | Media system best practices — naming conventions, view mode strategy, config management, Media Library optimization, security, and performance patterns. |
| Avoid common mistakes and anti-patterns | [Anti-Patterns & Common Mistakes](anti-patterns-mistakes.md) | Media system anti-patterns — architecture, configuration, display, Media Library, access control, and file system mistakes to avoid. |
| Understand security and performance implications | [Security & Performance](security-performance.md) | Media system security and performance — file upload validation, access control, oEmbed security, CSP, image delivery optimization, caching, and CDN integration. |
| Find key classes, services, and files | [Code Reference Map](code-reference-map.md) |  |
