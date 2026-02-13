---
description: Content framework patterns - AIDA, PAS, BAB, Inverted Pyramid, Storytelling for AI generation
drupal_version: "11.x"
---

# Content Framework Patterns

## When to Use

> Use content frameworks to structure AI content generation. Choose frameworks based on content goals: persuasion, information delivery, storytelling, or education.

## Framework Selection Guide

| Framework | Use For | Strength | Weakness |
|-----------|---------|----------|----------|
| AIDA | Marketing copy, landing pages, CTAs | Conversion-focused, tested pattern | Can feel salesy if overused |
| PAS | Blog posts addressing pain points, service pages | Emotionally engaging, builds urgency | Requires careful tone to avoid fear-mongering |
| BAB | Transformation stories, testimonials, feature announcements | Clear value proposition, aspirational | Needs concrete examples to be credible |
| Inverted Pyramid | News articles, announcements, informational content | SEO-friendly, scannable, journalistic credibility | Less persuasive for sales content |
| Storytelling Arc | Brand narratives, thought leadership | Memorable, emotionally resonant | Requires skilled execution, time-intensive |

## Decision

| Goal | Primary Framework | Secondary Option | Avoid |
|------|-------------------|------------------|-------|
| Drive conversions | AIDA | PAS | Inverted Pyramid |
| Explain complex topics | Inverted Pyramid | BAB | AIDA |
| Build emotional connection | Storytelling | PAS | Inverted Pyramid |
| Showcase transformation | BAB | Storytelling | AIDA |
| Deliver urgent news | Inverted Pyramid | PAS | Storytelling |
| Thought leadership | Storytelling | Inverted Pyramid | PAS |

## Pattern

Configure AI Automators with framework-specific prompts:

```yaml
# AIDA Framework Automator
automator_id: aida_body_generator
automator_type: llm_text_long
prompt: |
  Generate marketing content following the AIDA framework:

  Topic: [field:title]
  Target audience: [field:audience]
  Key benefit: [field:primary_benefit]

  Structure:
  - Attention: Compelling hook related to {{topic}}
  - Interest: Explain how this addresses {{audience}} needs
  - Desire: Create emotional connection to {{benefit}}
  - Action: Clear, specific next step

  Tone: Professional, persuasive
  Length: 300-400 words

# PAS Framework Automator
automator_id: pas_intro_generator
automator_type: llm_simple_text_long
prompt: |
  Write a PAS (Problem-Agitate-Solution) introduction:

  Problem: [field:pain_point]
  Solution: [field:product_name]

  1. Problem (2 sentences): State {{problem}} clearly
  2. Agitate (2-3 sentences): Amplify impact and urgency
  3. Solution (1 sentence): Introduce {{solution}} as answer

  Avoid: Fear-mongering, exaggeration
  Tone: Empathetic, authoritative
```

## Common Mistakes

- **Wrong**: Forcing frameworks onto inappropriate content → **Right**: News articles don't need AIDA; product specs don't need storytelling; match framework to content purpose
- **Wrong**: Mixing frameworks within single content piece → **Right**: Choose one primary framework per piece to maintain coherent structure and reader experience
- **Wrong**: Not customizing framework prompts → **Right**: Generic framework prompts produce generic content; add specific brand voice, audience, and tone requirements
- **Wrong**: Overusing persuasive frameworks → **Right**: AIDA and PAS fatigue readers if used on every page; balance persuasive and informational content
- **Wrong**: Ignoring framework in human review → **Right**: When editing AI content, verify it actually follows the intended framework structure

## See Also

- [Content Workflow](content-workflow.md)
- [AI Automator System](automators.md)
- [Content Quality & Review](quality-review.md)
