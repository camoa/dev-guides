---
description: Complete index of core classes, interfaces, plugins, forms, and config files for image styles and responsive images
---

# Code Reference Map

## When to Use

> Use this when you need to find the authoritative source code for image style and responsive image functionality.

## Core Entities

| Class | Path | Purpose |
|---|---|---|
| `ImageStyle` | core/modules/image/src/Entity/ImageStyle.php | Image style config entity |
| `ResponsiveImageStyle` | core/modules/responsive_image/src/Entity/ResponsiveImageStyle.php | Responsive image style config entity |

## Image Effect Plugins

| Plugin ID | Class Path | Purpose |
|---|---|---|
| `image_resize` | core/modules/image/src/Plugin/ImageEffect/ResizeImageEffect.php | Exact dimensions resize |
| `image_scale` | core/modules/image/src/Plugin/ImageEffect/ScaleImageEffect.php | Aspect-ratio preserving scale |
| `image_scale_and_crop` | core/modules/image/src/Plugin/ImageEffect/ScaleAndCropImageEffect.php | Scale then crop to exact size |
| `image_crop` | core/modules/image/src/Plugin/ImageEffect/CropImageEffect.php | Crop without scaling |
| `image_convert` | core/modules/image/src/Plugin/ImageEffect/ConvertImageEffect.php | Format conversion |
| `image_convert_avif` | core/modules/image/src/Plugin/ImageEffect/AvifImageEffect.php | AVIF conversion with fallback |
| `image_rotate` | core/modules/image/src/Plugin/ImageEffect/RotateImageEffect.php | Rotate by degrees |
| `image_desaturate` | core/modules/image/src/Plugin/ImageEffect/DesaturateImageEffect.php | Grayscale conversion |

## Base Classes & Interfaces

| Class | Path | Purpose |
|---|---|---|
| `ImageEffectInterface` | core/modules/image/src/ImageEffectInterface.php | Effect plugin interface |
| `ImageEffectBase` | core/modules/image/src/ImageEffectBase.php | Non-configurable effect base |
| `ConfigurableImageEffectBase` | core/modules/image/src/ConfigurableImageEffectBase.php | Configurable effect base |
| `ImageEffectPluginCollection` | core/modules/image/src/ImageEffectPluginCollection.php | Effect collection |
| `ImageEffectManager` | core/modules/image/src/ImageEffectManager.php | Effect plugin manager |

## Field Formatters

| Formatter ID | Class Path | Purpose |
|---|---|---|
| `image` | core/modules/image/src/Plugin/Field/FieldFormatter/ImageFormatter.php | Standard image formatter |
| `image_url` | core/modules/image/src/Plugin/Field/FieldFormatter/ImageUrlFormatter.php | URL-only formatter |
| `responsive_image` | core/modules/responsive_image/src/Plugin/Field/FieldFormatter/ResponsiveImageFormatter.php | Responsive image formatter |

## Forms & UI

| Class | Path | Purpose |
|---|---|---|
| `ImageStyleForm` | core/modules/image/src/Form/ImageStyleEditForm.php | Style edit form |
| `ImageStyleAddForm` | core/modules/image/src/Form/ImageStyleAddForm.php | Style add form |
| `ImageStyleDeleteForm` | core/modules/image/src/Form/ImageStyleDeleteForm.php | Style delete form |
| `ImageStyleFlushForm` | core/modules/image/src/Form/ImageStyleFlushForm.php | Derivative flush form |
| `ResponsiveImageStyleForm` | core/modules/responsive_image/src/ResponsiveImageStyleForm.php | Responsive style form |

## Storage & Manager

| Class | Path | Purpose |
|---|---|---|
| `ImageStyleStorage` | core/modules/image/src/ImageStyleStorage.php | Image style storage handler |
| `ImageToolkitManager` | core/lib/Drupal/Core/ImageToolkit/ImageToolkitManager.php | Toolkit plugin manager (GD, ImageMagick) |
| `ImageFactory` | core/lib/Drupal/Core/Image/ImageFactory.php | Image object factory |
| `BreakpointManager` | core/lib/Drupal/Core/Breakpoint/BreakpointManager.php | Breakpoint discovery/management |

## Config Schema

| File | Path | Purpose |
|---|---|---|
| `image.schema.yml` | core/modules/image/config/schema/image.schema.yml | Image style config schema |
| `responsive_image.schema.yml` | core/modules/responsive_image/config/schema/responsive_image.schema.yml | Responsive image config schema |

## Config Examples

| File | Path | Purpose |
|---|---|---|
| `image.style.thumbnail.yml` | core/modules/image/config/install/image.style.thumbnail.yml | Default thumbnail style |
| `image.style.medium.yml` | core/modules/image/config/install/image.style.medium.yml | Default medium style |
| `image.style.large.yml` | core/modules/image/config/install/image.style.large.yml | Default large style |
| `responsive_image.styles.wide.yml` | core/profiles/standard/config/optional/responsive_image.styles.wide.yml | Wide responsive style |
| `olivero.breakpoints.yml` | core/themes/olivero/olivero.breakpoints.yml | Olivero theme breakpoints |

## Recipe Examples

| File | Path | Purpose |
|---|---|---|
| `recipe.yml` | core/recipes/standard_responsive_images/recipe.yml | Responsive images recipe |

## See Also

- All previous sections reference these source files
- Reference: https://api.drupal.org/api/drupal/core!modules!image
- Reference: https://api.drupal.org/api/drupal/core!modules!responsive_image
