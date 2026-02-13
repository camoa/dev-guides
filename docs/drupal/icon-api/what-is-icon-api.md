---
description: Unified icon management for Drupal 11+ with SVG, sprites, fonts, and remote sources
drupal_version: "11.x"
---

# What is Icon API

## When to Use

> Use Icon API when you need a unified, performant system for managing icons across your Drupal site rather than manually handling SVG files, icon fonts, or external resources in templates and CSS.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single SVG files in theme | SVG extractor | Automatic discovery, template control, security sanitization |
| Large icon sets (50+ icons) | SVG sprite extractor | One HTTP request, smaller payload, faster rendering |
| CDN/external icons | Path extractor | Supports remote URLs, flexible formats (PNG, SVG, WebP) |
| Existing icon font | Font extractor | Leverages existing assets, CSS-controlled sizing/color |
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
