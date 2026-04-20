---
description: Configure hreflang tags for multilingual Drupal 11 sites using the metatag_hreflang submodule — automatic generation, x-default, and language-specific overrides
tldr: "You have a multilingual Drupal 11 site with content translated into multiple languages. Without hreflang tags, Google may treat translated pages as duplicate content or serve the wrong language to users."
drupal_version: "11.x"
---

# Metatag for Multilingual

## When to Use

> You have a multilingual Drupal 11 site with content translated into multiple languages. Without hreflang tags, Google may treat translated pages as duplicate content or serve the wrong language to users. Enable the `metatag_hreflang` submodule to auto-generate hreflang link elements for every translation of each piece of content.

## Decision

| If you need... | Approach | Why |
|----------------|----------|-----|
| hreflang on all translated content | Enable metatag_hreflang — no further config needed | Module auto-detects all active translations |
| x-default pointing to the main language | Configure x-default in metatag_hreflang settings | Signals to Google which URL to serve when no language matches |
| Language-specific title/description | Language-specific Metatag override at content type level | Each language entity has its own Metatag field values |
| hreflang on non-translatable pages (Views, custom routes) | Manual configuration or hook_page_attachments | Module only auto-generates for translatable content entities |
| Suppressing hreflang on admin/utility pages | Robots noindex + hreflang exclusion config | Indexed admin pages send confusing signals |

## Pattern

### Enable and configure

```
1. Enable submodule:
   /admin/modules → Metatag: hreflang

2. Configure x-default:
   /admin/config/search/metatag → Global group
   → hreflang x-default: [site:url]   (or the primary-language homepage URL)

3. Verify output at any translated node:
   View source → search for <link rel="alternate" hreflang=
```

### Automatic output for translated content

With `metatag_hreflang` enabled, Drupal outputs a `<link>` element for each available translation:

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/about" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/a-propos" />
<link rel="alternate" hreflang="es" href="https://example.com/es/acerca-de" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```

The module queries all enabled translations of the current content entity and generates the link set automatically — no per-node configuration required.

### Language-specific meta tag overrides

Each translation of a node has its own Metatag field values. Tokens resolve in the context of the current language:

```
Title (EN node):  [node:title] | [site:name]  → "About Us | Acme Corp"
Title (FR node):  [node:title] | [site:name]  → "À propos | Acme Corp"
```

Token values come from the translated field values, so `[node:title]` returns the French title on the French translation. No special configuration needed — this is standard Drupal content translation behavior.

For language-specific overrides that go beyond token differences (e.g., a different description strategy for the French market), edit the Metatag field on the specific translation entity.

## x-default Configuration

| x-default scenario | Config value | Notes |
|-------------------|-------------|-------|
| Site has a primary/default language | URL of the default-language homepage | Most common — signals the "fallback" language |
| Site is region-specific (no universal page) | Omit x-default | Google recommendation when no single URL is best for all locales |
| Separate domain per language (example.com, example.fr) | `https://example.com/` (the neutral domain) | If no neutral domain exists, omit x-default |

## Content Translation Integration

hreflang depends on Drupal's content translation system:

```
Requirements:
  - Language module enabled
  - Content Translation module enabled
  - Content type has "Translatable" enabled at /admin/config/regional/content-language
  - metatag_hreflang submodule enabled
```

When a node has no translation for a given language, Drupal does not emit a hreflang tag for that language — the module only lists languages with actual translations. This is correct behavior; do not manually add hreflang for untranslated content.

## Common Mistakes

- **Wrong**: Manually hardcoding hreflang URLs in template files → **Right**: The metatag_hreflang module auto-generates these from Drupal's translation system; manual implementations diverge when URLs change
- **Wrong**: Setting x-default to the English version's node URL (`/en/about`) → **Right**: x-default should point to a language-neutral or redirect URL (e.g., the homepage `/`) that serves the appropriate language based on browser preference
- **Wrong**: Enabling hreflang without enabling Content Translation for the content type → **Right**: The module only generates hreflang for entities configured as translatable; check `/admin/config/regional/content-language`
- **Wrong**: Expecting hreflang on Views pages or custom routes → **Right**: metatag_hreflang only auto-generates for content entities with translations; Views pages and custom routes need manual `hook_page_attachments` implementation
- **Wrong**: Using the same meta description across all language translations by relying on Global group → **Right**: Each translated entity has its own Metatag field; write distinct descriptions in each language rather than having all languages use the same token resolving to the source language value
- **Wrong**: Mixing hreflang with duplicate canonical URLs → **Right**: Each language URL should be its own canonical; hreflang and canonical work together — the canonical for `/en/about` is `/en/about`, not the French URL

## See Also

- [Metatag Architecture](metatag-architecture.md) — cascading inheritance and submodule setup
- [Core Meta Tags](core-meta-tags.md) — title and description configuration that applies per language
- [Canonical URLs](canonical-urls.md) — canonical and hreflang interaction for multilingual sites
- Reference: [Google hreflang documentation](https://developers.google.com/search/docs/specialty/international/localization-with-hreflang)
- Reference: [Metatag module on drupal.org](https://www.drupal.org/project/metatag)
