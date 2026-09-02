---
description: "No core extractor makes a server-side request for an icon — SSRF is not in the threat model unless a custom extractor fetches"
tldr: "path records a URL and the visitor's browser fetches it; svg filters remote sources out; svg_sprite accepts a remote source and then reads zero icons. SSRF applies only to a custom extractor you write that calls httpClient()."
drupal_version: "11.x"
---

# Remote Resource Security

## When to Use

You're loading icons from CDNs or external sources and need to understand what the actual risks are.

**No core extractor makes a server-side request for an icon.** This is the single most important fact in this section, and it eliminates SSRF from the threat model:

- `path` records the URL and stops. `{{ source }}` prints it, and the visitor's browser fetches it.
- `svg` filters remote sources out at discovery.
- `svg_sprite` accepts a remote source and then fails to read it, because `IconFinder::getFileContents()` refuses any URI with a scheme — so remote sprites discover zero icons.
- A custom extractor that calls `httpClient()` is a different matter; the SSRF surface, if any, is one you added.

The only server-side gate on a URL is `IconFinder::getFileFromUrl()`, which rejects schemes outside `UrlHelper::getAllowedProtocols()` and logs "Invalid icon source". Everything else is a client-side concern.

## Decision

| Risk | Real? | Mitigation | Applies to |
|---|---|---|---|
| SSRF (Server-Side Request Forgery) | **No** — Drupal never fetches | n/a | — |
| Third-party content / tampering | Yes | Vendor the file locally; CSP `img-src` | `path` |
| Privacy (visitor IP exposed to CDN) | Yes | Serve icons from your own origin | `path` |
| Mixed content (HTTP page asset) | Yes | Use HTTPS URLs only | `path` |
| Availability (CDN down) | Yes | Vendor locally; monitoring | `path` |
| Remote sprite silently empty | Yes | Vendor the sprite; it cannot work remotely | `svg_sprite` |

Subresource Integrity does **not** apply to an icon URL. SRI is an attribute on `<script>`/`<link>` elements; an `<img src>` or `<use href>` cannot carry it. If you need integrity guarantees, vendor the file.

## Pattern

```yaml
# ❌ Does not work at all - discovery reads the sprite and cannot fetch a URL
cdn_sprites:
  extractor: svg_sprite
  config:
    sources:
      - https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/bootstrap-icons.svg

# ✅ Vendor it. Same one-request-per-page result, no third-party dependency.
local_sprites:
  extractor: svg_sprite
  config:
    sources:
      - sprites/bootstrap-icons.svg

# ⚠️ Remote by URL is only possible with `path`, one URL per icon.
cdn_icons:
  extractor: path
  config:
    sources:
      - https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/icons/house.svg

# ❌ Never allow user-controlled URLs
# Bad: sources: ["{{ user_input_url }}"]
```

SRI is available for the *CSS* a font pack attaches, because that is a real `<link>` element — it is not available for the icon files themselves:

```yaml
# my_theme.libraries.yml
bootstrap_icons:
  remote: https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3
  css:
    theme:
      https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css:
        type: external
        attributes:
          integrity: sha384-[hash]
          crossorigin: anonymous
```

Validating URLs in a custom extractor, if you write one that fetches remotely. Note the pieces the shorter version of this example usually omits: the `#[IconExtractor]` attribute (without it the plugin is never discovered), the `array` return on every path, and the fact that sources live at `$this->configuration['config']['sources']`:

```php
<?php

namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\Core\Theme\Icon\Attribute\IconExtractor;
use Drupal\Core\Theme\Icon\IconDefinition;
use Drupal\Core\Theme\Icon\IconExtractorBase;

#[IconExtractor(
  id: 'secure_remote',
  label: new TranslatableMarkup('Secure remote'),
  description: new TranslatableMarkup('Remote icons from an allow-listed host.'),
)]
class SecureRemoteExtractor extends IconExtractorBase {

  private const ALLOWED_DOMAINS = [
    'cdn.jsdelivr.net',
    'cdnjs.cloudflare.com',
  ];

  protected function validateUrl(string $url): bool {
    $parsed = parse_url($url);
    if (($parsed['scheme'] ?? '') !== 'https') {
      return FALSE;
    }
    return in_array($parsed['host'] ?? '', self::ALLOWED_DOMAINS, TRUE);
  }

  public function discoverIcons(): array {
    $icons = [];

    foreach ($this->configuration['config']['sources'] ?? [] as $source) {
      if (!$this->validateUrl($source)) {
        \Drupal::logger('my_module')->error(
          'Blocked icon source from non-allowed domain: @url',
          ['@url' => $source]
        );
        continue;
      }

      $icon_id = pathinfo(parse_url($source, PHP_URL_PATH), PATHINFO_FILENAME);
      $full_id = IconDefinition::createIconId($this->configuration['id'], $icon_id);
      $icons[$full_id] = [
        'icon_id' => $icon_id,
        'source' => $source,
        'absolute_path' => $source,
      ];
    }

    return $icons;
  }

}
```

There is no CDN-then-local fallback. Sources are merged, not tried in order: every source is discovered, results are keyed by icon ID, and a later source **overwrites** an earlier one with the same ID. A remote-first, local-second list does not degrade gracefully — with `svg_sprite` the remote source contributes nothing and the local one supplies everything; with `path` the *local* entry wins because it comes second.

Monitor external dependencies:

```php
// In hook_cron or custom service
function my_module_check_icon_availability() {
  $urls = [
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/bootstrap-icons.svg',
  ];
  
  foreach ($urls as $url) {
    $response = \Drupal::httpClient()->head($url);
    
    if ($response->getStatusCode() !== 200) {
      \Drupal::logger('my_module')->warning(
        'Icon CDN unavailable: @url',
        ['@url' => $url]
      );
    }
  }
}
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/IconFinder.php:114-177` for the only URL handling core performs; OWASP SSRF Prevention Cheat Sheet if you write an extractor that fetches.

## Common Mistakes

- Designing against SSRF for core extractors → Not the threat; Drupal makes no outbound request for icons. Guard it only in custom extractors that fetch
- Expecting SRI to protect an icon URL → SRI is a `<script>`/`<link>` attribute; `<img src>` and `<use href>` cannot carry it
- Listing a CDN source and a local source as "fallback" → Sources merge, they do not fall back; the last matching ID wins
- Pointing `svg_sprite` at a CDN → Zero icons, no error
- HTTP instead of HTTPS → Mixed content warnings, MITM on the asset
- Not monitoring CDN availability → Icons break silently when the CDN changes or removes files

## See Also

- [SVG Security](svg-security-performance.md)
- [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md)
- Reference: [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
