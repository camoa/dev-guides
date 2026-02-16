---
description: The key pattern connecting media view modes to responsive image delivery — breakpoints, image styles, responsive image styles, and the full delivery chain.
---

## 7. The Responsive Image Strategy

**THIS IS THE MOST IMPORTANT PATTERN IN THE GUIDE.**

### When to Use

You need to deliver optimized images across devices and screen densities. This pattern connects media display configuration to responsive image delivery.

### Decision

The responsive image delivery chain:

```
Media Type (Image)
  ↓
Media Entity (content with uploaded image)
  ↓
View Mode (hero, card, thumbnail, embed)
  ↓
Image Field Formatter = responsive_image
  ↓
Responsive Image Style (hero_style, card_style, etc.)
  ↓
Breakpoints (mobile, tablet, desktop)
  ↓
Image Styles per Breakpoint (hero_mobile, hero_tablet, hero_desktop)
  ↓
Image Derivatives (actual resized files)
  ↓
<picture> or <img srcset> in HTML
```

### Pattern

**Step 1: Define breakpoints in your theme** (see `drupal-image-styles.md` Section 6):
```yaml
# mytheme.breakpoints.yml
mytheme.mobile:
  label: Mobile
  mediaQuery: '(min-width: 0px)'
  weight: 0
  multipliers:
    - 1x
    - 2x
mytheme.tablet:
  label: Tablet
  mediaQuery: '(min-width: 768px)'
  weight: 1
  multipliers:
    - 1x
    - 2x
mytheme.desktop:
  label: Desktop
  mediaQuery: '(min-width: 1200px)'
  weight: 2
  multipliers:
    - 1x
    - 2x
```

**Step 2: Create image styles** (see `drupal-image-styles.md` Section 4):
```yaml
# config/sync/image.style.hero_mobile.yml
langcode: en
status: true
name: hero_mobile
label: 'Hero Mobile'
effects:
  scale:
    uuid: unique-uuid-here
    id: image_scale
    weight: 0
    data:
      width: 768
      height: null
      upscale: false

# config/sync/image.style.hero_tablet.yml
langcode: en
status: true
name: hero_tablet
label: 'Hero Tablet'
effects:
  scale:
    uuid: unique-uuid-here
    id: image_scale
    weight: 0
    data:
      width: 1200
      height: null
      upscale: false

# config/sync/image.style.hero_desktop.yml
langcode: en
status: true
name: hero_desktop
label: 'Hero Desktop'
effects:
  scale:
    uuid: unique-uuid-here
    id: image_scale
    weight: 0
    data:
      width: 1920
      height: null
      upscale: false
```

**Step 3: Create responsive image style** (see `drupal-image-styles.md` Section 5):
```yaml
# config/sync/responsive_image.style.hero.yml
langcode: en
status: true
dependencies:
  config:
    - image.style.hero_mobile
    - image.style.hero_tablet
    - image.style.hero_desktop
  theme:
    - mytheme
id: hero
label: Hero
image_style_mappings:
  - breakpoint_id: mytheme.mobile
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: hero_mobile
  - breakpoint_id: mytheme.mobile
    multiplier: 2x
    image_mapping_type: image_style
    image_mapping: hero_tablet
  - breakpoint_id: mytheme.tablet
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: hero_tablet
  - breakpoint_id: mytheme.tablet
    multiplier: 2x
    image_mapping_type: image_style
    image_mapping: hero_desktop
  - breakpoint_id: mytheme.desktop
    multiplier: 1x
    image_mapping_type: image_style
    image_mapping: hero_desktop
  - breakpoint_id: mytheme.desktop
    multiplier: 2x
    image_mapping_type: image_style
    image_mapping: hero_desktop
breakpoint_group: mytheme
fallback_image_style: hero_desktop
```

**Step 4: Create media view mode**:
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

**Step 5: Configure view display to use responsive image formatter**:
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

**Step 6: Use the view mode when placing media**:

In Layout Builder:
```yaml
# Block config references the view mode
settings:
  view_mode: hero
```

In entity reference field display:
```yaml
# config/sync/core.entity_view_display.node.article.default.yml
content:
  field_hero_image:
    type: entity_reference_entity_view
    settings:
      view_mode: hero
```

In Views:
```yaml
# In view display config
fields:
  rendered_entity:
    type: rendered_entity
    settings:
      view_mode: hero
```

In CKEditor embedding:
- Users select "Hero" view mode from dropdown when embedding

### Common Mistakes

- Using single image style for heroes and cards → no responsive delivery; use responsive_image formatter with view mode-specific styles
- Hardcoding image styles in templates → bypasses editorial control and responsive delivery; reference media with view mode
- Not creating enough breakpoints → coarse delivery (mobile/desktop only) wastes bandwidth; add tablet breakpoint minimum
- Using same responsive image style for all contexts → hero needs 1920px, card needs 600px; create multiple responsive image styles
- Forgetting 2x multiplier → retina displays get blurry images; define 2x mappings
- Not setting fallback_image_style → older browsers get no image; set to largest image style
- Bypassing view modes → rendering field_media_image directly loses formatter config; render full media entity with view mode

### See Also

- [Media View Modes](media-view-modes.md)
- [Media Display Configuration](media-display-config.md)
- `drupal-image-styles.md` Section 5: Responsive Image Style Config
- `drupal-image-styles.md` Section 6: Breakpoint Configuration
- Reference: `/core/modules/responsive_image/src/Plugin/Field/FieldFormatter/ResponsiveImageFormatter.php`
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/responsive-image-module
