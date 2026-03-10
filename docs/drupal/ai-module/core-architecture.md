---
description: Drupal AI module architecture — ProviderProxy, core services, module hierarchy, and request lifecycle
drupal_version: "11.x"
---

# AI Module Core Architecture

## When to Use

> Use this guide to understand how the AI module works before writing any code. Use the [Provider System](provider-system.md) guide when you need to call or build a provider.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Need to call AI | Use `ai.provider` service | Gets ProviderProxy with events + guardrails |
| Need default model | `getDefaultProviderForOperationType()` | Config-driven, not hardcoded |
| Need to tag a request | Pass tags array to operation | Enables logging, guardrail filtering, cost attribution |
| Need to extend AI | Build a plugin (provider, guardrail, etc.) | Architecture is plugin-based throughout |

## Pattern

```php
// All AI calls go through ProviderProxy — never instantiate providers directly.
$providerManager = \Drupal::service('ai.provider');
$defaults = $providerManager->getDefaultProviderForOperationType('chat');
// ['provider_id' => 'anthropic', 'model_id' => 'claude-sonnet-4-20250514']

$provider = $providerManager->createInstance($defaults['provider_id']);
if (!$provider->isUsable('chat')) {
  // Provider not configured — handle gracefully.
  return;
}
$output = $provider->chat($input, $defaults['model_id'], ['my_module']);
```

## Module Hierarchy

```
ai (core)
├── ai_assistant_api    — Assistant config entities + action plugins
│   └── ai_chatbot      — DeepChat frontend + REST API
├── ai_automators       — Field-level AI automation (52 plugin types)
├── ai_ckeditor         — CKEditor 5 AI toolbar
├── ai_search           — Vector DB Search API backend
├── ai_translate        — Content translation [DEPRECATED]
├── ai_observability    — Production monitoring
├── ai_logging          — Entity-based request logging [DEPRECATED]
├── ai_api_explorer     — Developer testing UI
└── field_widget_actions — Framework for field widget action buttons
```

## Core Services

| Service ID | Purpose |
|------------|---------|
| `ai.provider` | Main entry point — create providers, get defaults |
| `ai.vdb_provider` | Vector database providers |
| `ai.form_helper` | Provider/model selection form elements |
| `ai.prompt_manager` | Manage prompt config entities |
| `ai.tokenizer` | Token counting for context management |
| `ai.text_chunker` | Split text into chunks for embeddings |
| `plugin.manager.ai.function_calls` | Discover FunctionCall plugins |
| `plugin.manager.ai_guardrail` | Discover guardrail plugins |

## ProviderProxy Request Lifecycle

All provider calls go through `ProviderProxy` (`src/Plugin/ProviderProxy.php`):

1. Normalize config, set tags, sync streaming/system-role
2. Generate UUID `$event_id` (ties pre/post events together)
3. Dispatch `PreGenerateResponseEvent` — subscribers can modify input, force early return
4. Call the real provider method
5. Catch and re-throw typed exceptions with logging
6. Dispatch `PostGenerateResponseEvent` — subscribers can modify output
7. For streamed responses, attach metadata to the iterator

## Common Mistakes

- **Wrong**: Calling providers directly without `ai.provider` → **Right**: Always use `ai.provider` service — bypassing it skips events, guardrails, and logging
- **Wrong**: Hardcoding provider/model IDs → **Right**: Use `getDefaultProviderForOperationType()` for config-driven defaults
- **Wrong**: Not passing tags → **Right**: Tags enable logging filters, guardrails, and event filtering
- **Wrong**: Not checking `isUsable()` before calling → **Right**: Provider may not be configured; always check first

## See Also

- [Provider System](provider-system.md)
- [Operation Types](operation-types.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/ai/src/Plugin/ProviderProxy.php`
