---
description: Drupal language negotiation — URL prefix, domain, session, browser, user preference detection methods and priority
---

# Language Negotiation

### When to Use
When configuring how Drupal detects the user's language — URL prefix, domain, session, browser, user preference.

### Decision: Negotiation Method Priority

| If you need... | Use... | Priority Order |
|---|---|---|
| SEO-friendly multilingual URLs | URL (path prefix) | 1st (highest) |
| Language-specific domains | URL (domain) | 1st (highest) |
| User account language preference | User | 2nd or 3rd |
| Temporary language switching | Session | 2nd or 3rd |
| First-time visitor detection | Browser | 4th |
| Fallback default | Selected language | Last (lowest) |

**Recommendation**: URL → User → Browser → Selected language

### Pattern: Configuring Language Negotiation

**File**: `config/install/language.types.yml`

```yaml
all:
  - language_interface
  - language_content
  - language_url
configurable:
  - language_interface
negotiation:
  language_content:
    enabled:
      language-interface: 0
  language_url:
    enabled:
      language-url: 0
      language-url-fallback: 1
  language_interface:
    enabled:
      language-url: 0
      language-user: 1
      language-browser: 2
      language-selected: 3
```

**File**: `config/install/language.negotiation.yml`

```yaml
session:
  parameter: language
url:
  source: path_prefix  # or 'domain'
  prefixes:
    en: ''  # No prefix for default
    es: es
    fr: fr
  domains:
    en: ''
selected_langcode: site_default
```

**URL prefix example**:
- English: `https://example.com/about` (no prefix)
- Spanish: `https://example.com/es/about`
- French: `https://example.com/fr/about`

**Domain example** (change `source: domain`):
- English: `https://example.com/about`
- Spanish: `https://es.example.com/about`
- French: `https://fr.example.com/about`

### Negotiation Methods Detail

**URL (path prefix)** — detects from `/en/`, `/es/`, `/fr/` in path:
- Plugin: `LanguageNegotiationUrl`
- SEO-friendly, explicit, cacheable
- Best for most multilingual sites

**URL (domain)** — detects from `en.example.com`, `es.example.com`:
- Plugin: `LanguageNegotiationUrl` with `source: domain`
- Good for separate regional sites
- Requires DNS configuration, SSL certificates per domain

**Session** — detects from `?language=es` query parameter:
- Plugin: `LanguageNegotiationSession`
- Temporary override, not SEO-friendly
- Good for language switcher links

**User** — uses authenticated user's language preference:
- Plugin: `LanguageNegotiationUI`
- Persists across sessions
- Only works for logged-in users

**Browser** — reads `Accept-Language` header:
- Plugin: `LanguageNegotiationBrowser`
- Good for first-time visitors
- Can be inaccurate (corporate proxies, VPNs)

**Selected** — site default language:
- Plugin: `LanguageNegotiationSelected`
- Always enabled as final fallback

### Common Mistakes

- **Using same prefix for multiple languages** → Each language must have unique prefix or domain. Empty string (`''`) only allowed for one language (typically default)
- **Wrong priority order** → Session before URL means query parameter overrides URL prefix, breaking SEO. URL should be highest priority
- **Not testing browser detection** → Browser language may not match site languages. If `Accept-Language: pt-BR` but site only has `es` and `en`, negotiation falls to next method
- **Forgetting to configure URL prefixes** → Enabling URL negotiation without setting prefixes causes all languages to use same URL, breaking cache contexts
- **Mixing path prefix and domain** → Choose one URL method. Both enabled simultaneously causes confusion and cache issues

### See Also
- → [URL & Language Routing](url-language-routing.md) — hreflang tags, path aliases
- → [Security, Performance & Caching](security-performance-caching.md) — cache contexts for language
- Reference: https://api.drupal.org/api/drupal/core!modules!language!src!LanguageNegotiatorInterface.php/interface/LanguageNegotiatorInterface/11.x
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/translating-site-interfaces/enable-language-negotiation
