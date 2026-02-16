---
description: Integrating a third-party API or custom service that doesn't support oEmbed and no contrib module exists.
---

# Custom Media Source Plugin

### When to Use

Integrating a third-party API or custom service that doesn't support oEmbed and no contrib module exists.

### Decision

| Integration Type | Source Field Type | Metadata Strategy |
|------------------|-------------------|-------------------|
| REST/GraphQL API with URLs | `string` or `link` | Fetch on demand, cache responses |
| API with numeric IDs | `string` | Store ID, fetch metadata via API |
| Local files with custom processing | `file` | Extend File class, add processing |
| Hybrid (URL + credentials) | `link` + config form | Store URL in field, credentials in config |

### Pattern

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

### Common Mistakes

- Not implementing `default_name` → Media items show as "Unsaved media"
- Missing `thumbnail_uri` → Media Library shows broken thumbnails
- Not caching API responses → Performance issues, rate limit hits
- Using static service calls → Breaks testability, violates DI principles
- No error handling → Network failures crash pages

**WHY these matter:**
- **default_name**: Required for automatic naming when editors create media without manually entering a title
- **Caching**: API calls are expensive; without caching, every page load hits the API, causing slowness and rate limit issues
- **Error handling**: Third-party APIs fail; graceful degradation prevents white screens and improves user experience

### See Also

- Next: [Extending OEmbed Sources](index.md)
- Reference: core/modules/media/src/Plugin/media/Source/File.php
- Reference: https://drupalize.me/tutorial/create-custom-media-source-plugin