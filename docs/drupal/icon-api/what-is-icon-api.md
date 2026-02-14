---
description: Unified system for managing and rendering icons across Drupal 11.1+ sites with support for SVG, sprites, fonts, and remote sources
drupal_version: "11.x"
---

# What is Icon API

## When to Use

You need a unified, performant system for managing icons across your Drupal 11.1+ site rather than manually handling SVG files, icon fonts, or external resources in templates and CSS. Icon API provides the core infrastructure; the UI Icons contrib module adds field integration, widgets, and additional extractors.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single SVG files in theme | SVG extractor (core) | Automatic discovery, template control, security sanitization |
| Large icon sets (50+ icons) | SVG sprite extractor (core) | One HTTP request, smaller payload, faster rendering |
| CDN/external icons | Path extractor (core) | Supports remote URLs, flexible formats (PNG, SVG, WebP) |
| Existing icon font | Font extractor (UI Icons contrib) | Leverages existing assets, codepoint metadata, CSS-controlled sizing/color |
| Field/menu/CKEditor integration | UI Icons module | Field widget, menu icon picker, WYSIWYG embedding |
| Programmatic icon access | IconPackManager service | Type-safe API, cache integration, plugin discovery |

## Pattern

Icon API provides plugin-based icon management through YAML definitions:

```yaml
# my_theme.icons.yml
my_icons:
  enabled: true
  label: "My Icons"
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg
  template: >-
    <svg width="{{ size|default(24) }}" height="{{ size|default(24) }}">
      {{ content }}
    </svg>
```

Use in templates with the `icon()` Twig function:

```twig
{{ icon('my_theme:home', { size: 32, color: '#007bff' }) }}
```

**Core extractors** (Drupal 11.1+): `svg`, `svg_sprite`, `path`. **Contrib extractors** (UI Icons module): `font` for icon fonts with codepoint metadata, `iconify` for Iconify CDN integration.

Reference: `/core/lib/Drupal/Core/Theme/Icon/` for API classes and interfaces.

## Common Mistakes

- **Wrong**: Manual SVG embedding in templates → **Right**: Use icon packs for discovery, caching, sanitization
- **Wrong**: Hardcoded icon paths in templates → **Right**: Use `icon()` function for flexibility, cache participation
- **Wrong**: One pack per icon → **Right**: Group related icons in packs for performance, organization
- **Wrong**: Missing accessibility attributes → **Right**: Include `aria-hidden="true"` for decorative icons, `aria-label` for semantic
- **Wrong**: Ignoring security on remote sources → **Right**: Use Path extractor with caution, validate URLs, prefer local sources

## See Also

- [Icon Pack Architecture](icon-pack-architecture.md)
- Reference: [Icon API documentation](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php`
