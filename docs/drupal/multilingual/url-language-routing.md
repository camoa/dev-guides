---
description: Drupal URL and language routing — path prefixes, domains, hreflang tags, path aliases, language switcher
---

# URL & Language Routing

### When to Use
When configuring multilingual URLs — path prefixes, domains, path aliases, hreflang tags for SEO.

### Decision: URL Structure

| If you need... | Use... | Example URLs |
|---|---|---|
| Path prefix (most common) | URL negotiation, source: path_prefix | `/en/about`, `/es/acerca` |
| No prefix for default language | Empty prefix for default | `/about`, `/es/acerca` |
| Language-specific domains | URL negotiation, source: domain | `en.example.com/about`, `es.example.com/about` |
| Query parameter (not recommended) | Session negotiation | `/about?language=es` |

**Recommendation**: Path prefix with no prefix for default language. Best for SEO and user experience.

### Pattern: Path Prefix Configuration

**File**: `config/install/language.negotiation.yml`

```yaml
url:
  source: path_prefix
  prefixes:
    en: ''        # No prefix for English (default)
    es: es        # /es/ for Spanish
    fr: fr        # /fr/ for French
  domains:
    en: ''
```

**Resulting URLs**:
- English: `https://example.com/about`
- Spanish: `https://example.com/es/about`
- French: `https://example.com/fr/about`

**Path aliases work per language**:
- English: `/about` (alias for `/node/1`)
- Spanish: `/es/acerca` (alias for `/node/1` in Spanish)
- French: `/fr/a-propos` (alias for `/node/1` in French)

### Pattern: Domain-Based Configuration

**File**: `config/install/language.negotiation.yml`

```yaml
url:
  source: domain
  prefixes:
    en: ''
    es: ''
    fr: ''
  domains:
    en: 'example.com'
    es: 'es.example.com'
    fr: 'fr.example.com'
```

**Resulting URLs**:
- English: `https://example.com/about`
- Spanish: `https://es.example.com/about`
- French: `https://fr.example.com/about`

**Requirements**:
- DNS configuration for subdomains
- SSL certificates for each domain
- Web server configuration (virtual hosts)

### Pattern: Hreflang Tags (SEO)

Drupal automatically adds hreflang tags when:
- Language module enabled
- Multiple languages configured
- Content has translations

**Generated HTML** (automatic):

```html
<link rel="alternate" hreflang="en" href="https://example.com/about" />
<link rel="alternate" hreflang="es" href="https://example.com/es/acerca" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/a-propos" />
<link rel="alternate" hreflang="x-default" href="https://example.com/about" />
```

**What hreflang does**:
- Tells Google/Bing which language version to show
- Prevents duplicate content penalties
- Improves international SEO
- `x-default` specifies default for unmatched languages

**Manual override** (if needed):

```php
// In hook_page_attachments_alter()
function mymodule_page_attachments_alter(&$attachments) {
  $attachments['#attached']['html_head_link'][] = [
    [
      'rel' => 'alternate',
      'hreflang' => 'es',
      'href' => 'https://example.com/es/custom-path',
    ],
  ];
}
```

### Pattern: Language-Aware Path Aliases

**Via UI**:
- Edit node → URL alias tab
- Enter alias per language
- English: `/about-us`
- Spanish: `/acerca-de`

**Via Pathauto (contrib)**:

```yaml
# Pattern per language
/admin/config/search/path/patterns
- English pattern: /[node:menu-link:parents:join-path]/[node:title]
- Spanish pattern: /[node:menu-link:parents:join-path]/[node:title]
```

Pathauto generates language-specific aliases using translated tokens.

### Pattern: Language Switcher Block

**Enable block**: `/admin/structure/block`
- Place "Language switcher" block in desired region
- Configure to show links for all languages

**Generated links**:

```html
<ul class="language-switcher">
  <li class="en"><a href="/about" hreflang="en">English</a></li>
  <li class="es"><a href="/es/acerca" hreflang="es">Español</a></li>
  <li class="fr"><a href="/fr/a-propos" hreflang="fr">Français</a></li>
</ul>
```

**Custom language switcher in Twig** (requires preprocess):

```php
// In mytheme.theme or mymodule.module
function mytheme_preprocess_block__language_block(&$variables) {
  $language_manager = \Drupal::languageManager();
  $current = $language_manager->getCurrentLanguage()->getId();
  $languages = $language_manager->getLanguages();
  $variables['languages'] = $languages;
  $variables['current_langcode'] = $current;
}
```

```twig
{# In block--language-block.html.twig #}
<ul>
  {% for langcode, language in languages %}
    <li{{ langcode == current_langcode ? ' class="is-active"' }}>
      <a href="{{ path('<current>', {}, {'language': language}) }}" hreflang="{{ langcode }}">
        {{ language.getName() }}
      </a>
    </li>
  {% endfor %}
</ul>
```

### Common Mistakes

- **Forgetting to configure URL prefixes** → Enabling URL negotiation without setting prefixes causes all languages to use same URL, breaking caching
- **Using same alias for multiple languages** → Path aliases must be unique per language. Same alias in English and Spanish causes conflicts
- **Not testing with clean URLs disabled** → Language prefixes require clean URLs. Testing with query strings (`?q=`) can cause unexpected behavior
- **Assuming hreflang works without translations** → Hreflang tags only appear if content has translations. Single-language content has no hreflang
- **Missing x-default hreflang** → Google recommends `x-default` for fallback. Drupal adds automatically if default language configured
- **Wrong domain in hreflang tags** → Domain-based setup requires correct domain in hreflang. Verify generated tags match actual domains

### See Also
- → [Language Negotiation](language-negotiation.md) — URL detection priority
- → [Security, Performance & Caching](security-performance-caching.md) — language cache contexts
- Reference: `core/modules/language/src/Plugin/LanguageNegotiation/LanguageNegotiationUrl.php`
- Reference: https://www.specbee.com/blogs/multilingual-seo-and-hreflang-how-drupal-makes-it-easier
- Reference: https://pantheon.io/learning-center/drupal/multilingual
