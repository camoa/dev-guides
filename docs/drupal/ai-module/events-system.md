---
description: AI events system — subscribe to pre/post generation events to modify requests, log responses, or add custom behavior
tldr: "Use events when you need to intercept AI requests or responses across all operations without modifying providers. Changed in 1.4: AiExceptionEvent fires when a provider throws — subscribers can rewrite the error or inject a recovery output to prevent re-throwing."
drupal_version: "11.x"
---

# Events System

## When to Use

> Use events when you need to intercept AI requests or responses across all operations without modifying providers. Use [Guardrails](guardrails-system.md) when you need content filtering. Use events for logging, caching, authentication override, or telemetry.

All AI operations fire events via Symfony's event dispatcher. Subscribe to modify requests, log responses, or add custom behavior.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Modify input before call | `PreGenerateResponseEvent` | Can rewrite input, change auth, force output |
| Cache/return early | `PreGenerateResponseEvent` + `setForcedOutputObject()` | Short-circuits the provider call |
| Log or audit responses | `PostGenerateResponseEvent` | Fires after non-streamed response |
| Audit streamed responses | `PostStreamingResponseEvent` | Read-only; fires after stream completes |
| Handle provider exceptions | `AiExceptionEvent` (1.4) | Rewrite error or inject fallback output |

## Pattern

```php
use Drupal\ai\Event\PreGenerateResponseEvent;
use Drupal\ai\Event\PostGenerateResponseEvent;

class MyEventSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PreGenerateResponseEvent::EVENT_NAME => ['onPreGenerate', 0],
      PostGenerateResponseEvent::EVENT_NAME => ['onPostGenerate', 0],
    ];
  }

  public function onPreGenerate(PreGenerateResponseEvent $event): void {
    $operationType = $event->getOperationType();
    $tags = $event->getTags();
    $input = $event->getInput();
    // Modify input, check cache, add context
    $event->setInput($modifiedInput);
  }

  public function onPostGenerate(PostGenerateResponseEvent $event): void {
    $output = $event->getOutput();
    $tokenUsage = $event->getTokenUsage(); // if available
    // Log, transform, cache, or audit
  }
}
```

## Event Types

| Event | Constant | When | Can Modify |
|-------|----------|------|------------|
| `PreGenerateResponseEvent` | `ai.pre_generate_response` | Before provider call | Input, config, auth, tags; can force output |
| `PostGenerateResponseEvent` | `ai.post_generate_response` | After non-streamed response | Output (post-process) |
| `PostStreamingResponseEvent` | `ai.post_streaming_response` | After streamed response completes | Read-only (collection only) |
| `ProviderDisabledEvent` | -- | Provider marked unavailable | -- |
| `AiExceptionEvent` | -- | **Changed in 1.4:** Fired by ProviderProxy when a provider throws an exception | Rewrite message; set forced recovery output |

All events extend `AiProviderRequestBaseEvent` which provides: `requestThreadId` (UUID linking pre/post events), `requestParentId` (for nested/chained calls), `metadata` (arbitrary key-value store that carries from pre to post), `providerId`, `operationType`, `configuration`, `input`, `modelId`, `tags`, `debugData`.

## PreGenerateResponseEvent — Advanced Capabilities

| Method | Purpose |
|--------|---------|
| `setAuthentication($auth)` | Override provider authentication at runtime (e.g., per-user API keys) |
| `setForcedOutputObject(OutputInterface $output)` | Short-circuit the provider call entirely — return a cached or default response |
| `getForcedOutputObject()` | Check if another subscriber forced an output |
| `setMetadata($key, $value)` | Store metadata that passes through to PostGenerateResponseEvent |

## PostStreamingResponseEvent

Fires after a streamed response completes. Extends `AiProviderResponseBaseEvent` (same as `PostGenerateResponseEvent`). Use `getRequestThreadId()` to correlate with the original `PostGenerateResponseEvent`. This event is **read-only** — it exists for collecting final results of streamed responses, not for modification.

## AiExceptionEvent (Changed in 1.4)

Fired by `ProviderProxy` immediately before re-throwing a caught provider exception. Subscribers can:

- Rewrite the exception message via `setMessage()` (useful for user-friendly error messages)
- Inject a recovery output via `setForcedOutputObject(OutputInterface $output)` — the proxy uses this instead of re-throwing (enables fallback providers or cached responses)

```php
use Drupal\ai\Event\AiExceptionEvent;

public function onAiException(AiExceptionEvent $event): void {
  if ($event->getException() instanceof AiRateLimitException) {
    // Serve a cached response from backup storage
    $event->setForcedOutputObject($cachedOutput);
  }
}

public static function getSubscribedEvents(): array {
  return [AiExceptionEvent::class => ['onAiException', 0]];
}
```

## Event Properties

| Method | Pre | Post | PostStreaming | Description |
|--------|-----|------|--------------|-------------|
| `getInput()` / `setInput()` | R/W | R | R | Operation input |
| `getOutput()` | -- | R/W | R | Operation output |
| `getOperationType()` | R | R | R | Type string (`chat`, etc.) |
| `getProviderId()` | R | R | R | Provider plugin ID |
| `getModelId()` | R | R | R | Model identifier |
| `getTags()` / `setTags()` | R/W | R | R | Request tags array |
| `getConfiguration()` / `setConfiguration()` | R/W | R | R | Provider config |
| `getRequestThreadId()` | R | R | R | UUID linking pre/post events |
| `getRequestParentId()` | R | R | R | Parent request UUID (chained calls) |
| `getMetadata($key)` / `setMetadata($key, $val)` | R/W | R/W | R | Arbitrary metadata store |
| `getDebugData()` / `setDebugData($key, $val)` | R/W | R/W | R | Debug data |
| `setAuthentication($auth)` | R/W | -- | -- | Override authentication at runtime |
| `setForcedOutputObject($output)` | R/W | -- | -- | Short-circuit the provider call |

## Tagging Convention

```php
$provider->chat($input, $model, [
  'my_module',                          // Module tag
  'my_module:feature:summarize',        // Feature tag
  'my_module:entity_type:node',         // Entity type
  'my_module:bundle:article',           // Bundle
]);
```

Tags enable: logging filters, guardrail targeting, event subscriber filtering, cost attribution.

## Common Mistakes

- **Wrong**: Not using `getRequestThreadId()` to correlate pre/post events → **Right**: UUID links pre and post events; use it for correlated logging
- **Wrong**: Modifying output in `PostStreamingResponseEvent` → **Right**: This event is read-only — use `PostGenerateResponseEvent` for modification
- **Wrong**: Not handling `AiExceptionEvent` for rate limits → **Right**: Subscribe to inject fallback responses instead of surfacing API errors to users

## See Also

- [Guardrails System](guardrails-system.md)
- [AI Observability](ai-observability.md)
- [Exceptions](exceptions.md)
- Reference: `web/modules/contrib/ai/src/Event/`
