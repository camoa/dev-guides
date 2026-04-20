---
description: Schema.org structured data for AI discoverability — priority types, SpeakableSpecification, schema stacking, and Drupal implementation with schema_metatag
tldr: "You want structured data to improve how AI systems understand, extract, and cite your content — beyond traditional Google rich results. Google AI Overviews, Microsoft Copilot, and ChatGPT are confirmed to use structured data for entity…"
drupal_version: "11.x"
---

# Schema.org for AI Discovery

## When to Use

> You want structured data to improve how AI systems understand, extract, and cite your content — beyond traditional Google rich results. Google AI Overviews, Microsoft Copilot, and ChatGPT are confirmed to use structured data for entity understanding and answer generation. This guide focuses on which Schema.org types matter most for GEO and how to implement them in Drupal. For general Schema Metatag setup, see Schema Metatag Setup.

## Decision

| Goal | Schema type | Priority |
|------|------------|---------|
| Article or blog post | Article (or BlogPosting, NewsArticle) | High — most AI platforms prioritize editorial content |
| Q&A or FAQ content | FAQPage | High — directly maps to AI answer format |
| Product or service | Product | High — used by shopping AI features |
| Step-by-step process | HowTo | High — maps to AI Overviews procedural answers |
| Organization/brand identity | Organization | High — entity disambiguation for brand mentions |
| Voice or AI assistant readout | SpeakableSpecification | Medium — marks specific content for audio extraction |
| Events | Event | Medium — Google and Perplexity surface event data |
| Persons / authors | Person | Medium — E-E-A-T signals for author credibility |
| Breadcrumb trail | BreadcrumbList | Medium — AI uses for page context |
| Courses or educational content | Course | Low-Medium — emerging AI education use |

## Confirmed Impact

| Platform | How structured data is used | Evidence |
|----------|----------------------------|---------|
| Google AI Overviews | Entity extraction, answer generation, source selection | Google Search Central documentation (2024) |
| Microsoft Copilot | Bing structured data feeds AI answer generation | Microsoft Learn — Bing Webmaster Guidelines |
| ChatGPT Browse | Schema used during web retrieval for entity understanding | Data World study: GPT-4 accuracy 16% → 54% with schema |
| Google Rich Results | FAQ, HowTo, Product rich snippets in SERP | Google Rich Results Test |

The Data World finding (GPT-4 accuracy from 16% to 54% with Schema.org markup) is the strongest quantified evidence. The mechanism: LLMs treat JSON-LD properties as explicit, machine-readable assertions rather than inferring facts from prose.

## Priority Schema Types for GEO

### Article

Maps your editorial content to AI answer generation. AI systems prefer Article over bare WebPage for content they will cite.

**Required for GEO impact:**
- `headline` — matches page title
- `datePublished` — enables recency filtering
- `dateModified` — 89.7% of ChatGPT citations go to recently modified pages
- `author` (Person type) — E-E-A-T signal
- `publisher` (Organization type) — brand entity
- `image` — AI visual context

### FAQPage

The highest-impact type for AI Overviews. FAQ content maps directly to the question-answer format AI systems use for answers. Google AI Overviews heavily samples FAQPage content.

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is Generative Engine Optimization?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "GEO is the practice of optimizing content to be cited and summarized by AI systems such as ChatGPT, Google AI Overviews, and Perplexity."
      }
    }
  ]
}
```

### HowTo

Maps to procedural AI answers. When a user asks "how to configure X in Drupal," AI systems with HowTo markup can extract steps directly rather than parsing prose.

```json
{
  "@type": "HowTo",
  "name": "How to configure llms.txt in Drupal",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Create the file",
      "text": "Create web/llms.txt in your Drupal root."
    },
    {
      "@type": "HowToStep",
      "name": "Add the H1 and description",
      "text": "Start with # Site Name and a blockquote description."
    }
  ]
}
```

### Organization

Entity disambiguation. AI systems use Organization markup to associate brand mentions across the web. Without it, "Drupal" might be attributed to multiple unrelated entities. Include for every site.

**Key properties:** `name`, `url`, `logo`, `sameAs` (Wikipedia, LinkedIn, social profiles)

### SpeakableSpecification

Marks specific text blocks for voice assistants and AI audio readout. Currently used by Google Assistant and emerging AI voice features.

```json
{
  "@type": "WebPage",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-headline", ".article-summary"]
  }
}
```

Target: headline + first paragraph (the direct answer). Do not mark entire page bodies — AI voice systems need the 1-2 sentence summary, not a full article.

## Schema Stacking

Multiple Schema.org types can coexist on a single page. Stack types to give AI systems richer entity context.

**Common stack patterns:**

| Page type | Primary type | Stack with |
|-----------|-------------|------------|
| Blog post | Article | BreadcrumbList, Person (author), Organization (publisher) |
| FAQ page | FAQPage | WebPage, Organization |
| Tutorial | HowTo | Article, BreadcrumbList |
| Product page | Product | Organization, BreadcrumbList, Offer |
| Team member | Person | Organization |

**Stacking as separate JSON-LD blocks** (preferred approach):
```html
<script type="application/ld+json">
{"@type": "Article", ...}
</script>

