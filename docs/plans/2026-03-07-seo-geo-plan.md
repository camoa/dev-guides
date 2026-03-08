# Drupal SEO & GEO Guide — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create 27 atomic decision guides for Drupal SEO & GEO configuration under `docs/drupal/seo-geo/`.

**Architecture:** Recipe-layered approach — 5 layers from foundation (SEO recipes) through meta tags, structured data, technical SEO, to GEO. Each guide follows the existing format: YAML frontmatter → H1 → When to Use → Decision table → Pattern → Common Mistakes → See Also.

**Tech Stack:** MkDocs Material, Markdown, YAML frontmatter (`description`, `drupal_version`)

---

## Guide Format Reference

Every guide follows this structure (from existing guides like `docs/drupal/forms/architecture-core-classes.md`):

```markdown
---
description: One-line description for SEO and LLM consumption
drupal_version: "11.x"
---

# Guide Title

## When to Use

> One-paragraph decision context.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| ... | ... | ... |

## Pattern

[Code examples, configuration steps, admin paths]

## Common Mistakes

- **Wrong**: ... → **Right**: ...

## See Also

- [Related Guide](filename.md)
- Reference: [External link](url)
```

## File Naming Convention

Kebab-case, no numeric prefix. Example: `pathauto-patterns.md`, `open-graph.md`, `geo-overview.md`.

## Research Sources

Each guide should draw from the research agents' findings. Key sources:

- **SEO Recipes:** drupal.org/project/drupal_cms_seo_basic, drupal_cms_seo_tools (both 2.0.1)
- **Metatag:** drupal.org/project/metatag (2.2.0) — 11 submodules, cascading inheritance
- **Schema Metatag:** drupal.org/project/schema_metatag (3.0.4) — 25 Schema.org types, JSON-LD via tokens
- **Schema.org Blueprints:** drupal.org/project/schemadotorg (alpha37) — schema-first content modeling
- **Simple Sitemap:** drupal.org/project/simple_sitemap (4.2.3) — IndexNow, multilingual
- **Pathauto:** drupal.org/project/pathauto (1.14)
- **Redirect:** drupal.org/project/redirect (1.12)
- **AEO Module:** drupal.org/project/aeo — AI readiness scoring
- **GEO Paper:** arxiv.org/abs/2311.09735 — Princeton/Georgia Tech foundational research
- **llms.txt:** llmstxt.org — specification by Jeremy Howard

---

## Task 1: Create index.md and overview.md

**Files:**
- Create: `docs/drupal/seo-geo/index.md`
- Create: `docs/drupal/seo-geo/overview.md`

**Step 1: Create the directory**

```bash
mkdir -p docs/drupal/seo-geo
```

**Step 2: Write index.md**

The index follows the "I need to..." table pattern. List all 27 guides organized by layer with section headers.

```markdown
---
description: Drupal SEO & GEO — search engine optimization, structured data, meta tags, and generative engine optimization for Drupal 11
---

# Drupal SEO & GEO

> Recipe-first approach to SEO and GEO. Start with the Drupal CMS SEO recipes, then customize meta tags, structured data, technical SEO, and AI discoverability.

## Foundation

| I need to... | Guide |
|-------------|-------|
| Understand the SEO/GEO landscape | [Overview](overview.md) |
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
| Choose between Schema Metatag and Blueprints | [Structured Data Decision](structured-data-decision.md) |
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
```

**Step 3: Write overview.md**

Cover: what SEO/GEO is, the module stack landscape, decision tree for which modules to install, and how the guide is organized.

**Step 4: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add index and overview guides"
```

---

## Task 2: Layer 1 — Foundation guides (3 files)

**Files:**
- Create: `docs/drupal/seo-geo/seo-recipe-baseline.md`
- Create: `docs/drupal/seo-geo/pathauto-patterns.md`
- Create: `docs/drupal/seo-geo/redirect-management.md`
- Create: `docs/drupal/seo-geo/breadcrumbs-structured-data.md`

**Step 1: Write seo-recipe-baseline.md**

Cover:
- What the two recipes install (drupal_cms_seo_basic: Pathauto, Redirect, Easy Breadcrumb, Token; drupal_cms_seo_tools: Metatag, Yoast SEO, Simple Sitemap, SEO Checklist, ECA, Field Group, Focal Point)
- Decision: apply both vs selective install
- Composer commands, Drupal 11.3+ requirement
- What config the recipes provide out of the box

**Step 2: Write pathauto-patterns.md**

Cover:
- Pattern syntax with tokens (`/blog/[node:title]`, `[node:content-type]/[node:title]`)
- Per-content-type patterns
- Bulk generation and update strategies
- Transliteration settings
- Common mistakes: not enabling clean URLs, duplicate aliases

**Step 3: Write redirect-management.md**

Cover:
- Manual redirect creation (admin/config/search/redirect)
- redirect_404 submodule for logging and bulk fixing
- Auto-redirect on alias change (Pathauto integration)
- Status codes: 301 vs 302 decision
- Redirect Domain submodule for domain migrations

**Step 4: Write breadcrumbs-structured-data.md**

Cover:
- Easy Breadcrumb config and JSON-LD BreadcrumbList output
- Decision: Easy Breadcrumb built-in vs manual hook_page_attachments vs Metatag Schema
- Reference existing breadcrumbs guide for detailed patterns

**Step 5: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add foundation layer guides (recipe, pathauto, redirects, breadcrumbs)"
```

