---
description: Maximum flexibility for any image format from local or remote sources
drupal_version: "11.x"
---

# Path Extractor

## When to Use

> Use when you need maximum flexibility for any image format (SVG, PNG, WebP) from local or remote sources, and don't need content manipulation.

## Decision

| If icons are... | Pattern... | Security consideration |
|---|---|---|
| Local images (any format) | `images/{icon_id}.png` | Safe, no sanitization needed |
| CDN/remote URLs | `https://cdn.example.com/{icon_id}.svg` | Validate URL patterns, prevent SSRF |
| Mixed formats | Multiple source patterns | First matching file wins |
| User-uploaded | Never use path extractor | High XSS risk, use Media with sanitization |

## Pattern

Path extractor configuration:

```yaml
path_pack:
  extractor: path
  config:
    sources:
      - images/icons/{icon_id}.svg
      - images/icons/{icon_id}.png
      - https://cdn.example.com/icons/{icon_id}.svg
  template: >-
    <img src="{{ source }}"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         alt="{{ alt|default('') }}"
         class="icon icon-{{ icon_id|clean_class }}"
         loading="lazy">
```

The `{{ source }}` variable contains the full resolved path or URL to the icon file.

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/PathExtractor.php`

## Common Mistakes

- **Wrong**: Using for user-uploaded content → **Right**: High XSS risk, use Media field with validation
- **Wrong**: No lazy loading → **Right**: Add `loading="lazy"` for below-fold icons
- **Wrong**: Missing alt text for semantic icons → **Right**: Decorative icons use empty alt, semantic icons need descriptive alt
- **Wrong**: Hardcoded dimensions for responsive icons → **Right**: Use CSS or `srcset` for responsive images
- **Wrong**: Allowing arbitrary remote URLs → **Right**: Whitelist CDN domains to prevent SSRF attacks

## See Also

- [SVG Sprite Extractor](svg-sprite-extractor.md)
- [Font Extractor](font-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/PathExtractor.php`
