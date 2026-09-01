---
description: Drupal Media Types — custom media source plugins, metadata systems, oEmbed extensions, and third-party service integrations.
guide-meta:
  concepts:
    - media source plugins
    - custom media types
    - oEmbed extensions
    - metadata attributes
    - field mapping
    - thumbnail generation
    - media validation
  not:
    - Media Library widget (see drupal/media-system)
    - media view modes (see drupal/media-system)
    - image styles (see drupal/image-styles)
  requires:
    - drupal/plugins
  complements:
    - drupal/media-system
    - drupal/image-styles
    - drupal/entities
  category: drupal
tracks:
  - project: drupal
    channel: stable
    declared: null
    verified: 2026-02-16
    note: core topic; states no version of its own and inherits the guides.yml core baseline
---

# Media Types

**Purpose**: Create custom media source plugins to integrate third-party services (APIs, platforms), extend oEmbed sources, manage metadata attributes, map fields, generate thumbnails, and configure display/form widgets.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide between core/contrib/custom media types | [Media Type Selection Strategy](media-type-selection-strategy.md) | Starting a media integration project and deciding whether to use core media types, contrib modules, or build a custom media source plugin. |
| Choose the right base class for a custom plugin | [Base Class Selection](base-class-selection.md) | Building a custom media source plugin and choosing which base class to extend (MediaSourceBase, File, or OEmbed). |
| Understand the media source architecture | [Architecture Overview](architecture-overview.md) | Understanding how media source plugins fit into Drupal's entity and plugin systems before implementing custom functionality. |
| Create a custom API integration plugin | [Custom Media Source Plugin](custom-media-source-plugin.md) | Integrating a third-party API or custom service that doesn't support oEmbed and no contrib module exists. |
| Extend oEmbed for Instagram/Twitter/TikTok | [Extending OEmbed Sources](extending-oembed-sources.md) | Service supports oEmbed protocol but needs custom URL validation, additional metadata extraction, or provider-specific handling. |
| Extract and provide metadata attributes | [Metadata System](metadata-system.md) | Defining what information a media source can provide and implementing the extraction logic. |
| Map metadata to entity fields | [Field Mapping](field-mapping.md) | Making metadata searchable, filterable in views, or editable by site builders through the field mapping UI. |
| Generate and cache thumbnails | [Thumbnail Generation](thumbnail-generation.md) | Providing thumbnails for Media Library display and media entity views. |
| Inject services (HTTP client, logger, cache) | [Dependency Injection](dependency-injection.md) | Media source plugin needs services like HTTP client, logger, cache, file system, or custom services. |
| Validate source field values | [Validation Constraints](validation-constraints.md) | Validating source field values before saving media entities (URL patterns, API connectivity, file types). |
| Configure display and form widgets | [Display Configuration](display-configuration.md) | Customizing how media source fields are displayed in views and edited in forms when media type is created. |
| Apply security best practices | [Security Best Practices](security-best-practices.md) | Every media source plugin must implement security measures to prevent common vulnerabilities. |
| Optimize performance and caching | [Performance Optimization](performance-optimization.md) | Media source plugin causes slow page loads, high API usage, or database performance issues. |
| Test media source plugins | [Testing Strategies](testing-strategies.md) | Ensuring media source plugin works correctly across different scenarios and preventing regressions. |
| Avoid common mistakes | [Anti-Patterns](anti-patterns.md) | Avoiding common mistakes that lead to maintenance problems, security issues, or performance degradation. |
