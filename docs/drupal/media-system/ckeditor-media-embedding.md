---
description: Enabling CKEditor media embedding — text format filters, CKEditor 5 toolbar config, view mode selection, and the drupal-media tag.
---

## 11. CKEditor Media Embedding

### When to Use

You need to let editors embed media (images, videos) directly in WYSIWYG content.

### Decision

| Embedding Method | Use Case |
|---|---|
| Media Library button in CKEditor | Drupal-native, view mode selection, reusable media |
| Image upload button | One-off images not in media library |
| oEmbed paste (Drupal 11+) | Paste YouTube/Vimeo URLs directly |

### Pattern

**Text format with media embedding**:
```yaml
# config/sync/filter.format.full_html.yml
langcode: en
status: true
dependencies:
  module:
    - media
name: 'Full HTML'
format: full_html
weight: 0
filters:
  filter_html:
    id: filter_html
    provider: filter
    status: false
    weight: -10
    settings:
      allowed_html: '<a href hreflang> <em> <strong> <cite> <blockquote cite> <code> <ul type> <ol start type> <li> <dl> <dt> <dd> <h2 id> <h3 id> <h4 id> <h5 id> <h6 id> <drupal-media data-entity-type data-entity-uuid data-view-mode data-align data-caption alt>'
  media_embed:
    id: media_embed
    provider: media
    status: true
    weight: 100
    settings:
      default_view_mode: default
      allowed_view_modes:
        default: default
        embed: embed
        hero: hero
        card: card
      allowed_media_types:
        image: image
        remote_video: remote_video
```

**CKEditor 5 configuration**:
```yaml
# config/sync/editor.editor.full_html.yml
langcode: en
status: true
dependencies:
  config:
    - filter.format.full_html
  module:
    - ckeditor5
    - media_library
format: full_html
editor: ckeditor5
settings:
  toolbar:
    items:
      - bold
      - italic
      - link
      - bulletedList
      - numberedList
      - drupalMediaLibrary
      - sourceEditing
  plugins:
    ckeditor5_sourceEditing:
      allowed_tags: []
    media_media:
      allow_view_mode_override: true
image_upload:
  status: false
```

**Drupal-media tag in content**:
```html
<drupal-media
  data-entity-type="media"
  data-entity-uuid="abc-123-uuid-here"
  data-view-mode="embed"
  data-align="center"
  data-caption="Photo caption here"
  alt="Alt text">
</drupal-media>
```

### Common Mistakes

- Not enabling `media_embed` filter → `<drupal-media>` tags render as HTML, not embedded media
- Allowing all view modes → "default" and "media_library" modes not suitable for embedding; limit to embed-specific modes
- Not setting `allowed_media_types` → editors can embed documents and audio in text; restrict to image and video
- Using `filter_html` without adding `<drupal-media>` to allowed tags → filter strips media embeds
- Not providing caption and alignment → poor editorial experience; allow `data-align` and `data-caption` attributes
- Forgetting alt text → accessibility failure; require alt attribute in filter settings

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md) (embedded images should use responsive styles)
- Reference: `/core/modules/ckeditor5/src/Plugin/CKEditor5Plugin/Media.php`
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/media-module/embedding-media
