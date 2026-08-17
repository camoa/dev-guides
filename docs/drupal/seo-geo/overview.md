---
description: Drupal SEO & GEO overview — the module stack landscape, two Drupal CMS SEO recipes, decision tree for which modules to install, and how this guide is organized
tldr: "Read this guide first. It maps the entire SEO/GEO module landscape, explains why GEO extends rather than replaces traditional SEO, and gives you the decision tree for which modules to install before you touch configuration."
drupal_version: "11.x"
---

# Overview: SEO & GEO for Drupal 11

## When to Use

> Read this guide first. It maps the entire SEO/GEO module landscape, explains why GEO extends rather than replaces traditional SEO, and gives you the decision tree for which modules to install before you touch configuration.

## The SEO vs GEO Landscape

Traditional SEO optimizes for search engine crawlers — Googlebot, Bingbot. The goal is ranking in the 10 blue links. Generative Engine Optimization (GEO) optimizes for AI retrieval systems — ChatGPT, Perplexity, Google AI Overviews, Claude. The goal is being cited in AI-generated answers.

They share the same foundation. The same well-structured, authoritative, schema-tagged content that ranks well in traditional search is the content AI systems extract and cite. GEO is an extension layer, not a replacement.

| Dimension | Traditional SEO | GEO |
|-----------|-----------------|-----|
| Target system | Search engine crawlers | AI retrieval and generation systems |
| Primary signal | Backlinks, authority, relevance | Structured data, entity salience, citation patterns |
| Success metric | SERP position, organic traffic | Citation frequency, AI mention share |
| Content focus | Keyword targeting, long-tail queries | Answer-first design, self-contained sections |
| Key technical layer | Meta tags, sitemaps, canonicals | JSON-LD schema, llms.txt, SpeakableSpecification |
| Drupal tooling | Metatag, Pathauto, Simple Sitemap | Schema Metatag, AEO module, llms.txt routes |

**The 2026 reality:** AI Overviews appear in approximately 16% of Google searches. ChatGPT has 800M+ weekly active users. Critically, 83.3% of AI Overview citations come from content beyond the top-10 organic results — meaning structured, well-tagged content can earn AI citations even without top organic rankings. The Princeton/Georgia Tech research (KDD 2024) demonstrated that specific content strategies — citing sources, adding statistics, including expert quotations — increased AI citation frequency by 30-40%.

## The Two Drupal CMS SEO Recipes

Drupal CMS ships two complementary recipes that together provide a complete SEO baseline. Both are stable (2.0.1, February 2026) and require Drupal 11.3+.

### drupal_cms_seo_basic

The foundational layer. Installs infrastructure modules that every Drupal site should have.

| Module | Purpose |
|--------|---------|
| Pathauto | Automatic URL alias generation from tokens |
| Redirect | 301/302 redirect management, redirect_404 logging |
| Easy Breadcrumb | Configurable breadcrumbs with JSON-LD BreadcrumbList output |
| Token | Token system required by Pathauto and Metatag |

### drupal_cms_seo_tools

The editorial and visibility layer. Installs tooling for content editors and search engine submission.

| Module | Purpose |
|--------|---------|
| Metatag | Meta tag management with cascading inheritance (11 submodules) |
| Real-time SEO (Yoast) | Content scoring, readability analysis, focus keyword tracking |
| Simple Sitemap | XML sitemap generation with multilingual support and IndexNow |
| SEO Checklist | Task-based audit dashboard for SEO configuration |
| ECA | Event-Condition-Action automation (used for SEO workflows) |
| Field Group | Field grouping in entity forms (used for SEO field organization) |
| Focal Point | Image focal point for cropping (used for OG image optimization) |

### What the recipes do NOT install

Structured data (JSON-LD schema) requires additional modules beyond the recipes:

- **Schema Metatag** — for existing sites adding JSON-LD via Metatag tokens
- **Schema.org Blueprints** — for greenfield builds doing schema-first content modeling
- **AEO module** — for AI readiness scoring and automated content audits

## Module Stack Decision Tree

### Step 1: Always start here

Apply `drupal_cms_seo_basic` on every Drupal 11.3+ site. It provides infrastructure that all other SEO configuration depends on.

```bash
composer require drupal/drupal_cms_seo_basic
```

If you are building a Drupal CMS site (not vanilla Drupal), the recipes may already be applied. Check with `drush pm:list | grep pathauto`.

### Step 2: Apply drupal_cms_seo_tools when you need editorial tooling

| Situation | Apply drupal_cms_seo_tools? |
|-----------|----------------------------|
| Site has content editors who need SEO guidance | Yes |
| You need meta tag management beyond Drupal core | Yes |
| You need XML sitemaps | Yes |
| API-only or headless Drupal site | No — manage meta tags in the frontend layer |
| Site is already using metatag independently | Evaluate conflicts first |

