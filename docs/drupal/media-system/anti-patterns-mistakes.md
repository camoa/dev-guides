---
description: Media system anti-patterns — architecture, configuration, display, Media Library, access control, and file system mistakes to avoid.
---

## 19. Anti-Patterns & Common Mistakes

### Architecture Anti-Patterns

**Using "default" view mode for everything**
- **Why it's wrong**: Loses context-specific control. Hero images need different treatment than thumbnails.
- **Fix**: Create view modes per usage context (hero, card, thumbnail, embed).

**Direct file field references instead of media**
- **Why it's wrong**: Tight coupling, no reusability, no centralized management.
- **Fix**: Use media entities for reusable assets, direct fields only for one-off uploads.

**Creating custom media types for core use cases**
- **Why it's wrong**: Duplicates core functionality, maintenance burden, misses core updates.
- **Fix**: Use core Image, Document, Remote Video types. Only create custom for truly unique needs.

**Hardcoding image styles in templates**
- **Why it's wrong**: Bypasses editorial control, breaks responsive delivery, violates separation of concerns.
- **Fix**: Render media entities with view modes. Let display config control formatters.

### Configuration Anti-Patterns

**Not using responsive image formatter**
- **Why it's wrong**: Single image size for all devices wastes bandwidth on mobile, looks pixelated on retina.
- **Fix**: Use responsive_image formatter pointing to responsive image style.

**Single responsive image style for all contexts**
- **Why it's wrong**: Hero needs 1920px, card needs 600px. Using hero style for cards wastes bandwidth.
- **Fix**: Create responsive image styles per view mode context.

**Not setting alt_field_required**
- **Why it's wrong**: Accessibility failure, WCAG violation, SEO penalty.
- **Fix**: Set `alt_field: true` and `alt_field_required: true` on all image fields.

**Unlimited file uploads**
- **Why it's wrong**: Disk space exhaustion, memory issues, slow processing.
- **Fix**: Set `max_filesize: '10 MB'` and `max_resolution: '3840x3840'`.

**Not organizing uploads**
- **Why it's wrong**: Thousands of files in one directory causes filesystem performance issues.
- **Fix**: Use `file_directory: '[date:custom:Y]-[date:custom:m]'`.

### Display Anti-Patterns

**Using entity_reference_label formatter**
- **Why it's wrong**: Shows "Image: filename.jpg" as link instead of rendered image.
- **Fix**: Use `entity_reference_entity_view` formatter with view mode.

**Not hiding media metadata fields**
- **Why it's wrong**: Shows "Created: 2026-02-16, Author: admin" in display.
- **Fix**: Set `hidden: {created: true, uid: true, name: true}` in view display.

**Rendering field_media_image directly**
- **Why it's wrong**: Bypasses media view mode config, loses formatter settings.
- **Fix**: Render full media entity with view mode, not the image field.

**Not using lazy loading**
- **Why it's wrong**: All images load immediately, slows page load, wastes bandwidth.
- **Fix**: Set `image_loading: attribute: lazy` on all image formatters (except above-fold heroes).

### Media Library Anti-Patterns

**Custom upload forms instead of Media Library widget**
- **Why it's wrong**: Reinvents the wheel, misses core functionality, harder to maintain.
- **Fix**: Use `media_library_widget` on entity reference fields.

**Not filtering media types in widget**
- **Why it's wrong**: Shows all media types in browser (images, documents, videos mixed).
- **Fix**: Set `media_types: [image]` to limit to needed types.

**Modifying core media_library view**
- **Why it's wrong**: Lost on core updates.
- **Fix**: Export to config/sync or create view override via config rewrite.

### Access Control Anti-Patterns

**Granting "administer media" to content editors**
- **Why it's wrong**: Too broad; allows field config changes, media type creation.
- **Fix**: Use type-specific permissions: `create image media`, `edit own image media`.

**Not granting "view media" to authenticated users**
- **Why it's wrong**: Media doesn't display for logged-in users.
- **Fix**: Grant `view media` to authenticated role minimum.

**Exposing unpublished media in listings**
- **Why it's wrong**: Shows draft media to public.
- **Fix**: Add status filter: `value: '1'` to views and queries.

### File System Anti-Patterns

**Using private:// for public images**
- **Why it's wrong**: Breaks image styles, CDN delivery, performance overhead.
- **Fix**: Use public:// for site images, private:// only for access-controlled documents.

**Allowing all file extensions**
- **Why it's wrong**: Security risk (PHP, JS upload), server execution.
- **Fix**: Whitelist: `file_extensions: 'png gif jpg jpeg webp'`.

**Hardcoding file paths**
- **Why it's wrong**: Breaks portability, violates Drupal patterns.
- **Fix**: Use stream wrappers: `public://`, `private://`.

### See Also

- [Best Practices & Patterns](best-practices-patterns.md)
- [Security & Performance](security-performance.md)
