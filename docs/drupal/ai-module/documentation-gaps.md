---
description: Documentation gaps in Drupal AI 1.4.2 — undocumented features identified by comparing official docs to source code
tldr: "Undocumented features verified against 1.4.2 source. 1.4 gaps: ChatProcessor, global guardrails, AiExceptionEvent. 1.4.2 gaps: ai_file, ai.file_manager, AiFileProviderInterface, ChatWithPdf, restrict_to_topic, StreamableGuardrailInterface."
drupal_version: "11.x"
---

# Documentation Gaps

## When to Use

> Use this guide when the official documentation doesn't match actual behavior.

Gaps identified by comparing official docs to actual code through 1.4.2. New in 1.4.0-rc1: ChatProcessor plugin system, global guardrails, and `AiExceptionEvent` are not yet in official docs. New in 1.4.2: `ai_file` entity, `ai.file_manager` service, `AiFileProviderInterface`, `ChatWithPdf` capability, `restrict_to_topic` guardrail, and `StreamableGuardrailInterface` are not yet in official docs.

Each gap below names where this guide set covers it, or marks it as still undocumented anywhere.

## Core Module

- ProviderProxy wrapping pattern undocumented — covered in [Core Architecture](core-architecture.md)
- Guardrails system has no developer guide — covered in [Guardrails System](guardrails-system.md)
- Short-term memory plugin system undocumented — covered in [Short-Term Memory](short-term-memory.md)
- `AiDataTypeConverter` plugin system undocumented — still undocumented
- Prompt config entity system (`ai.ai_prompt`) minimally documented — covered in [Prompt System](prompt-system.md)
- `ai.text_chunker` service not in developer guide — still undocumented
- ChatProcessor plugin type (1.4) — covered in [Core Architecture](core-architecture.md) and [AI Chatbot](ai-chatbot-deepchat.md)
- `AiExceptionEvent` (1.4) — covered in [Events System](events-system.md)
- Global guardrails in `ai.settings` (1.4) — covered in [Guardrails System](guardrails-system.md)
- `ai_file` content entity, `ai.file_manager` service (1.4.2) — covered in [Core Architecture](core-architecture.md) and [Operation Types](operation-types.md)
- `AiFileProviderInterface` (1.4.2) — covered in [Provider System](provider-system.md)
- `ChatWithPdf` capability (1.4.2) — covered in [Enums & DTOs](enums-and-dtos.md)
- `StreamableGuardrailInterface` and `restrict_to_topic` guardrail (1.4.2) — covered in [Guardrails System](guardrails-system.md)

## ai_assistant_api

- `use_function_calling` mode (tool calls vs JSON-in-prompt) not documented — covered in [AI Assistant API](ai-assistant-api.md)
- `AgentRunner` path (assistant delegates to ai_agents) not documented — covered in [AI Assistant API](ai-assistant-api.md) and [AI Agents](ai-agents.md)
- `setVerboseMode()`, `setThrowException()` undocumented — covered in [AI Assistant API](ai-assistant-api.md)
- Specific error message overrides on entity undocumented — covered in [AI Assistant API](ai-assistant-api.md)
- `AiAssistantPassContextToAgentEvent` not in docs — covered in [AI Assistant API](ai-assistant-api.md)

## ai_chatbot

- Full POST payload schema for `/api/deepchat` not documented — covered in [AI Chatbot](ai-chatbot-deepchat.md)
- `should_continue` protocol for tool-call round-trips not documented — covered in [AI Chatbot](ai-chatbot-deepchat.md)
- `verbose_mode`, `show_copy_icon`, `show_structured_results` block settings undocumented — covered in [AI Chatbot](ai-chatbot-deepchat.md)
- CSRF token acquisition flow incomplete in docs — covered in [AI Chatbot](ai-chatbot-deepchat.md)
- `hook_deepchat_prepend_message` not documented — covered in [AI Chatbot](ai-chatbot-deepchat.md)

