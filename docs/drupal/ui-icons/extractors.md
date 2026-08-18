---
description: "Choose between path, svg, svg_sprite, and font icon extractors based on how icons are stored."
tldr: "Use svg for individual SVG files needing inline content, svg_sprite for a single sprite sheet, path for URL-referenced files, and font (ui_icons_font) for TTF/WOFF packs. Only font ships from UI Icons; the other three live in Drupal core. Never print font content bare — it isn't a glyph."
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

`{group}` is **not** a template variable. The captured subdirectory is stored on the icon definition (`IconDefinition::getGroup()`) and used to group icons in pickers and in the Media source plugin; `Icon::preRenderIcon()` never puts it in the Twig context, so `{{ group }}` in a pack template is always empty.

## Pattern: `svg` extractor

```yaml
extractor: svg
config:
  sources:
    - icons/*.svg
```

Template variables: `{{ source }}` (file path), `{{ content }}` (parsed inner SVG markup), `{{ icon_id }}`, and `{{ attributes }}` — an `Attribute` object carrying **every attribute of the source file's root `<svg>` element**, `viewBox` included (`SvgExtractor::extractSvg()` copies them across). Core also injects an empty `Attribute` object when an extractor did not create one, so `{{ attributes }}` is safe in any pack template.

Take the `viewBox` from the source file instead of hardcoding one:

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="{{ attributes.viewBox|default('0 0 24 24') }}"
     width="{{ size|default(24) }}" height="{{ size|default(24) }}">
  {{ content|raw }}
</svg>
```

A literal `viewBox="0 0 24 24"` is correct only for a pack whose source files are all 24-unit — upstream's own test packs hardcode one because their fixtures are homogeneous. Most real packs are not: Bootstrap Icons ship `viewBox="0 0 16 16"`, so a hardcoded 24-unit box draws every icon at two-thirds scale in the corner of its frame.

Printing the whole object (`{{ attributes }}`) also works, but it re-emits whatever the source root carried — Bootstrap Icons files carry `width`, `height`, `fill` and `class` too, and a duplicated `width` beats your `size` setting because browsers honour the first occurrence. Strip them first if you go that route: `{{ attributes.removeAttribute('width', 'height', 'class') }}`.

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
  offset: 3                      # optional — drop the first N discovered icons
                                 # (TTF parsing usually leads with .notdef and friends)
```

Codepoints file:

```
arrow-left f101
menu f102
close f103
```

Template variables: `{{ icon_id }}`, plus `{{ content }}` **only for `.codepoints` sources** — and there `content` is the raw second column as text, not a glyph. `FontExtractor::getCodePoints()` stores `'content' => $values[1]` verbatim with no hex-to-character conversion, so for `arrow-left f101` the template prints the literal text `f101`. `.ttf`, `.woff`, `.json` and `.yml` sources store no `content` at all — those three `get*Icons()` methods return `$icons[$id] = []`. There is no `{{ source }}` on this extractor either: it calls `createIcon()` with an empty source, and core omits the variable when it is empty.

Never print `content` bare. Follow upstream's own font pack and fall back to the icon id, then let CSS supply the glyph:

```twig
<i class="icon icon-{{ icon_id|clean_class }}" style="font-size:{{ size|default(24) }}px">
  {{ content|default(icon_id)|spaceless }}
</i>
```

The glyph itself comes from the stylesheet, keyed off the same class:

```css
.icon-arrow-left::before { content: "\f101"; }
```

Pair the pack with a CSS library that defines `@font-face` for the font file, and wire it in with the pack's `library:` key ([Icon Pack Format](pack-format.md)) — declaring it in `{theme}.libraries.yml` alone attaches nothing.

## Common Mistakes

- **Wrong**: using `path` extractor when you need inline SVG manipulation → **Right**: `path` outputs `<img>` URLs; switch to `svg` for inline content
- **Wrong**: sprite sheet without `<symbol>` elements → **Right**: `svg_sprite` finds nothing; convert with svgo or sprite-builder tools
- **Wrong**: printing `{{ content }}` bare in a font template → **Right**: `.ttf`/`.woff`/`.json`/`.yml` sources never set it (empty `<i>`), and `.codepoints` sets it to the literal hex text (`f101` renders as the characters `f101`). Use `{{ content|default(icon_id) }}` and put the glyph in CSS
- **Wrong**: hardcoding `viewBox="0 0 24 24"` in an `svg` pack template → **Right**: wrong for any pack that isn't 24-unit. Read it from the source with `{{ attributes.viewBox }}`
- **Wrong**: font extractor with `.ttf` but no `dompdf/php-font-lib` → **Right**: the pack yields no icons and the status report warns "Missing Font library!" with the remedy `composer require dompdf/php-font-lib`. Check `/admin/reports/status` before assuming the YAML is wrong; or use `.codepoints` and skip the library

## See Also

- [Icon Pack Format](pack-format.md)
- [Settings & Rendering](settings-rendering.md)
- Reference: `core/lib/Drupal/Core/Theme/Plugin/IconExtractor/`
- Reference: `modules/ui_icons_font/src/Plugin/IconExtractor/FontExtractor.php`
