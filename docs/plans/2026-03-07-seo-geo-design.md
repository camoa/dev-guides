# Drupal SEO & GEO Guide — Design Document

## Overview

A comprehensive, recipe-first guide covering traditional SEO configuration and Generative Engine Optimization (GEO) for Drupal 11. Organized in 5 layers progressing from foundation to AI discoverability.

**Topic key:** `drupal/seo-geo`
**Estimated guides:** 27 atomic decision guides
**Audience:** Both site builders (admin UI config) and developers (custom plugins, hooks)
**Drupal version:** 11.x (11.3+ for recipe support)

## Approach

**Recipe-layered** — start with the Drupal CMS SEO recipes as baseline, then layer customizations by concern area. Each guide is an atomic decision reference following the existing format (When to Use → Decision → Pattern → Anti-patterns).

## Research Summary

### SEO Recipes (Drupal CMS)

Two complementary recipes, both stable (2.0.1, February 2026), requiring Drupal 11.3+:

- **drupal_cms_seo_basic** — Pathauto, Redirect, Easy Breadcrumb, Token
- **drupal_cms_seo_tools** — Metatag, Yoast SEO, Simple Sitemap, SEO Checklist, ECA, Field Group, Focal Point

### Metatag Ecosystem

- **Metatag 2.2.0** (September 2025) — 11 submodules including Open Graph, Twitter Cards, hreflang, Dublin Core
- **Schema Metatag 3.0.4** (February 2026) — JSON-LD via Metatag tokens, 25 Schema.org types
- Cascading inheritance: Global → Content type → Per-entity overrides

### Schema.org Blueprints (schemadotorg)

- **1.0.0-alpha37** (March 2026) — still alpha, ~210 installs
- Schema-first content modeling: Schema.org types generate Drupal content types + fields
- 50+ submodules including schemadotorg_jsonld for automatic JSON-LD
- Best for greenfield projects; not a drop-in replacement for schema_metatag on existing sites

### GEO (Generative Engine Optimization)

- Coined by Princeton/Georgia Tech 2023 paper (KDD 2024)
- Key strategies: cite sources (+40% visibility), add statistics, expert quotations
- Schema markup makes pages 3x more likely to be referenced by AI platforms
- llms.txt standard (September 2024, Jeremy Howard) — adopted by Cloudflare, Supabase, Stripe, Anthropic
- Drupal AEO module (drupal/aeo) — automated AI search readiness scoring
- AI crawlers: GPTBot, ClaudeBot, PerplexityBot — block training, allow search/retrieval

## Guide Structure

### Layer 1: Foundation (SEO Recipe)

| # | Guide | Covers |
|---|-------|--------|
| 1 | Overview | SEO vs GEO landscape, module stack decision tree |
| 2 | SEO Recipe Baseline | drupal_cms_seo_basic + drupal_cms_seo_tools — what they install, what you get |
| 3 | Pathauto Patterns | URL alias patterns, token strategies, bulk generation |
| 4 | Redirect Management | 301/302 redirects, redirect_404, alias change auto-redirects |
| 5 | Breadcrumbs & Structured Data | Easy Breadcrumb config, JSON-LD BreadcrumbList |

### Layer 2: Meta Tags & Social

| # | Guide | Covers |
|---|-------|--------|
| 6 | Metatag Architecture | Module overview, cascading inheritance, token system |
| 7 | Core Meta Tags | Title, description, canonical, robots per content type |
| 8 | Open Graph | og:title, og:image, og:type — Facebook/LinkedIn/WhatsApp/Slack |
| 9 | Twitter Cards | Card types, fallback to OG, twitter:site/creator |
| 10 | Metatag for Multilingual | hreflang automation, language-specific overrides |

### Layer 3: Structured Data (JSON-LD)

| # | Guide | Covers |
|---|-------|--------|
| 11 | Structured Data Decision | Schema Metatag vs Schema.org Blueprints — when to use which |
| 12 | Schema Metatag Setup | Install, configure Article/Organization/WebPage, token mappings |
| 13 | Schema Types Reference | Article, FAQPage, Product, HowTo, Event, Person, Organization |
| 14 | Schema.org Blueprints | Schema-first content modeling, schemadotorg_jsonld, drush commands |
| 15 | Custom Schema Types | Extending schema_metatag with custom plugins |
| 16 | Testing & Validation | Rich Results Test, Schema.org validator, debugging JSON-LD |

### Layer 4: Technical SEO

| # | Guide | Covers |
|---|-------|--------|
| 17 | XML Sitemap | Simple Sitemap vs XML Sitemap, config, multilingual, IndexNow |
| 18 | Robots.txt | Core robots.txt, custom rules, AI crawler policies |
| 19 | Canonical URLs | Canonical tag strategy, duplicate content, domain redirects |
| 20 | Performance & Core Web Vitals | LCP/FID/CLS, Drupal caching + CDN, image optimization |
| 21 | SEO Audit Workflow | SEO Checklist module, Yoast/Real-time SEO, audit patterns |

### Layer 5: Generative Engine Optimization (GEO)

| # | Guide | Covers |
|---|-------|--------|
| 22 | GEO Overview | What GEO is, Princeton research, citation metrics |
| 23 | Content Patterns for AI | Answer-first design, entity salience, statistics, citations |
| 24 | llms.txt Implementation | The standard, Drupal implementation, per-topic bundling |
| 25 | AI Crawler Policy | robots.txt for AI crawlers — training vs search vs retrieval |
| 26 | Schema.org for AI Discovery | Priority schema types for GEO, SpeakableSpecification, stacking |
| 27 | AEO Module & AI Scoring | drupal/aeo — readiness scoring, auto-fix drafts, AI content |

## Key Sources

- Drupal CMS SEO Basic: drupal.org/project/drupal_cms_seo_basic
- Drupal CMS SEO Tools: drupal.org/project/drupal_cms_seo_tools
- Metatag: drupal.org/project/metatag (2.2.0)
- Schema Metatag: drupal.org/project/schema_metatag (3.0.4)
- Schema.org Blueprints: drupal.org/project/schemadotorg (alpha37)
- AEO Module: drupal.org/project/aeo
- GEO Paper: arxiv.org/abs/2311.09735
- llms.txt Spec: llmstxt.org
- Simple Sitemap: drupal.org/project/simple_sitemap (4.2.3)
- Pathauto: drupal.org/project/pathauto (1.14)
- Redirect: drupal.org/project/redirect (1.12)
