---
description: Guardrails system — pre/post processing plugins for content moderation, PII filtering, and prompt injection detection
tldr: "Use guardrails when you need to intercept AI requests before they reach the provider (pre-processing) or after receiving a response (post-processing). Required for user-facing AI features."
drupal_version: "11.x"
---

# Guardrails System

## When to Use

> Use guardrails when you need to intercept AI requests before they reach the provider (pre-processing) or after receiving a response (post-processing). Required for user-facing AI features.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Content moderation | Pre + post guardrail | Block unsafe input and output |
| PII filtering | Pre guardrail | Scrub before sending to provider |
| Prompt injection detection | Pre guardrail | Catch injection attempts before processing |
| AI-based moderation | `NonDeterministicGuardrailInterface` | Guardrail itself uses AI; receives `AiProviderPluginManager` |
| Streaming response | Avoid `NonStreamableGuardrailInterface` | Skipped for streaming calls automatically |

## Pattern

```php
use Drupal\ai\Attribute\AiGuardrail;

#[AiGuardrail(
  id: 'safety:pii_filter',  // ID must match or be prefixed by group ("safety")
  label: new TranslatableMarkup('PII Filter'),
  description: new TranslatableMarkup('Removes PII before sending to AI'),
)]
class PiiFilter extends AiGuardrailPluginBase {

  public function processInput(InputInterface $input): GuardrailResultInterface {
    // Return PassResult, StopResult, or RewriteInputResult.
    return new RewriteInputResult('Input scrubbed', $this, []);
  }

  public function processOutput(OutputInterface $output): GuardrailResultInterface {
    return new PassResult('Output passed', $this, []);
  }
}
```

## Guardrail Result Types

| Result Class | `stop()` | Purpose |
|-------------|---------|---------|
| `PassResult` | `false` | Input/output passes without changes |
| `StopResult` | `true` | Block the request; includes a `$score` |
| `RewriteInputResult` | `false` | Rewrite the input before sending |
| `RewriteOutputResult` | `false` | Rewrite the output before returning |

## Request Lifecycle

1. `PreGenerateResponseEvent` fires
2. `GuardrailsEventSubscriber` loads matching guardrails
3. Each guardrail's `processInput()` runs
4. Provider processes the request
5. `PostGenerateResponseEvent` fires
6. Each guardrail's `processOutput()` runs

## Config Entities

| Entity Type | Purpose |
|-------------|---------|
| `ai_guardrail` | Individual guardrail config entity |
| `ai_guardrail_set` | Groups guardrails with pre/post lists and a stop threshold |

## AiGuardrailRepository

```php
$repo = \Drupal::service('Drupal\ai\Guardrail\AiGuardrailRepository');
$guardrail = $repo->getGuardrailById('safety:pii_filter');
$set = $repo->getGuardrailSetById('my_guardrail_set');
```

## Common Mistakes

- **Wrong**: ID doesn't match its group prefix → **Right**: ID must match or be prefixed by group (e.g., group "safety" → ID `safety` or `safety:pii_filter`)
- **Wrong**: Applying streaming-incompatible guardrails without `NonStreamableGuardrailInterface` → **Right**: Mark as `NonStreamableGuardrailInterface` and it will be skipped for streaming calls
- **Wrong**: Not enabling guardrails on user-facing features → **Right**: Prompt injection can bypass agent instructions without guardrails

## See Also

- [Events System](events-system.md)
- [AI Agents](ai-agents.md)
- [Security](security.md)
- Reference: `web/modules/contrib/ai/src/Guardrail/`
