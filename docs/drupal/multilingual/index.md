---
description: Drupal multilingual and translation system — language setup, content translation, config translation, interface translation, best practices
guide-meta:
  concepts:
    - content translation
    - config translation
    - interface translation
    - language negotiation
    - TranslatableMarkup
    - t() function
    - .po files
    - multilingual routing
    - language-aware queries
    - TMGMT
  not:
    - machine translation services
    - AI translation
  requires:
    - drupal/entities
    - drupal/config-management
  complements:
    - drupal/twig
    - drupal/views
    - drupal/caching
  specializes: ""
  category: drupal
---

# Multilingual & Translation

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the multilingual architecture | [Multilingual Overview](multilingual-overview.md) | When building a site that needs to serve content in multiple languages — either content translation (nodes, terms, media), interface translation (UI strings, labels), or config translation (views, menus, site settings). |
| Add languages and configure negotiation | [Language Setup](language-setup.md), [Language Negotiation](language-negotiation.md) | When initializing a multilingual site — adding languages, setting default language, configuring language fallback. |
| Enable content translation for entities | [Content Translation Setup](content-translation-setup.md) | When enabling entity translation for nodes, taxonomy terms, media, blocks, menu links, or custom entities. |
| Translate nodes, terms, or media | [Translating Content Entities](translating-content-entities.md) | When creating or managing translations for nodes, taxonomy terms, media, blocks, menu links. |
| Control which fields are translatable | [Field Translatability](field-translatability.md) | When configuring which fields should have separate values per language vs shared values across all translations. |
| Handle translated revisions | [Translation & Revisions](translation-revisions.md) | When working with revisionable entities (nodes, media, custom entities) that support both translation and revision tracking. |
| Translate config (views, menus, field labels) | [Config Translation](config-translation.md) | When translating configuration entities and simple config: views, menus, field labels, site name, content type labels, block labels. |
| Import/export interface translations (.po files) | [Interface Translation](interface-translation.md) | When translating UI strings, system messages, form labels, module-provided text — anything wrapped in `t()` or `TranslatableMarkup`. |
| Use t() and TranslatableMarkup correctly | [TranslatableMarkup & t()](translatable-markup.md) | When translating UI strings in PHP code — form labels, system messages, error messages, navigation text. |
| Add translations programmatically | [Programmatic Entity Translation](programmatic-entity-translation.md) | When creating or managing entity translations in code — migrations, import scripts, automated workflows, REST API endpoints. |
| Translate text in Twig templates | [Twig Translation](twig-translation.md) | When translating text in Twig templates — theme templates, custom template files, template suggestions. |
| Configure URL prefixes or domains | [URL & Language Routing](url-language-routing.md) | When configuring multilingual URLs — path prefixes, domains, path aliases, hreflang tags for SEO. |
| Query entities by language | [Language-Aware Queries](language-aware-queries.md) | When querying entities by language — Views filters, entity queries, getting content in specific language. |
| Implement translation workflows | [Translation Workflows](translation-workflows.md) | When implementing translation processes beyond basic UI — professional translation services, translation jobs, external translators, automated workflows. |
| Make my custom module translatable | [Translating Custom Modules](translating-custom-modules.md) | When developing custom modules that need to support multilingual sites — providing translatable strings, config, and .po files. |
| Know about Drupal 11 deprecations | [Drupal 11 Changes](drupal-11-changes.md) | When upgrading to Drupal 11 or maintaining modules compatible with Drupal 11.x. |
| Follow best practices | [Best Practices](best-practices.md), [Anti-Patterns](anti-patterns.md) | When planning multilingual architecture, deployment workflows, or optimizing translation management. |
| Understand security and performance | [Security, Performance & Caching](security-performance-caching.md) | When optimizing multilingual site performance, securing translation access, or debugging cache issues. |
| Find core files and services | [Code Reference Map](code-reference-map.md) |  |
| Check source references and maintenance notes | [Sources & Maintenance](sources-maintenance.md) |  |
