---
description: AI API Explorer — developer UI for testing AI operations interactively with code examples
tldr: "Use `ai_api_explorer` for interactive testing of AI operations during development. **Do not enable on production.** Use [Operation Types](operation-types.md) for the actual PHP API."
drupal_version: "11.x"
---

# AI API Explorer

## When to Use

> Use `ai_api_explorer` for interactive testing of AI operations during development. **Do not enable on production.** Use [Operation Types](operation-types.md) for the actual PHP API.

Developer-only UI for testing AI operations interactively. **Do not enable on production.**

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Test a provider/model | Chat Explorer | Most feature-rich; supports streaming, tools, vision |
| Test tool/function calling | Tools Explorer | Lists all FunctionCall plugins; dynamic form per tool |
| Test any operation type | Specific explorer | 16 explorers for all operation types |
| Get copy-paste code | Any explorer | Every explorer generates a PHP snippet |

## Features

- Interactive form per operation type (16 explorers)
- Provider/model selection
- Response display with streaming support
- Copy-paste PHP code examples
- Supports file uploads (images, audio, documents)

## Available Explorers (16 total)

Chat, Text-to-Image, Text-to-Speech, Speech-to-Text, Speech-to-Speech, Audio-to-Audio, Embeddings, Moderation, Image-to-Image, Image Classification, Object Detection, Rerank, Summarize, Translate, Image-and-Audio-to-Video, Tools

## Explorer Feature Matrix

| Feature | Chat | Text-to-Image | Speech-to-Text | Tools | Others |
|---------|------|---------------|---------------|-------|--------|
| Streaming (SSE) | Yes | No | No | No | No |
| File uploads | Yes (images, docs) | No | Yes (audio) | No | Varies |
| Tool/function calling | Yes | No | No | Yes (primary) | No |
| Guardrail set selection | Yes | No | No | No | No |
| Structured output (JSON schema) | Yes | No | No | No | No |
| Code example generation | Yes | Yes | Yes | No | All |

The **Chat Explorer** is the most feature-rich: 3-column layout (input, response, code), streaming support, vision model image upload, document upload, tool calling, guardrail selection, and structured output.

The **Tools Explorer** tests function calling tools directly: lists all registered `FunctionCall` plugins grouped by `FunctionGroup`, dynamically generates form fields from tool context definitions, and supports property constraints (allow all, only certain values, force value).

## Code Example Generation

Every explorer generates a copy-paste PHP code example showing how to call the AI provider programmatically with the same settings used in the form. The `addProviderCodeExample($provider)` method on the base class generates this snippet.

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

| Mistake | Why it's wrong |
|---------|---------------|
| Enabling `ai_api_explorer` on production | Developer tool only — it exposes every configured provider and model to anyone holding `access ai prompt` |
| Using explorer responses directly in production code | Use the generated PHP snippet as a starting point, not the rendered response |

## See Also

- [Operation Types](operation-types.md)
- [Provider System](provider-system.md)
- Reference: `web/modules/contrib/ai/modules/ai_api_explorer/`
