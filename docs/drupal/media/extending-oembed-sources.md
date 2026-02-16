---
description: Service supports oEmbed protocol but needs custom URL validation, additional metadata extraction, or provider-specific handling.
---

# Extending OEmbed Sources

### When to Use

Service supports oEmbed protocol but needs custom URL validation, additional metadata extraction, or provider-specific handling.

### Decision

| Provider Type | Approach | Example |
|---------------|----------|---------|
| Standard oEmbed, no customization | Use core Remote video type | YouTube, Vimeo already work |
| oEmbed + custom URL patterns | Extend OEmbed, add validation regex | Instagram (multiple URL formats) |
| oEmbed + extra metadata | Extend OEmbed, override getMetadata() | Twitter (extract tweet ID) |
| oEmbed + custom display | Extend OEmbed, override prepareViewDisplay() | Custom embed formatter |

### Pattern

Extending OEmbed for custom provider (13 lines):
```php
use Drupal\media\Plugin\media\Source\OEmbed;
use Drupal\media\Attribute\MediaSource;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[MediaSource(
  id: "oembed:tiktok",
  label: new TranslatableMarkup("TikTok"),
  allowed_field_types: ["string", "link"],
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

### Common Mistakes

- Not specifying `providers` array → oEmbed resolution fails for custom providers
- Weak regex patterns → Accepts invalid URLs, validation bypassed
- Not calling parent methods → Loses core oEmbed functionality (thumbnails, embed HTML)
- Hardcoding provider domain → Breaks when provider changes URLs

**WHY:**
- **providers array**: Core oEmbed system matches URLs against provider registry; without correct provider name, resolution fails silently
- **Strong regex**: URL validation is security-critical; weak patterns allow injection of unintended content
- **Parent methods**: Core OEmbed handles complex thumbnail downloading, caching, and HTML generation; reimplementing loses these features

### See Also

- Previous: [Custom Media Source Plugin](index.md)
- Next: [Metadata System](index.md)
- Reference: modules/contrib/media_entity_instagram/src/Plugin/media/Source/Instagram.php