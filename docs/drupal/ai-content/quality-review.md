---
description: Content quality review with AI - 4 C's framework, automated quality checks, lifecycle management
drupal_version: "11.x"
---

# Content Quality & Review

## When to Use

> Use AI-powered quality review to ensure consistency, readability, and effectiveness across all content. Use the 4 C's framework (Clear, Concise, Compelling, Credible) for structured quality assessment.

## Decision

| Quality Criterion | What It Measures | Target Score | Action If Below Target |
|-------------------|------------------|--------------|------------------------|
| Clear | Readability, structure, jargon-free | 70+ | Simplify language, add structure |
| Concise | Word efficiency, focus | 75+ | Remove redundancy, tighten focus |
| Compelling | Engagement, relevance | 70+ | Improve opening, add examples |
| Credible | Accuracy, sources, expertise | 80+ | Add citations, verify facts |

## The 4 C's Quality Framework

**Clear**
- Easy to understand by target audience
- Free of jargon or unexplained technical terms
- Logical structure and flow
- Appropriate reading level

**Concise**
- No unnecessary words or repetition
- Focused on core message
- Respects reader's time
- Appropriate length for content type

**Compelling**
- Engages reader interest
- Addresses reader needs and pain points
- Strong opening and closing
- Actionable takeaways

**Credible**
- Factually accurate
- Properly cited sources
- Author expertise evident
- Professional tone and polish

## Pattern

**AI Content Advisor Implementation**:

```php
// Content analysis
$advisor = \Drupal::service('ai_content_advisor.analyzer');

$analysis = $advisor->analyzeContent($node, [
  'readability' => TRUE,
  'seo' => TRUE,
  'completeness' => TRUE,
  'engagement' => TRUE,
]);

// Results structure
$results = [
  'readability' => [
    'score' => 65, // Flesch Reading Ease
    'grade_level' => 8,
    'recommendations' => [
      'Reduce average sentence length from 24 to 15-20 words',
      'Replace complex words: "utilize" → "use"',
    ],
  ],
  'seo' => [
    'score' => 78,
    'keyword_density' => 1.2,
    'recommendations' => [
      'Add primary keyword to first paragraph',
      'Include 2-3 subheadings with keyword variations',
    ],
  ],
];
```

**Automated Quality Scoring**:

```yaml
automator_type: llm_json_native_binary
field: field_quality_score
trigger: [create, update]

prompt: |
  Analyze this content using the 4 C's framework:

  Title: [node:title]
  Content: [node:body]

  Evaluate each criterion (0-100):

  1. Clear: Is it easy to understand?
  2. Concise: Is it appropriately brief?
  3. Compelling: Does it engage the reader?
  4. Credible: Is it trustworthy and accurate?

  For each, provide:
  - Score (0-100)
  - 2-3 specific improvement recommendations

  Output as JSON
```

## Quality Gate Integration

Implement quality gates in publishing workflow:

```php
/**
 * Implements hook_node_presave().
 */
function custom_quality_node_presave(NodeInterface $node) {
  // Run quality check before publishing
  if ($node->isPublished() && $node->isNew()) {
    $advisor = \Drupal::service('ai_content_advisor.analyzer');
    $quality = $advisor->assessQuality($node);

    // Minimum score to publish
    $min_score = 75;

    if ($quality['overall_score'] < $min_score) {
      $node->setUnpublished();
      \Drupal::messenger()->addWarning(
        sprintf(
          'Content quality score (%d) below publication threshold (%d). Saved as draft.',
          $quality['overall_score'],
          $min_score
        )
      );

      // Store quality report
      $node->set('field_quality_report', json_encode($quality));
    }
  }
}
```

## Best Practices

**Readability**:
- Target Flesch Reading Ease score of 60-70 for general audiences
- Keep sentences under 20 words on average
- Use active voice (target 80% or higher)
- Break long paragraphs (max 4-5 sentences)
- Add subheadings every 300-400 words

**Fact-Checking AI Content**:
- Verify all statistics and data points
- Check that cited sources actually support claims
- Validate technical accuracy with subject matter experts
- Test any code examples or instructions
- Cross-reference with authoritative sources

**Human Review Requirements**:
AI-generated content requires human review for:
- Factual accuracy (AI hallucinates)
- Brand voice and tone consistency
- Legal and regulatory compliance
- Sensitive topics (medical, legal, financial)
- Competitive positioning and messaging

## Common Mistakes

- **Wrong**: Publishing AI content without human review → **Right**: AI hallucinates facts, misunderstands context, and produces plausible-sounding nonsense; always verify
- **Wrong**: Using quality scores as strict gates without context → **Right**: A technically excellent how-to guide may score low on "compelling"; apply framework contextually
- **Wrong**: Not updating quality criteria over time → **Right**: Readability targets, SEO requirements, and content standards evolve; review criteria quarterly
- **Wrong**: Ignoring quality signals in analytics → **Right**: High bounce rate, low time-on-page, and poor engagement indicate quality issues; correlate with quality scores
- **Wrong**: Over-optimizing for AI quality scores → **Right**: Writing to satisfy AI metrics can produce robotic content; optimize for humans first, metrics second

## See Also

- [CKEditor AI Integration](ckeditor.md)
- [Vector Databases & RAG](vector-rag.md)
- [Content Workflow](content-workflow.md)
- Reference: `/modules/contrib/ai_content_advisor/`
- Reference: https://www.droptica.com/blog/how-generate-image-alt-text-and-content-strategy-ai-modules-drupal/
