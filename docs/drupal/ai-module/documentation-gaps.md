---
description: Documentation gaps in Drupal AI 1.3.0-rc2 — undocumented features identified by comparing official docs to source code
drupal_version: "11.x"
---

# Documentation Gaps

## When to Use

> Use this guide when the official documentation doesn't match actual behavior. These gaps were identified by comparing official docs to source code in AI 1.3.0-rc2.

## Core Module

| Gap | Covered In |
|-----|------------|
| ProviderProxy wrapping pattern | [Core Architecture](core-architecture.md) |
| Guardrails system developer guide | [Guardrails System](guardrails-system.md) |
| Short-term memory plugin system | [Short-Term Memory](short-term-memory.md) |
| Prompt config entity system (`ai.ai_prompt`) | [Prompt System](prompt-system.md) |

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

## ai_observability

| Gap | Covered In |
|-----|------------|
| All config settings | [AI Observability](ai-observability.md) |
| `AiObservabilityUtils` | [AI Observability](ai-observability.md) |

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

## See Also

- Reference: https://project.pages.drupalcode.org/ai/
- Reference: https://git.drupalcode.org/project/ai