## ai_automators

- `AutomatorsTool` entity and function-calling integration undocumented — covered in [AI Automators](ai-automators.md)
- All 4 events (`AutomatorConfigEvent`, `ProcessFieldEvent`, `ValuesChangeEvent`, `RuleIsAllowedEvent`) undocumented — covered in [AI Automators](ai-automators.md)
- `ViewsExtractor` plugin undocumented — listed in [AI Automators](ai-automators.md)
- Full 52-plugin inventory not listed — covered in [AI Automators](ai-automators.md)
- `$settings['ai_automator_advanced_mode_enabled']` undocumented — covered in [AI Automators](ai-automators.md)

## ai_ckeditor

- `module_dependencies` silencing mechanism undocumented — covered in [AI CKEditor](ai-ckeditor.md)
- `ReformatHtml`, `ModifyPrompt`, `Help` plugins undocumented — listed in [AI CKEditor](ai-ckeditor.md)
- `AiAutomatorsCKEditor` cross-module plugin undocumented — covered in [AI CKEditor](ai-ckeditor.md)
- Global `ai_ckeditor.settings` prompts config undocumented — covered in [AI CKEditor](ai-ckeditor.md)

## ai_search

- `include_raw_embedding_vector` feature undocumented — covered in [AI Search](ai-search-vector-rag.md)
- `AiVdbProviderSearchApiInterface` requirements undocumented — covered in [AI Search](ai-search-vector-rag.md)
- `search_api_ai_get_chunks_result` query option undocumented — covered in [AI Search](ai-search-vector-rag.md)
- Chunk preview tool in Fields form undocumented — still undocumented

## ai_translate

- Drush commands (`ai:translate-entity`, `ai:translate-text`) undocumented — covered in [AI Translate](ai-translate.md)
- `hook_ai_translate_translation_alter` undocumented — covered in [AI Translate](ai-translate.md)
- `ChatTranslationProvider` plugin undocumented — covered in [AI Translate](ai-translate.md)
- Layout Builder translation integration undocumented — covered in [AI Translate](ai-translate.md)
- Programmatic API not documented — covered in [AI Translate](ai-translate.md)

## ai_observability

- All config settings undocumented (docs is 5 sentences) — covered in [AI Observability](ai-observability.md)
- OpenTelemetry spans and metrics undocumented — covered in [AI Observability](ai-observability.md)
- `AiObservabilityUtils` undocumented — covered in [AI Observability](ai-observability.md)
- Token usage tracking capabilities undocumented — covered in [AI Observability](ai-observability.md)

## ai_validations

- XTRUE/XFALSE protocol is the critical missing piece — covered in [AI Validations](ai-validations.md)
- Image classification is deny-list (not allow-list) — not clarified — covered in [AI Validations](ai-validations.md)
- FieldValidation module version requirement not prominent — covered in [AI Validations](ai-validations.md)

## field_widget_actions

- `FieldWidgetFormActionBase` modal pattern undocumented — covered in [Field Widget Actions](field-widget-actions.md)
- `FillEditorCommand`/`FillSimpleFieldCommand` Ajax commands undocumented — covered in [Field Widget Actions](field-widget-actions.md)
- `FORM_ELEMENT_PROPERTY` constant requirement undocumented — covered in [Field Widget Actions](field-widget-actions.md)
- Config Action for Recipes (`SetupFieldWidgetAction`) undocumented — covered in [Field Widget Actions](field-widget-actions.md)

## ai_eca

- Docs describe a working module; actual code is a deprecated migration stub — see [Deprecated Modules](deprecated-modules.md)

## ai_logging

- `prompt_logging_excluded_tags` undocumented — covered in [AI Logging](ai-logging.md)
- Deprecation notice missing from docs — the module is deprecated; use [AI Observability](ai-observability.md)

## See Also

- Reference: https://project.pages.drupalcode.org/ai/1.3.x/
- Reference: https://git.drupalcode.org/project/ai
