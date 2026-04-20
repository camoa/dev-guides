---
description: AI enums and DTOs — AiModelCapability, AiProviderCapability, StructuredOutputSchema, TokenUsageDto, and ChatProviderLimitsDto
tldr: "Use this guide when filtering models by capability, building structured output schemas, or tracking token usage from provider responses."
drupal_version: "11.x"
---

# Enums & DTOs

## When to Use

> Use this guide when filtering models by capability, building structured output schemas, or tracking token usage from provider responses.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Filter models by capability | `AiModelCapability` enum | Pass as array to `getConfiguredModels()` |
| Require structured JSON output | `StructuredOutputSchema` DTO | Provider enforces schema |
| Track token costs | `TokenUsageDto` | Extracted from provider response |
| Check rate limit headers | `ChatProviderLimitsDto` | Parsed from provider response headers |

## AiModelCapability (Chat)

| Case | Value | Description |
|------|-------|-------------|
| `ChatWithImageVision` | `chat_with_image_vision` | Model accepts image inputs |
| `ChatSystemRole` | `chat_system_role` | Model supports system role |
| `ChatJsonOutput` | `chat_json_output` | Reliable complex JSON output |
| `ChatStructuredResponse` | `chat_structured_response` | Native structured/schema responses |
| `ChatTools` | `chat_tools` | Native tool/function calling |
| `ChatCombinedToolsAndStructuredResponse` | combined | Tools + structured response in one call |

```php
// Get models that support vision.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithImageVision]);
```

## StructuredOutputSchema DTO

```php
use Drupal\ai\Dto\StructuredOutputSchema;

$schema = new StructuredOutputSchema(
  name: 'weather_response',   // Lowercase, hyphens, underscores only
  description: 'Weather data',
  strict: TRUE,
  json_schema: [
    'properties' => [
      'temperature' => ['type' => 'number'],
      'location' => ['type' => 'string'],
    ],
  ],
);

$input = new ChatInput([new ChatMessage('user', 'What is the weather?')]);
$input->setChatStructuredJsonSchema($schema);
```

Validation: `name` must match `/^[a-z0-9_-]+$/`; `json_schema` must have a `properties` key.

## TokenUsageDto

| Property | Type | Description |
|----------|------|-------------|
| `input` | `?int` | Input tokens |
| `output` | `?int` | Output tokens |
| `total` | `?int` | Total tokens |
| `reasoning` | `?int` | Reasoning tokens (e.g., o1 models) |
| `cached` | `?int` | Cached tokens |

## AiProviderCapability (Provider-level)

| Case | Value | Description |
|------|-------|-------------|
| `StreamChatOutput` | `stream_chat_output` | Provider supports chat streaming |
| `ChatFiberSupport` | `chat_fiber_support` | Provider supports PHP Fibers |

## VdbSimilarityMetrics

`CosineSimilarity`, `EuclideanDistance`, `InnerProduct`

## Common Mistakes

- **Wrong**: Using `StructuredOutputSchema` with `name` containing uppercase or spaces → **Right**: Name must match `/^[a-z0-9_-]+$/`
- **Wrong**: Assuming all providers support `ChatTools` → **Right**: Check `AiModelCapability::ChatTools` via `getConfiguredModels()` first

## See Also

- [Operation Types](operation-types.md)
- [Provider System](provider-system.md)
- Reference: `web/modules/contrib/ai/src/Enum/AiModelCapability.php`
- Reference: `web/modules/contrib/ai/src/Dto/StructuredOutputSchema.php`
