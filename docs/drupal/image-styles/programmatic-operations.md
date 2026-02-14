---
description: Generate derivatives or create custom effects programmatically
drupal_version: "11.x"
---

# Programmatic Image Operations

## When to Use

> Use this when you need to load image styles, generate derivatives, flush caches, or create custom image effects programmatically. **Prefer YAML config for creating image styles.**

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Generate derivative URL | `$style->buildUrl($uri)` | Includes security token, handles URL generation |
| Force derivative creation | `$style->createDerivative($source, $dest)` | Generates file immediately (normally lazy) |
| Add custom transformation | Custom ImageEffect plugin | Integrates with UI, exportable config |
| Batch regenerate derivatives | Flush then lazy regeneration | Let Drupal regenerate on demand, avoid memory issues |
| Complex image manipulation | Custom effect + image toolkit | Toolkit abstraction works with GD or ImageMagick |

## Pattern - Loading and Using Image Styles

```php
// Load image style
$image_style = \Drupal\image\Entity\ImageStyle::load('large');

// Generate derivative URL
$file_uri = 'public://images/example.jpg';
$derivative_url = $image_style->buildUrl($file_uri);
// Returns: /sites/default/files/styles/large/public/images/example.jpg?itok=abc123

// Generate derivative file
$derivative_uri = $image_style->buildUri($file_uri);
$success = $image_style->createDerivative($file_uri, $derivative_uri);

// Flush derivatives
$image_style->flush();  // All derivatives for this style
$image_style->flush('public://images/example.jpg');  // Specific source
```

## Pattern - Custom Image Effect Plugin

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

Clear cache after creating plugin: `drush cr`

## Common Mistakes

- **Wrong**: Creating image styles programmatically instead of config → **Right**: Use YAML config (not exportable, hard to maintain, breaks on config import)
- **Wrong**: Forgetting security token in derivative URLs → **Right**: Use `buildUrl()` (image access denied if `allow_insecure_derivatives` is FALSE)
- **Wrong**: Calling `createDerivative()` in hot paths → **Right**: Use lazy generation or queue (expensive operation, should be lazy/queued)
- **Wrong**: Not implementing `transformDimensions()` in custom effects → **Right**: Implement for responsive image support (responsive images can't calculate dimensions)
- **Wrong**: Manually building derivative paths → **Right**: Use `buildUri()` (manual paths break with scheme changes)

## See Also

- [Creating Image Styles via Config](creating-styles-config.md) (preferred approach)
- [Security & Performance](security-performance.md)
- Reference: core/modules/image/src/Entity/ImageStyle.php
- Reference: core/modules/image/src/ImageEffectBase.php