### Step 3: Add structured data modules based on project type

| Situation | Module | Why |
|-----------|--------|-----|
| Retrofitting existing site with JSON-LD | Schema Metatag 3.0.4 | Token-based, stable, integrates with Metatag admin UI |
| Greenfield build, schema-first approach | Schema.org Blueprints 1.0.0-alpha38 | Generates content types from schema — but still alpha |
| Both rich snippets now AND schema-first architecture | Both together | Schema Metatag for immediate output, Blueprints for new content types |
| Minimal install, custom JSON-LD | `hook_page_attachments` | Roll your own — only for simple, single-type cases |

### Step 4: Add GEO tooling based on AI discoverability goals

| Goal | Module/Approach |
|------|----------------|
| Audit AI readiness and score content | AEO module (`drupal/aeo`) |
| Expose structured content index to AI systems | llms.txt (custom route or static file) |
| Block AI training crawlers, allow search crawlers | robots.txt configuration |
| Optimize for AI citation frequency | Content patterns — no module, editorial approach |

## Full Module Stack Reference

| Module | Version | Layer | Required? |
|--------|---------|-------|-----------|
| Pathauto | 8.x-1.15 | Foundation | Yes, via recipe |
| Redirect | 8.x-1.13 | Foundation | Yes, via recipe |
| Easy Breadcrumb | — | Foundation | Yes, via recipe |
| Token | — | Foundation | Yes, via recipe |
| Metatag | 2.2.0 | Meta tags | Yes, via recipe |
| Simple Sitemap | 4.2.3 | Technical SEO | Yes, via recipe |
| Real-time SEO (Yoast) | — | Editorial | Via recipe |
| SEO Checklist | 5.2.x | Editorial | Via recipe |
| Schema Metatag | 3.0.4 | Structured data | Add manually |
| Schema.org Blueprints | 1.0.0-alpha38 | Structured data | Add manually (greenfield) |
| AEO | — | GEO | Add manually |

## How This Guide Is Organized

Five layers, each with atomic decision guides:

**Layer 1 — Foundation:** SEO recipe baseline, Pathauto URL patterns, redirect management, breadcrumbs. Start here if you are configuring a new site.

**Layer 2 — Meta Tags & Social:** Metatag module architecture, core tags (title/description/canonical), Open Graph for social sharing, Twitter/X Cards, multilingual hreflang. The Metatag module is the hub for all of this.

**Layer 3 — Structured Data:** The most consequential layer for both traditional SEO rich snippets and GEO citation. Covers the Schema Metatag vs Schema.org Blueprints decision, setup, the 25 supported schema types, custom type plugins, and validation.

**Layer 4 — Technical SEO:** XML sitemaps, robots.txt, canonical URL strategy, Core Web Vitals, and the SEO audit workflow using the SEO Checklist and Yoast modules.

**Layer 5 — GEO:** What GEO is, content patterns proven to increase AI citation, llms.txt implementation, AI crawler access policy, schema types that AI systems specifically use, and the AEO scoring module.

## Common Mistakes

- **Wrong**: Installing Schema Metatag on a greenfield build → **Right**: Evaluate Schema.org Blueprints first; its schema-first modeling produces better structured output at the cost of alpha stability
- **Wrong**: Treating GEO as a separate discipline from SEO → **Right**: GEO extends SEO — build the structured data, canonical URLs, and authority signals that serve both
- **Wrong**: Applying `drupal_cms_seo_tools` on a headless Drupal site → **Right**: On decoupled sites, meta tags are a frontend concern; the recipe installs modules you will not use
- **Wrong**: Skipping the `drupal_cms_seo_basic` recipe and installing modules ad hoc → **Right**: The recipe configures default patterns and module settings you would otherwise have to configure manually
- **Wrong**: Assuming top-10 organic ranking is required for AI citations → **Right**: 83.3% of AI Overview citations come from beyond top-10 results; structured data and authority signals matter more than rank

## See Also

- [SEO Recipe Baseline](seo-recipe-baseline.md)
- [Structured Data Decision](structured-data-decision.md)
- [GEO Overview](geo-overview.md)
- Reference: [drupal_cms_seo_basic](https://www.drupal.org/project/drupal_cms_seo_basic)
- Reference: [drupal_cms_seo_tools](https://www.drupal.org/project/drupal_cms_seo_tools)
- Reference: [GEO — Generative Engine Optimization](https://arxiv.org/abs/2311.09735) (Princeton/Georgia Tech, KDD 2024)
