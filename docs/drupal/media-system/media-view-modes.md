---
description: Creating media view modes for different display contexts — hero, card, thumbnail, embed — with view display configuration.
---

## 5. Media View Modes

### When to Use

You need different displays per usage context: hero images, cards, thumbnails, embedded in text.

### Decision

| View Mode | Use Case | Typical Image Style/Responsive Image Style |
|---|---|---|
| `default` | General purpose, full content display | `large` or responsive style |
| `media_library` | Media Library browser thumbnails | `medium` |
| `hero` (custom) | Full-width hero sections | Responsive style: 1920px-3840px widths |
| `card` (custom) | Card components in grids | Responsive style: 300px-800px widths |
| `thumbnail` (custom) | Small preview images | Single style: 150x150 |
| `embed` (custom) | CKEditor embedded images | Responsive style: 400px-1200px widths |
| `square` (custom) | Square aspect ratio for grids | Single style: 600x600 with focal point |

### Pattern

**Creating a custom view mode**:
```yaml
# config/sync/core.entity_view_mode.media.hero.yml
langcode: en
status: true
dependencies:
  module:
    - media
id: media.hero
label: Hero
description: 'Full-width hero images with responsive delivery.'
targetEntityType: media
cache: true
```

**View display configuration for the view mode**:
```yaml
# config/sync/core.entity_view_display.media.image.hero.yml
langcode: en
status: true
dependencies:
  config:
    - core.entity_view_mode.media.hero
    - field.field.media.image.field_media_image
    - media.type.image
    - responsive_image.style.hero
  module:
    - responsive_image
id: media.image.hero
targetEntityType: media
bundle: image
mode: hero
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
hidden:
  created: true
  thumbnail: true
  uid: true
  name: true
```

### Common Mistakes

- Using "default" for everything → loses context-specific control; create view modes per usage pattern
- Not hiding unused fields → shows metadata in output; set `hidden: true` for created, uid, name
- Forgetting to enable view mode → status: false makes it invisible in UI; set `status: true`
- Not using responsive_image formatter → uses single image style; lose multi-resolution delivery
- Inconsistent naming → use descriptive names matching usage: hero, card, thumbnail, embed, square

### See Also

- [Media Display Configuration](media-display-config.md)
- **[The Responsive Image Strategy](responsive-image-strategy.md)** (THE KEY CONNECTION)
- Reference: `/core/modules/media/config/install/core.entity_view_mode.media.full.yml`
