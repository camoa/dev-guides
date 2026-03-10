---
description: AI API Explorer — developer UI for testing AI operations interactively with code examples
drupal_version: "11.x"
---

# AI API Explorer

## When to Use

> Use `ai_api_explorer` for interactive testing of AI operations during development. **Do not enable on production.** Use [Operation Types](operation-types.md) for the actual PHP API.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Test a provider/model | Chat Explorer | Most feature-rich; supports streaming, tools, vision |
| Test tool/function calling | Tools Explorer | Lists all FunctionCall plugins; dynamic form per tool |
| Test any operation type | Specific explorer | 16 explorers for all operation types |
| Get copy-paste code | Any explorer | Every explorer generates a PHP snippet |

## Features

- 16 interactive explorers (chat, T2I, TTS, STT, embeddings, moderation, etc.)
- Provider/model selection per request
- Streaming support (Chat Explorer)
- File uploads (images, audio, documents)
- Copy-paste PHP code example generation
- Guardrail set selection (Chat Explorer)
- Structured output / JSON schema testing

## Explorer Feature Matrix

| Feature | Chat | Text-to-Image | Speech-to-Text | Tools |
|---------|------|---------------|---------------|-------|
| Streaming (SSE) | Yes | No | No | No |
| File uploads | Yes (images, docs) | No | Yes (audio) | No |
| Tool/function calling | Yes | No | No | Yes (primary) |
| Structured output | Yes | No | No | No |
| Code example generation | Yes | Yes | Yes | No |

## Custom Explorer Plugin

```php
#[AiApiExplorer(
  id: 'my_explorer',
  title: new TranslatableMarkup('My Explorer'),
  description: new TranslatableMarkup('Tests my operation.'),
)]
class MyExplorer extends AiApiExplorerPluginBase {
  public function isActive(): bool {
    return $this->providerManager->hasProvidersForOperationType('my_type');
  }
  // buildForm(), getResponse(), etc.
}
```

Route auto-registered at `/admin/config/ai/explorers/{plugin_id}`.

## Permission

- `access ai prompt` — required for all explorers

## Common Mistakes

- **Wrong**: Enabling on production → **Right**: Developer tool only; exposes all providers and models to anyone with the permission
- **Wrong**: Using explorer responses in production code → **Right**: Use the generated PHP code snippet as a starting point

## See Also

- [Operation Types](operation-types.md)
- [Provider System](provider-system.md)
- Reference: `web/modules/contrib/ai/modules/ai_api_explorer/`
