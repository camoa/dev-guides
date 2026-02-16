---
description: When to use Drupal's Media subsystem vs direct file/image fields — architecture, decision criteria, and common mistakes.
---

## 1. Media System Overview

### When to Use

You're deciding whether to use the Media subsystem or direct file/image fields on your content types.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Reusable media across multiple content items | Media entity | Central repository, single update propagates everywhere |
| One-off file uploads unique to each node | Direct file/image field | Simpler, no media entity overhead |
| Centralized media management UI | Media entity | Media Library provides browse, search, bulk operations |
| Rich metadata (alt text, credits, licenses) | Media entity | Media types bundle multiple metadata fields |
| Different display modes per context (hero vs card) | Media entity | View modes control display per usage context |
| Remote videos (YouTube, Vimeo) | Media entity with Remote Video type | oEmbed integration, thumbnail fetching |
| Editorial workflow for media approval | Media entity | Leverage moderation workflows, revisions |
| Simple file download links | Direct file field | No display complexity, direct file URL |

### Pattern

**Media architecture**:
```
Media Type (bundle config) → defines source plugin and source field
  ↓
Media Entity (content) → references the actual file/video/embed via source field
  ↓
View Mode (display config) → controls how media renders per context
  ↓
Field Formatter (on source field) → renders image/video/embed
  ↓
Responsive Image Style (for images) → breakpoints and derivatives
```

### Common Mistakes

- Using media for every file → overhead for simple one-off uploads; use direct file fields when media isn't reused
- Not creating view modes → using "default" everywhere loses context-specific control
- Bypassing Media Library → building custom upload forms misses core functionality
- Direct file field references → creates tight coupling; media entity provides abstraction layer
- Hardcoding display in templates → breaks editorial control; use view modes and formatters

### See Also

- [Core Media Types](core-media-types.md)
- [The Responsive Image Strategy](responsive-image-strategy.md) (THE KEY PATTERN)
- Reference: `/core/modules/media/src/Entity/Media.php`
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/media-module