<script type="application/ld+json">
{"@type": "BreadcrumbList", ...}
</script>
```

Separate script blocks are cleaner than nested types and easier to debug with Google's Rich Results Test.

## Drupal Implementation with schema_metatag

Schema Metatag 3.0.4 implements JSON-LD via the Metatag module's token system. Configuration is at `/admin/config/search/metatag`.

**Step 1: Enable relevant submodules**

```
drush en schema_article schema_web_page schema_organization schema_person
```

For FAQPage and HowTo, you need a compatible field or a custom plugin — these types require dynamic structured data from field values, not static token mappings.

**Step 2: Configure Article per content type**

At `/admin/config/search/metatag` → Edit defaults for your Article content type:

| Schema property | Token |
|----------------|-------|
| `@type` | `Article` |
| `headline` | `[node:title]` |
| `datePublished` | `[node:created:html_datetime]` |
| `dateModified` | `[node:changed:html_datetime]` |
| `author.name` | `[node:author:display-name]` |
| `author.@type` | `Person` |
| `publisher.name` | `[site:name]` |
| `publisher.@type` | `Organization` |
| `image` | `[node:field_image:entity:url]` |

**Step 3: Organization in Global defaults**

Set Organization in the Global metatag defaults so every page carries publisher entity data. This is the minimum viable schema for brand entity disambiguation.

**Step 4: Verify output**

```
curl -s https://example.com/your-article | grep -A 20 'application/ld+json'
```

Or use View Source in browser and search for `ld+json`.

## Common Mistakes

- **Wrong**: Using Microdata or RDFa instead of JSON-LD → **Right**: JSON-LD is Google's recommendation and is cleanest for AI parsing; JSON-LD lives in `<script>` tags, not embedded in HTML attributes
- **Wrong**: Adding FAQPage markup to a page that is not actually a FAQ → **Right**: Google and AI systems penalize misleading structured data; only use FAQPage when the page structure matches
- **Wrong**: Setting `dateModified` to the original publish date → **Right**: `dateModified` must reflect the last actual content change; AI uses this for recency filtering
- **Wrong**: Omitting `author` because the site has no bylines → **Right**: Create a Person entity for the organization's content team; E-E-A-T matters to AI citation weighting
- **Wrong**: Stacking all types in one nested JSON-LD object → **Right**: Use separate `<script type="application/ld+json">` blocks per type for cleaner validation
- **Wrong**: Only validating with Google Rich Results Test → **Right**: Also test with schema.org/validator and inspect actual JSON-LD in page source; Rich Results Test only covers Google-specific rich result types

## See Also

- [Schema Metatag Setup](schema-metatag-setup.md) — installing and configuring schema_metatag
- [Schema Types Reference](schema-types-reference.md) — all 25 supported types with properties
- [Content Patterns for AI](content-patterns-ai.md) — content writing complements structured data
- [GEO Overview](geo-overview.md) — why structured data matters for AI citation
- Reference: [Google Structured Data documentation](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- Reference: [Schema.org full vocabulary](https://schema.org)