---

## Task 3: Layer 2 — Meta Tags & Social guides (5 files)

**Files:**
- Create: `docs/drupal/seo-geo/metatag-architecture.md`
- Create: `docs/drupal/seo-geo/core-meta-tags.md`
- Create: `docs/drupal/seo-geo/open-graph.md`
- Create: `docs/drupal/seo-geo/twitter-cards.md`
- Create: `docs/drupal/seo-geo/metatag-multilingual.md`

**Step 1: Write metatag-architecture.md**

Cover:
- Module overview, 11 submodules, attribute-based plugins (2.2.0)
- Cascading inheritance: Global → Content type → Per-entity
- Token system for dynamic values
- Admin path: /admin/config/search/metatag
- Dependency: Token module

**Step 2: Write core-meta-tags.md**

Cover:
- Title tag patterns with tokens
- Meta description strategy
- Canonical URL configuration
- Robots meta (noindex, nofollow) per content type
- Metatag defaults for Global, Front Page, Content, Taxonomy

**Step 3: Write open-graph.md**

Cover:
- Enable metatag_open_graph submodule
- Key tags: og:title, og:description, og:image, og:url, og:type, og:site_name
- Token mappings for each tag
- Image requirements (1200x630 minimum)
- Platform-specific behavior: Facebook, LinkedIn, WhatsApp, Slack
- Debugging: Facebook Sharing Debugger, LinkedIn Post Inspector

**Step 4: Write twitter-cards.md**

Cover:
- Enable metatag_twitter_cards submodule
- Card types: summary, summary_large_image
- Key tags: twitter:card, twitter:title, twitter:description, twitter:image, twitter:site
- Fallback strategy: OG tags as defaults
- Twitter Card Validator

**Step 5: Write metatag-multilingual.md**

Cover:
- metatag_hreflang submodule
- Automatic hreflang generation for translated content
- x-default tag configuration
- Language-specific meta tag overrides
- Integration with Drupal's content translation system

**Step 6: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add meta tags & social layer guides (metatag, OG, twitter, multilingual)"
```

---

## Task 4: Layer 3 — Structured Data guides (6 files)

**Files:**
- Create: `docs/drupal/seo-geo/structured-data-decision.md`
- Create: `docs/drupal/seo-geo/schema-metatag-setup.md`
- Create: `docs/drupal/seo-geo/schema-types-reference.md`
- Create: `docs/drupal/seo-geo/schemadotorg-blueprints.md`
- Create: `docs/drupal/seo-geo/custom-schema-types.md`
- Create: `docs/drupal/seo-geo/testing-validation.md`

**Step 1: Write structured-data-decision.md**

Cover:
- Decision table: Schema Metatag (retrofit existing sites) vs Schema.org Blueprints (greenfield)
- JSON-LD vs Microdata vs RDFa — JSON-LD is Google's recommendation
- When to use both together
- Stability comparison: Schema Metatag 3.0.4 (stable) vs schemadotorg alpha37

**Step 2: Write schema-metatag-setup.md**

Cover:
- Install: `composer require drupal/schema_metatag:^3.0`
- Enable submodules: schema_article, schema_web_page, schema_organization
- Configure at /admin/config/search/metatag
- Token mappings for Article: @type, name, datePublished, dateModified, author, image, publisher
- Organization setup for publisher reference
- Per-content-type configuration

**Step 3: Write schema-types-reference.md**

Cover:
- Table of all 25 supported top-level types with their key properties
- Priority types for GEO: Article, FAQPage, Product, HowTo, Organization
- Field-to-property mapping patterns
- Nested types: PostalAddress, Offer, Rating, BreadcrumbList
- Which content types map to which schema types

**Step 4: Write schemadotorg-blueprints.md**

Cover:
- What it is: Schema.org-first content modeling
- When to use: greenfield builds, decoupled sites, standardized API output
- Drush commands: `drush schemadotorg:create-type node:Event`
- schemadotorg_jsonld for automatic JSON-LD
- Key submodules overview
- Alpha stability warning and migration considerations

**Step 5: Write custom-schema-types.md**

Cover:
- When the 25 built-in types aren't enough
- Creating a custom schema_metatag plugin (attribute-based in 2.2.0+)
- Plugin structure: SchemaType attribute, property definitions
- Example: adding LocalBusiness or MedicalEntity
- Testing custom types with Rich Results Test

**Step 6: Write testing-validation.md**

Cover:
- Google Rich Results Test (search.google.com/test/rich-results)
- Schema.org Validator (validator.schema.org)
- Chrome DevTools: inspect JSON-LD in page source
- Drupal debugging: view rendered metatags, check token values
- Common validation errors and fixes
- Automated testing with Drush or CI

**Step 7: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add structured data layer guides (schema metatag, blueprints, validation)"
```

