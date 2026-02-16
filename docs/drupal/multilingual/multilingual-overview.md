---
description: Drupal multilingual architecture overview — language types, negotiation, entity translation, field translatability, config translation
---

# Multilingual Overview

### When to Use
When building a site that needs to serve content in multiple languages — either content translation (nodes, terms, media), interface translation (UI strings, labels), or config translation (views, menus, site settings).

### Decision: Which Modules to Enable

| If you need... | Enable... | Why |
|---|---|---|
| Basic language management (always required) | Language module | Foundation — defines languages, language types, negotiation |
| Translate site interface (UI strings, buttons, labels) | Locale module | Manages .po files, imports translations from localize.drupal.org |
| Translate content entities (nodes, terms, media) | Content Translation module | Provides entity translation handlers, field translatability |
| Translate configuration (views, menus, field labels) | Config Translation module | Discovers translatable config via schema, provides translation UI |
| Complex translation workflows, external services | TMGMT (contrib) | Translation jobs, translators, integration with services like DeepL |

### Pattern: Core Multilingual Architecture

**Language Types** — Drupal has 3 language types:
- **Interface** (`language_interface`) — UI language for buttons, labels, system messages
- **Content** (`language_content`) — Language of content entities being displayed
- **URL** (`language_url`) — Language determined from URL (prefix or domain)

**Language Negotiation** — detection methods in priority order:
1. URL (path prefix like `/en/` or domain like `en.example.com`)
2. Session (query parameter like `?language=fr`)
3. User preference (from user account settings)
4. Browser (Accept-Language header)
5. Selected language (site default)

**Entity Translation** — content entities (nodes, taxonomy terms, media, blocks, menu links) can have translations via `addTranslation()`, `getTranslation()`, `hasTranslation()` API.

**Field Translatability** — each field can be marked translatable or non-translatable. Translatable fields have separate values per language; non-translatable fields share the same value across all translations.

**Config Translation** — configuration entities (views, content types, menus, field definitions) can be translated. Config schema defines which keys are translatable via `type: label` or `translatable: true`.

**Interface Translation** — strings wrapped in `t()` or `TranslatableMarkup` are extracted to .po files, imported via Locale module, and displayed based on interface language.

### Common Mistakes

- **Enabling Content Translation without Language module** → Content Translation requires Language module. Enable Language first, add languages, then enable Content Translation
- **Forgetting to enable translation per entity type** → Enabling Content Translation module doesn't automatically make entities translatable — must enable per entity type and bundle via config or UI
- **Mixing up language types** → Interface language (UI) is separate from content language (displayed entity). A French user can view English content if that's the URL language
- **Not configuring language negotiation priority** → Default priority may not match your needs. URL detection should typically come first for SEO, followed by user preference
- **Assuming all fields are translatable** → Fields are non-translatable by default. Must explicitly mark fields as translatable in field settings

### See Also
- → [Language Setup & Configuration](language-setup.md) — adding languages
- → [Language Negotiation](language-negotiation.md) — detection methods and priority
- → [Content Translation Setup](content-translation-setup.md) — enabling translation per entity
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide
