---
description: "Choose between path, svg, svg_sprite, and font icon extractors based on how icons are stored."
tldr: "Use svg for individual SVG files needing inline content, svg_sprite for a single sprite sheet, path for URL-referenced files, and font (ui_icons_font) for TTF/WOFF packs. Only font ships from UI Icons; the other three live in Drupal core."
drupal_version: "11.x"
---

# Extractors

## When to Use

> Picking the right extractor based on how your icons are stored.

## Decision

| Storage | Extractor | Provided by | Best for |
|---|---|---|---|
| Individual files (PNG/SVG/JPG/GIF) in directories | `path` | Drupal core | Mixed-format icons; URL-referenced icons |
| Individual SVG files, content inlined into output | `svg` | Drupal core | Most modern icon sets (Heroicons, Lucide, Tabler, etc.) |
| Single SVG sprite sheet with `<symbol>`s | `svg_sprite` | Drupal core | Hundreds of icons; one HTTP request |
| Web font (TTF/WOFF + codepoints/JSON/YAML metadata) | `font` | `ui_icons_font` submodule | FontAwesome, Material Symbols (font version), legacy IcoMoon packs |

Only `font` comes from UI Icons. The other three live in core at `core/lib/Drupal/Core/Theme/Plugin/IconExtractor/` and work whether or not UI Icons is installed.

## Pattern: `path` extractor

```yaml
extractor: path
config:
  sources:
    - icons/flat/*.png
    - icons/group/{group}/*.svg     # {group} captures subdirectory as metadata
    - icons/{icon_id}_outline.png   # {icon_id} parses filename pattern
```

Template variables: `{{ source }}` (full URL), `{{ icon_id }}`. Image format agnostic.

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

Icon IDs come from `<symbol id="...">`:

```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <defs>
    <symbol id="arrow-left" viewBox="0 0 24 24"><path d="..."/></symbol>
    <symbol id="menu" viewBox="0 0 24 24"><path d="..."/></symbol>
  </defs>
</svg>
```

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
    - fonts/icons.ttf            # parsed via dompdf/php-font-lib
    - fonts/icons.codepoints     # space-separated: "icon_name unicode"
    - fonts/icons.json           # keys = icon names
    - fonts/icons.yml            # keys = icon names
```

Codepoints file:

```
arrow-left f101
menu f102
close f103
```

Template variables: `{{ content }}` (Unicode character), `{{ icon_id }}`.

```twig
<i class="icon-{{ icon_id|clean_class }}" style="font-size:{{ size|default(24) }}px">
  {{ content|raw }}
</i>
```

Pair with a CSS library that defines `@font-face` for the font file (in `{theme}.libraries.yml`).

## Common Mistakes

- **Wrong**: using `path` extractor when you need inline SVG manipulation → **Right**: `path` outputs `<img>` URLs; switch to `svg` for inline content
- **Wrong**: sprite sheet without `<symbol>` elements → **Right**: `svg_sprite` finds nothing; convert with svgo or sprite-builder tools
- **Wrong**: font extractor with `.ttf` but no `dompdf/php-font-lib` → **Right**: the pack yields no icons and status report warns "Missing Font library!"; install the library or use `.codepoints` instead

## See Also

- [Icon Pack Format](pack-format.md)
- [Settings & Rendering](settings-rendering.md)
- Reference: `core/lib/Drupal/Core/Theme/Plugin/IconExtractor/`
