---
description: Translate Klaro UI, service descriptions, and purposes for multi-language sites
drupal_version: "11.x"
---

# Translation and Localization

## When to Use

> Translate Klaro's consent interface for multi-language Drupal sites. Requires Configuration Translation module enabled.

## Decision

| If you need to translate... | Navigate to... | Why |
|---|---|---|
| All Klaro texts at once | `/admin/config/user-interface/klaro/translate` | Bulk translation of UI strings |
| Individual service descriptions | Services tab → Translate per service | Per-language service names/descriptions |
| Purpose labels | Purposes tab → Translate per purpose | Category names in each language |
| Button labels and notices | Texts tab → Translate | Modal content and buttons |
| Custom service fields | Service edit → Translate | Privacy URLs, descriptions per language |

## Pattern

**Enable Translation** (prerequisite):
```bash
drush en config_translation language content_translation
```

**Translate Klaro UI** (`/admin/config/user-interface/klaro/translate`):
1. Select target language (e.g., German)
2. Click "Add" to create translation
3. Translate all visible strings
4. Save translation

**Translate Service** (per-service translation):
```yaml
# English (default)
service:
  label: "Visitor Statistics"
  description: "We use analytics to improve our site."
  privacy_policy_url: "https://example.com/privacy"

# German translation
service:
  label: "Besucherstatistiken"
  description: "Wir nutzen Analysetools zur Verbesserung unserer Website."
  privacy_policy_url: "https://example.com/de/datenschutz"
```

**Translation Workflow**:
1. Configure service in default language
2. Navigate to Services tab
3. Find service → Dropdown → "Translate"
4. Add translation for each language
5. Klaro automatically displays correct language based on user's language preference

**Reference**: Drupal Configuration Translation module documentation

## Common Mistakes

- **Wrong**: Not enabling Configuration Translation module → **Right**: Translation options don't appear; enable first
- **Wrong**: Translating only service labels but not descriptions → **Right**: Inconsistent language; translate all fields
- **Wrong**: Forgetting to translate privacy policy URLs → **Right**: English URLs for non-English users; localize all URLs
- **Wrong**: Missing translations for button labels → **Right**: Mixed language modal; translate all UI strings
- **Wrong**: Not testing language switching → **Right**: Verify Klaro detects language correctly; test all languages
- **Wrong**: Translating machine names → **Right**: Machine names never translate; only translate labels/descriptions

## See Also

- [Styling and UI Customization](styling-and-ui-customization.md)
- [Automatic Resource Attribution](automatic-resource-attribution.md)
- Reference: [Drupal Configuration Translation](https://www.drupal.org/docs/8/multilingual/configuration-translation)
