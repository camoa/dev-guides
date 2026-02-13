---
description: Integrate existing icon fonts with Icon API and CSS-based rendering
drupal_version: "11.x"
---

# Font Extractor

## When to Use

> Use when you have existing icon fonts (TTF, WOFF, WOFF2) and want to integrate them with Icon API while leveraging CSS-based rendering.

## Decision

| If you need... | Configuration... | Why |
|---|---|---|
| Existing icon font | Font extractor + library | Reuse existing assets, CSS-controlled |
| New icon system | SVG extractor instead | Better accessibility, easier customization, no FOUT |
| Font with CSS classes | Map icon_id to CSS classes | Maintain compatibility with existing CSS |
| Web font from CDN | Include in library CSS | Standard font loading patterns |

## Pattern

Font extractor configuration:

```yaml
font_pack:
  extractor: font
  config:
    sources:
      - fonts/icon-font.woff2
      - fonts/icon-font.woff
      - fonts/icon-font.ttf
  library: "my_theme/icon_fonts"
  template: >-
    <i class="icon-font icon-{{ icon_id }}"
       style="font-size: {{ size|default(24) }}px; color: {{ color|default('currentColor') }};"
       aria-hidden="true">
    </i>
```

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

.icon-home::before { content: "\e900"; }
.icon-user::before { content: "\e901"; }
```

Reference: Font extractor requires UI Icons contrib module.

## Common Mistakes

- **Wrong**: Missing library attachment → **Right**: Icons render as text, font never loads
- **Wrong**: No `font-display: swap` → **Right**: FOUT (Flash of Unstyled Text) on slow connections
- **Wrong**: Using icon fonts for new projects → **Right**: SVG extractors offer better accessibility and performance
- **Wrong**: Inline styles instead of CSS classes → **Right**: Violates CSP, harder to maintain
- **Wrong**: Missing accessibility attributes → **Right**: Use `aria-hidden="true"` and provide text alternatives

## See Also

- [Path Extractor](path-extractor.md)
- [Template Variables](template-variables.md)
- Reference: [UI Icons module](https://www.drupal.org/project/ui_icons)
