---
description: Extending core OEmbed source for custom providers and validation
drupal_version: "11.x"
---

# Extending OEmbed Sources

## When to Use

> Use OEmbed extension when service supports oEmbed protocol but needs custom URL validation, additional metadata extraction, or provider-specific handling.

## Decision

| Provider Type | Approach | Example |
|---------------|----------|---------|
| Standard oEmbed, no customization | Use core Remote video type | YouTube, Vimeo already work |
| oEmbed + custom URL patterns | Extend OEmbed, add validation regex | Instagram (multiple URL formats) |
| oEmbed + extra metadata | Extend OEmbed, override getMetadata() | Twitter (extract tweet ID) |
| oEmbed + custom display | Extend OEmbed, override prepareViewDisplay() | Custom embed formatter |

## Pattern

Extending OEmbed for custom provider (13 lines):
```php
use Drupal\media\Plugin\media\Source\OEmbed;
use Drupal\media\Attribute\OEmbedMediaSource;

#[OEmbedMediaSource(
  id: "oembed:tiktok",
  label: new TranslatableMarkup("TikTok"),
  allowed_field_types: ["string", "link"],
  providers: ["TikTok"],
  default_thumbnail_filename: "tiktok.png"
)]
class TikTok extends OEmbed {
  const PATTERN = '@tiktok\\.com/@[^/]+/video/(\\d+)@i';

  public function getMetadataAttributes(): array {
    return parent::getMetadataAttributes() + [
      'video_id' => $this->t('Video ID'),
    ];
  }

  public function getMetadata(MediaInterface $media, $attribute_name): mixed {
    if ($attribute_name === 'video_id') {
      $url = $this->getSourceFieldValue($media);
      return preg_match(static::PATTERN, $url, $m) ? $m[1] : NULL;
    }
    return parent::getMetadata($media, $attribute_name);
  }
}
```

## Common Mistakes

- **Wrong**: Not specifying `providers` array → **Right**: Match provider name in oEmbed registry
- **Wrong**: Weak regex patterns → **Right**: Strong regex with full URL structure validation
- **Wrong**: Not calling parent methods → **Right**: Call parent for core functionality
- **Wrong**: Hardcoding provider domain → **Right**: Use regex that handles URL variations

## See Also

- Previous: [Custom Media Source Plugin](custom-media-source-plugin.md)
- Next: [Metadata System](metadata-system.md)
- Reference: modules/contrib/media_entity_instagram/src/Plugin/media/Source/Instagram.php
