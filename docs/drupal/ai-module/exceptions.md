---
description: AI exception types — catch hierarchy, when each exception fires, and ProviderProxy re-throw behavior
tldr: "Use this guide when handling errors from AI provider calls. Always catch specific exceptions before the generic AiExceptionInterface. Changed in 1.4: ProviderProxy also dispatches AiExceptionEvent before re-throwing — subscribe to inject fallback output instead of surfacing errors to users."
drupal_version: "11.x"
---

# AI Exceptions

## When to Use

> Use this guide when handling errors from AI provider calls. Always catch specific exceptions before the generic `AiExceptionInterface`.

All AI exceptions implement `AiExceptionInterface` (extends `\Throwable`). Catch this interface to handle any AI-specific error generically.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Handle all AI errors generically | `AiExceptionInterface` | All AI exceptions implement this |
| Rate limit with backoff | `AiRateLimitException` | Provider hit rate limit |
| Out of credits | `AiQuotaException` | Provider quota exhausted |
| Content blocked | `AiUnsafePromptException` | Guardrail or moderation blocked |
| Bad API key / setup | `AiSetupFailureException` | Known broken setup |
| Provider doesn't support feature | `AiMissingFeatureException` | e.g., streaming on non-streaming provider |
| Graceful failover on any error | `AiExceptionEvent` subscriber (1.4) | Inject cached/fallback response before re-throw |

## Pattern

```php
use Drupal\ai\Exception\AiExceptionInterface;
use Drupal\ai\Exception\AiRateLimitException;
use Drupal\ai\Exception\AiUnsafePromptException;

try {
  $output = $provider->chat($input, $model, ['my_module']);
} catch (AiRateLimitException $e) {
  // Retry with exponential backoff.
} catch (AiUnsafePromptException $e) {
  // Content was blocked by moderation/guardrails.
  $this->messenger->addError($this->t('Request blocked.'));
} catch (AiExceptionInterface $e) {
  // Generic AI error handling.
  $this->logger->error('AI error: @msg', ['@msg' => $e->getMessage()]);
}
```

## Exception Reference

| Exception | When Thrown |
|-----------|------------|
| `AiBadRequestException` | Malformed request, missing model ID, client invocation error, or unclassified provider error |
| `AiRateLimitException` | Provider reports rate limiting |
| `AiQuotaException` | Provider reports exhausted credits/quota |
| `AiAccessDeniedException` | Provider denies access even though setup is correct (e.g., model-level restriction) |
| `AiRequestErrorException` | Request structure error or generic request failure |
| `AiResponseErrorException` | Unexpected or malformed provider response |
| `AiSetupFailureException` | Known provider setup is broken (bad API key, misconfigured endpoint) |
| `AiMissingFeatureException` | Requested feature not supported by provider (e.g., streaming on non-streaming provider) |
| `AiUnsafePromptException` | Content moderation or guardrail blocked the prompt |
| `AiBrokenOutputException` | Input or output corrupted by manipulation (e.g., guardrail rewrite produced invalid data) |
| `AiOperationTypeMissingException` | Called an operation type the provider doesn't implement |
| `AiToolsValidationException` | Tool/function call validation failed |
| `AiFunctionCallingExecutionError` | Error during tool/function execution |
| `ChunkingTooSmallException` | Text chunk smaller than minimum constraints (embedding strategy) |

## ProviderProxy Exception Handling

The `ProviderProxy` catches exceptions from provider calls and re-throws them with logging. Specific types (`AiResponseErrorException`, `AiMissingFeatureException`, `AiQuotaException`, `AiRateLimitException`, `AiUnsafePromptException`, `AiRequestErrorException`) are re-thrown as-is. `ClientExceptionInterface` (PSR HTTP) is wrapped in `AiBadRequestException`. Any other `\Exception` is wrapped in `AiRequestErrorException`.

**Changed in 1.4:** Before re-throwing, the proxy dispatches `AiExceptionEvent`. Subscribers can inject a forced recovery output via `setForcedOutputObject()` — the proxy uses this instead of re-throwing. See [Events System](events-system.md).

## Common Mistakes

- **Wrong**: Catching only `\Exception` → **Right**: Catch `AiExceptionInterface` to specifically handle AI errors
- **Wrong**: Not catching `AiUnsafePromptException` in user-facing features → **Right**: This exception is thrown when guardrails block content; handle gracefully
- **Wrong**: Not using `AiExceptionEvent` for rate limit fallback (1.4) → **Right**: Subscribe to `AiExceptionEvent` to inject cached responses when providers fail

## See Also

- [Guardrails System](guardrails-system.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/ai/src/Exception/`
