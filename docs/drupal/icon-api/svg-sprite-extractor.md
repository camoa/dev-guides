---
description: "svg_sprite reads symbol IDs from a local sprite only — a remote sprite source discovers zero icons, silently"
tldr: "You have a large local SVG sprite and want one cached request for every icon; remote sprites cannot work — IconFinder refuses any URI with a scheme, so a CDN sprite source discovers nothing."
drupal_version: "11.x"
---

# SVG Sprite Extractor

## When to Use

You have large icon sets (50+ icons) in a **local** SVG sprite file and want one cached request to serve every icon.

## Decision

| Sprite format... | Template pattern... | Why |
|---|---|---|
| Local sprite file | `<use href="{{ source }}#{{ icon_id }}"/>` | Standard SVG `<use>` reference — the only configuration that works |
| Remote sprite (CDN URL) | Not supported | The extractor must read the file to enumerate `<symbol id>` values, and `IconFinder::getFileContents()` refuses any URI with a scheme. Discovery returns zero icons, silently |
| Inline sprite | Embed sprite in page, use fragment ID | Zero HTTP requests, better for critical icons — outside Icon API |

Unlike the `svg` extractor, `svg_sprite` never reads SVG markup into the page ("no SVG is parsed or printed", `SvgSpriteExtractor.php:16-17`). There is no `{{ content }}` and no `{{ attributes }}` from this extractor — only `{{ icon_id }}`, `{{ source }}`, and your settings.

## Pattern

SVG sprite extractor configuration:

```yaml
sprite_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/icons.svg  # Local only. A URL here discovers nothing.
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

Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgSpriteExtractor.php`

## Common Mistakes

- Pointing `sources` at a CDN URL → Zero icons discovered, no error. Vendor the sprite into your extension
- Using `<svg>` instead of `<symbol>` in sprite → The extractor reads `$svg->symbol`, falling back to `$svg->defs->symbol`; both top-level and `<defs>`-wrapped symbols work, nothing else does
- Symbol IDs containing dots, colons, or spaces → `extractIdsFromSymbols()` rejects any ID matching `/[^\w-]/` and drops it silently; keep IDs to letters, digits, underscore and hyphen
- Missing `viewBox` on symbols → Each symbol needs `viewBox` for proper scaling; the sprite extractor exposes no `{{ attributes }}` to fall back on
- Not preloading critical sprite → Use `<link rel="preload" as="image" href="sprite.svg">` for above-fold icons

## See Also

- [SVG Extractor](svg-extractor.md)
- [Path Extractor](path-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgSpriteExtractor.php`
