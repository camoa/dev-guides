---
description: Choose the right UI Icons extractor (path, svg, svg_sprite, font) based on how icon assets are stored.
tldr: Use svg for individual SVG files with inline content, svg_sprite for a single sprite sheet, path for URL-referenced files (PNG/JPG/SVG), and font for TTF/WOFF packs. The sprite extractor requires symbols; the font extractor requires dompdf/php-font-lib for TTF or a metadata file (.codepoints/.json/.yml) as an alternative.
drupal_version: "11.x"
---

# Extractors

## When to Use

> Picking the right extractor based on how your icons are stored.

## Decision

| Storage | Extractor | Best for |
|---|---|---|
| Individual files (PNG/SVG/JPG/GIF) in directories | `path` | Mixed-format icons; URL-referenced icons |
| Individual SVG files, content inlined into output | `svg` | Most modern icon sets (Heroicons, Lucide, Tabler, etc.) |
| Single SVG sprite sheet with `<symbol>`s | `svg_sprite` | Hundreds of icons; one HTTP request |
| Web font (TTF/WOFF + codepoints/JSON/YAML metadata) | `font` | FontAwesome, Material Symbols, legacy IcoMoon packs |

## Pattern: `path` extractor

```yaml
extractor: path
config:
  sources:
    - icons/flat/*.png
    - icons/group/{group}/*.svg   # {group} captures subdirectory as metadata
    - icons/{icon_id}_outline.png # {icon_id} parses filename pattern
```

Template variables: `{{ source }}` (full URL), `{{ icon_id }}`. Format agnostic — outputs `<img>` URLs.

## Pattern: `svg` extractor

```yaml
extractor: svg
config:
  sources:
    - icons/*.svg
```

Template variables: `{{ source }}` (file path), `{{ content }}` (parsed inner SVG markup), `{{ icon_id }}`.

```twig
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
     width="{{ size|default(24) }}" height="{{ size|default(24) }}">
  {{ content|raw }}
</svg>
```

## Pattern: `svg_sprite` extractor

```yaml
extractor: svg_sprite
config:
  sources:
    - icons/sprite.svg
```

Sprite file must use `<symbol id="...">` elements. Template:

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     width="{{ size|default(24) }}" height="{{ size|default(24) }}">
  <use xlink:href="{{ source }}#{{ icon_id }}"/>
</svg>
```

## Pattern: `font` extractor

```yaml
extractor: font
config:
  sources:
    - fonts/icons.ttf        # requires dompdf/php-font-lib
    - fonts/icons.codepoints # space-separated: "icon_name unicode"
    - fonts/icons.json       # keys = icon names
    - fonts/icons.yml        # keys = icon names
```

Codepoints file format: `arrow-left f101` (one per line).

```twig
<i class="icon-{{ icon_id|clean_class }}" style="font-size:{{ size|default(24) }}px">
  {{ content|raw }}
</i>
```

Pair with a CSS library defining `@font-face` for the font file.

## Common Mistakes

- **Wrong**: using `path` extractor when you need inline SVG manipulation → **Right**: switch to `svg`; `path` outputs `<img>` URLs, not inline content
- **Wrong**: sprite sheet without `<symbol>` elements → **Right**: `svg_sprite` extractor finds nothing; convert to symbol form
- **Wrong**: font extractor with `.ttf` but no `dompdf/php-font-lib` → **Right**: use `.codepoints` metadata, or install the library

## See Also

- [Pack Format](pack-format.md)
- [Settings & Rendering](settings-rendering.md)
- [Pre-built Pack Catalog](pack-catalog.md)
