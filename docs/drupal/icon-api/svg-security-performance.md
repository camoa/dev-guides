---
description: SVG security implications and optimization techniques
drupal_version: "11.x"
---

# SVG Security & Performance

## When to Use

> Use when you're working with SVG icons and need to understand security implications and optimization techniques.

## Decision

| Risk level | Source | Mitigation |
|---|---|---|
| Low | Local SVG files (theme/module) | SVG extractor sanitizes automatically |
| Medium | Sprite files (local) | Sprite extractor validates structure |
| High | Remote SVG URLs | Never use SVG extractor, use Path with CSP |
| Critical | User-uploaded SVG | Never use Icon API, use Media with validation |

## Pattern

Secure SVG handling:

```yaml
# ✅ Safe - Local SVG files
safe_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg  # Local only, sanitized by extractor

# ⚠️ Caution - Remote sprites (sprite extractor allows)
remote_sprite:
  extractor: svg_sprite
  config:
    sources:
      - https://trusted-cdn.example.com/sprite.svg  # Validate domain

# ❌ Never - User-uploaded SVG via Icon API
# Use Media entity with SVG sanitization module instead
```

SVG sanitization in extractor:

```php
// SVG extractor automatically sanitizes content
// Removes:
// - <script> tags
// - Event handlers (onclick, onload, etc.)
// - External references (xlink:href to external domains)
// - Embedded stylesheets with expressions
```

Optimize SVG sources:

```bash
# Install SVGO
npm install -g svgo

# Optimize all icons
svgo --folder icons/ --config svgo.config.js

# svgo.config.js
module.exports = {
  plugins: [
    'removeDoctype',
    'removeXMLProcInst',
    'removeComments',
    'removeMetadata',
    'removeEditorsNSData',
    'cleanupAttrs',
    'mergeStyles',
    'inlineStyles',
    'minifyStyles',
    'cleanupIds',
    'removeUselessDefs',
    'cleanupNumericValues',
    'convertColors',
    'removeUnknownsAndDefaults',
    'removeNonInheritableGroupAttrs',
    'removeUselessStrokeAndFill',
    'removeViewBox',  // Remove if you control viewBox in template
    'cleanupEnableBackground',
    'removeHiddenElems',
    'removeEmptyText',
    'convertShapeToPath',
    'moveElemsAttrsToGroup',
    'moveGroupAttrsToElems',
    'collapseGroups',
    'convertPathData',
    'convertTransform',
    'removeEmptyAttrs',
    'removeEmptyContainers',
    'mergePaths',
    'removeUnusedNS',
    'sortAttrs',
    'removeTitle',
    'removeDesc',
  ]
};
```

Content Security Policy for remote sprites:

```php
// In SecurityHeadersSubscriber or similar
$response->headers->set('Content-Security-Policy',
  "default-src 'self'; img-src 'self' https://trusted-cdn.example.com;"
);
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconExtractor/SvgExtractor.php`

## Common Mistakes

- **Wrong**: Trusting user-uploaded SVG → **Right**: Never use Icon API for user content, use Media with SVG sanitizer
- **Wrong**: No CSP for remote sprites → **Right**: Restrict domains via Content-Security-Policy header
- **Wrong**: Not optimizing SVG sources → **Right**: Run svgo before deployment for smaller file sizes
- **Wrong**: Including complex SVG features → **Right**: Remove animations, scripts, external references
- **Wrong**: Storing sensitive data in SVG metadata → **Right**: SVGO removes metadata, but verify manually

## See Also

- [Performance Best Practices](performance-best-practices.md)
- [Remote Resource Security](remote-resource-security.md)
- Reference: [OWASP SVG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SVG_Security_Cheat_Sheet.html)
