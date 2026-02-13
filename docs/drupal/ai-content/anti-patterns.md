---
description: Common anti-patterns to avoid - trusting AI output, synchronous processing, token limits, hardcoding
drupal_version: "11.x"
---

# Common Anti-Patterns

## When to Use

> Learn from common mistakes to avoid technical debt, security vulnerabilities, poor user experience, and cost overruns. Every anti-pattern includes WHY it's problematic.

## Anti-Pattern: Trusting AI Output Without Validation

**Wrong**:
```php
$summary = $ai->generateSummary($node->body->value);
$node->set('field_summary', $summary);
$node->save();
```

**Why it's wrong**:
- AI hallucinates facts and makes up plausible-sounding nonsense
- Generated content may contain factual errors, broken logic, or biased perspectives
- No validation means errors propagate to published content
- Legal/compliance risk for regulated content (medical, legal, financial)

**Right**:
```php
$summary = $ai->generateSummary($node->body->value);

// Validate and sanitize
$summary = $this->validateAIContent($summary, [
  'max_length' => 500,
  'check_facts' => TRUE,
  'sanitize_html' => TRUE,
]);

// Flag for human review if confidence is low
if ($summary['confidence'] < 0.8) {
  $node->set('field_needs_review', TRUE);
}

$node->set('field_summary', $summary['content']);
$node->save();
```

## Anti-Pattern: Synchronous AI in Request Cycle

**Wrong**:
```php
// Blocks form submission for 10-30 seconds
function mymodule_node_presave(NodeInterface $node) {
  if ($node->isNew()) {
    $tags = $ai->generateTags($node);  // Blocks here
    $node->set('field_tags', $tags);
  }
}
```

**Why it's wrong**:
- Users wait 10-30+ seconds for form to save
- Timeouts cause form submission failures
- Poor user experience drives users away
- Concurrent requests pile up, degrading site performance

**Right**:
```php
// Queue for background processing
function mymodule_node_presave(NodeInterface $node) {
  if ($node->isNew()) {
    $queue = \Drupal::queue('ai_tag_generation');
    $queue->createItem(['node_id' => $node->id()]);
    // Form saves immediately, AI runs in background
  }
}
```

## Anti-Pattern: Not Implementing Token Limits

**Wrong**:
```php
// Can send 50,000 token prompts
$prompt = "Summarize: " . $node->body->value;
$summary = $ai->chat($prompt);
```

**Why it's wrong**:
- Exceeds model token limits (crashes)
- Costs scale with tokens (can be $5+ per request for GPT-4)
- Slow responses (30+ seconds for long prompts)
- Wasteful (most content only needs excerpt for context)

**Right**:
```php
// Enforce token limits
$tokenizer = \Drupal::service('ai.tokenizer');
$body = $node->body->value;

// Truncate to 7000 tokens to leave room for response
if ($tokenizer->count($body, 'gpt-4') > 7000) {
  $body = $tokenizer->truncate($body, 7000, 'gpt-4');
}

$prompt = "Summarize: " . $body;
$summary = $ai->chat($prompt);
```

## Anti-Pattern: Hardcoding Model Names

**Wrong**:
```php
$response = $ai_provider->chat($messages, 'gpt-4');
```

**Why it's wrong**:
- Models deprecate (GPT-3.5-turbo, text-davinci-003 already deprecated)
- No runtime model switching for cost/performance tuning
- Can't A/B test different models
- Forces code changes to update models

**Right**:
```php
// Use configuration
$model = \Drupal::config('mymodule.settings')->get('default_chat_model') ?? 'gpt-4-turbo';
$response = $ai_provider->chat($messages, $model);

// Or use model selection in automator config (UI-driven)
```

## Anti-Pattern: Ignoring Provider Capabilities

**Wrong**:
```php
// Assumes all providers support all operations
$provider = $ai_provider_manager->createInstance($provider_id);
$image = $provider->generateImage($prompt);  // May not be supported
```

