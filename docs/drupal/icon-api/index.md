---
description: Icon API - unified system for managing and rendering icons across Drupal 11.1+ sites
guide-meta:
  concepts:
    - Icon API
    - icon packs
    - SVG extractor
    - SVG sprite extractor
    - font extractor
    - path extractor
    - Twig icon function
    - SDC icon props
    - IconPackManager
  not:
    - Font Awesome module
    - manual SVG include
    - CSS icon sprites
  requires:
    - drupal/sdc
  complements:
    - drupal/twig
    - drupal/ui-patterns
  specializes: ""
  category: drupal
---

# Icon API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the Icon API system | [What is Icon API](what-is-icon-api.md) | You need a unified, performant system for managing icons across your Drupal 11.1+ site rather than manually handling SVG files, icon fonts, or external resources in templates and CSS. Icon API provides the core infrastructure; the UI Icons… |
| Understand icon pack discovery and lifecycle | [Icon Pack Architecture](icon-pack-architecture.md) | You need to understand how icon packs are discovered, loaded, and rendered to design efficient icon systems or troubleshoot icon discovery issues. |
| Create a new icon pack in YAML | [Icon Pack Definition](icon-pack-definition.md) | You're creating a new icon pack in a theme or module and need the complete YAML structure with all required and optional properties. |
| Choose the right extractor for my icons | [Choosing Extractors](choosing-extractors.md) | You need to select the appropriate extractor plugin for your icon source format and security requirements. |
| Use individual SVG files | [SVG Extractor](svg-extractor.md) | You have individual SVG files stored locally in your theme or module and want automatic discovery, sanitization, and template rendering. |
| Use SVG sprite files for large icon sets | [SVG Sprite Extractor](svg-sprite-extractor.md) | You have large icon sets (50+ icons) in SVG sprite format and want optimal performance with single-file loading. |
| Use any image format or remote sources | [Path Extractor](path-extractor.md) | You need maximum flexibility for any image format (SVG, PNG, WebP) from local or remote sources, and don't need content manipulation. |
| Integrate existing icon fonts | [Font Extractor](font-extractor.md) | You have existing icon fonts (TTF, WOFF, WOFF2) with codepoint metadata files and want to integrate them with Icon API. The font extractor is provided by the **UI Icons** contrib module (not Drupal core). |
| Add icon fields, menu icons, or CKEditor integration | [UI Icons Module Features](ui-icons-module-features.md) | You need icon integration beyond rendering in templates: icon field types, menu icons, CKEditor embedding, or icon browsing UI for content editors. UI Icons is a contrib module that extends core Icon API functionality. |
| Understand template variables | [Template Variables](template-variables.md) | You're writing icon pack templates and need to understand available variables and how to use them effectively. |
| Render icons in Twig templates | [Twig Icon Function](twig-icon-function.md) | You need to render icons in Twig templates with type safety, caching, and settings support. |
| Build SDC components with icon props | [SDC Icon Props](sdc-icon-props.md) | You're building Single Directory Components that need configurable icons as props for reusable, flexible component APIs. |
| Use icon slots in components | [Icon Slots](icon-slots.md) | Your component needs maximum flexibility for icon content, including custom SVG, multiple icons, or complex icon compositions. |
| Access icons programmatically in PHP | [IconPackManager Service](iconpackmanager-service.md) | You need programmatic access to icon packs and icons in PHP (controllers, services, forms, preprocess) rather than templates. |
| Understand icon caching | [Caching Strategy](caching-strategy.md) | You need to understand Icon API caching behavior to optimize performance or troubleshoot cache-related issues. |
| Optimize icon performance | [Performance Best Practices](performance-best-practices.md) | You're optimizing icon rendering performance for large-scale sites with many icons or slow networks. |
| Handle SVG security and optimization | [SVG Security & Performance](svg-security-performance.md) | You're working with SVG icons and need to understand security implications and optimization techniques. |
| Secure remote icon sources | [Remote Resource Security](remote-resource-security.md) | You're loading icons from CDNs or external sources and need to understand SSRF, mixed content, and availability risks. |
| Debug icon discovery issues | [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md) | Icons aren't appearing, pack definitions aren't loading, or icon IDs aren't resolving correctly. |
| Debug template rendering issues | [Debugging Templates](debugging-templates.md) | Icons render incorrectly, template variables are missing, or SVG markup is malformed. |
| Migrate from existing icon systems | [Migration Patterns](migration-patterns.md) | You're migrating from manual icon management, icon fonts, or other icon systems to Icon API. |
| Build a custom extractor plugin | [Custom Extractor Development](custom-extractor-development.md) | Core extractors (SVG, SVG Sprite, Path, Font) don't support your icon source (API, database, generated icons, external service). |
