---
description: AI module architecture - provider layer, model types, plugin system, and service layer
drupal_version: "11.x"
---

# AI Module Architecture

## When to Use

> Use AI module architecture knowledge before implementing any AI functionality. Understanding the provider layer, model types, and plugin system is essential for choosing the right approach for your use case.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Simple text generation | Chat models via provider | Direct API access, minimal overhead |
| Field-level automation | AI Automators | Built-in field integration, workflow support |
| Semantic search | Vector database + Search API | Native Drupal search integration |
| Multi-step AI workflows | Automator chains | Complex logic with field dependencies |
| Custom AI operations | Function calling plugins | Extensible, reusable AI tools |

## Core Components

The Drupal AI module 1.2.x provides a unified abstraction layer for integrating AI services. The architecture consists of four primary layers:

**Provider Layer**: Manages connections to AI services (OpenAI, Anthropic Claude, AWS Bedrock, Amazee.io). Each provider implements the `AiProviderInterface` and exposes available models through plugin discovery.

**Model Types**: AI models are categorized by capability:
- Text generation (chat, completion)
- Text-to-text (embeddings, moderation)
- Text-to-image (DALL-E, Stable Diffusion)
- Image-to-text (vision, OCR)
- Audio-to-text (transcription, Whisper)
- Text-to-audio (speech synthesis)

**Plugin System**: Extensible architecture supporting:
- `AiProvider`: Provider implementations
- `AiVdbProvider`: Vector database providers
- `AiAutomatorType`: Field automation types (50+ types)
- `AiFunctionCall`: Function calling capabilities
- `AiFunctionGroup`: Grouped function definitions
- `AiDataTypeConverter`: Data transformation
- `AiShortTermMemory`: Conversation memory management

**Service Layer**: Core services include:
- `ai.provider`: Provider plugin manager
- `ai.vdb_provider`: Vector database manager
- `ai.prompt_manager`: Prompt template management
- `ai.tokenizer`: Token counting and limits
- `ai.text_chunker`: Content chunking for embeddings

## Pattern

```php
// Access AI provider service
$ai_provider = \Drupal::service('ai.provider');

// Get available providers
$providers = $ai_provider->getDefinitions();

// Load a specific model
$model = $ai_provider->createInstance('openai', [
  'model_name' => 'gpt-4',
]);

// Generate text
$response = $model->chat([
  ['role' => 'user', 'content' => 'Summarize this content...']
], 'gpt-4');
```

## Common Mistakes

- **Wrong**: Using providers without checking capabilities → **Right**: Always verify model type support before calling methods (e.g., not all providers support vision or audio)
- **Wrong**: Hardcoding model names → **Right**: Use configuration entities or settings forms to allow runtime model selection
- **Wrong**: Ignoring rate limits in provider config → **Right**: Configure rate limiting and queueing to prevent API errors
- **Wrong**: Not handling provider failures gracefully → **Right**: Implement fallback providers or queue retry mechanisms
- **Wrong**: Loading entire AI module when only needing one feature → **Right**: Enable only required submodules (ai_automators, ai_search, etc.)

## See Also

- [Provider Configuration](provider-configuration.md)
- Reference: `/modules/contrib/ai/src/AiProviderPluginManager.php`
- Reference: https://project.pages.drupalcode.org/ai/
