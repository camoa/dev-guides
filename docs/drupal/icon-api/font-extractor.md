---
description: "UI Icons contrib's font extractor maps by file extension — .woff2 is silently unsupported, and only .codepoints sources set {{ content }}"
tldr: "You have an icon font with codepoint metadata and want it in Icon API via the UI Icons contrib module; .woff2 sources are silently skipped, and {{ content }} exists only for .codepoints sources — guard it with |default(icon_id)."
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

**Requirements**: UI Icons module — `composer require 'drupal/ui_icons:^2.0'` (2.0.0, released 2026-08-03, requires core `^11.3 || ^12.0`; use `^1.1` on core 11.1/11.2). Then enable `ui_icons_font`, whose own `composer.json` pulls in `dompdf/php-font-lib`.

## Pattern

The extractor dispatches on the source file's **extension** (`FontExtractor::discoverIcons()`), and anything it does not recognise falls through `default: break` with no warning:

| Extension | How icon IDs are found | Sets `{{ content }}`? |
|---|---|---|
| `.ttf`, `.woff` | Glyph names from the font's `post` table via `FontLib\Font` | No |
| `.json` | Top-level object keys (values ignored) | No |
| `.yml`, `.yaml` | Top-level keys | No |
| `.codepoints` | First space-separated token per line | Yes — the second token, verbatim |
| **`.woff2`, anything else** | **Not handled — silently skipped** | — |

```yaml
# Example: Bootstrap Icons font pack
bootstrap_icons_font:
  extractor: font
  config:
    sources:
      # .woff2 is NOT a recognised extension. Point at .woff/.ttf, or skip the
      # font file entirely and let the metadata file supply the icon IDs.
      - fonts/bootstrap-icons.json
  library: "my_theme/bootstrap_icons"
  template: >-
    <i class="bi bi-{{ icon_id }}"
       style="font-size: {{ size|default(24) }}px; color: {{ color|default('currentColor') }};"
       aria-hidden="true">
    </i>
```

**Metadata file** (JSON example for `bootstrap-icons.json`):

```json
{
  "home": "f3db",
  "search": "f3e5",
  "user": "f4da"
}
```

Only the **keys** are read — `getJsonIcons()` calls `array_keys(json_decode(...))` and discards the codepoint values. They live in your CSS (`.bi-home::before { content: "\f3db"; }`), not in the icon pack.

`dompdf/php-font-lib` is used only on the `.ttf`/`.woff` branch, to read glyph names out of the font's `post` table. Nothing in the extractor cross-references a font file against a metadata file; each source contributes icon IDs independently and the results are merged, so listing both a `.woff` and a `.json` gives you the union of two ID lists, not a validated intersection.

Font icons carry **no `{{ source }}`** — `FontExtractor::loadIcon()` passes an empty string. `{{ content }}` exists only for `.codepoints` sources, and it is the raw second token from the line (`arrow-left f101` yields the *string* `"f101"`, not the glyph). Guard it: `{{ content|default(icon_id) }}`.

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

- Listing a `.woff2` source → Silently skipped; the pack ends up empty. Use `.woff`, `.ttf`, `.json`, `.yaml`, or `.codepoints`
- Missing `library:` in the pack → Icons render as empty `<i>` elements because the `@font-face` never loads. `library:` on the pack is what makes `preRenderIcon()` attach it; a `libraries.yml` entry alone does nothing
- No `font-display: swap` → FOUT (Flash of Unstyled Text) on slow connections
- Using icon fonts for new projects → SVG extractors (core) offer better accessibility and performance
- Printing bare `{{ content }}` in a font template → Only `.codepoints` sources set it, and then as literal hex text. Use `{{ content|default(icon_id) }}` or drop it and drive the glyph from CSS
- Trying to use font extractor without UI Icons module → Not available in core, install `drupal/ui_icons` and enable `ui_icons_font`
- Inline styles instead of CSS classes → Violates CSP, harder to maintain
- Missing accessibility attributes → Use `aria-hidden="true"` and provide text alternatives

## See Also

- [Path Extractor](path-extractor.md)
- [UI Icons Module Features](ui-icons-module-features.md)
- Reference: [UI Icons module](https://www.drupal.org/project/ui_icons)
- Reference: [Font extractor issue #3466316](https://www.drupal.org/project/ui_icons/issues/3466316)
