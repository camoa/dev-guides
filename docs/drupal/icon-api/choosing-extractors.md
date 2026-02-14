---
description: Select the appropriate extractor plugin for your icon source format and security requirements
drupal_version: "11.x"
---

# Choosing Extractors

## When to Use

You need to select the appropriate extractor plugin for your icon source format and security requirements.

## Decision

| If icons are... | Use extractor... | Provided by | Security | Performance |
|---|---|---|---|---|
| Individual SVG files (local) | `svg` | Core | High (sanitized) | Fast (cached) |
| SVG sprite file (local/remote) | `svg_sprite` | Core | Medium (sprite only) | Fastest (one file) |
| Any format, any source | `path` | Core | Low (no sanitization) | Varies (depends on source) |
| Icon font with codepoints | `font` | UI Icons contrib | High (local only) | Fast (CSS-rendered) |
| Iconify CDN | `iconify` | Iconify Icons contrib | Medium (remote) | Fast (CDN cached) |
| Custom source (API, database) | Custom extractor | Your module | Varies | Varies |

## Pattern

Choose based on icon count and source:

```yaml
# <10 icons, local SVGs
small_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg

# 50+ icons, one sprite file
large_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/all-icons.svg

# Remote CDN icons
cdn_pack:
  extractor: path
  config:
    sources:
      - https://cdn.example.com/icons/{icon_id}.svg

# Existing icon font
font_pack:
  extractor: font
  config:
    sources:
      - fonts/icons.woff2
  library: "my_theme/icon_font"
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/` for core extractors.

## Common Mistakes

- **Wrong**: Using `path` for local SVGs → **Right**: Use `svg` for sanitization and better DX
- **Wrong**: Using `svg` for sprites → **Right**: Use `svg_sprite` to avoid reading entire file per icon
- **Wrong**: Using `svg_sprite` for remote sprites with user input → **Right**: Validate URLs to prevent SSRF
- **Wrong**: Missing `library` for font extractors → **Right**: Font CSS won't load, icons appear as missing glyphs
- **Wrong**: Custom extractors without caching → **Right**: Implement `CacheableDependencyInterface` for performance

## See Also

- [Icon Pack Definition](icon-pack-definition.md)
- [SVG Extractor](svg-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorInterface.php`
