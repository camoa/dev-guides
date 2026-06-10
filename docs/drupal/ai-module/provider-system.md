---
description: AI provider plugins — using, building, file handling, and selecting providers for AI operations
tldr: "Extend OpenAiBasedProviderClientBase for OpenAI-compatible APIs; always check isUsable() before calling. 1.4.2 adds AiFileProviderInterface for provider-side file uploads; use ai.file_manager service, not direct provider methods."
drupal_version: "11.x"
---

# AI Provider System

## When to Use

> Use this guide when calling a specific provider, building a custom provider plugin, or working with the provider/model selection form. Use [Operation Types](operation-types.md) for the typed Input/Output classes.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Provider with unique API | `AiProviderClientBase` | Full flexibility to implement any API |
| Provider with OpenAI-compatible API | `OpenAiBasedProviderClientBase` | Gets chat, embeddings, TTS, STT, T2I for free |
| List models for a form | `getSimpleProviderModelOptions()` | Returns formatted `provider__model => label` array |
| Check if operation is available | `hasProvidersForOperationType()` | Boolean check before calling |
| Upload file to provider | `ai.file_manager` service | Lifecycle management; don't call provider file methods directly |

## Pattern

```php
$providerManager = \Drupal::service('ai.provider');

// Get default provider for an operation type.
$defaults = $providerManager->getDefaultProviderForOperationType('chat');

// Create a provider instance (returns ProviderProxy).
$provider = $providerManager->createInstance('anthropic');

// Check availability before calling.
if (!$provider->isUsable('chat')) {
  return;
}

// Get models for a select element.
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
    return ['chat'];
  }

  public function getConfiguredModels(string $operation_type): array {
    return ['my-model-v1' => 'My Model v1'];
  }

  public function chat(ChatInput $input, string $model_id, array $tags = []): ChatOutput {
    // Call API, normalize response.
    return new ChatOutput($input, $normalizedMessages, $rawResponse, []);
  }
}
```

## Provider File Handling (New in 1.4.2)

Providers that support a remote Files API implement `AiFileProviderInterface` (`Drupal\ai\AiFileProviderInterface`):

| Method | Purpose |
|--------|---------|
| `uploadFile(AiFileInterface $ai_file, mixed $file): AiFileInterface` | Upload binary/stream; MUST set remote ID on entity |
| `deleteFile(AiFileInterface $ai_file): bool` | Delete remote file by stored remote ID |
| `downloadFile(AiFileInterface $ai_file, ?string $destination = NULL): string` | Download to path, or return raw contents when no destination given |
| `supportsMimeType(string $mime_type, string $purpose): bool` | Whether MIME type is allowed for the purpose |

OpenAI-compatible providers get this via `FileApiTrait` (`Drupal\ai\Traits\OpenAi\FileApiTrait`), which maps to the OpenAI `files()` endpoint. Don't call provider file methods directly — use `ai.file_manager`. See [Operation Types](operation-types.md) for the `AiFileManager` API.

## Scaffolding (New in 1.4)

```bash
drush generate plugin:ai:provider       # alias: ai-provider
drush generate plugin:ai:guardrail      # alias: ai-guardrail
drush generate plugin:ai:automator-type # alias: ai-automator-type
```

## Provider Matrix

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

## Base Classes

| Class | Use When |
|-------|----------|
| `AiProviderClientBase` | Custom provider with unique API |
| `OpenAiBasedProviderClientBase` | Provider with OpenAI-compatible API (e.g., Ollama, LiteLLM) |

`OpenAiBasedProviderClientBase` implements `ChatInterface`, `ModerationInterface`, `EmbeddingsInterface`, `TextToSpeechInterface`, `SpeechToTextInterface`, and `TextToImageInterface` out of the box. It handles streaming, token usage extraction into `TokenUsageDto`, rate limit parsing into `ChatProviderLimitsDto`, and standard error mapping. Only `loadClient()` needs to be provided.

## Key AiProviderInterface Methods

| Method | Purpose |
|--------|---------|
| `getAvailableConfiguration($op, $model)` | Returns configurable parameters for model config UI |
| `getDefaultConfigurationValues($op, $model)` | Default parameter values |
| `setAuthentication($auth)` | Override authentication at runtime |
| `getSupportedCapabilities()` | Returns `AiModelCapability[]` or `AiProviderCapability[]` the provider supports |
| `getSetupData()` | Returns `key_config_name` (Key module) + `default_models` |
| `setTag($tag)` / `getTags()` | Tag management for logging/filtering |
| `setDebugData($key, $value)` / `getDebugData()` | Attach debug metadata to requests |

## Common Mistakes

- **Wrong**: Using `createInstance()` without checking `isUsable()` → **Right**: Provider may lack API key — check first
- **Wrong**: Not implementing `getAvailableConfiguration()` → **Right**: Breaks the form helper's model configuration UI
- **Wrong**: Missing `loadClient()` → **Right**: Base class expects this for lazy client initialization
- **Wrong**: Calling provider file methods directly → **Right**: Always use `ai.file_manager` service for file lifecycle management

## See Also

- [Core Architecture](core-architecture.md)
- [Operation Types](operation-types.md)
- Reference: `web/modules/contrib/ai/src/Base/AiProviderClientBase.php`
- Reference: `web/modules/contrib/ai/src/Base/OpenAiBasedProviderClientBase.php`
- Reference: `web/modules/contrib/ai/src/AiFileProviderInterface.php`
