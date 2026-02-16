---
description: Smart cropping with Focal Point and Crop API — automatic focal-point-based cropping, manual crop per image style, and combined strategies.
---

## 16. Focal Point & Crop Integration

### When to Use

You need smart cropping where editors specify the important area of an image (face, product) that must stay visible across all crops.

### Decision

| Module | Use Case |
|---|---|
| Focal Point | Simple focal point selection (X/Y coordinates), automatic smart cropping |
| Crop API + Image Widget Crop | Manual crop per image style, multiple crops per image |
| Focal Point + Crop API | Combined: focal point for automatic, manual override per style |

### Pattern

**Focal Point setup**:

1. Install module: `composer require drupal/focal_point`
2. Enable: `drush en focal_point`
3. Configure image field to use Focal Point widget:

```yaml
# config/sync/core.entity_form_display.media.image.default.yml
content:
  field_media_image:
    type: image_focal_point
    weight: 0
    region: content
    settings:
      progress_indicator: throbber
      preview_image_style: thumbnail
      preview_link: true
      offsets: '50,50'
    third_party_settings: {}
```

4. Configure image styles to use Focal Point effects:

```yaml
# config/sync/image.style.hero_desktop_crop.yml
langcode: en
status: true
name: hero_desktop_crop
label: 'Hero Desktop (Cropped with Focal Point)'
effects:
  focal_point_scale_and_crop:
    uuid: unique-uuid-here
    id: focal_point_scale_and_crop
    weight: 0
    data:
      width: 1920
      height: 600
      crop_type: focal_point
```

**Crop API + Image Widget Crop setup**:

1. Install: `composer require drupal/crop drupal/image_widget_crop`
2. Enable: `drush en crop image_widget_crop`
3. Configure crop types:

```yaml
# config/sync/crop.type.hero_crop.yml
langcode: en
status: true
dependencies: {}
id: hero_crop
label: 'Hero Crop'
description: 'Crop for hero images'
aspect_ratio: '16:9'
soft_limit_width: 1920
soft_limit_height: 1080
hard_limit_width: 3840
hard_limit_height: 2160
```

4. Configure image field widget:

```yaml
# config/sync/core.entity_form_display.media.image.default.yml
content:
  field_media_image:
    type: image_widget_crop
    settings:
      crop_list:
        - hero_crop
        - card_crop
      crop_preview_image_style: thumbnail
      show_crop_area: true
```

5. Configure image styles to use crop effect:

```yaml
# config/sync/image.style.hero_desktop_manual_crop.yml
effects:
  crop_crop:
    uuid: unique-uuid-here
    id: crop_crop
    weight: 0
    data:
      crop_type: hero_crop
```

### Common Mistakes

- Not setting preview_link: true → editors can't test focal point before saving
- Using Focal Point without smart defaults → 50,50 center default often wrong; analyze image content
- Manual crop for every style → massive editorial burden; use focal point for automatic, manual only for art direction
- Not configuring aspect ratio constraints → crops produce unexpected dimensions
- Mixing crop approaches → using both manual crop and focal point on same style causes confusion; choose one strategy per style
- Not educating editors → focal point and manual crop require training; provide guidelines and examples

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md)
- Reference: https://www.drupal.org/project/focal_point
- Reference: https://www.drupal.org/project/crop
- Reference: https://www.drupal.org/project/image_widget_crop
