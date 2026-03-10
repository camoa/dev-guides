---
description: AI events system — subscribe to pre/post generation events to modify requests, log responses, or add custom behavior
drupal_version: "11.x"
---

# Events System

## When to Use

> Use events when you need to intercept AI requests or responses across all operations without modifying providers. Use [Guardrails](guardrails-system.md) when you need content filtering. Use events for logging, caching, authentication override, or telemetry.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Modify input before call | `PreGenerateResponseEvent` | Can rewrite input, change auth, force output |
| Cache/return early | `PreGenerateResponseEvent` + `setForcedOutputObject()` | Short-circuits the provider call |
| Log or audit responses | `PostGenerateResponseEvent` | Fires after non-streamed response |
| Audit streamed responses | `PostStreamingResponseEvent` | Read-only; fires after stream completes |

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
    $tags = $event->getTags();
    $input = $event->getInput();
    // Modify input or check cache.
    $event->setInput($modifiedInput);
  }

  public function onPostGenerate(PostGenerateResponseEvent $event): void {
    $output = $event->getOutput();
    $tokenUsage = $event->getTokenUsage();
    // Log, cache, or audit.
  }
}
```

## Event Types

| Event | Constant | When | Can Modify |
|-------|----------|------|------------|
| `PreGenerateResponseEvent` | `ai.pre_generate_response` | Before provider call | Input, config, auth, tags; can force output |
| `PostGenerateResponseEvent` | `ai.post_generate_response` | After non-streamed response | Output |
| `PostStreamingResponseEvent` | `ai.post_streaming_response` | After streamed response completes | Read-only |

## Event Properties

| Method | Pre | Post | PostStreaming |
|--------|-----|------|--------------|
| `getInput()` / `setInput()` | R/W | R | R |
| `getOutput()` | -- | R/W | R |
| `getOperationType()` | R | R | R |
| `getProviderId()` | R | R | R |
| `getTags()` / `setTags()` | R/W | R | R |
| `getRequestThreadId()` | R | R | R |
| `getMetadata($key)` / `setMetadata($key, $val)` | R/W | R/W | R |
| `setAuthentication($auth)` | R/W | -- | -- |
| `setForcedOutputObject($output)` | R/W | -- | -- |

## Tagging Convention

```php
$provider->chat($input, $model, [
  'my_module',                     // Module tag
  'my_module:feature:summarize',   // Feature tag
  'my_module:entity_type:node',    // Entity type
  'my_module:bundle:article',      // Bundle
]);
```

Tags enable: logging filters, guardrail targeting, event subscriber filtering, cost attribution.

## Common Mistakes

- **Wrong**: Not using `getRequestThreadId()` to correlate pre/post events → **Right**: UUID links pre and post events; use it for correlated logging
- **Wrong**: Modifying output in `PostStreamingResponseEvent` → **Right**: This event is read-only — use `PostGenerateResponseEvent` for modification

## See Also

- [Guardrails System](guardrails-system.md)
- [AI Observability](ai-observability.md)
- Reference: `web/modules/contrib/ai/src/Event/`
