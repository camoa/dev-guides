---
description: 8-stage AI content workflow - from strategic planning to publishing and discovery optimization
drupal_version: "11.x"
---

# AI Content Workflow

## When to Use

> Use the 8-stage AI content workflow when creating, managing, or optimizing content at scale. Use when you need consistent quality, SEO optimization, and strategic alignment.

## Decision

| Content Type | Recommended Stages to Automate | Human Touch Required |
|---|---|---|
| Blog posts | 4 (drafting), 6 (SEO), 7 (QA) | 2, 5, 8 |
| Product descriptions | 4 (drafting), 6 (SEO) | 5, 7 |
| Landing pages | 3 (framework), 4 (drafting), 6 (SEO) | 2, 5, 7, 8 |
| News articles | 4 (drafting), 6 (SEO) | 2, 5, 7, 8 |
| Technical documentation | 4 (structure), 6 (SEO) | 2, 3, 5, 7, 8 |

## The 8-Stage Workflow

**Stage 1: Strategic Planning**
- Use AI Content Advisor to analyze existing content and identify gaps
- Generate content briefs based on keyword research and competitive analysis
- Map content to user journey stages
- Define success metrics (traffic, engagement, conversion)

**Stage 2: Research & Preparation**
- Leverage RAG (Retrieval Augmented Generation) to analyze existing site content
- Use vector search to identify related content and avoid duplication
- Extract key facts, statistics, and quotes using AI summarization
- Validate source credibility and freshness

**Stage 3: Content Framework Selection**
- Choose appropriate framework (AIDA, PAS, BAB, Inverted Pyramid, Storytelling)
- Define tone, voice, and target audience
- Set content structure and required sections
- Establish word count and depth targets

**Stage 4: AI-Assisted Drafting**
- Use AI Automators or CKEditor AI for initial content generation
- Apply selected framework to structure content
- Generate field-level content (titles, summaries, tags)
- Create multiple variants for A/B testing

**Stage 5: Human Review & Enhancement**
- Review AI-generated content for accuracy and brand alignment
- Add unique insights, examples, and expert perspective (E-E-A-T)
- Refine tone and ensure natural language flow
- Fact-check AI-generated claims

**Stage 6: SEO Optimization**
- Generate optimized metatags (title, description, Open Graph, Twitter Cards)
- Create structured data markup
- Optimize heading hierarchy and keyword placement
- Generate alt text for images

**Stage 7: Quality Assurance**
- Apply 4 C's framework (Clear, Concise, Compelling, Credible)
- Run AI Content Advisor for improvement suggestions
- Check readability scores and reading level
- Validate links and references

**Stage 8: Publishing & Discovery**
- Enable AI-powered content recommendations
- Configure chatbots with RAG for content discovery
- Monitor AI search rankings and discovery patterns
- Iterate based on performance data

## Pattern

```php
// Stage 1: AI Content Advisor analysis
$advisor = \Drupal::service('ai_content_advisor.analyzer');
$recommendations = $advisor->analyzeContent($node);

// Stage 2: RAG-based research
$vdb = \Drupal::service('ai.vdb_provider');
$related_content = $vdb->proximitySearch($query_embedding, 10);

// Stage 4: Automator-based drafting
// Configured via UI at node type field settings

// Stage 6: SEO automation
// AI SEO Automator generates metatags on save

// Stage 7: Quality check
$quality_score = $advisor->assessQuality($node, [
  'readability' => TRUE,
  'completeness' => TRUE,
  'seo_optimization' => TRUE,
]);
```

## Common Mistakes

- **Wrong**: Skipping human review (Stage 5) → **Right**: AI-generated content requires human verification for accuracy and brand alignment; publishing raw AI output risks factual errors and tone mismatches
- **Wrong**: Over-automating creative content → **Right**: Personal stories, thought leadership, and unique insights cannot be AI-generated; reserve automation for tactical, data-driven content
- **Wrong**: Not monitoring AI content performance → **Right**: Track AI-generated content separately to measure ROI and identify optimization opportunities
- **Wrong**: Ignoring E-E-A-T in Stage 5 → **Right**: Search engines prioritize Experience, Expertise, Authoritativeness, Trustworthiness; add human expertise signals
- **Wrong**: Using same framework for all content → **Right**: Match framework to content type and audience; not all content benefits from AIDA or storytelling

## See Also

- [Provider Configuration](provider-configuration.md)
- [Content Framework Patterns](framework-patterns.md)
- [Content Quality & Review](quality-review.md)
- Reference: `/modules/contrib/ai_content_advisor/`
