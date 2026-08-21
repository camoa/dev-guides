---
description: "Core never sanitizes SVG — the security model is refusing remote sources, not cleaning trusted ones"
tldr: "Core does not sanitize SVG anywhere; the svg extractor inlines file contents unescaped and only refuses remote sources, so review every file you ship as trusted code — never route user uploads through Icon API."
drupal_version: "11.x"
---

# SVG Security & Performance

## When to Use

You're working with SVG icons and need to understand security implications and optimization techniques.

## Decision

**Core does not sanitize SVG. Anywhere.** The `svg` extractor inlines whatever the file contains, unescaped. The security model is *refusal of untrusted sources*, not cleaning of trusted ones:

- `SvgExtractor::discoverIcons()` drops every source whose `parse_url()` yields a scheme, so remote SVG can never be inlined.
- `IconFinder::getFileContents()` returns `FALSE` for any URI with a scheme or host.
- `IconFinder::ALLOWED_EXTENSION` limits local discovery to `svg`, `png`, `gif`, "so a definition can not be used to expose the content of a non image to the extractor".

What actually reaches the page: `extractSvg()` concatenates each child element's `asXML()` and wraps it in a `FormattableMarkup` (`SvgExtractor.php:120-130`), which implements `MarkupInterface` and is therefore printed verbatim. A `<script>` element, an `onload=` attribute, or an `xlink:href` to an external host inside a file in your `icons/` directory is served to every visitor.

| Risk level | Source | Reality |
|---|---|---|
| Low | Local SVG files you authored or vendored | Fine — but it is *your* review that makes it fine, not the extractor |
| Low | Vendored third-party icon set | Diff it on upgrade; nothing in the pipeline will catch an injected script |
| N/A | Remote SVG URLs with the `svg` extractor | Silently filtered out at discovery; not a risk, just a pack that stays empty |
| Critical | User-uploaded SVG | Never route through Icon API. Use Media with a dedicated SVG sanitizer |

## Pattern

```yaml
# ✅ Local SVG files. Remote sources are stripped at discovery, so this is
# structurally local-only -- but the file contents are inlined unsanitized.
safe_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg

# ❌ Does not work - svg_sprite cannot read a remote file, so this pack is empty
remote_sprite:
  extractor: svg_sprite
  config:
    sources:
      - https://trusted-cdn.example.com/sprite.svg

# ✅ Remote icons - `path` is the only extractor that works, and the browser
# (not Drupal) fetches the file, so restrict it with CSP img-src.
remote_pack:
  extractor: path
  config:
    sources:
      - https://trusted-cdn.example.com/icons/home.svg

# ❌ Never - User-uploaded SVG via Icon API
# Use Media entity with SVG sanitization module instead
```

Reviewing a vendored icon set before you ship it:

```bash
# Anything here is a reason not to inline the file with the `svg` extractor.
grep -rlE '<script|on[a-z]+\s*=|xlink:href="https?:|<foreignObject' icons/
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
    // Do NOT enable 'removeViewBox' for an `svg` pack. The extractor copies the
    // source root's attributes into {{ attributes }}, which is how a template
    // stays correct across icon sets with different coordinate systems.
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

Content Security Policy for remote `path` icons. This is the browser fetching the URL from `{{ source }}`, so `img-src` is the relevant directive:

```php
// In SecurityHeadersSubscriber or similar
$response->headers->set('Content-Security-Policy', 
  "default-src 'self'; img-src 'self' https://trusted-cdn.example.com;"
);
```

Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgExtractor.php`, `/core/lib/Drupal/Core/Theme/Icon/IconFinder.php`

## Common Mistakes

- **Wrong**: Believing the `svg` extractor sanitizes → **Right**: It does not; review the files instead
- **Wrong**: Trusting user-uploaded SVG → **Right**: Never use Icon API for user content, use Media with SVG sanitizer
- **Wrong**: Expecting a CSP to protect an inlined SVG → **Right**: CSP `img-src` governs `path` icons; an inlined `<script>` from an `svg` pack is same-origin page content
- **Wrong**: Running svgo with `removeViewBox` → **Right**: Breaks `{{ attributes }}`-based scaling
- **Wrong**: Storing sensitive data in SVG metadata → **Right**: SVGO removes metadata, but verify manually

## See Also

- [Performance Best Practices](performance-best-practices.md)
- [Remote Resource Security](remote-resource-security.md)
- Reference: [OWASP SVG Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SVG_Security_Cheat_Sheet.html)
