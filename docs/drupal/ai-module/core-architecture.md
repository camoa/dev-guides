---
description: Drupal AI module architecture — ProviderProxy, core services, module hierarchy, and request lifecycle
tldr: "Use this guide to understand how the AI module works before writing any code. All AI calls route through ProviderProxy, which fires pre/post events and applies guardrails — never instantiate providers directly. Key gotcha: 1.4 adds a ChatProcessor plugin type and a GlobalGuardrailsEventSubscriber that prepends site-wide guardrail sets before any caller-attached sets."
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
├── ai_translate        — Content + interface translation [DEPRECATED]
├── ai_observability    — Production monitoring (logger + OpenTelemetry)
├── ai_logging          — Entity-based request logging [DEPRECATED]
├── ai_api_explorer     — Developer testing UI
├── ai_validations      — AI-powered field validation [DEPRECATED]
├── ai_content_suggestions — Content review panels [DEPRECATED]
├── ai_external_moderation — Migration shim [DEPRECATED]
├── ai_eca              — Migration shim [DEPRECATED]
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
| `plugin.manager.ai.chat_processor` | **Changed in 1.4:** Discover ChatProcessor plugins (new plugin type for preprocessing chat inputs) |
| `ai.exception_event_subscriber` | **Changed in 1.4:** Logs AI exceptions via `AiExceptionEvent`; enables graceful failover |

## Key Concepts

| Concept | Description |
|---------|-------------|
| **ProviderProxy** | Transparent wrapper that fires events (pre/post) and applies guardrails |
| **Guardrail** | Pre/post processing plugin (content moderation, PII filtering, etc.) |
| **Global Guardrails** | **Changed in 1.4:** Site-wide guardrail sets configured in `ai.settings` and applied to every AI request before caller-attached guardrails |
| **ChatProcessor** | **Changed in 1.4:** New plugin type (`#[ChatProcessor]`) for preprocessing chat inputs before they reach the provider |

## ProviderProxy Request Lifecycle

All provider calls go through `ProviderProxy` (`src/Plugin/ProviderProxy.php`):

1. Normalize config, set tags, sync streaming/system-role
2. Generate UUID `$event_id` (ties pre/post events together)
3. Dispatch `PreGenerateResponseEvent` — subscribers can modify input, force early return
4. Call the real provider method
5. Catch and re-throw typed exceptions with logging. **Changed in 1.4:** Also dispatches `AiExceptionEvent` before re-throwing — allows subscribers to inject a recovery output via `setForcedOutputObject()`
6. Dispatch `PostGenerateResponseEvent` — subscribers can modify output
7. For streamed responses, attach metadata to the iterator

**Drupal core requirement:** `^10.5 || ^11.2` (raised from `^10.3 || ^11` in earlier releases).

## Common Mistakes

- **Wrong**: Calling providers directly without `ai.provider` → **Right**: Always use `ai.provider` service — bypassing it skips events, guardrails, and logging
- **Wrong**: Hardcoding provider/model IDs → **Right**: Use `getDefaultProviderForOperationType()` for config-driven defaults
- **Wrong**: Not passing tags → **Right**: Tags enable logging filters, guardrails, and event filtering
- **Wrong**: Not checking `isUsable()` before calling → **Right**: Provider may not be configured; always check first

## See Also

- [Provider System](provider-system.md)
- [Operation Types](operation-types.md)
- [Events System](events-system.md)
- [Guardrails System](guardrails-system.md)
- Reference: `web/modules/contrib/ai/src/Plugin/ProviderProxy.php`
