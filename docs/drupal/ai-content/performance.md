---
description: Performance optimization for AI - rate limiting, caching, queue processing, cost management
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Performance optimization is critical for AI features because API calls are slow (1-30+ seconds) and expensive. Optimize from day one to prevent poor user experience and cost overruns.

## Decision

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| GPT-4-turbo | 5-15s | High | Excellent | Complex analysis, long-form |
| GPT-4 | 10-30s | Highest | Excellent | When quality critical |
| GPT-3.5-turbo | 1-3s | Low | Good | Real-time, high volume |
| Claude Haiku | 1-2s | Low | Good | Speed-critical operations |
| Claude Sonnet | 3-8s | Medium | Excellent | Balanced needs |

## Rate Limiting & Quotas

**Provider Rate Limits**:

| Provider | Tier | Requests/min | Tokens/min | Cost Impact |
|----------|------|--------------|------------|-------------|
| OpenAI Free | Free | 3 | 40,000 | Unusable for production |
| OpenAI Tier 1 | $5+ spent | 500 | 2M | Adequate for small sites |
| OpenAI Tier 2 | $50+ spent | 5,000 | 10M | Medium sites |
| Anthropic Free | Free | 5 | 50,000 | Testing only |
| Anthropic Tier 1 | - | 50 | 2M | Production ready |

**Configure Module Rate Limits BELOW Provider Limits**:

```yaml
# /admin/config/ai/providers/openai
rate_limit:
  requests_per_minute: 450  # Set below 500 limit
  tokens_per_minute: 1800000  # Set to 90% of 2M limit
  retry_after: 60
  queue_overflow: TRUE  # Queue requests exceeding limit
```

**Graceful Degradation**:

```php
try {
  $response = $ai_provider->chat($messages, 'gpt-4');
} catch (RateLimitException $e) {
  // Fall back to cached response or simpler model
  \Drupal::logger('ai')->warning('Rate limit hit, using fallback');
  $response = $this->getCachedResponse($cache_key) ?? $this->simpleFallback();
}
```

## Caching Strategies

**Cache AI responses aggressively**:

```php
// Cache by content hash
$cache_key = 'ai:summary:' . md5($node->body->value);
$cached = \Drupal::cache('ai')->get($cache_key);

if ($cached) {
  return $cached->data;
}

$summary = $ai_provider->chat([...], 'gpt-3.5-turbo');

// Cache for 30 days (AI responses rarely change)
\Drupal::cache('ai')->set($cache_key, $summary, time() + 2592000);
```

**Cache Invalidation**:
- Invalidate when source content changes
- Provide manual "regenerate" button for editors
- Set long TTL (30+ days) for stable content
- Use cache tags for bulk invalidation

**Render Caching**:

```php
$build = [
  '#cache' => [
    'keys' => ['ai_summary', $node->id()],
    'contexts' => ['languages'],
    'tags' => $node->getCacheTags(),
    'max-age' => 86400, // 24 hours
  ],
];
```

## Queue Processing

**Never run AI operations synchronously in form submissions**:

```php
/**
 * Queue AI processing instead of blocking submission.
 */
function queueAIProcessing(NodeInterface $node) {
  $queue = \Drupal::queue('ai_content_generation');
  $queue->createItem([
    'node_id' => $node->id(),
    'operations' => ['summary', 'tags', 'metatags'],
  ]);

  \Drupal::messenger()->addStatus('Content saved. AI enhancements will be processed in the background.');
}
```

**Queue Configuration**:
```yaml
# custom_ai.queue.yml
ai_content_generation:
  worker: Drupal\custom_ai\Plugin\QueueWorker\AIContentGenerationWorker
  cron: { time: 60 }  # Process for 60 seconds during cron
  lease_time: 300  # 5 minute timeout per item
```

**Process queue via cron or dedicated worker**:
```bash
# Cron-based (for low volume)
drush cron

# Dedicated worker (for high volume)
drush queue:run ai_content_generation --time-limit=3600
```

## Cost Optimization

**Token Usage Awareness**:

```php
$tokenizer = \Drupal::service('ai.tokenizer');

// Count tokens before sending
$prompt_tokens = $tokenizer->count($prompt, 'gpt-4');

if ($prompt_tokens > 8000) {
  // Trim or chunk content
  $prompt = $this->trimToTokenLimit($prompt, 7000, 'gpt-4');
}

// Estimate cost
$cost_per_1k_tokens = 0.03; // GPT-4 input tokens
$estimated_cost = ($prompt_tokens / 1000) * $cost_per_1k_tokens;

if ($estimated_cost > 0.50) {
  \Drupal::logger('ai')->warning('High-cost request: @cost', ['@cost' => $estimated_cost]);
}
```

**Cost-Saving Strategies**:
- Cache aggressively (cache hits cost $0)
- Use cheaper models when quality difference is minimal
- Truncate prompts to minimum necessary context
- Batch related operations into single request
- Set monthly budget alerts with providers
- Monitor cost per operation type

**Cost Monitoring**:

```php
/**
 * Implements hook_ai_post_request().
 */
function custom_ai_cost_tracking_ai_post_request($provider, $operation, $input, $output, $metadata) {
  $cost_tracker = \Drupal::service('custom_ai.cost_tracker');

  $cost_tracker->recordUsage([
    'provider' => $provider,
    'model' => $metadata['model'],
    'operation' => $operation,
    'prompt_tokens' => $metadata['usage']['prompt_tokens'],
    'completion_tokens' => $metadata['usage']['completion_tokens'],
    'total_cost' => $metadata['cost'],
    'timestamp' => time(),
  ]);

  // Alert if approaching monthly budget
  if ($cost_tracker->getMonthlyTotal() > 800) {
    \Drupal::messenger()->addWarning('AI costs approaching monthly budget limit.');
  }
}
```

## Common Performance Mistakes

- **Wrong**: Synchronous AI calls in form submissions → **Right**: Users wait 10-30 seconds for form to save; always use queue processing for AI operations
- **Wrong**: Not caching AI responses → **Right**: Identical prompts re-run waste money and time; cache by content hash with long TTL
- **Wrong**: Using GPT-4 for everything → **Right**: GPT-4 costs 10x more than GPT-3.5-turbo; use faster/cheaper models for simple tasks
- **Wrong**: Sending entire node body in prompts → **Right**: Long prompts cost more and hit token limits; send summaries or relevant excerpts only
- **Wrong**: No rate limit configuration → **Right**: Provider rate limits cause random failures; configure module limits below provider limits
- **Wrong**: Not monitoring costs → **Right**: AI costs can spiral to thousands/month unexpectedly; implement cost tracking and alerts
- **Wrong**: Processing AI during high-traffic periods → **Right**: Queue processing during peak traffic degrades site performance; schedule heavy AI work for off-peak

## See Also

- [Security & Privacy](security-privacy.md)
- [Common Anti-Patterns](anti-patterns.md)
- [AI Automator System](automators.md)
- Reference: https://openai.com/pricing