**Why it's wrong**:
- Not all providers support all operation types
- Crashes when provider doesn't support requested operation
- Anthropic doesn't support image generation
- Some providers don't support function calling

**Right**:
```php
// Check capabilities
$provider = $ai_provider_manager->createInstance($provider_id);

if ($provider->supportsOperation('image_generation')) {
  $image = $provider->generateImage($prompt);
} else {
  \Drupal::messenger()->addWarning('Selected provider does not support image generation');
  // Fall back to alternative provider or show error
}
```

## Anti-Pattern: Not Handling Provider Failures

**Wrong**:
```php
// No error handling
$summary = $ai_provider->chat($messages, 'gpt-4');
$node->set('field_summary', $summary);
```

**Why it's wrong**:
- API failures are common (rate limits, outages, network issues)
- Unhandled exceptions crash the request
- No fallback means lost work
- Users see cryptic error messages

**Right**:
```php
// Graceful error handling
try {
  $summary = $ai_provider->chat($messages, 'gpt-4');
  $node->set('field_summary', $summary);
} catch (RateLimitException $e) {
  // Queue for retry
  $queue->createItem(['node_id' => $node->id(), 'retry' => 3]);
  \Drupal::messenger()->addWarning('AI service busy, summary will be generated shortly.');
} catch (AiException $e) {
  // Log error, use fallback
  \Drupal::logger('ai')->error('AI generation failed: @msg', ['@msg' => $e->getMessage()]);
  $node->set('field_summary', '');  // Leave empty for manual entry
}
```

## Anti-Pattern: Over-Automating Editorial Content

**Wrong**: Automating 100% of blog posts, thought leadership, personal stories with AI.

**Why it's wrong**:
- AI cannot replicate human experience, unique insights, or brand voice
- Readers detect and reject generic AI content
- SEO penalizes low-quality, mass-generated content
- Thought leadership requires human expertise (E-E-A-T)
- Legal risk: AI-generated content may plagiarize or spread misinformation

**Right**:
- **Automate tactical content**: Product descriptions, meta tags, summaries, alt text
- **AI-assist editorial content**: Outlines, research, first drafts requiring heavy editing
- **Human-only content**: Thought leadership, case studies, personal stories, expert analysis
- **Hybrid workflow**: AI drafts + mandatory human review and enhancement

## Anti-Pattern: Not Setting Cost Budgets

**Wrong**: Deploying AI features without cost monitoring or limits.

**Why it's wrong**:
- AI costs are variable and can spike unexpectedly
- Uncontrolled automation can cost thousands per month
- No visibility into cost drivers
- Budget overruns force emergency shutdowns

**Right**:
```php
// Implement cost tracking
$cost_tracker = \Drupal::service('mymodule.cost_tracker');

$monthly_cost = $cost_tracker->getMonthlyTotal();
$budget = \Drupal::config('mymodule.settings')->get('monthly_budget') ?? 500;

if ($monthly_cost > $budget * 0.9) {
  // Approaching budget - switch to cheaper models
  $model = 'gpt-3.5-turbo';  // Fallback to cheaper
  \Drupal::logger('ai')->warning('Approaching monthly budget, using cheaper models');
}

if ($monthly_cost > $budget) {
  // Exceeded budget - disable non-critical AI
  throw new BudgetExceededException('Monthly AI budget exceeded');
}
```

## Anti-Pattern: Not Providing Manual Override

**Wrong**: AI automations with no way for editors to regenerate or manually edit.

**Why it's wrong**:
- Editors cannot fix AI mistakes
- No recovery from poor AI output
- Frustrates content creators
- Forces workarounds (disabling automations entirely)

**Right**:
- Provide "Regenerate" button for each AI-generated field
- Allow manual editing of AI output
- Include "Skip AI generation" checkbox for edge cases
- Store AI confidence scores and flag low-confidence content for manual review

## See Also

- [Performance Optimization](performance.md)
- [Security & Privacy](security-privacy.md)
- [Content Workflow](content-workflow.md)