---

## Task 5: Layer 4 — Technical SEO guides (5 files)

**Files:**
- Create: `docs/drupal/seo-geo/xml-sitemap.md`
- Create: `docs/drupal/seo-geo/robots-txt.md`
- Create: `docs/drupal/seo-geo/canonical-urls.md`
- Create: `docs/drupal/seo-geo/performance-core-web-vitals.md`
- Create: `docs/drupal/seo-geo/seo-audit-workflow.md`

**Step 1: Write xml-sitemap.md**

Cover:
- Decision: Simple Sitemap (recommended) vs XML Sitemap
- Simple Sitemap 4.2.3: config, entity inclusion, priority, changefreq
- Multilingual sitemap with hreflang
- IndexNow support (simple_sitemap_engines submodule)
- Image sitemaps for Google
- Admin path: /admin/config/search/simplesitemap

**Step 2: Write robots-txt.md**

Cover:
- Drupal core robots.txt location and behavior
- drupal_cms_seo_tools robots.append.txt pattern
- Common rules: disallow admin, files, private paths
- Sitemap reference in robots.txt
- AI crawler section (reference to AI Crawler Policy guide in Layer 5)

**Step 3: Write canonical-urls.md**

Cover:
- Metatag canonical URL configuration
- Drupal's default canonical handling
- Avoiding duplicate content: www vs non-www, trailing slashes
- Redirect module for domain-level canonicalization
- Multilingual canonical with hreflang
- Pagination canonicalization

**Step 4: Write performance-core-web-vitals.md**

Cover:
- LCP, INP (replaces FID), CLS definitions and Drupal impact
- Drupal caching layers: page cache, dynamic page cache, render cache
- BigPipe for perceived performance
- Image optimization: responsive images, WebP/AVIF, lazy loading
- CDN integration patterns
- Aggregation: CSS/JS optimization

**Step 5: Write seo-audit-workflow.md**

Cover:
- SEO Checklist module (seo_checklist 5.2.x) — task-based audit
- Yoast SEO (Real-time SEO) module — content scoring, readability
- Manual audit checklist: meta tags, structured data, sitemaps, redirects
- Google Search Console integration
- Ongoing monitoring patterns

