---
description: Configuring media display formatters — responsive image, single image style, oEmbed video, file download, and thumbnail formatters.
---

## 6. Media Display Configuration

### When to Use

You need to configure how media renders: image formatters, video players, file download links.

### Decision

| Content to Display | Formatter | Settings |
|---|---|---|
| Responsive images | `responsive_image` | responsive_image_style, image_link, image_loading |
| Single image style | `image` | image_style, image_link, image_loading |
| oEmbed video player | `oembed` | max_width, max_height, loading.attribute |
| File download link | `file_default` | link text, new window |
| File with icon | `file_icon` | icon, file size, link text |
| Media thumbnail | `media_thumbnail` | image_style, image_link (uses media.thumbnail field) |

### Pattern

**Responsive image formatter** (PREFERRED for images):
```yaml
# In core.entity_view_display.media.image.hero.yml
content:
  field_media_image:
    type: responsive_image
    label: hidden
    settings:
      responsive_image_style: hero
      image_link: ''
      image_loading:
        attribute: lazy
    third_party_settings: {}
    weight: 1
    region: content
```

**Single image style formatter**:
```yaml
# In core.entity_view_display.media.image.thumbnail.yml
content:
  field_media_image:
    type: image
    label: hidden
    settings:
      image_style: thumbnail
      image_link: ''
      image_loading:
        attribute: lazy
    third_party_settings: {}
    weight: 1
    region: content
```

**oEmbed video formatter**:
```yaml
# In core.entity_view_display.media.remote_video.default.yml
content:
  field_media_oembed_video:
    type: oembed
    label: hidden
    settings:
      max_width: 0
      max_height: 0
      loading:
        attribute: lazy
    third_party_settings: {}
    weight: 1
    region: content
```

### Common Mistakes

- Using `image` formatter everywhere → loses responsive delivery; use `responsive_image` for hero, card, embed contexts
- Not setting `image_loading: attribute: lazy` → all images load immediately; enable lazy loading for performance
- Linking images to file URL (`image_link: file`) without reason → unexpected navigation; usually leave empty
- Showing label → clutters output; set `label: hidden` for clean display
- Wrong formatter for field type → `responsive_image` requires image field; `oembed` requires string field with URL

### See Also

- **[The Responsive Image Strategy](responsive-image-strategy.md)** (THE KEY PATTERN)
- Reference: `/core/modules/responsive_image/src/Plugin/Field/FieldFormatter/ResponsiveImageFormatter.php`
- Reference: `/core/modules/media/src/Plugin/Field/FieldFormatter/OEmbedFormatter.php`
