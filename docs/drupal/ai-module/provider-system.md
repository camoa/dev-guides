---
description: AI provider plugins — using, building, file handling, and selecting providers for AI operations
tldr: "Extend OpenAiBasedProviderClientBase for OpenAI-compatible APIs; always check isUsable() before calling. 1.4.2 adds AiFileProviderInterface for provider-side file uploads; use ai.file_manager service, not direct provider methods."
drupal_version: "11.x"
---

# AI Provider System

## When to Use

> Use this guide when calling a specific provider, building a custom provider plugin, or working with the provider/model selection form. Use [Operation Types](operation-types.md) for the typed Input/Output classes.

Providers are plugins implementing `AiProviderInterface`. Each provider wraps one AI service and declares which operation types it supports.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Provider with unique API | `AiProviderClientBase` | Full flexibility to implement any API |
| Provider with OpenAI-compatible API | `OpenAiBasedProviderClientBase` | Gets chat, embeddings, TTS, STT, T2I for free |
| List models for a form | `getSimpleProviderModelOptions()` | Returns formatted `provider__model => label` array |
| Check if operation is available | `hasProvidersForOperationType()` | Boolean check before calling |
| Upload file to provider | `ai.file_manager` service | Lifecycle management; don't call provider file methods directly |

## Using Providers

```php
// Get the provider manager
$providerManager = \Drupal::service('ai.provider');

// Get default provider for an operation type
$defaults = $providerManager->getDefaultProviderForOperationType('chat');
// Returns: ['provider_id' => 'anthropic', 'model_id' => 'claude-sonnet-4-20250514']

// Create a provider instance (returns ProviderProxy)
$provider = $providerManager->createInstance('anthropic');

// Check availability
$providerManager->hasProvidersForOperationType('embeddings'); // bool

// Get all models for operation type
$models = $provider->getConfiguredModels('chat');

// Get simple options for form selects
$options = $providerManager->getSimpleProviderModelOptions('chat');
// Returns: ['anthropic__claude-3-sonnet' => 'Anthropic: Claude 3 Sonnet', ...]
```

## Building a Custom Provider

```php
use Drupal\ai\Attribute\AiProvider;
use Drupal\ai\Base\AiProviderClientBase;

#[AiProvider(
  id: 'my_provider',
  label: new TranslatableMarkup('My Provider'),
)]
class MyProvider extends AiProviderClientBase implements ChatInterface {

  public function isUsable(?string $operation_type = NULL): bool {
    return !empty($this->getApiKey());
  }

  public function getSupportedOperationTypes(): array {
    return ['chat', 'embeddings'];
  }

  public function getConfiguredModels(string $operation_type): array {
    return ['my-model-v1' => 'My Model v1'];
  }

  public function chat(ChatInput $input, string $model_id, array $tags = []): ChatOutput {
    $client = $this->loadClient($model_id);
    // ... call API, normalize response
    return new ChatOutput($input, $normalizedMessages, $rawResponse, []);
  }
}
```

## Provider Matrix (Key Providers)

| Provider | Chat | Embeddings | Moderation | TTS | STT | T2I | Translation |
|----------|------|-----------|------------|-----|-----|-----|-------------|
| Anthropic | Yes | | | | | | |
| OpenAI | Yes | Yes | Yes | Yes | Yes | Yes | |
| Google/Gemini | Yes | | | | | | |
| Ollama | Yes | Yes | | | | | |
| AWS Bedrock | Yes | Yes | | | | Yes | |
| Azure | Yes | Yes | Yes | Yes | Yes | Yes | |
| LiteLLM | Yes | Yes | Yes | Yes | Yes | Yes | |
| DeepL | | | | | | | Yes |
| Vertex AI | Yes | Yes | | | | | Yes |

## Key AiProviderInterface Methods

Beyond `getConfiguredModels()`, `isUsable()`, `getSupportedOperationTypes()`:

