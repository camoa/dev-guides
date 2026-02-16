---
description: Media system best practices — naming conventions, view mode strategy, config management, Media Library optimization, security, and performance patterns.
---

## 18. Best Practices & Patterns

### Naming Conventions

**Media types**: lowercase, underscores, descriptive
- `image`, `document`, `remote_video`, `instagram`, `product_image`

**View modes**: lowercase, descriptive, context-specific
- `hero`, `card`, `thumbnail`, `embed`, `square`, `gallery_item`

**Responsive image styles**: match view mode names
- View mode: `hero` → Responsive style: `hero` → Image styles: `hero_mobile`, `hero_tablet`, `hero_desktop`

**Fields**: `field_media_[type]` for source fields
- `field_media_image`, `field_media_document`, `field_media_oembed_video`

**Fields**: `field_[context]` for entity reference fields on content
- `field_hero_image`, `field_gallery`, `field_featured_media`

### View Mode Strategy

**Create view modes per usage context, not per size**:
- `hero`, `card`, `embed` (context-driven)
- `small`, `medium`, `large` (size-driven; that's what responsive image styles do)

**Map one view mode to one responsive image style**:
- View mode `hero` → Responsive style `hero` → breakpoint-specific image styles
- View mode `card` → Responsive style `card` → breakpoint-specific image styles

**Minimum view modes for most sites**:
1. `default` (full content display, large)
2. `hero` (full-width hero sections)
3. `card` (card components in grids)
4. `thumbnail` (small previews)
5. `embed` (CKEditor embedded images)

### Configuration Management

**Export and commit all media config**:
```bash
drush config:export
git add config/sync/media.type.*
git add config/sync/core.entity_view_mode.media.*
git add config/sync/core.entity_view_display.media.*
git add config/sync/field.field.media.*
git commit -m "Add media configuration"
```

**Use Features or Config Split for media bundles**:
- Group all media configs for a feature (e.g., Instagram integration) into a Feature module
- Enables/disables as a unit

### Media Library Optimization

**Enable lazy loading by default**:
```yaml
# In all view displays:
settings:
  image_loading:
    attribute: lazy
```

**Set reasonable upload limits**:
```yaml
# In field config:
settings:
  max_filesize: '10 MB'
  max_resolution: '3840x3840'
  file_extensions: 'png gif jpg jpeg webp'
```

**Configure thumbnail style for Media Library**:
```yaml
# media_library view mode uses "medium" image style
# Adjust if needed for performance
```

### Security Patterns

**Require alt text**:
```yaml
settings:
  alt_field: true
  alt_field_required: true
```

**Whitelist file extensions**:
```yaml
settings:
  file_extensions: 'png gif jpg jpeg webp'  # Images
  # NOT: 'png gif jpg jpeg webp svg php js'
```

**Validate oEmbed providers**:
```yaml
source_configuration:
  providers:
    - YouTube
    - Vimeo
    # Don't allow arbitrary URLs
```

**Use private files for restricted documents**:
```yaml
settings:
  uri_scheme: private
```

### Performance Patterns

**Queue remote thumbnails**:
```yaml
queue_thumbnail_downloads: true
```

**Enable media entity caching**:
```yaml
# In core.entity_view_mode.media.[mode].yml
cache: true
```

**Use responsive images for contextual content images**:
- Use for hero, card, embed — any image that displays at different sizes across viewports
- Don't over-engineer: fixed-size UI elements (avatars, icons) only need a single image style

**Lazy load all images**:
- Except above-the-fold hero images (disable lazy loading for first hero)

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.drupal.org/docs/drupal-apis/configuration-api/managing-configuration-in-drupal
