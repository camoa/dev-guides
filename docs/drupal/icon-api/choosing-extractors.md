---
description: "Pick svg / svg_sprite / path / font by source location and format — remote sprites discover zero icons, and local files are limited to svg/png/gif"
tldr: "Select the right extractor by icon source and remoteness; svg_sprite cannot read a remote sprite (discovers zero icons, silently), and local sources are restricted to svg/png/gif."
drupal_version: "11.x"
---

# Choosing Extractors

## When to Use

You need to select the appropriate extractor plugin for your icon source format and security requirements.

## Decision

| If icons are... | Use extractor... | Provided by | Remote sources | What reaches the page |
|---|---|---|---|---|
| Individual SVG files (local) | `svg` | Core | Silently filtered out | SVG markup inlined; zero extra requests |
| SVG sprite file (**local only**) | `svg_sprite` | Core | Accepted then yields **zero icons** | `<use href="…#id">`; one request for the sprite |
| `.svg`/`.png`/`.gif` locally, any format by URL | `path` | Core | Yes — the only extractor that works remotely | A URL in `{{ source }}`; the browser fetches it |
| Icon font (`.ttf`/`.woff`/`.json`/`.yaml`/`.codepoints`) | `font` | UI Icons contrib | No | CSS-rendered glyph; font loaded via `library:` |
| Iconify CDN | `iconify` | Iconify Icons contrib (`drupal/iconify_icons`) | Yes | Depends on the pack template |
| Custom source (API, database) | Custom extractor | Your module | Your responsibility | Your responsibility |

**Remote sprites do not work.** `SvgSpriteExtractor::discoverIcons()` must read the sprite to enumerate `<symbol id>` values, and it reads through `IconFinder::getFileContents()`, which returns `FALSE` for any URI with a scheme or host (`IconFinder.php:114-123`). Core's own unit test locks that in for `http://`, `https://`, `ftp://`, `ssh://` and protocol-relative URLs (`IconFinderTest::providerGetFileContents()`). A remote sprite source is accepted by the finder and then discovers nothing — a silent empty pack, not an error. The `IconPackManager` docblock claiming "`path` and `svg_sprite` allow remote files" describes intent the code does not deliver.

**Local file extensions are restricted.** `IconFinder::ALLOWED_EXTENSION` is `['svg', 'png', 'gif']` (`IconFinder.php:93`). A local source ending in `.webp`, `.jpg`, or `.woff2` logs "Invalid icon path extension" and returns no files. The restriction applies to local paths only; URL sources skip extension validation but must use a scheme in `UrlHelper::getAllowedProtocols()`.

## Pattern

Choose based on icon count and source:

```yaml
# <10 icons, local SVGs
small_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg

# 50+ icons, one LOCAL sprite file (remote sprites discover nothing)
large_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/all-icons.svg

# Remote CDN icons -- `path` is the only extractor that works here
cdn_pack:
  extractor: path
  config:
    sources:
      - https://cdn.example.com/icons/{icon_id}.svg

# Existing icon font. `.woff2` is NOT a recognised source extension --
# the extractor's switch handles .ttf, .woff, .json, .yml/.yaml, .codepoints.
font_pack:
  extractor: font
  config:
    sources:
      - fonts/icons.woff
  library: "my_theme/icon_font"
```

Reference: `/core/lib/Drupal/Core/Theme/Plugin/IconExtractor/` for the three core extractors.

## Common Mistakes

- **Wrong**: Using `path` for local SVGs → **Right**: `svg` inlines the markup so it can be styled with `currentColor` and needs no extra request
- **Wrong**: Using `svg` for sprites → **Right**: `svg` reads and inlines each file separately; `svg_sprite` emits one `<use>` reference
- **Wrong**: Pointing `svg_sprite` at a CDN URL → **Right**: Discovers zero icons, silently. Copy the sprite into the extension instead
- **Wrong**: Naming a local source `.webp`/`.jpg` → **Right**: Not in `ALLOWED_EXTENSION`; the pack is empty and only a logger warning marks it
- **Wrong**: Missing `library` for font extractors → **Right**: Font CSS won't load, icons appear as missing glyphs
- **Wrong**: Custom extractors without caching → **Right**: Cache expensive discovery yourself; nothing in the base class does it for you

## See Also

- [Icon Pack Definition](icon-pack-definition.md)
- [SVG Extractor](svg-extractor.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconExtractorInterface.php`, `/core/lib/Drupal/Core/Theme/Icon/IconFinder.php`
