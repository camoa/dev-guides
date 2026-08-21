---
description: "The most common UI Icons mistakes across security, caching, accessibility, and pack authoring."
tldr: "Never trust SVG as fully sanitized — UI Icons does not strip <script> tags. Always prefix pack IDs, clear cache after file changes, declare decorative/ariaLabel settings, and enable only the integrations a site actually uses."
drupal_version: "11.x"
---

# Anti-Patterns

## Common Mistakes

- **Wrong**: pasting raw SVG into a node body via Source mode → **Right**: enable the CKEditor 5 icon button + filter; use `<drupal-icon>`
- **Wrong**: treating SVG content as fully trusted → **Right**: only ship SVG you authored or vetted. SVG can carry `<script>`; UI Icons does not sanitize automatically
- **Wrong**: hardcoding icon paths in Twig templates → **Right**: render through pack templates so settings, cache metadata, and a11y templating apply
- **Wrong**: pack IDs without a theme/module prefix → **Right**: prefix to avoid collisions
- **Wrong**: changing icon files but expecting Drupal to detect it → **Right**: clear cache; YamlDiscovery + extractor results are cached
- **Wrong**: missing `decorative` / `ariaLabel` settings → **Right**: declare them so editors can comply with WCAG
- **Wrong**: relying on `dompdf/php-font-lib` without requiring it via Composer → **Right**: install the library, or ship a `.codepoints` / `.json` metadata file alongside the font
- **Wrong**: enabling all submodules "just in case" → **Right**: enable only the integrations the site uses; each adds form alters and routes

## See Also

- [Settings & Rendering](settings-rendering.md)
- [Installation](installation.md)
- [UI Icons Overview](overview.md)
