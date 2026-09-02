---
description: AI enums and DTOs — AiModelCapability, AiProviderCapability, StructuredOutputSchema, TokenUsageDto, and ChatProviderLimitsDto
tldr: "Filter models by AiModelCapability, enforce structured output via StructuredOutputSchema, or track token costs via TokenUsageDto. New in 1.4: ChatWithPdf capability. Deprecated: setChatStrictSchema() — set strict: TRUE on StructuredOutputSchema."
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

## AiModelCapability Enum

Typed capabilities that models can declare. Used to filter `getConfiguredModels()` results.

**Chat capabilities:**

| Case | Value | Description |
|------|-------|-------------|
| `ChatWithImageVision` | `chat_with_image_vision` | Model accepts image inputs |
| `ChatWithAudio` | `chat_with_audio` | Model accepts audio inputs |
| `ChatWithVideo` | `chat_with_video` | Model accepts video inputs |
| `ChatWithPdf` | `chat_with_pdf` | **New in 1.4:** Model accepts PDF document inputs |
| `ChatSystemRole` | `chat_system_role` | Model supports system role |
| `ChatJsonOutput` | `chat_json_output` | Reliable complex JSON output |
| `ChatStructuredResponse` | `chat_structured_response` | Native structured/schema responses |
| `ChatTools` | `chat_tools` | Native tool/function calling |
| `ChatCombinedToolsAndStructuredResponse` | `chat_combined_tools_and_structured_response` | Tools + structured response in one call |

```php
// Get models that support vision.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithImageVision]);

// Get models that support PDF input.
$models = $provider->getConfiguredModels('chat', [AiModelCapability::ChatWithPdf]);
```

## AiModelCapability — Image-to-Image

**Image-to-Image capabilities:** `ImageToImageUpscale`, `ImageToImageOutpaint`, `ImageToImageInpaint`, `ImageToImageErase`, `ImageToImageSearchReplace`, `ImageToImageSearchRecolor`, `ImageToImageRemoveBackground`, `ImageToImageSketch`, `ImageToImageStyleGuide`, `ImageToImageStyleTransfer`

Each case has `getBaseOperationType()` (returns `chat` or `image_to_image`), `getTitle()`, and `getDescription()`.

## AiProviderCapability Enum

Provider-level (not model-level) capabilities:

| Case | Value | Description |
|------|-------|-------------|
| `StreamChatOutput` | `stream_chat_output` | Provider supports chat streaming |
| `ChatFiberSupport` | `chat_fiber_support` | Provider supports PHP Fibers for streaming |

## StructuredOutputSchema DTO

Defines how the AI provider should structure its response. Pass to `ChatInput::setChatStructuredJsonSchema()`.

```php
use Drupal\ai\Dto\StructuredOutputSchema;

$schema = new StructuredOutputSchema(
  name: 'weather_response',       // lowercase, hyphens, underscores only
  description: 'Weather data',
  strict: TRUE,                    // provider must follow schema exactly
  json_schema: [
    'properties' => [
      'temperature' => ['type' => 'number'],
      'location' => ['type' => 'string'],
    ],
  ],
);

// Or from array (e.g., from config):
$schema = StructuredOutputSchema::fromArray([
  'name' => 'my_schema',
  'schema' => ['properties' => ['answer' => ['type' => 'string']]],
]);

$input = new ChatInput([new ChatMessage('user', 'What is the weather?')]);
$input->setChatStructuredJsonSchema($schema);
```

Validation: `name` must match `/^[a-z0-9_-]+$/`; `json_schema` must have a `properties` key. `fromArray()` validates on creation and throws `\InvalidArgumentException` on failure.

**Deprecated in 1.4:** `ChatInput::setChatStrictSchema(bool $strict)` and `getChatStrictSchema()` are deprecated and will be removed in 2.0.0. Set `strict: TRUE` on the `StructuredOutputSchema` DTO instead. `setChatStructuredJsonSchema()` now accepts both array and `StructuredOutputSchema` instances.

## TokenUsageDto

Tracks token consumption from provider responses:

| Property | Type | Description |
|----------|------|-------------|
| `input` | `?int` | Input tokens |
| `output` | `?int` | Output tokens |
| `total` | `?int` | Total tokens |
| `reasoning` | `?int` | Reasoning tokens (e.g., o1 models) |
| `cached` | `?int` | Cached tokens |

## ChatProviderLimitsDto

Rate limit information from provider response headers:

| Property | Type | Description |
|----------|------|-------------|
| `rateLimitMaxRequests` | `?int` | Max requests allowed |
| `rateLimitMaxTokens` | `?int` | Max tokens allowed |
| `rateLimitRemainingRequests` | `?int` | Remaining requests |
| `rateLimitRemainingTokens` | `?int` | Remaining tokens |
| `rateLimitResetRequests` | `?int` | Seconds until request limit resets |
| `rateLimitResetTokens` | `?int` | Seconds until token limit resets |

Both DTOs use `DtoBaseMethodsTrait` providing `create(array $values)` (factory) and `toArray()`.

## Other Enums

| Enum | Values |
|------|--------|
| `VdbSimilarityMetrics` | `CosineSimilarity`, `EuclideanDistance`, `InnerProduct` |
| `VdbCapability` | `GroupBy` (grouping matches to avoid duplicates) |
| `EmbeddingStrategyCapability` | `MultipleMainContent` |
| `EmbeddingStrategyIndexingOptions` | `MainContent`, `ContextualContent`, `Attributes`, `Ignore` -- with `getKey()`, `getLabel()`, `getDescription()` |

## Common Mistakes

- **Wrong**: Using `StructuredOutputSchema` with `name` containing uppercase or spaces → **Right**: Name must match `/^[a-z0-9_-]+$/`
- **Wrong**: Assuming all providers support `ChatTools` → **Right**: Check `AiModelCapability::ChatTools` via `getConfiguredModels()` first
- **Wrong**: Calling `setChatStrictSchema()` in 1.4.x → **Right**: Deprecated; set `strict: TRUE` on `StructuredOutputSchema` DTO

## See Also

- [Operation Types](operation-types.md)
- [Provider System](provider-system.md)
- Reference: `web/modules/contrib/ai/src/Enum/AiModelCapability.php`
- Reference: `web/modules/contrib/ai/src/Dto/StructuredOutputSchema.php`
