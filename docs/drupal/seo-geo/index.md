---
description: Drupal SEO & GEO — search engine optimization, structured data, meta tags, and generative engine optimization for Drupal 11
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
  specializes: ""
  category: drupal
---

# Drupal SEO & GEO

> Recipe-first approach to SEO and GEO. Start with the Drupal CMS SEO recipes as the baseline, then layer in meta tags, structured data, technical configuration, and AI discoverability. Traditional SEO and Generative Engine Optimization share the same foundation — structured, authoritative, well-tagged content.

## Foundation

| I need to... | Guide |
|-------------|-------|
| Understand the SEO/GEO landscape and module stack | [Overview](overview.md) |
| Start with the Drupal CMS SEO recipes | [SEO Recipe Baseline](seo-recipe-baseline.md) |
| Configure clean URL aliases | [Pathauto Patterns](pathauto-patterns.md) |
| Manage redirects and prevent 404s | [Redirect Management](redirect-management.md) |
| Add breadcrumb structured data | [Breadcrumbs & Structured Data](breadcrumbs-structured-data.md) |

## Meta Tags & Social

| I need to... | Guide |
|-------------|-------|
| Understand the Metatag module system | [Metatag Architecture](metatag-architecture.md) |
| Configure title, description, canonical | [Core Meta Tags](core-meta-tags.md) |
| Add Open Graph tags for social sharing | [Open Graph](open-graph.md) |
| Configure Twitter/X Cards | [Twitter Cards](twitter-cards.md) |
| Handle meta tags for multilingual sites | [Metatag for Multilingual](metatag-multilingual.md) |

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
