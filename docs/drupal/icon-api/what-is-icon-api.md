---
description: "Unified system for managing and rendering icons across Drupal 11.1+ sites; core classes remain experimental/internal"
tldr: "You need a unified, performant system for managing icons across Drupal 11.1+ rather than hand-rolling SVG, icon fonts, or external resources in templates and CSS; Icon API's PHP classes are marked experimental/internal, so treat *.icons.yml and icon() as the stable surface."
drupal_version: "11.x"
---

# What is Icon API

## When to Use

You need a unified, performant system for managing icons across your Drupal 11.1+ site rather than manually handling SVG files, icon fonts, or external resources in templates and CSS. Icon API provides the core infrastructure; the UI Icons contrib module adds field integration, widgets, and additional extractors.

**Stability caveat**: every class in `core/lib/Drupal/Core/Theme/Icon/` is marked `@internal … This API is experimental` — including `IconPackManager`, whose docblock adds "is not meant for production use" (`core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php:142-144`, still true in 11.3.11). The `*.icons.yml` format and the `icon()` Twig function are the stable-in-practice surface; the PHP classes can change in a patch release.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single SVG files in theme | SVG extractor (core) | Automatic discovery, template control, SVG markup inlined into the page |
| Large icon sets (50+ icons) | SVG sprite extractor (core) | Reads symbol IDs from one local sprite, renders `<use href>` |
| CDN/external icons | Path extractor (core) | Only extractor that works with remote URLs; local files limited to `.svg`, `.png`, `.gif` |
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

Use in templates with the `icon()` Twig function. It takes **three separate arguments** — pack, icon, settings — never a combined `pack:id` string:

```twig
{{ icon('my_theme', 'home', { size: 32, color: '#007bff' }) }}
```

**Core extractors** (Drupal 11.1+): `svg`, `svg_sprite`, `path`. **Contrib extractors**: `font` (UI Icons module) for icon fonts, `iconify` (Iconify Icons module) for Iconify CDN integration.

Reference: `/core/lib/Drupal/Core/Theme/Icon/` for API classes and interfaces; `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/` for the three core extractor plugins.

## Common Mistakes

- **Wrong**: Calling `icon('pack:id')` or `icon('pack:id', {…})` → **Right**: Fatal. `getIconRenderable(?string $pack_id, ?string $icon_id, ?array $settings = [])` has no default on `$icon_id`, and the file is `declare(strict_types=1)`; always pass three arguments
- **Wrong**: Manual SVG embedding in templates → **Right**: Use icon packs for discovery, caching, and a single place to change markup
- **Wrong**: Assuming the SVG extractor sanitizes → **Right**: It does not; it only refuses remote sources. Only ship SVG files you control
- **Wrong**: One pack per icon → **Right**: Group related icons in packs for performance, organization
- **Wrong**: Missing accessibility attributes → **Right**: Include `aria-hidden="true"` for decorative icons, `aria-label` for semantic

## See Also

- [Icon Pack Architecture](icon-pack-architecture.md)
- Reference: [Icon API documentation](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php`
