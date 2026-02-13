---
description: AI-powered SEO - automated metatags, structured data, E-E-A-T implementation
drupal_version: "11.x"
---

# SEO with AI

## When to Use

> Use AI-powered SEO automation to generate optimized meta tags, descriptions, structured data, and content that ranks well in both traditional search engines and AI-powered discovery tools (ChatGPT, Perplexity, Google SGE).

## Decision

| Approach | Best For | Automation Level | Human Review |
|----------|----------|------------------|--------------|
| AI SEO Analyzer | Analysis and recommendations | Report generation | Review required |
| Metatag AI Automator | Automatic generation on save | Fully automated | Optional review |
| Metatag AI Module | Generate with button in UI | On-demand | Required before save |

## Implementation Patterns

**Method 1: AI SEO Analyzer** (analysis and recommendations)

```php
// Configuration at /admin/config/ai/seo
// 1. Select provider and model
// 2. Configure analysis criteria
// 3. Set permissions for SEO Analyzer tab

// Usage: Navigate to node view, click "SEO Analyzer" tab
// Generates report with:
// - Keyword density analysis
// - Readability scores
// - Meta tag recommendations
// - Content structure review
// - Improvement suggestions
```

**Method 2: Metatag AI Automator** (automatic generation)

```yaml
# Configure on content type
automator_type: llm_metatag
field: metatags
trigger: [create, update]

prompt: |
  Generate SEO-optimized meta tags:

  Content: [node:title] - [node:body:summary]
  Target audience: [node:field_audience]
  Primary keyword: [node:field_keyword]

  Requirements:
  - Title: 50-60 characters, include {{keyword}}
  - Description: 150-160 characters, compelling, include {{keyword}}
  - Open Graph title: Engaging, social-optimized
  - Open Graph description: 2-3 sentences, shareable
  - Twitter Card: Optimized for Twitter

  Output as JSON:
  {
    "title": "...",
    "description": "...",
    "og_title": "...",
    "og_description": "...",
    "twitter_title": "...",
    "twitter_description": "..."
  }
```

## E-E-A-T Implementation

E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) is critical for search ranking and AI discovery:

**Experience Signals**:
```yaml
# Automator prompt including experience
prompt: |
  Write content incorporating first-hand experience:

  Topic: [node:title]
  Author expertise: [node:uid:entity:field_bio]

  Include:
  - Specific examples from real usage
  - Concrete outcomes and results
  - Challenges encountered and solutions
  - Timeline and context

  Avoid: Generic advice, theoretical knowledge only
```

**Expertise Indicators**:
- Author bylines with credentials
- Citations and references to authoritative sources
- Technical depth appropriate to topic
- Industry-specific terminology used correctly

**Authoritativeness**:
- Link to recognized industry sources
- Include expert quotes and interviews
- Reference original research or data
- Display author credentials and affiliations

**Trustworthiness**:
- Fact-check AI-generated claims before publishing
- Add publication date and last updated date
- Include sources and citations
- Display editorial policies and review process

## Structured Data Automation

Generate schema.org structured data with AI:

```yaml
automator_type: llm_json_native_binary
field: field_structured_data
prompt: |
  Generate schema.org JSON-LD for this article:

  Title: [node:title]
  Author: [node:uid:entity:name]
  Published: [node:created:custom:c]
  Content: [node:body:summary]

  Schema types to include:
  - Article (headline, author, datePublished, description)
  - Person (author details)
  - Organization (publisher)

  Output valid JSON-LD following schema.org standards.

output_format: json_ld
validation: schema_org
```

## SEO Best Practices

**Title Tags**:
- 50-60 characters optimal length
- Include primary keyword near beginning
- Make unique per page
- Match user search intent
- Avoid keyword stuffing

**Meta Descriptions**:
- 150-160 characters (Google's typical display limit)
- Include primary keyword naturally
- Write compelling copy to drive clicks
- Unique per page, not duplicated
- Call-to-action when appropriate

**Open Graph & Twitter Cards**:
- Optimize for social sharing, not just search
- Use more engaging, conversational tone than meta description
- Test preview rendering in social platforms
- Include relevant hashtags in Twitter description

**AI Discovery Optimization**:
- Structure content with clear sections and headings
- Use Q&A format when appropriate (FAQ schema)
- Provide direct, factual answers near top of content
- Include relevant context and definitions
- Cite sources that AI tools can reference

## Common Mistakes

- **Wrong**: Generating identical metatags for all content → **Right**: Every page needs unique tags; configure prompts to use page-specific tokens
- **Wrong**: Exceeding character limits → **Right**: Search engines truncate long tags; enforce strict length limits in prompts
- **Wrong**: Keyword stuffing in AI prompts → **Right**: Modern SEO and AI penalize over-optimization; use natural language
- **Wrong**: Not reviewing AI-generated tags before publishing → **Right**: AI may miss context or nuance; human review is essential for brand consistency
- **Wrong**: Ignoring social media optimization → **Right**: Open Graph and Twitter Cards drive social traffic; don't auto-generate from meta description
- **Wrong**: Forgetting to update metatags when content changes → **Right**: Set automators to trigger on update, not just create
- **Wrong**: Not tracking SEO performance of AI-generated content → **Right**: Monitor rankings and adjust prompts based on performance data

## See Also

- [AI Automator System](automators.md)
- [CKEditor AI Integration](ckeditor.md)
- [Content Workflow](content-workflow.md)
- Reference: `/modules/contrib/ai_seo/`
- Reference: https://www.drupal.org/project/ai_seo
- Reference: https://www.drupal.org/project/metatag_ai
- Reference: https://www.prometsource.com/tool/metatag-ai