**Step 6: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add technical SEO layer guides (sitemap, robots, canonicals, performance, audit)"
```

---

## Task 6: Layer 5 — GEO guides (6 files)

**Files:**
- Create: `docs/drupal/seo-geo/geo-overview.md`
- Create: `docs/drupal/seo-geo/content-patterns-ai.md`
- Create: `docs/drupal/seo-geo/llms-txt-implementation.md`
- Create: `docs/drupal/seo-geo/ai-crawler-policy.md`
- Create: `docs/drupal/seo-geo/schema-ai-discovery.md`
- Create: `docs/drupal/seo-geo/aeo-module.md`

**Step 1: Write geo-overview.md**

Cover:
- What GEO is and how it differs from traditional SEO (table comparison)
- The Princeton/Georgia Tech research (arxiv.org/abs/2311.09735)
- Key metrics: citation frequency, AI mention share
- 2026 landscape: ChatGPT 800M+ weekly users, AI Overviews in 16% of searches
- 83.3% of AI Overview citations come from beyond top-10 organic results
- GEO extends SEO — not a replacement

**Step 2: Write content-patterns-ai.md**

Cover:
- Three proven strategies from Princeton research (+30-40% visibility):
  1. Cite sources — add credible citations throughout
  2. Statistics addition — replace qualitative with quantitative
  3. Quotation addition — expert quotes for authenticity
- Entity salience: semantic centrality > keyword density, test with NL API
- Answer-first design: first 200 words must directly answer the query
- Self-contained sections: each section standalone for AI extraction
- Recency signals: 89.7% of ChatGPT citations go to recently updated pages

**Step 3: Write llms-txt-implementation.md**

Cover:
- The llms.txt specification (llmstxt.org)
- Format: H1, blockquote, H2 sections with links
- Drupal implementation options: static file, custom route, build script
- Per-topic bundling pattern (reference this project's own implementation)
- llms-full.txt for RAG vectorization
- Major adopters: Cloudflare, Supabase, Stripe, Anthropic
- Current limitations: no AI company has committed to honoring it at inference time

**Step 4: Write ai-crawler-policy.md**

Cover:
- AI crawler user agents table:
  - OpenAI: GPTBot (training), OAI-SearchBot (search), ChatGPT-User (user-initiated)
  - Anthropic: ClaudeBot (training), Claude-SearchBot (search), Claude-User
  - Google: Google-Extended (Gemini training)
  - Perplexity: PerplexityBot
- Recommended policy: block training, allow search/retrieval
- robots.txt configuration patterns
- Decision tree: full block vs selective vs full allow

**Step 5: Write schema-ai-discovery.md**

Cover:
- Confirmed impact: Google, Microsoft, ChatGPT use structured data for AI features
- GPT-4 accuracy: 16% → 54% with structured data (Data World study)
- Priority schema types for GEO: Article, FAQPage, Product, HowTo, Organization, SpeakableSpecification
- Schema stacking: multiple types per page for richer context
- SpeakableSpecification: marks content for voice/AI readout
- Implementation patterns in Drupal with schema_metatag

**Step 6: Write aeo-module.md**

Cover:
- AEO module (drupal/aeo) — what it does
- Automatic content audits: summaries, FAQs, schema, alt text, author data, freshness
- AEO scoring: 0-100 with category breakdowns (Structure, Schema, Media, E-E-A-T, Freshness)
- Fix suggestions and safe auto-apply (non-destructive drafts)
- Optional AI integration with drupal/ai module
- Decision: when to install AEO vs manual audit workflow

**Step 7: Commit**

```bash
git add docs/drupal/seo-geo/
git commit -m "feat(seo-geo): add GEO layer guides (overview, content patterns, llms.txt, AI crawlers, schema, AEO)"
```

---

## Task 7: Update mkdocs.yml and partition-manifest.json

**Files:**
- Modify: `mkdocs.yml` — add seo-geo section to llmstxt-md plugin config
- Modify: `partition-manifest.json` — add `drupal/seo-geo` entry

**Step 1: Add seo-geo entries to mkdocs.yml llmstxt-md sections**

Add all 28 files (index + 27 guides) under the "Drupal" section, following the existing pattern with descriptions.

**Step 2: Add partition-manifest.json entry**

```json
"drupal/seo-geo": {
  "source_hash": "<computed>",
  "partitioned": "2026-03-07",
  "partitioned_by": "Carlos Ospina",
  "guides_extracted": 27
}
```

**Step 3: Verify mkdocs build**

```bash
mkdocs build 2>&1 | tail -5
```

Expected: "Documentation built in X seconds" with no errors for seo-geo files.

**Step 4: Verify llms.txt generation**

```bash
python3 scripts/generate_llms.py 2>&1 | grep seo-geo
```

Expected: `drupal-seo-geo.txt — 27 guides, XXkb, ~XX,XXX tokens`

**Step 5: Commit**

```bash
git add mkdocs.yml partition-manifest.json
git commit -m "feat(seo-geo): register in mkdocs.yml and partition-manifest"
```

---

## Task 8: Final push and verification

**Step 1: Push all commits**

```bash
git push origin main
```

**Step 2: Watch GitHub Actions**

```bash
gh run list --limit 1 --json status,conclusion
# Wait for completion
gh run watch <run-id> --exit-status
```

**Step 3: Verify live deployment**

```bash
curl -s https://camoa.github.io/dev-guides/llms/drupal-seo-geo.txt | head -20
curl -s https://camoa.github.io/dev-guides/llms.txt | grep seo-geo
```

Expected: per-topic file serves with TOC header, and llms.txt index includes the new topic.
