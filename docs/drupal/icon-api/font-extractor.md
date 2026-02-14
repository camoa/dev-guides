---
description: Integrate existing icon fonts with codepoint metadata files via UI Icons contrib module
drupal_version: "11.x"
---

# Font Extractor

## When to Use

You have existing icon fonts (TTF, WOFF, WOFF2) with codepoint metadata files and want to integrate them with Icon API. The font extractor is provided by the **UI Icons** contrib module (not Drupal core).

## Decision

| If you need... | Configuration... | Why |
|---|---|---|
| Existing icon font (Bootstrap Icons, FontAwesome) | Font extractor + codepoint file + library | Reuse existing assets, CSS-controlled |
| New icon system | SVG extractor instead | Better accessibility, easier customization, no FOUT, core feature |
| Font with CSS classes | Map icon_id to CSS classes via codepoint file | Maintain compatibility with existing CSS |
| Web font from CDN | Include in library CSS | Standard font loading patterns |

**Requirements**: UI Icons module (`composer require 'drupal/ui_icons:^1.1'`) for Drupal 11.1+.

## Pattern

Font extractor configuration (requires codepoint metadata file):

```yaml
# Example: Bootstrap Icons font pack
bootstrap_icons_font:
  extractor: font
  config:
    sources:
      - fonts/bootstrap-icons.woff2  # Font file
      - fonts/bootstrap-icons.json   # Codepoint metadata (JSON, YAML, or .txt format)
  library: "my_theme/bootstrap_icons"
  template: >-
    <i class="bi bi-{{ icon_id }}"
       style="font-size: {{ size|default(24) }}px; color: {{ color|default('currentColor') }};"
       aria-hidden="true">
    </i>
```

**Codepoint metadata file** (JSON example for `bootstrap-icons.json`):

```json
{
  "home": "f3db",
  "search": "f3e5",
  "user": "f4da"
}
```

The font extractor uses the `dompdf/php-font-lib` library to parse TTF/WOFF files and matches glyphs against codepoint metadata for proper icon naming.

Accompanying library definition (`my_theme.libraries.yml`):

```yaml
icon_fonts:
  css:
    theme:
      css/icon-font.css: {}
```

Icon font CSS (`css/icon-font.css`):

```css
@font-face {
  font-family: 'IconFont';
  src: url('../fonts/icon-font.woff2') format('woff2'),
       url('../fonts/icon-font.woff') format('woff');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.icon-font {
  font-family: 'IconFont', sans-serif;
  speak: never;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.bi-home::before { content: "\f3db"; }
.bi-search::before { content: "\f3e5"; }
```

Reference: Font extractor provided by UI Icons contrib module. Core Drupal does not include a font extractor.

## Common Mistakes

- **Wrong**: Missing library attachment → **Right**: Icons render as text, font never loads
- **Wrong**: No `font-display: swap` → **Right**: FOUT (Flash of Unstyled Text) on slow connections
- **Wrong**: Using icon fonts for new projects → **Right**: SVG extractors (core) offer better accessibility and performance
- **Wrong**: Missing codepoint metadata file → **Right**: Font extractor needs JSON/YAML/TXT file mapping icon IDs to Unicode codepoints
- **Wrong**: Trying to use font extractor without UI Icons module → **Right**: Not available in core, install `drupal/ui_icons`
- **Wrong**: Inline styles instead of CSS classes → **Right**: Violates CSP, harder to maintain
- **Wrong**: Missing accessibility attributes → **Right**: Use `aria-hidden="true"` and provide text alternatives

## See Also

- [Path Extractor](path-extractor.md)
- [UI Icons Module Features](ui-icons-module-features.md)
- Reference: [UI Icons module](https://www.drupal.org/project/ui_icons)
- Reference: [Font extractor issue #3466316](https://www.drupal.org/project/ui_icons/issues/3466316)
