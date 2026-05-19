---
description: Guardrails system — pre/post processing plugins for content moderation, PII filtering, and prompt injection detection
tldr: "Use guardrails when you need to intercept AI requests before they reach the provider (pre-processing) or after receiving a response (post-processing). Required for user-facing AI features. Changed in 1.4: inputs now hold multiple guardrail sets (addGuardrailSet/getGuardrailSets); global site-wide sets are prepended before any caller-attached sets."
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
| Site-wide enforcement | Global guardrail sets (1.4) | Applied to every request before caller-attached sets |

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
| `StopResult` | `true` | Block the request; includes a `$score` compared against set threshold |
| `RewriteInputResult` | `false` | Rewrite the input before sending |
| `RewriteOutputResult` | `false` | Rewrite the output before returning |

## Request Lifecycle

1. `PreGenerateResponseEvent` fires
2. **Changed in 1.4:** `GlobalGuardrailsEventSubscriber` (priority 100) prepends site-wide guardrail sets from `ai.settings` — global sets always run first and cannot be bypassed by callers
3. `GuardrailsEventSubscriber` loads the merged guardrail set list from the input
4. Each guardrail's `processInput()` runs (can modify input or block request)
5. Provider processes the request
6. `PostGenerateResponseEvent` fires
7. Each guardrail's `processOutput()` runs

## Global Guardrails (Changed in 1.4)

Configure site-wide guardrail sets that apply to **every** AI request regardless of caller. Configure at `/admin/config/ai/settings`.

```yaml
# ai.settings
global_guardrails:
  - my_pii_guardrail_set
  - my_content_moderation_set
```

## Multiple Guardrail Sets per Input (Changed in 1.4)

In 1.3.x, each input held a single guardrail set. In 1.4.x, inputs hold multiple sets.

| 1.3.x (deprecated in 1.4) | 1.4.x replacement |
|---------------------------|-------------------|
| `setGuardrailSet($set)` | `addGuardrailSet($set)` or `setGuardrailSets([$set])` |
| `getGuardrailSet()` | `getGuardrailSets()` — returns array keyed by set ID |

```php
// 1.4.x (recommended)
$input->addGuardrailSet($guardrailSet);      // Add one set; replaces if same ID
$input->setGuardrailSets([$set1, $set2]);   // Replace all sets
$sets = $input->getGuardrailSets();          // Returns array keyed by set ID
```

## Config Entities

| Entity Type | Purpose |
|-------------|---------|
| `ai_guardrail` | Individual guardrail config entity |
| `ai_guardrail_set` | Groups guardrails with pre/post lists and a stop threshold |

`AiGuardrailSetInterface` key methods:
- `getPreGenerateGuardrails()` — guardrails that run before AI generation
- `getPostGenerateGuardrails()` — guardrails that run after AI generation
- `getStopThreshold()` — float threshold for `StopResult` scores

## Built-in Guardrail Plugins

| Plugin | Purpose |
|--------|---------|
| `regexp_guardrail` | Block inputs/outputs matching a configurable regex (fixed in 1.3.5 — `processOutput()` now executes the pattern) |
| `input_length_limit` | **Changed in 1.4:** Built-in DoS protection — blocks requests exceeding a configurable character limit |

## AiGuardrailRepository

```php
$repo = \Drupal::service('Drupal\ai\Guardrail\AiGuardrailRepository');
$guardrail = $repo->getGuardrailById('safety:pii_filter');
$set = $repo->getGuardrailSetById('my_guardrail_set');
$all = $repo->getAllGuardrailSets();
```

## Specialized Interfaces

| Interface | Purpose |
|-----------|---------|
| `NonDeterministicGuardrailInterface` | Guardrail that uses AI itself; receives `AiProviderPluginManager` via `setAiPluginManager()` |
| `NonStreamableGuardrailInterface` | Marker — guardrail cannot process streamed responses; skipped for streaming calls |

## Common Mistakes

- **Wrong**: ID doesn't match its group prefix → **Right**: ID must match or be prefixed by group (e.g., group "safety" → ID `safety` or `safety:pii_filter`)
- **Wrong**: Applying streaming-incompatible guardrails without `NonStreamableGuardrailInterface` → **Right**: Mark as `NonStreamableGuardrailInterface` and it will be skipped for streaming calls
- **Wrong**: Not enabling guardrails on user-facing features → **Right**: Prompt injection can bypass agent instructions without guardrails
- **Wrong**: Using `setGuardrailSet()` in 1.4.x → **Right**: Deprecated; use `addGuardrailSet()` or `setGuardrailSets()`

## See Also

- [Events System](events-system.md)
- [AI Agents](ai-agents.md)
- [Security](security.md)
- Reference: `web/modules/contrib/ai/src/Guardrail/`
