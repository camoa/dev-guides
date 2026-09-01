---
description: Drupal SEO & GEO — search engine optimization, structured data, meta tags, and generative engine optimization for Drupal 11
tracks:
  - project: metatag
    channel: stable
    declared: "2.2.0"
    verified: 2026-08-17
  - project: simple_sitemap
    channel: stable
    declared: "4.2.3"
    verified: 2026-08-17
  - project: pathauto
    channel: stable
    declared: "8.x-1.15"
    verified: 2026-08-17
  - project: redirect
    channel: stable
    declared: "8.x-1.13"
    verified: 2026-08-17
  - project: schema_metatag
    channel: stable
    declared: "3.0.4"
    verified: 2026-08-17
  - project: schemadotorg
    channel: alpha
    reason: project has never had a stable release
    declared: "1.0.0-alpha38"
    verified: 2026-08-17
guide-meta:
  concepts:
    - SEO recipes
    - Pathauto
    - Metatag module
    - Open Graph
    - Twitter Cards
    - JSON-LD structured data
    - Schema.org
    - sitemap
    - GEO
    - generative engine optimization
  not:
    - Google Analytics setup
    - search API indexing
  requires: []
  complements:
    - drupal/breadcrumbs
    - drupal/multilingual
    - drupal/recipes
  category: drupal
---

# Drupal SEO & GEO

> Recipe-first approach to SEO and GEO. Start with the Drupal CMS SEO recipes as the baseline, then layer in meta tags, structured data, technical configuration, and AI discoverability. Traditional SEO and Generative Engine Optimization share the same foundation — structured, authoritative, well-tagged content.

## Foundation

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the SEO/GEO landscape and module stack | [Overview](overview.md) | Read this guide first. It maps the entire SEO/GEO module landscape, explains why GEO extends rather than replaces traditional SEO, and gives you the decision tree for which modules to install before you touch configuration. |
| Start with the Drupal CMS SEO recipes | [SEO Recipe Baseline](seo-recipe-baseline.md) | Start here when setting up SEO for any Drupal 11.3+ site. The two Drupal CMS SEO recipes give you a battle-tested module stack with sane defaults in minutes. |
| Configure clean URL aliases | [Pathauto Patterns](pathauto-patterns.md) | Configure Pathauto when you need clean, SEO-friendly URL aliases generated automatically from content fields. Pathauto runs on every node/term/user save and applies your token-based pattern to produce the alias — no manual entry required. |
| Manage redirects and prevent 404s | [Redirect Management](redirect-management.md) | Use the Redirect module whenever URL aliases change, content moves, or domains migrate. A site without redirect management bleeds SEO equity every time a URL changes — search engines and users hit 404s that could be 301s. |
| Add breadcrumb structured data | [Breadcrumbs & Structured Data](breadcrumbs-structured-data.md) | Add JSON-LD `BreadcrumbList` structured data to help Google display breadcrumb trails in search results instead of bare URLs. This is a quick SEO win — one checkbox if you have Easy Breadcrumb installed. |

## Meta Tags & Social

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the Metatag module system | [Metatag Architecture](metatag-architecture.md) | You are setting up meta tags on a Drupal 11 site. Start here to understand how the Metatag module is structured before configuring individual tags or submodules. |
| Configure title, description, canonical | [Core Meta Tags](core-meta-tags.md) | You need to configure the foundational meta tags — title, description, canonical, and robots — that affect search engine indexing and click-through rates. These are configured in the Metatag module's core submodule (always enabled) at… |
| Add Open Graph tags for social sharing | [Open Graph](open-graph.md) | You need content shared on Facebook, LinkedIn, WhatsApp, or Slack to display a rich preview with title, image, and description instead of a bare URL. Enable the `metatag_open_graph` submodule and configure token-based defaults for each… |
| Configure Twitter/X Cards | [Twitter Cards](twitter-cards.md) | You need content shared on Twitter/X to display a rich card preview rather than a bare link. Enable the `metatag_twitter_cards` submodule. |
| Handle meta tags for multilingual sites | [Metatag for Multilingual](metatag-multilingual.md) | You have a multilingual Drupal 11 site with content translated into multiple languages. Without hreflang tags, Google may treat translated pages as duplicate content or serve the wrong language to users. |

## Structured Data (JSON-LD)

| I need to... | Guide |
|-------------|-------|
| Choose between Schema Metatag and Schema.org Blueprints | [Structured Data Decision](structured-data-decision.md) |
| Set up Schema Metatag with token mappings | [Schema Metatag Setup](schema-metatag-setup.md) |
| Map content types to Schema.org types | [Schema Types Reference](schema-types-reference.md) |
| Use Schema.org Blueprints for new builds | [Schema.org Blueprints](schemadotorg-blueprints.md) |
| Create custom Schema.org type plugins | [Custom Schema Types](custom-schema-types.md) |
| Test and validate structured data output | [Testing & Validation](testing-validation.md) |

## Technical SEO

| I need to... | Guide |
|-------------|-------|
| Generate and configure XML sitemaps | [XML Sitemap](xml-sitemap.md) |
| Configure robots.txt rules | [Robots.txt](robots-txt.md) |
| Prevent duplicate content with canonicals | [Canonical URLs](canonical-urls.md) |
| Optimize Core Web Vitals | [Performance & Core Web Vitals](performance-core-web-vitals.md) |
| Run an SEO audit | [SEO Audit Workflow](seo-audit-workflow.md) |

## Generative Engine Optimization (GEO)

| I need to... | Guide |
|-------------|-------|
| Understand GEO and AI search optimization | [GEO Overview](geo-overview.md) |
| Write content that AI systems cite | [Content Patterns for AI](content-patterns-ai.md) |
| Implement llms.txt for my Drupal site | [llms.txt Implementation](llms-txt-implementation.md) |
| Control AI crawler access | [AI Crawler Policy](ai-crawler-policy.md) |
| Use structured data for AI discoverability | [Schema.org for AI Discovery](schema-ai-discovery.md) |
| Score and improve AI search readiness | [AEO Module & AI Scoring](aeo-module.md) |
