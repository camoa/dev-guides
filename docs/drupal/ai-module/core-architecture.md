---
description: Drupal AI module architecture — ProviderProxy, core services, ai_file entity, and request lifecycle
tldr: "Route all AI calls through ai.provider (ProviderProxy) — never bypass it. 1.4 adds ChatProcessor and site-wide global guardrails. 1.4.2 adds ai.file_manager service for provider-side file uploads and the ai_file content entity."
drupal_version: "11.x"
---

# AI Module Core Architecture

## When to Use

> Use this guide to understand how the AI module works before writing any code. Use the [Provider System](provider-system.md) guide when you need to call or build a provider.

The Drupal AI module provides a **provider-agnostic abstraction layer** for AI operations. Any module can call AI operations without coupling to a specific provider (Anthropic, OpenAI, Google, etc.).

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

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Provider** | Plugin wrapping an AI service (Anthropic, OpenAI, Ollama, etc.) |
| **Operation Type** | A category of AI work (chat, embeddings, text-to-image, etc.) |
| **ProviderProxy** | Transparent wrapper that fires events (pre/post) and applies guardrails |
| **Guardrail** | Pre/post processing plugin (content moderation, PII filtering, etc.) |
| **Global Guardrails** | **Changed in 1.4:** Site-wide guardrail sets configured in `ai.settings` and applied to every AI request before caller-attached guardrails |
| **Function Calling** | Tools that agents can invoke during reasoning loops |
| **ChatProcessor** | **Changed in 1.4:** New plugin type (`#[ChatProcessor]`) for preprocessing chat inputs before they reach the provider |
| **Short-Term Memory** | Plugin for managing conversation context within a session |

## Module Hierarchy

