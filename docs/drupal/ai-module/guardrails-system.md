---
description: Guardrails system — pre/post processing plugins for content moderation, PII filtering, and prompt injection detection
tldr: "Pre/post process AI requests: block unsafe input, filter PII, or inject context. Required for user-facing features. 1.4 adds multiple guardrail sets per input, global site-wide enforcement, and StreamableGuardrailInterface for mid-stream redaction."
drupal_version: "11.x"
---

# Guardrails System

## When to Use

> Use guardrails when you need to intercept AI requests before they reach the provider (pre-processing) or after receiving a response (post-processing). Required for user-facing AI features.

Guardrails are plugins that process AI requests before and/or after they reach the provider. Use them for content moderation, PII filtering, prompt injection detection, etc.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Content moderation | Pre + post guardrail | Block unsafe input and output |
| PII filtering | Pre guardrail | Scrub before sending to provider |
| Prompt injection detection | Pre guardrail | Catch injection attempts before processing |
| AI-based moderation | `NonDeterministicGuardrailInterface` | Guardrail itself uses AI; receives `AiProviderPluginManager` |
| Streaming response | Avoid `NonStreamableGuardrailInterface` | Skipped for streaming calls automatically |
| Redact content mid-stream | `StreamableGuardrailInterface` (1.4) | Buffer streamed output and redact before client sees it |
| Site-wide enforcement | Global guardrail sets (1.4) | Applied to every request before caller-attached sets |

## Plugin Attribute

```php
use Drupal\ai\Attribute\AiGuardrail;

#[AiGuardrail(
  id: 'my_guardrail',
  label: new TranslatableMarkup('My Guardrail'),
  description: new TranslatableMarkup('Blocks unsafe content'),
)]
class MyGuardrail extends AiGuardrailPluginBase {
  // Implement pre/post processing methods
}
```

**ID convention:** Must match or be prefixed by group. E.g., group "safety" -> ID must be "safety" or "safety:pii_filter".

## Services

| Service | Purpose |
|---------|---------|
| `plugin.manager.ai_guardrail` | Plugin manager |
| `Drupal\ai\Guardrail\AiGuardrailRepository` | Loads configured guardrails |
| `ai.guardrail_helper` | Helper for guardrail operations |
| `Drupal\ai\EventSubscriber\GuardrailsEventSubscriber` | Applies guardrails on pre/post events |

## How Guardrails Work

1. `PreGenerateResponseEvent` fires
2. **Changed in 1.4:** `GlobalGuardrailsEventSubscriber` (priority 100) prepends site-wide guardrail sets from `ai.settings` config before any caller-attached sets — global sets always run first
3. `GuardrailsEventSubscriber` loads the full merged guardrail set list from the input
4. Each guardrail's pre-processing runs (can modify input or block request)
5. Provider processes the request
6. `PostGenerateResponseEvent` fires
7. Each guardrail's post-processing runs (can modify or reject output)

## Config Entities

| Entity Type | Interface | Purpose |
|-------------|-----------|---------|
| `ai_guardrail` | `AiGuardrailEntityInterface` | Individual guardrail config entity |
| `ai_guardrail_set` | `AiGuardrailSetInterface` | Groups guardrails with pre/post lists and a stop threshold |

`AiGuardrailSetInterface` key methods:

- `getPreGenerateGuardrails()` — guardrails that run before AI generation
- `getPostGenerateGuardrails()` — guardrails that run after AI generation
- `getStopThreshold()` — float threshold for `StopResult` scores

## AiGuardrailInterface Methods

```php
interface AiGuardrailInterface {
  public function label(): string;
  public function isAvailable(): bool;
  public function processInput(InputInterface $input): GuardrailResultInterface;
  public function processOutput(OutputInterface $output): GuardrailResultInterface;
}
```

## Guardrail Result Types

| Result Class | `stop()` | Purpose |
|-------------|---------|---------|
| `PassResult` | `false` | Input/output passes without changes |
| `StopResult` | `true` | Block the request; includes a `$score` (float) compared against set threshold |
| `RewriteInputResult` | `false` | Rewrite the input before sending to provider |
| `RewriteOutputResult` | `false` | Rewrite the output before returning to caller |

All result types extend `AbstractResult(string $message, AiGuardrailInterface $guardrail, array $context)`.

