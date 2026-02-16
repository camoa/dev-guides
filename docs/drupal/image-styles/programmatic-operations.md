---
description: Load image styles, generate derivatives, flush caches, and create custom image effect plugins programmatically via PHP
---

# Programmatic Image Operations

## When to Use

> Use this when you need to load image styles, generate derivatives, flush caches, or create custom image effects programmatically.

## Steps - Loading and Using Image Styles

### 1. Load image style entity

```php
$image_style = \Drupal\image\Entity\ImageStyle::load('large');
```

### 2. Generate derivative URL

```php
$file_uri = 'public://images/example.jpg';
$derivative_url = $image_style->buildUrl($file_uri);
// Returns: /sites/default/files/styles/large/public/images/example.jpg?itok=abc123
```

### 3. Generate derivative file

```php
$derivative_uri = $image_style->buildUri($file_uri);
$success = $image_style->createDerivative($file_uri, $derivative_uri);
```

### 4. Flush derivatives

```php
// Flush all derivatives for a style
$image_style->flush();

// Flush derivative for specific source image
$image_style->flush('public://images/example.jpg');
```

## Steps - Creating Custom Image Effect Plugin

### 1. Create plugin class

At `src/Plugin/ImageEffect/CustomEffect.php`

```php
namespace Drupal\my_module\Plugin\ImageEffect;

use Drupal\Core\Image\ImageInterface;
use Drupal\image\ConfigurableImageEffectBase;
use Drupal\Core\Form\FormStateInterface;

#[ImageEffect(
  id: "custom_watermark",
  label: new TranslatableMarkup("Add Watermark"),
  description: new TranslatableMarkup("Adds a watermark to the image."),
)]
class WatermarkImageEffect extends ConfigurableImageEffectBase {

  public function applyEffect(ImageInterface $image) {
    // Apply watermark logic
    return TRUE;
  }

  public function defaultConfiguration() {
    return ['opacity' => 50];
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state) {
    $form['opacity'] = [
      '#type' => 'number',
      '#title' => $this->t('Opacity'),
      '#default_value' => $this->configuration['opacity'],
    ];
    return $form;
  }
}
```

### 2. Clear cache to discover new plugin

```bash
drush cr
```

## Steps - Programmatic Image Style Creation

**Avoid this.** Use config YAML instead. If absolutely necessary:

```php
use Drupal\image\Entity\ImageStyle;

$style = ImageStyle::create([
  'name' => 'custom_style',
  'label' => 'Custom Style (800x600)',
]);

$style->addImageEffect([
  'id' => 'image_scale',
  'data' => [
    'width' => 800,
    'height' => 600,
    'upscale' => FALSE,
  ],
  'weight' => 0,
]);

$style->save();
```

## Decision Points

| If you need... | Use... | Why |
|---|---|---|
| Generate derivative URL | `$style->buildUrl($uri)` | Includes security token, handles URL generation |
| Force derivative creation | `$style->createDerivative($source, $dest)` | Generates file immediately (normally lazy) |
| Add custom transformation | Custom ImageEffect plugin | Integrates with UI, exportable config |
| Batch regenerate derivatives | Flush then lazy regeneration | Let Drupal regenerate on demand, avoid memory issues |
| Complex image manipulation | Custom effect + image toolkit | Toolkit abstraction works with GD or ImageMagick |

## Common Mistakes

- Creating image styles programmatically instead of config → Not exportable, hard to maintain, breaks on config import
- Forgetting security token in derivative URLs → Image access denied if `allow_insecure_derivatives` is FALSE
- Calling `createDerivative()` in hot paths → Expensive operation, should be lazy/queued
- Not implementing `transformDimensions()` in custom effects → Responsive images can't calculate dimensions
- Using static service calls in plugins → Not testable, bypasses dependency injection
- Manually building derivative paths → Use `buildUri()`, manual paths break with scheme changes

## See Also

- [Creating Image Styles via Config](creating-styles-config.md) (preferred approach)
- [Security & Performance](security-performance.md) (derivative security)
- Reference: core/modules/image/src/Entity/ImageStyle.php
- Reference: core/modules/image/src/ImageEffectBase.php
