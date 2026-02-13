---
description: Optimal performance for large icon sets with single-file SVG sprites
drupal_version: "11.x"
---

# SVG Sprite Extractor

## When to Use

> Use when you have large icon sets (50+ icons) in SVG sprite format and want optimal performance with single-file loading.

## Decision

| Sprite format... | Template pattern... | Why |
|---|---|---|
| Local sprite file | `<use href="{{ source }}#{{ icon_id }}"/>` | Standard SVG `<use>` reference |
| Remote sprite (trusted) | Same with remote URL | CDN delivery, shared across sites |
| Inline sprite | Embed sprite in page, use fragment ID | Zero HTTP requests, better for critical icons |

## Pattern

SVG sprite extractor configuration:

```yaml
sprite_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/icons.svg
      - https://cdn.example.com/sprites/icons.svg  # Remote allowed
  template: >-
    <svg width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         fill="{{ color|default('currentColor') }}"
         aria-hidden="true"
         focusable="false">
      <use href="{{ source }}#{{ icon_id }}"/>
    </svg>
```

Sprite file format (symbols with IDs matching icon_id):

```xml
<!-- sprites/icons.svg -->
<svg xmlns="http://www.w3.org/2000/svg">
  <symbol id="home" viewBox="0 0 24 24">
    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
  </symbol>
  <symbol id="user" viewBox="0 0 24 24">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
  </symbol>
</svg>
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/SvgSpriteExtractor.php`

## Common Mistakes

- **Wrong**: Using `<svg>` instead of `<symbol>` in sprite → **Right**: Sprite extractor looks for `<symbol>` elements
- **Wrong**: Mismatched IDs → **Right**: Symbol `id` must match `icon_id` used in templates
- **Wrong**: Missing `viewBox` on symbols → **Right**: Each symbol needs `viewBox` for proper scaling
- **Wrong**: Loading entire sprite per icon → **Right**: Browser caches sprite file, one HTTP request serves all icons
- **Wrong**: Not preloading critical sprite → **Right**: Use `<link rel="preload" as="image" href="sprite.svg">` for above-fold icons

## See Also

- [SVG Extractor](svg-extractor.md)
- [Path Extractor](path-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/SvgSpriteExtractor.php`