## Specialized Guardrail Interfaces

| Interface | Purpose |
|-----------|---------|
| `NonDeterministicGuardrailInterface` | Guardrail that uses AI itself (e.g., LLM-based moderation). Receives `AiProviderPluginManager` via `setAiPluginManager()` |
| `NonStreamableGuardrailInterface` | Marker interface — guardrail cannot process streamed responses (skipped for streaming calls) |
| `StreamableGuardrailInterface` | **New in 1.4:** Evaluate streamed output mid-stream. `getStartRegex()` begins buffering, `getStopRegex()` ends it, and `processStreamedBuffer(string $buffered): GuardrailResultInterface` decides — used to redact sensitive content (e.g. an unreleased product name) before it reaches the client |

## Repository: `AiGuardrailRepository`

Autowired service for loading guardrail entities:

| Method | Returns |
|--------|---------|
| `getGuardrailById($id)` | `AiGuardrailInterface` or `null` |
| `getAllGuardrails()` | `AiGuardrailInterface[]` |
| `getGuardrailSetById($id)` | `AiGuardrailSetInterface` or `null` |
| `getAllGuardrailSets()` | `AiGuardrailSetInterface[]` |

```php
$repo = \Drupal::service('Drupal\ai\Guardrail\AiGuardrailRepository');
$guardrail = $repo->getGuardrailById('safety:pii_filter');
$set = $repo->getGuardrailSetById('my_guardrail_set');
$all = $repo->getAllGuardrailSets();
```

## Built-in Guardrail Plugins

| Plugin | Purpose |
|--------|---------|
| `regexp_guardrail` | Block inputs/outputs matching a configurable regex pattern (fixed in 1.3.5 — `processOutput()` now executes the pattern) |
| `input_length_limit` | **Changed in 1.4:** Built-in DoS protection — blocks requests whose input text exceeds a configurable character limit |
| `restrict_to_topic` | **New in 1.4:** Non-deterministic (LLM-based) guardrail that blocks inputs/outputs outside a configured topic. 1.4.2 added a re-entrancy guard so its internal LLM call can't recurse into global guardrails, and it now parses the classifier response via the `ai.prompt_json_decode` service |

## Global Guardrails (Changed in 1.4)

Configure site-wide guardrail sets that apply to **every** AI request regardless of caller:

```yaml
# ai.settings
global_guardrails:
  - my_pii_guardrail_set
  - my_content_moderation_set
```

These sets are prepended to any caller-attached guardrail sets. Global sets cannot be bypassed by callers. Configure at `/admin/config/ai/settings`.

## InputInterface: Multiple Guardrail Sets (Changed in 1.4)

In 1.3.x, each input held a single guardrail set. In 1.4.x, inputs hold multiple sets. The old methods are deprecated:

| 1.3.x (deprecated in 1.4) | 1.4.x replacement |
|---------------------------|-------------------|
| `setGuardrailSet($set)` | `addGuardrailSet($set)` or `setGuardrailSets([$set])` |
| `getGuardrailSet()` | `getGuardrailSets()` — returns array keyed by set ID |

```php
// 1.3.x (still works, deprecated)
$input->setGuardrailSet($guardrailSet);

// 1.4.x (recommended)
$input->addGuardrailSet($guardrailSet);      // Add one set; replaces if same ID
$input->setGuardrailSets([$set1, $set2]);   // Replace all sets
$sets = $input->getGuardrailSets();          // Returns array keyed by set ID
```

## Built-in Moderation

The `ModeratePreRequestEventSubscriber` intercepts chat calls and routes them through a separate moderation provider if configured (migrated from the deprecated `ai_external_moderation` module).

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Plugin ID that does not match its group prefix | ID must match or be prefixed by group — group "safety" means ID `safety` or `safety:pii_filter` |
| Applying a streaming-incompatible guardrail without `NonStreamableGuardrailInterface` | It will run against streamed calls; mark it and it is skipped instead |
| Not enabling guardrails on user-facing features | Prompt injection can bypass agent instructions |
| Using `setGuardrailSet()` on 1.4.x | Deprecated — use `addGuardrailSet()` or `setGuardrailSets()` |

## See Also

- [Events System](events-system.md)
- [AI Agents](ai-agents.md)
- [Security](security.md)
- Reference: `web/modules/contrib/ai/src/Guardrail/`
