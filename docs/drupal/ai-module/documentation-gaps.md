---
description: Documentation gaps in Drupal AI 1.4.2 — undocumented features identified by comparing official docs to source code
tldr: "Undocumented features verified against 1.4.2 source. 1.4 gaps: ChatProcessor, global guardrails, AiExceptionEvent. 1.4.2 gaps: ai_file, ai.file_manager, AiFileProviderInterface, ChatWithPdf, restrict_to_topic, StreamableGuardrailInterface."
drupal_version: "11.x"
---

# Documentation Gaps

## When to Use

> Use this guide when the official documentation doesn't match actual behavior. These gaps were identified by comparing official docs to source code through 1.4.2. New in 1.4.0-rc1 and not yet in official docs: ChatProcessor plugin system, global guardrails, and `AiExceptionEvent`. New in 1.4.2: `ai_file` entity, `ai.file_manager`, `AiFileProviderInterface`, `ChatWithPdf` capability, `restrict_to_topic` guardrail, and `StreamableGuardrailInterface`.

## Core Module

| Gap | Covered In |
|-----|------------|
| ProviderProxy wrapping pattern | [Core Architecture](core-architecture.md) |
| Guardrails system developer guide | [Guardrails System](guardrails-system.md) |
| Short-term memory plugin system | [Short-Term Memory](short-term-memory.md) |
| `AiDataTypeConverter` plugin system | — (undocumented) |
| Prompt config entity system (`ai.ai_prompt`) | [Prompt System](prompt-system.md) |
| `ai.text_chunker` service | — (undocumented) |
| ChatProcessor plugin type (1.4) | [Core Architecture](core-architecture.md) |
| `AiExceptionEvent` (1.4) | [Events System](events-system.md) |
| Global guardrails in `ai.settings` (1.4) | [Guardrails System](guardrails-system.md) |
| `ai_file` content entity (1.4.2) | [Core Architecture](core-architecture.md) |
| `ai.file_manager` service (1.4.2) | [Core Architecture](core-architecture.md), [Operation Types](operation-types.md) |
| `AiFileProviderInterface` (1.4.2) | [Provider System](provider-system.md) |
| `ChatWithPdf` capability (1.4.2) | [Enums & DTOs](enums-and-dtos.md), [Operation Types](operation-types.md) |
| `StreamableGuardrailInterface` (1.4.2) | [Guardrails System](guardrails-system.md) |
| `restrict_to_topic` guardrail (1.4.2) | [Guardrails System](guardrails-system.md) |

## ai_assistant_api

| Gap | Covered In |
|-----|------------|
| `use_function_calling` mode (tool calls vs JSON-in-prompt) | [AI Assistant API](ai-assistant-api.md) |
| `AgentRunner` path (assistant delegates to ai_agents) | [AI Agents](ai-agents.md) |
| `setVerboseMode()`, `setThrowException()` | [AI Assistant API](ai-assistant-api.md) |
| `AiAssistantPassContextToAgentEvent` | [AI Assistant API](ai-assistant-api.md) |

## ai_chatbot

| Gap | Covered In |
|-----|------------|
| Full POST payload schema for `/api/deepchat` | [AI Chatbot](ai-chatbot-deepchat.md) |
| `should_continue` protocol for tool-call round-trips | [AI Chatbot](ai-chatbot-deepchat.md) |
| `verbose_mode`, `show_copy_icon`, `show_structured_results` block settings | [AI Chatbot](ai-chatbot-deepchat.md) |
| `hook_deepchat_prepend_message` | [AI Chatbot](ai-chatbot-deepchat.md) |

## ai_automators

| Gap | Covered In |
|-----|------------|
| `AutomatorsTool` entity and function-calling integration | [AI Automators](ai-automators.md) |
| All 4 events (`AutomatorConfigEvent`, etc.) | [AI Automators](ai-automators.md) |
| Full 52-plugin inventory | [AI Automators](ai-automators.md) |
| `$settings['ai_automator_advanced_mode_enabled']` | [AI Automators](ai-automators.md) |

## ai_ckeditor

| Gap | Covered In |
|-----|------------|
| `module_dependencies` silencing mechanism | [AI CKEditor](ai-ckeditor.md) |
| `AiAutomatorsCKEditor` cross-module plugin | [AI CKEditor](ai-ckeditor.md) |
| Global `ai_ckeditor.settings` prompts config | [AI CKEditor](ai-ckeditor.md) |

## ai_search

| Gap | Covered In |
|-----|------------|
| `include_raw_embedding_vector` feature | [AI Search](ai-search-vector-rag.md) |
| `search_api_ai_get_chunks_result` query option | [AI Search](ai-search-vector-rag.md) |
| `AiVdbProviderSearchApiInterface` requirements | [AI Search](ai-search-vector-rag.md) |

## ai_translate

| Gap | Covered In |
|-----|------------|
| Drush commands (`ai:translate-entity`, `ai:translate-text`) | [AI Translate](ai-translate.md) |
| `hook_ai_translate_translation_alter` | [AI Translate](ai-translate.md) |
| Layout Builder translation integration | [AI Translate](ai-translate.md) |
| `ChatTranslationProvider` plugin | [AI Translate](ai-translate.md) |

## ai_observability

| Gap | Covered In |
|-----|------------|
| All config settings | [AI Observability](ai-observability.md) |
| `AiObservabilityUtils` | [AI Observability](ai-observability.md) |
| OpenTelemetry spans and metrics | [AI Observability](ai-observability.md) |
| `fallback_log_message_mode` config option | [AI Observability](ai-observability.md) |

## ai_validations

| Gap | Covered In |
|-----|------------|
| XTRUE/XFALSE protocol (critical) | [AI Validations](ai-validations.md) |
| Image classification is deny-list (not allow-list) | [AI Validations](ai-validations.md) |

## field_widget_actions

| Gap | Covered In |
|-----|------------|
| `FieldWidgetFormActionBase` modal pattern | [Field Widget Actions](field-widget-actions.md) |
| `FillEditorCommand`/`FillSimpleFieldCommand` | [Field Widget Actions](field-widget-actions.md) |
| Config Action for Recipes pattern | [Field Widget Actions](field-widget-actions.md) |

## ai_eca

| Gap | Note |
|-----|------|
| Docs describe a working module | Actual code is a deprecated migration stub |

## ai_logging

| Gap | Note |
|-----|------|
| `prompt_logging_excluded_tags` undocumented | Covered in [AI Logging](ai-logging.md) |
| Deprecation notice missing from docs | Module is deprecated; use `ai_observability` |

## See Also

- Reference: https://project.pages.drupalcode.org/ai/1.3.x/
- Reference: https://git.drupalcode.org/project/ai