```
ai (core)
├── ai_assistant_api    — Assistant config entities + action plugins
│   └── ai_chatbot      — DeepChat frontend + REST API
├── ai_automators       — Field-level AI automation (52 plugin types)
├── ai_ckeditor         — CKEditor 5 AI toolbar
├── ai_search           — Vector DB Search API backend
├── ai_translate        — Content + interface translation [DEPRECATED → standalone drupal/ai_translate]
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

| Service ID | Class | Purpose |
|------------|-------|---------|
| `ai.provider` | `AiProviderPluginManager` | Main entry point — create providers, get defaults |
| `ai.vdb_provider` | `AiVdbProviderPluginManager` | Vector database providers |
| `ai.form_helper` | `AiProviderFormHelper` | Provider/model selection form elements |
| `ai.prompt_json_decode` | `PromptJsonDecoder` | Parse JSON from LLM responses |
| `ai.prompt_code_block_extractor` | `PromptCodeBlockExtractor` | Extract code blocks from LLM responses |
| `ai.prompt_manager` | `AiPromptManager` | Manage prompt config entities |
| `ai.prompt_subform` | `AiPromptSubform` | Embed prompt selection in other forms |
| `ai.tokenizer` | `Tokenizer` | Token counting for context management |
| `ai.text_chunker` | `TextChunker` | Split text into chunks for embeddings |
| `ai.context_definition_normalizer` | `ContextDefinitionNormalizer` | Normalize context definitions for function calls |
| `ai.hostname_filter_service` | `HostnameFilter` | Restrict outbound AI calls to allowed hosts |
| `plugin.manager.ai.function_calls` | `FunctionCallPluginManager` | Discover FunctionCall plugins |
| `plugin.manager.ai.function_groups` | `FunctionGroupPluginManager` | Discover FunctionGroup plugins |
| `plugin.manager.ai_guardrail` | `AiGuardrailPluginManager` | Discover guardrail plugins |
| `plugin.manager.ai.short_term_memory` | `AiShortTermMemoryPluginManager` | Short-term memory plugins |
| `plugin.manager.ai_data_type_converter` | `AiDataTypeConverterPluginManager` | Data type conversion plugins |
| `ai.function_call_form_helper` | `PropertyFormBuilder` | Build forms for function call properties |
| `ai.tools_library.ui_builder` | `AiToolsLibraryUiBuilder` | Tools library UI rendering |
| `plugin.manager.ai.chat_processor` | `ChatProcessorPluginManager` | **Changed in 1.4:** Discover ChatProcessor plugins (new plugin type for preprocessing chat inputs) |
| `ai.exception_event_subscriber` | `AiExceptionEventSubscriber` | **Changed in 1.4:** Logs AI exceptions via `AiExceptionEvent`; enables graceful failover |
| `ai.file_manager` | `AiFileManager` | **New in 1.4.2:** Manages the AI File lifecycle — uploads local files to a provider's Files API, tracks them as `ai_file` entities, deletes and loads them by purpose |

## Content Entities

**New in 1.4.2:** The module defines the `ai_file` content entity (`Drupal\ai\Entity\AiFile`), a reference to a file uploaded to a provider's Files API (provider id, remote id, filename, MIME type, size, purpose, JSON metadata, optional local `file` reference, owner). It is managed through the `ai.file_manager` service and administered at `/admin/config/ai/files` (permission: `administer ai`). See [Operation Types — Chat with PDF / Provider Files](operation-types.md) and [Provider System](provider-system.md).

## Dependencies

```
drupal/key: ^1.18          — API key storage
league/html-to-markdown: ^5.1  — HTML-to-Markdown conversion
yethee/tiktoken: ^0.5.1    — Token counting
openai-php/client: >=v0.10.1  — OpenAI API client (used by multiple providers)
```

**Drupal core requirement:** `^11.2`.

## ProviderProxy (Request Lifecycle)

All provider calls go through `ProviderProxy` (`src/Plugin/ProviderProxy.php`), which wraps the real provider plugin via `__call()` magic method. Only "trigger methods" (methods whose name matches an `OperationTypeInterface` implementation) are proxied; other methods pass through directly.

**Proxied call flow:**

1. Normalize configuration, set tags, sync streaming/system-role between input and provider
2. Generate a UUID `$event_id` (ties pre/post events together)
3. Dispatch `PreGenerateResponseEvent` — subscribers can:
   - Modify input, configuration, tags, or authentication (`setAuthentication()`)
   - Force an early return via `setForcedOutputObject()` (e.g., cached response)
   - Set metadata that carries through to the post event
4. Call the real provider method
5. Catch and re-throw typed exceptions (`AiRateLimitException`, `AiQuotaException`, etc.) with logging. **Changed in 1.4:** The proxy also dispatches `AiExceptionEvent` before re-throwing, allowing subscribers to rewrite the error message or inject a forced recovery output via `setForcedOutputObject()`
6. Dispatch `PostGenerateResponseEvent` — subscribers can modify the output
7. For streamed responses, attach metadata (input, provider, model, tags, thread ID) to the iterator

**Key non-proxied special cases:**

| Method | Behavior |
|--------|----------|
| `getConfiguredModels()` | Merges extra models from provider config |
| `getApiDefinition()` | Cached permanently in `ai` cache bin |

```php
// ProviderProxy exposes magic property access (__get/__set) and delegates
// to the wrapped plugin, so callers use it as if it were the provider itself.
$proxy = \Drupal::service('ai.provider')->createInstance('anthropic');
$proxy->setChatSystemRole('You are helpful.');
$output = $proxy->chat($input, $model, ['my_tag']);
// ^ this triggers the full proxy lifecycle
```

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Calling providers directly without `ai.provider` | Bypasses ProviderProxy — no events, no guardrails, no logging |
| Hardcoding provider/model IDs | Use `getDefaultProviderForOperationType()` for config-driven defaults |
| Ignoring tags parameter | Tags enable filtering in logging, guardrails, and event subscribers |
| Not checking `isUsable()` before calling | Provider may not be configured; always check availability |

## See Also

- [Provider System](provider-system.md)
- [Operation Types](operation-types.md)
- [Events System](events-system.md)
- [Guardrails System](guardrails-system.md)
- Reference: `web/modules/contrib/ai/src/Plugin/ProviderProxy.php`
