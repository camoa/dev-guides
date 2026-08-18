---
description: "path is the only core extractor that works with remote URLs — Drupal never fetches the file, the visitor's browser does"
tldr: "You need to reference icon files by URL — local svg/png/gif or any remote format; path never reads the file server-side, and {icon_id} is not expanded in remote URLs, so one URL means one icon."
drupal_version: "11.x"
---

# Path Extractor

## When to Use

You need to reference icon files by URL rather than inline their markup — local `.svg`/`.png`/`.gif`, or any format at all from a remote URL. This is the only core extractor that works with remote sources.

## Decision

| If icons are... | Pattern... | Constraint |
|---|---|---|
| Local images | `images/{icon_id}.png` | Extension must be `svg`, `png` or `gif` — `IconFinder::ALLOWED_EXTENSION`. `.webp`/`.jpg` log a warning and yield nothing |
| CDN/remote URLs | `https://cdn.example.com/icon.svg` | No extension check, but the scheme must be in `UrlHelper::getAllowedProtocols()`. `{icon_id}` is **not** expanded in URLs — the icon ID comes from the URL's filename, so one URL means one icon |
| Mixed formats | Multiple source patterns | Icons are keyed by ID, so a later source with the same ID replaces an earlier one |
| User-uploaded | Never use path extractor | Use Media with validation |

The `path` extractor never reads the file. `discoverIcons()` records `source` and `absolute_path` and stops; the template prints `{{ source }}` and the **browser** does the fetching. Drupal makes no outbound request for a `path` icon.

## Pattern

Path extractor configuration:

```yaml
path_pack:
  extractor: path
  config:
    sources:
      - images/icons/{icon_id}.svg
      - images/icons/{icon_id}.png
      # One URL == one icon; {icon_id} is not expanded for remote sources.
      - https://cdn.example.com/icons/home.svg
  template: >-
    <img src="{{ source }}" 
         width="{{ size|default(24) }}" 
         height="{{ size|default(24) }}"
         alt="{{ alt|default('') }}"
         class="icon icon-{{ icon_id|clean_class }}"
         loading="lazy">
```

The `{{ source }}` variable contains the browser-facing path (run through `FileUrlGenerator`) or the verbatim URL.

Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/PathExtractor.php`

## Common Mistakes

- **Wrong**: Using a `.webp` or `.jpg` local source → **Right**: Not in `ALLOWED_EXTENSION`; the pack is empty and only a logger warning records it
- **Wrong**: Putting `{icon_id}` in a remote URL → **Right**: Placeholders are a local-path feature; for URLs the filename becomes the icon ID
- **Wrong**: Using for user-uploaded content → **Right**: High XSS risk, use Media field with validation
- **Wrong**: No lazy loading → **Right**: Add `loading="lazy"` for below-fold icons
- **Wrong**: Missing alt text for semantic icons → **Right**: Decorative icons use empty alt, semantic icons need descriptive alt
- **Wrong**: Hardcoded dimensions for responsive icons → **Right**: Use CSS or `srcset` for responsive images

## See Also

- [SVG Sprite Extractor](svg-sprite-extractor.md)
- [Font Extractor](font-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/PathExtractor.php`, `/core/lib/Drupal/Core/Theme/Icon/IconFinder.php`
