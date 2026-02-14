---
description: Automatic discovery, sanitization, and template rendering for individual SVG files
drupal_version: "11.x"
---

# SVG Extractor

## When to Use

You have individual SVG files stored locally in your theme or module and want automatic discovery, sanitization, and template rendering.

## Decision

| If you need... | Configuration... | Why |
|---|---|---|
| One icon per file | `sources: [icons/{icon_id}.svg]` | Standard pattern, simple discovery |
| Multiple source patterns | Multiple source entries | Fallback paths, organized subdirectories |
| Nested directories | `icons/category/{icon_id}.svg` | Organized by category without multiple packs |
| File naming variations | `icons/{icon_id}-icon.svg` | Match existing file conventions |

## Pattern

Basic SVG extractor configuration:

```yaml
svg_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg
      - icons/special/{icon_id}-icon.svg  # Fallback pattern
  template: >-
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         fill="{{ color|default('currentColor') }}"
         aria-hidden="true"
         focusable="false">
      {{ content }}
    </svg>
```

The `{icon_id}` placeholder is replaced with the icon identifier. SVG content is extracted (without `<svg>` wrapper) and available as `{{ content }}` variable.

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/SvgExtractor.php`

## Common Mistakes

- **Wrong**: Including `<svg>` tag in source files → **Right**: Extractor strips outer `<svg>`, provide inner content only (paths, circles, etc.)
- **Wrong**: Hardcoded width/height in SVG source → **Right**: Use `viewBox` in source, control dimensions in template
- **Wrong**: Missing `xmlns` in template → **Right**: Include `xmlns="http://www.w3.org/2000/svg"` for proper rendering
- **Wrong**: Unsanitized user-generated SVGs → **Right**: SVG extractor sanitizes, but validate sources are trusted
- **Wrong**: No fallback for missing icons → **Right**: Define multiple source patterns for graceful degradation

## See Also

- [Choosing Extractors](choosing-extractors.md)
- [SVG Sprite Extractor](svg-sprite-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/SvgExtractor.php`
