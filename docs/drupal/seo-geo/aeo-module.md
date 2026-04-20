---
description: Drupal AEO module for automated AI search readiness scoring — audits, 0-100 scoring categories, auto-fix drafts, and optional AI integration
tldr: "You want to audit and score your Drupal content for AI search readiness systematically — not page by page manually. The AEO (AI Engine Optimization) module at drupal.org/project/aeo runs automated content audits against GEO criteria,…"
drupal_version: "11.x"
---

# AEO Module & AI Scoring

## When to Use

> You want to audit and score your Drupal content for AI search readiness systematically — not page by page manually. The AEO (AI Engine Optimization) module at drupal.org/project/aeo runs automated content audits against GEO criteria, produces 0-100 scores per content item, and generates safe, non-destructive fix suggestions. Use it when you have enough content that manual GEO audit is impractical, or when you want measurable baseline scores before and after GEO work.

## Decision

| Situation | Approach | Why |
|-----------|----------|-----|
| <20 pages, starting GEO work | Manual audit with [Content Patterns](content-patterns-ai.md) | AEO overhead not justified for small sites |
| 20-500 pages, ongoing content team | AEO module for scoring + editorial workflow | Score-driven content improvement at scale |
| 500+ pages, existing content | AEO module + bulk audit view | Triage what to fix first by lowest score |
| You have drupal/ai integration | AEO + AI module for AI-generated fix suggestions | AI module generates summaries and FAQ content |
| You want automated improvement | AEO auto-apply on safe categories only | Non-destructive; auto-applies alt text, meta descriptions |

## AEO Module Overview

**Module:** `drupal/aeo`
**Install:** `composer require drupal/aeo`

AEO adds an AI readiness layer on top of Drupal's content editing workflow. It does not modify your published content automatically — all fixes are presented as suggestions or draft revisions.

**What it audits per content item:**

| Audit area | What is checked |
|-----------|----------------|
| Summaries | Is there a concise summary or meta description? Is it <160 chars? |
| FAQs | Does the page have FAQ content? Is it structured for FAQPage schema? |
| Schema markup | Is Article/WebPage/relevant schema present? Are required fields populated? |
| Alt text | Do all images have descriptive alt text? |
| Author data | Is author name and metadata present? (E-E-A-T signal) |
| Freshness | When was the content last substantively updated? |
| Answer-first | Does the first 200 words answer the implied question? |

## AEO Scoring System

Scores are 0-100 per content item, broken into five categories:

| Category | Weight | What it measures |
|----------|--------|-----------------|
| Structure | 25% | Heading hierarchy, answer-first pattern, self-contained sections |
| Schema | 25% | Structured data presence, required properties, type appropriateness |
| Media | 20% | Image alt text, image presence, media optimization |
| E-E-A-T | 20% | Author data, citation quality, credibility signals |
| Freshness | 10% | Last modified date, recent statistics, recency signals in content |

**Score interpretation:**

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | AI-ready | Maintain; set freshness reminder |
| 60-79 | Needs improvement | Address lowest-scoring category first |
| 40-59 | Significant gaps | Structure and Schema fixes likely highest ROI |
| 0-39 | Not AI-ready | Major revision needed; consider whether this content should be prioritized |

## Auto-Apply: Safe Categories Only

AEO's auto-apply feature generates fix suggestions and applies them as drafts — never publishing without human review. "Safe" categories are those where automated changes are non-destructive:

| Category | Auto-apply safe? | Notes |
|----------|-----------------|-------|
| Alt text (missing) | Yes — generates from image filename/context | Always review AI-generated alt text for accuracy |
| Meta description (missing) | Yes — generates from first paragraph | Review for brand voice |
| Schema @type selection | Yes — suggests based on content type | Review before enabling |
| Summary field | Yes — generates draft only | Content team reviews before publish |
| Article body restructure | No — requires human judgment | AEO flags; editor rewrites |
| Adding statistics | No — requires factual accuracy | AEO flags gaps; editor adds data |

Auto-apply creates a new revision marked as draft. The editorial workflow remains: auto-apply → review → publish.

## Optional drupal/ai Integration

If you have the `drupal/ai` module installed and configured with an LLM provider (OpenAI, Anthropic, Ollama, etc.), AEO can use AI to generate suggestions rather than rule-based templates.

**Without drupal/ai:** AEO generates template-based suggestions (e.g., "Add author name to this field")

**With drupal/ai:** AEO generates content-aware suggestions (e.g., generates a 2-sentence summary of the actual page content, suggests FAQ questions derived from the page body)

```
composer require drupal/ai drupal/aeo
drush en ai ai_openai aeo
```

Configure your AI provider at `/admin/config/ai/providers`, then AEO picks it up automatically.

**Cost consideration:** AI-generated suggestions consume LLM API tokens. On a 500-page site, an initial bulk audit with AI generation can cost several dollars. Cache audit results to avoid re-running.

## Pattern: Bulk Audit Workflow

```
1. Install AEO: composer require drupal/aeo && drush en aeo
2. Run initial audit: Admin → Content → AEO Audit (admin/content/aeo)
3. Sort by AEO Score ascending — worst pages first
4. Filter by lowest-scoring category to batch fixes
5. For Schema gaps: use schema_metatag config, not per-page editing
6. For Structure gaps: update content template / editorial guidelines
7. Re-run audit after changes to track score improvement
```

**Admin paths:**
- Bulk audit view: `/admin/content/aeo`
- Per-node score: node edit form → AEO sidebar widget
- AEO settings: `/admin/config/search/aeo`

## AEO vs Manual Audit

| Factor | AEO module | Manual audit |
|--------|-----------|-------------|
| Setup time | ~1 hour | None |
| Per-page time | Seconds (automated) | 10-30 min per page |
| Coverage | All published content | Sample or priority pages |
| Scoring consistency | Consistent algorithmic criteria | Varies by reviewer |
| Fix generation | Automated drafts | Manual editing |
| AI integration | Optional with drupal/ai | Manual research |
| Ongoing monitoring | Continuous scoring on save | Periodic manual review |
| Best for | Sites with 20+ pages, ongoing content | Small sites or one-time audit |

## Common Mistakes

- **Wrong**: Running AEO and auto-applying all suggestions without review → **Right**: Auto-apply is safe for missing fields, but always review AI-generated content for accuracy before publishing
- **Wrong**: Treating AEO score as the goal → **Right**: AEO score is a proxy metric; actual goal is increased AI citation frequency. Validate score improvements against real AI citation changes
- **Wrong**: Fixing individual pages through the node editor → **Right**: For systematic gaps (e.g., all Article nodes missing dateModified), fix at the Schema Metatag or content type level, not page by page
- **Wrong**: Installing AEO without schema_metatag → **Right**: AEO's Schema scoring requires structured data to already be configured; install and configure schema_metatag first
- **Wrong**: Ignoring the E-E-A-T category because it scores lowest → **Right**: Author and credibility signals disproportionately affect AI citation for health, finance, and legal content; E-E-A-T is highest priority for YMYL content

## See Also

- [Content Patterns for AI](content-patterns-ai.md) — the content changes AEO will flag
- [Schema.org for AI Discovery](schema-ai-discovery.md) — improving AEO's Schema score
- [GEO Overview](geo-overview.md) — context for what AEO is measuring
- [SEO Audit Workflow](seo-audit-workflow.md) — traditional SEO audit alongside AEO
- Reference: [AEO Module (drupal.org/project/aeo)](https://www.drupal.org/project/aeo)
