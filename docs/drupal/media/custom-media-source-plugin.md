---
description: Creating custom media source plugins for third-party API integrations
drupal_version: "11.x"
---

# Custom Media Source Plugin

## When to Use

> Use custom MediaSourceBase plugin when integrating a third-party API or custom service that doesn't support oEmbed and no contrib module exists.

## Decision

| Integration Type | Source Field Type | Metadata Strategy |
|------------------|-------------------|-------------------|
| REST/GraphQL API with URLs | `string` or `link` | Fetch on demand, cache responses |
| API with numeric IDs | `string` | Store ID, fetch metadata via API |
| Local files with custom processing | `file` | Extend File class, add processing |
| Hybrid (URL + credentials) | `link` + config form | Store URL in field, credentials in config |

## Pattern

Complete custom source plugin (12-15 lines):
```php
namespace Drupal\yourmodule\Plugin\media\Source;

use Drupal\media\MediaSourceBase;
use Drupal\media\MediaInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\media\Attribute\MediaSource;

#[MediaSource(
  id: "custom_api",
  label: new TranslatableMarkup("Custom API Source"),
  allowed_field_types: ["string", "link"],
  default_thumbnail_filename: "custom-api.png"
)]
class CustomApi extends MediaSourceBase {
  public function getMetadataAttributes(): array {
    return [
      'title' => $this->t('Title'),
      'author' => $this->t('Author'),
      'duration' => $this->t('Duration'),
      'thumbnail_uri' => $this->t('Thumbnail URI'),
    ];
  }

  public function getMetadata(MediaInterface $media, $attribute_name): mixed {
    $value = $this->getSourceFieldValue($media);

    return match($attribute_name) {
      'default_name' => $this->fetchFromApi($value, 'title'),
      'thumbnail_uri' => $this->fetchFromApi($value, 'thumbnail_url'),
      'title', 'author', 'duration' => $this->fetchFromApi($value, $attribute_name),
      default => parent::getMetadata($media, $attribute_name),
    };
  }

  protected function fetchFromApi(string $id, string $field): mixed {
    // Implement API logic with caching
  }
}
```

## Common Mistakes

- **Wrong**: Not implementing `default_name` → **Right**: Return title/name for automatic naming
- **Wrong**: Missing `thumbnail_uri` → **Right**: Return URI or NULL for fallback icon
- **Wrong**: Not caching API responses → **Right**: Cache with tags, 1-hour TTL minimum
- **Wrong**: Using static service calls → **Right**: Inject services via constructor
- **Wrong**: No error handling → **Right**: Catch exceptions, return NULL gracefully

## See Also

- Next: [Extending OEmbed Sources](extending-oembed-sources.md)
- Reference: core/modules/media/src/Plugin/media/Source/File.php
- Reference: https://drupalize.me/tutorial/create-custom-media-source-plugin
