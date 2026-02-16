---
description: Drupal language setup and configuration — adding languages via config YAML, programmatically, setting default language
---

# Language Setup & Configuration

### When to Use
When initializing a multilingual site — adding languages, setting default language, configuring language fallback.

### Decision: How to Add Languages

| If you need... | Use... | Why |
|---|---|---|
| Add languages via UI | `/admin/config/regional/language/add` | Simple, interactive, good for initial setup |
| Add languages via config YAML (recommended) | `config/install/language.entity.*.yml` | Repeatable, version-controlled, deployment-friendly |
| Programmatically add languages | `ConfigurableLanguage::create()` | For migrations, install hooks, test fixtures |

### Pattern: Adding Languages via Config YAML

**File**: `config/install/language.entity.es.yml`

```yaml
langcode: en
status: true
dependencies: {}
id: es
label: Spanish
direction: ltr
weight: 1
locked: false
```

**Explanation**:
- `id: es` — language code (ISO 639-1)
- `label: Spanish` — human-readable name
- `direction: ltr` — text direction (ltr or rtl)
- `weight: 1` — sort order (lower weights appear first)
- `locked: false` — can be disabled/removed

**Programmatic example**:

```php
use Drupal\language\Entity\ConfigurableLanguage;

$language = ConfigurableLanguage::create([
  'id' => 'es',
  'label' => 'Spanish',
  'direction' => 'ltr',
  'weight' => 1,
]);
$language->save();
```

**Default language** — set via `config/install/system.site.yml`:

```yaml
langcode: en
default_langcode: en
```

### Common Mistakes

- **Using wrong language code** → Must use valid ISO 639-1 code (en, es, fr). Invalid codes throw validation error. Check `LanguageInterface::VALID_LANGCODE_REGEX` for pattern
- **Forgetting to export config after UI changes** → Adding language via UI doesn't automatically update config YAML. Export config after changes for deployment consistency
- **Setting locked: true without understanding** → Locked languages cannot be disabled or removed. Only lock system languages (en, und, zxx) or when you have a specific deployment reason
- **Not considering RTL languages** → Arabic, Hebrew require `direction: rtl`. Test layout with RTL to catch CSS issues early
- **Adding languages before enabling Language module** → Language module must be enabled first. Enable via config or `drush en language` before adding languages

### See Also
- → [Language Negotiation](language-negotiation.md) — detection configuration
- → [Content Translation Setup](content-translation-setup.md) — enabling translation per entity
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/choosing-and-installing-multilingual-modules
