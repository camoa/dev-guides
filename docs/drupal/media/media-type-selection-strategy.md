---
description: Starting a media integration project and deciding whether to use core media types, contrib modules, or build a custom media source plugin.
---

# Media Type Selection Strategy

### When to Use

Starting a media integration project and deciding whether to use core media types, contrib modules, or build a custom media source plugin.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Local files (PDFs, docs, archives) | Core "File" media type | Built-in file handling, no code needed |
| Local images with dimensions | Core "Image" media type | Image metadata extraction, EXIF support |
| YouTube/Vimeo/standard oEmbed | Core "Remote video" type | Provider in oembed.com registry, auto-thumbnails |
| Instagram posts | Contrib media_entity_instagram | Facebook Graph API integration, proven solution |
| Twitter/X posts | Contrib media_entity_twitter | Twitter API v2 handling, active maintenance |
| Custom API (non-oEmbed) | Custom MediaSourceBase plugin | Full control, custom auth, specific metadata |
| oEmbed service (TikTok, Spotify) | Custom OEmbed extension | Leverage core oEmbed, add custom validation |

### Pattern

Decision tree flow:
```
Is it local files? → Use core File/Image/Audio/Video type
  └─ No
Is provider in https://oembed.com/providers.json? → Use core Remote video
  └─ No
Does contrib module exist and is maintained? → Use contrib
  └─ No
Does service support oEmbed? → Create custom OEmbed extension
  └─ No
Create custom MediaSourceBase plugin
```

### Common Mistakes

- Using custom plugin when core type sufficient → Adds unnecessary maintenance burden
- Not checking contrib first → Reinventing the wheel, missing community updates
- Extending wrong base class → File source for APIs, MediaSourceBase for local files
- Building oEmbed integration from scratch → Core provides OEmbed infrastructure for free

### See Also

- Next: [Base Class Selection](index.md)
- Reference: https://www.drupal.org/docs/8/core/modules/media/creating-and-configuring-media-types