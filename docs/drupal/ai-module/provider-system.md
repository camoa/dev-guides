---
description: AI provider plugins — using, building, and selecting providers for AI operations
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

## Provider Matrix

| Provider | Chat | Embeddings | Moderation | TTS | STT | T2I |
|----------|------|-----------|------------|-----|-----|-----|
| Anthropic | Yes | | | | | |
| OpenAI | Yes | Yes | Yes | Yes | Yes | Yes |
| Google/Gemini | Yes | | | | | |
| Ollama | Yes | Yes | | | | |
| AWS Bedrock | Yes | Yes | | | | Yes |
| Azure | Yes | Yes | Yes | Yes | Yes | Yes |
| LiteLLM | Yes | Yes | Yes | Yes | Yes | Yes |

## Key AiProviderInterface Methods

| Method | Purpose |
|--------|---------|
| `getAvailableConfiguration($op, $model)` | Returns configurable parameters for model config UI |
| `getDefaultConfigurationValues($op, $model)` | Default parameter values |
| `setAuthentication($auth)` | Override authentication at runtime |
| `getSupportedCapabilities()` | Returns `AiModelCapability[]` the provider supports |
| `getSetupData()` | Returns `key_config_name` (Key module) + `default_models` |
| `setTag($tag)` / `getTags()` | Tag management for logging/filtering |

## Common Mistakes

- **Wrong**: Using `createInstance()` without checking `isUsable()` → **Right**: Provider may lack API key — check first
- **Wrong**: Not implementing `getAvailableConfiguration()` → **Right**: Breaks the form helper's model configuration UI
- **Wrong**: Missing `loadClient()` → **Right**: Base class expects this for lazy client initialization

## See Also

- [Core Architecture](core-architecture.md)
- [Operation Types](operation-types.md)
- Reference: `web/modules/contrib/ai/src/Base/AiProviderClientBase.php`
- Reference: `web/modules/contrib/ai/src/Base/OpenAiBasedProviderClientBase.php`