| Method | Purpose |
|--------|---------|
| `getAvailableConfiguration($op, $model)` | Returns configurable parameters (temperature, max_tokens, etc.) for the model config UI |
| `getDefaultConfigurationValues($op, $model)` | Default values for configuration parameters |
| `setAuthentication($auth)` | Override authentication at runtime (used by PreGenerateResponseEvent) |
| `setConfiguration($config)` / `getConfiguration()` | Runtime config override |
| `getSupportedCapabilities()` | Returns `AiModelCapability[]` or `AiProviderCapability[]` the provider supports |
| `loadModelsForm($form, $state, $op, $model)` | Builds per-model config form in admin UI |
| `hasPredefinedModels()` | `false` = system generates model list dynamically |
| `getSetupData()` | Returns `key_config_name` (Key module integration) + `default_models` for initial setup |
| `setTag($tag)` / `getTags()` / `resetTags()` | Tag management for logging/filtering |
| `setDebugData($key, $value)` / `getDebugData()` | Attach debug metadata to requests |

## Base Classes

| Class | Use When |
|-------|----------|
| `AiProviderClientBase` | Custom provider with unique API |
| `OpenAiBasedProviderClientBase` | Provider with OpenAI-compatible API (e.g., Ollama, LiteLLM) |

`OpenAiBasedProviderClientBase` implements `ChatInterface`, `ModerationInterface`, `EmbeddingsInterface`, `TextToSpeechInterface`, `SpeechToTextInterface`, and `TextToImageInterface` out of the box using the `openai-php/client` library. It handles streaming via `OpenAiTypeStreamedChatMessageIterator`, token usage extraction into `TokenUsageDto`, rate limit parsing into `ChatProviderLimitsDto`, and standard error mapping to AI exceptions. Extend it when your provider's API is OpenAI-compatible — you only need to provide `loadClient()` with your endpoint/key.

## Provider File Handling (New in 1.4.2)

Providers that support a remote Files API (upload a document once, reference it across requests) implement `AiFileProviderInterface` (`Drupal\ai\AiFileProviderInterface`):

| Method | Purpose |
|--------|---------|
| `uploadFile(AiFileInterface $ai_file, mixed $file): AiFileInterface` | Upload binary/stream to the provider; implementation MUST set the remote id on the entity |
| `deleteFile(AiFileInterface $ai_file): bool` | Delete the remote file by its stored remote id |
| `downloadFile(AiFileInterface $ai_file, ?string $destination = NULL): string` | Download remote file to a path, or return raw contents when no destination is given |
| `supportsMimeType(string $mime_type, string $purpose): bool` | Whether a MIME type is allowed for the declared purpose |

OpenAI-compatible providers get this for free via the `FileApiTrait` (`Drupal\ai\Traits\OpenAi\FileApiTrait`), which maps to the OpenAI `files()` endpoint and enforces per-purpose MIME rules (batch/fine-tune → `text/plain`, `application/jsonl`, `application/json`; vision → images; otherwise unrestricted). Don't call a provider's file methods directly — go through the `ai.file_manager` service (see [Operation Types](operation-types.md)).

## Scaffolding Providers (New in 1.4)

The module ships a Drush code generator for new providers:

```bash
drush generate plugin:ai:provider   # alias: ai-provider
```

(Companion generators exist for guardrails — `plugin:ai:guardrail` — and automator types — `plugin:ai:automator-type`.)

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Using `createInstance()` without checking `isUsable()` | Provider may lack API key — check first |
| Not implementing `getAvailableConfiguration()` | Breaks the form helper's model configuration UI |
| Missing `loadClient()` | Base class expects this for lazy client initialization |
| Calling a provider's file methods directly | Always use the `ai.file_manager` service for file lifecycle management |

## See Also

- [Core Architecture](core-architecture.md)
- [Operation Types](operation-types.md)
- Reference: `web/modules/contrib/ai/src/Base/AiProviderClientBase.php`
- Reference: `web/modules/contrib/ai/src/Base/OpenAiBasedProviderClientBase.php`
- Reference: `web/modules/contrib/ai/src/AiFileProviderInterface.php`
