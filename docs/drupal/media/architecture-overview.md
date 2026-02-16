---
description: Understanding how media source plugins fit into Drupal's entity and plugin systems before implementing custom functionality.
---

# Architecture Overview

### When to Use

Understanding how media source plugins fit into Drupal's entity and plugin systems before implementing custom functionality.

### Decision

| Component | Purpose | Key File |
|-----------|---------|----------|
| **MediaSourceInterface** | Defines plugin contract (metadata, fields, validation) | core/modules/media/src/MediaSourceInterface.php |
| **MediaSourceBase** | Abstract implementation with DI, config, field management | core/modules/media/src/MediaSourceBase.php |
| **Plugin Attribute** | PHP 8 attribute defining plugin metadata | core/modules/media/src/Attribute/MediaSource.php |
| **Media Entity** | Content entity storing metadata and source field | core/modules/media/src/Entity/Media.php |
| **Media Type** | Bundle configuration linking to source plugin | core/modules/media/src/Entity/MediaType.php |

### Pattern

Class hierarchy and plugin structure:
```
MediaSourceInterface (contract)
  └── MediaSourceBase (abstract base)
        ├── File (local files)
        │     └── Image (extends File + dimensions)
        ├── OEmbed (oEmbed protocol)
        │     └── Instagram (extends OEmbed + shortcode)
        └── YourCustomSource (your implementation)

Plugin Discovery Flow:
1. Attribute scanned by MediaSourceManager
2. Plugin definition cached
3. Media type references plugin by ID
4. Plugin instantiated via create() factory
5. Services injected via constructor
```

### Common Mistakes

- Not implementing MediaSourceInterface contract → Missing required methods causes fatal errors
- Skipping plugin attribute → Plugin not discovered by manager
- Hardcoding service access → Use DI, not \Drupal::service() in plugins
- Misunderstanding field ownership → Media type owns fields, source defines requirements

### See Also

- Previous: [Base Class Selection](index.md)
- Next: [Custom Media Source Plugin](index.md)
- Reference: core/modules/media/src/MediaSourceInterface.php