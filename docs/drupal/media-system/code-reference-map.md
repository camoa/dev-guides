---
description: Code reference map for Drupal's media system — core modules, key classes, services, config schema, templates, JavaScript, and hooks.
---

## 21. Code Reference Map

### Core Modules

| Module | Path | Purpose |
|---|---|---|
| Media | `core/modules/media/` | Media entity, types, source plugins |
| Media Library | `core/modules/media_library/` | Media Library widget, browser UI |
| Responsive Image | `core/modules/responsive_image/` | Responsive image formatter, styles |
| Image | `core/modules/image/` | Image field, image styles, effects |
| File | `core/modules/file/` | File management, upload handling |

### Key Classes

**Media Entity**:
- `Drupal\media\Entity\Media` — Media entity class
- `Drupal\media\Entity\MediaType` — Media type config entity
- `Drupal\media\MediaInterface` — Media entity interface

**Media Sources**:
- `Drupal\media\MediaSourceInterface` — Media source plugin interface
- `Drupal\media\MediaSourceBase` — Base class for media sources
- `Drupal\media\Plugin\media\Source\Image` — Image source plugin
- `Drupal\media\Plugin\media\Source\File` — File source plugin
- `Drupal\media\Plugin\media\Source\OEmbed` — oEmbed source plugin

**Media Library**:
- `Drupal\media_library\Plugin\Field\FieldWidget\MediaLibraryWidget` — Media Library field widget
- `Drupal\media_library\MediaLibraryState` — Browser state management
- `Drupal\media_library\MediaLibraryUiBuilder` — Library UI builder

**Formatters**:
- `Drupal\responsive_image\Plugin\Field\FieldFormatter\ResponsiveImageFormatter` — Responsive image formatter
- `Drupal\image\Plugin\Field\FieldFormatter\ImageFormatter` — Single image style formatter
- `Drupal\media\Plugin\Field\FieldFormatter\OEmbedFormatter` — oEmbed video formatter

**Access Control**:
- `Drupal\media\MediaAccessControlHandler` — Media entity access checking

### Key Services

```php
// Media type storage
$media_type_storage = \Drupal::entityTypeManager()->getStorage('media_type');

// Media storage
$media_storage = \Drupal::entityTypeManager()->getStorage('media');

// Media source manager
$source_manager = \Drupal::service('plugin.manager.media.source');

// oEmbed resolver
$oembed_resolver = \Drupal::service('media.oembed.url_resolver');

// oEmbed provider repository
$provider_repository = \Drupal::service('media.oembed.provider_repository');

// Responsive image style storage
$responsive_style_storage = \Drupal::entityTypeManager()->getStorage('responsive_image_style');

// Image style storage
$image_style_storage = \Drupal::entityTypeManager()->getStorage('image_style');
```

### Config Schema

**Media type schema**: `core/modules/media/config/schema/media.schema.yml`

Key sections:
```yaml
media.type.*             # Media type config
media.settings           # Global media settings
media.source.*           # Source plugin schemas
field.formatter.settings.media_thumbnail
field.formatter.settings.oembed
```

**Media Library schema**: `core/modules/media_library/config/schema/media_library.schema.yml`

### Important Files

**Default configs**:
- `core/profiles/standard/config/optional/media.type.*.yml` — Core media types
- `core/modules/media_library/config/install/views.view.media_library.yml` — Media Library view
- `core/modules/media_library/config/install/core.entity_view_mode.media.media_library.yml` — Media Library view mode

**Templates**:
- `core/modules/media/templates/media.html.twig` — Media entity template
- `core/modules/media_library/templates/media-library-item.html.twig` — Library item template

**JavaScript**:
- `core/modules/media_library/js/media_library.widget.js` — Widget behavior
- `core/modules/ckeditor5/js/ckeditor5_plugins/drupalMedia/` — CKEditor5 media plugin

### Hooks

```php
// Alter media types
hook_media_source_info_alter(&$sources)

// Alter oEmbed resource URL
hook_oembed_resource_url_alter(array &$parsed_url, Provider $provider)

// Control media access
hook_media_access(\Drupal\media\MediaInterface $media, $operation, \Drupal\Core\Session\AccountInterface $account)

// Alter Media Library state
hook_media_library_widget_allowed_types_alter(array &$allowed_types, $form_state)
```

### See Also

- `drupal_media_types_guide.md` for custom source plugin development
- `drupal-image-styles.md` for image style and responsive image style details
- Reference: https://api.drupal.org/api/drupal/core!modules!media!media.api.php
- Reference: https://git.drupalcode.org/project/drupal/-/tree/11.x/core/modules/media
