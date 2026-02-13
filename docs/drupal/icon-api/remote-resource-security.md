---
description: Loading icons from CDNs with SSRF, mixed content, and availability protection
drupal_version: "11.x"
---

# Remote Resource Security

## When to Use

> Use when you're loading icons from CDNs or external sources and need to understand SSRF, mixed content, and availability risks.

## Decision

| Risk | Mitigation | Applies to extractor |
|---|---|---|
| SSRF (Server-Side Request Forgery) | Whitelist domains, validate URLs | Path, SVG Sprite |
| Mixed content (HTTP/HTTPS) | Enforce HTTPS, use SRI | Path, SVG Sprite |
| Availability (CDN down) | Fallback to local, monitoring | Path, SVG Sprite |
| Content tampering | Subresource Integrity (SRI) | SVG Sprite via library |
| Privacy (tracking pixels) | Proxy through your server | Path |

## Pattern

Secure remote icon configuration:

```yaml
# ⚠️ Remote sprites require validation
cdn_sprites:
  extractor: svg_sprite
  config:
    sources:
      - https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/bootstrap-icons.svg
  library: "my_theme/bootstrap_icons"  # Include SRI in library

# ❌ Never allow user-controlled URLs
# Bad: sources: ["{{ user_input_url }}"]
```

Library with Subresource Integrity:

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

Validate remote URLs in custom extractor:

```php
<?php
namespace Drupal\my_module\Plugin\IconExtractor;

use Drupal\Core\Theme\Icon\IconExtractorBase;

class SecureRemoteExtractor extends IconExtractorBase {

  private const ALLOWED_DOMAINS = [
    'cdn.jsdelivr.net',
    'cdnjs.cloudflare.com',
  ];

  protected function validateUrl(string $url): bool {
    $parsed = parse_url($url);

    // Require HTTPS
    if ($parsed['scheme'] !== 'https') {
      return FALSE;
    }

    // Whitelist domains
    if (!in_array($parsed['host'], self::ALLOWED_DOMAINS, TRUE)) {
      return FALSE;
    }

    return TRUE;
  }

  public function discoverIcons(): array {
    $sources = $this->configuration['sources'] ?? [];

    foreach ($sources as $source) {
      if (!$this->validateUrl($source)) {
        \Drupal::logger('my_module')->error(
          'Blocked icon source from non-whitelisted domain: @url',
          ['@url' => $source]
        );
        continue;
      }

      // Process validated source
    }
  }
}
```

Fallback to local icons:

```yaml
icons_with_fallback:
  extractor: svg_sprite
  config:
    sources:
      - https://cdn.example.com/icons.svg  # Try CDN first
      - sprites/icons-local.svg  # Fallback to local
```

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

Reference: OWASP SSRF Prevention Cheat Sheet

## Common Mistakes

- **Wrong**: No domain whitelist → **Right**: Allows SSRF to internal services (localhost, 169.254.169.254)
- **Wrong**: HTTP instead of HTTPS → **Right**: Mixed content warnings, MITM attacks
- **Wrong**: No SRI for external resources → **Right**: CDN compromise injects malicious code
- **Wrong**: Single point of failure → **Right**: No fallback when CDN is down
- **Wrong**: Not monitoring CDN availability → **Right**: Icons break silently when CDN changes/removes files

## See Also

- [SVG Security & Performance](svg-security-performance.md)
- [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md)
- Reference: [Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
