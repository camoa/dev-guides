---
description: Common UI Icons mistakes covering SVG security, caching, a11y, and integration shortcuts.
tldr: The most critical mistakes are trusting unvetted SVG content (UI Icons does not sanitize), missing the icon_embed filter for CKEditor output, using pack IDs without a theme/module prefix, and skipping decorative/ariaLabel settings that editors need for WCAG compliance.
drupal_version: "11.x"
---

# Anti-Patterns

## Wrong vs Right

- **Wrong**: pasting raw SVG into a node body via Source mode → **Right**: enable CKEditor 5 icon button + filter; use `<drupal-icon>`
- **Wrong**: treating SVG content as fully trusted → **Right**: only ship SVG you authored or vetted — SVG can carry `<script>`; UI Icons does not sanitize automatically
- **Wrong**: hardcoding icon paths in Twig templates → **Right**: render through pack templates so settings, cache metadata, and a11y templating apply
- **Wrong**: pack IDs without theme/module prefix → **Right**: prefix to avoid collisions with other packs
- **Wrong**: changing icon files but expecting Drupal to detect the change → **Right**: clear cache; YamlDiscovery and extractor results are cached
- **Wrong**: missing `decorative` / `ariaLabel` settings → **Right**: declare them so editors can comply with WCAG
- **Wrong**: relying on `dompdf/php-font-lib` without requiring it in Composer → **Right**: install the library, or ship a `.codepoints`/`.json` metadata file alongside the font
- **Wrong**: enabling all submodules without a plan → **Right**: enable only the integrations the site uses; each adds form alters, routes, and schema

## See Also

- [Overview](overview.md)
- [Pack Format](pack-format.md)
- [Settings & Rendering](settings-rendering.md)
- [Authoring & Distribution](authoring.md)
