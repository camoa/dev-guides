---
description: Drupal AI module — provider abstraction, AI operations, agents, automators, chatbot API, CKEditor, vector search/RAG, guardrails, and all 14 sub-modules (1.4.7 stable)
tracks:
  - project: ai
    channel: stable
    declared: "1.4.7"
    verified: 2026-08-20
guide-meta:
  concepts:
    - Drupal AI module
    - AI providers
    - AI operations
    - AI agents
    - AI automators
    - DeepChat
    - AI chatbot
    - vector search
    - RAG
    - AI CKEditor
    - guardrails
    - function calling
    - ai_assistant_api
    - ai_automators
    - ai_search
    - ai_chatbot
    - ProviderProxy
    - AiProviderInterface
    - embeddings
    - short-term memory
    - prompt system
    - AI observability
    - ai_file
    - AiFileManager
    - ChatWithPdf
    - AiFileProviderInterface
    - StreamableGuardrailInterface
  not:
    - Claude API
    - OpenAI API
    - Anthropic SDK
    - AI module 2.x
    - machine learning training
    - ChatGPT plugin
  requires: []
  complements:
    - drupal/services
    - drupal/forms
    - drupal/entities
    - drupal/caching
  category: drupal
---

# Drupal AI Module

Provider-agnostic AI abstraction for Drupal 11. Covers provider setup, all 16 operation types, agents, automators, the DeepChat chatbot, CKEditor integration, vector search/RAG, guardrails, and the complete sub-module ecosystem. Based on AI module 1.4.7 stable with "New in 1.4" / "Changed in 1.4" callouts.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the AI module architecture and request lifecycle | [Core Architecture](core-architecture.md) | Route all AI calls through ai.provider (ProviderProxy) — never bypass it. 1.4 adds ChatProcessor and site-wide global guardrails. 1.4.2 adds ai.file_manager service for provider-side file uploads and the ai_file content entity. |
| Work with AI providers (Anthropic, OpenAI, Ollama, etc.) | [Provider System](provider-system.md) | Extend OpenAiBasedProviderClientBase for OpenAI-compatible APIs; always check isUsable() before calling. 1.4.2 adds AiFileProviderInterface for provider-side file uploads; use ai.file_manager service, not direct provider methods. |
| Call an AI operation (chat, embeddings, TTS, etc.) | [Operation Types](operation-types.md) | 16 operation types, each with typed Input/Output classes. Vision, audio, tools, and PDF are capabilities within chat — not separate types. 1.4.2 adds ChatWithPdf capability and ai.file_manager for provider-side document uploads. |
| Build a REST chat API or embed a chatbot | [AI Chatbot (DeepChat)](ai-chatbot-deepchat.md) | Integrate DeepChat as a Drupal block or call its REST API from decoupled frontends; always fetch CSRF token first. New in 1.4: ChatProcessorInterface is the stable contract for any chat UI; extend ChatProcessorBase. |
| Create AI assistants with action plugins | [AI Assistant API](ai-assistant-api.md) | Use this guide when creating AI assistants, writing custom action plugins, or calling the runner programmatically. Use [AI Chatbot](ai-chatbot-deepchat.md) for the frontend chatbot configuration. |
| Build autonomous AI agents | [AI Agents](ai-agents.md) | Use this guide when building autonomous AI agents that make decisions. Use [AI Automators](ai-automators.md) for fixed field-population workflows that don't need autonomous decision-making. |
| Create custom tools/functions for agents | [Function Calling](function-calling.md) | Use this guide when building custom tools that agents or assistants can invoke. Implement OverridableFunctionCallInterface (added 1.3.3) to allow per-instance parameter overrides. Use [AI Agents](ai-agents.md) for configuring which tools an agent uses. |
| Auto-generate field content on entity save | [AI Automators](ai-automators.md) | Use this guide when auto-generating field content on entity save. 1.4 adds guardrail_set_id per automator, RunAutomatorAction for VBO backfilling without re-saving, and a drush generator for custom automator types. |
| Add AI features to CKEditor 5 | [AI CKEditor](ai-ckeditor.md) | Use this guide when adding AI text-generation capabilities to CKEditor 5. Use [AI Automators](ai-automators.md) for field-level automation outside the editor. |
| Set up vector search / RAG | [AI Search (Vector/RAG)](ai-search-vector-rag.md) | Use this guide when setting up semantic search or Retrieval-Augmented Generation (RAG) with vector databases. Use [AI Assistant API](ai-assistant-api.md) to wire the `rag_action` into an assistant. |
| Translate content with AI | [AI Translate](ai-translate.md) | **Status: STANDALONE** — `drupal/ai_translate` 1.3.1 (split from AI Core per #3570275). Requires `drupal/ai >1.2.1` + content_translation; Drupal ^10.4 \|\| ^11. Use for one-click AI content/interface translation with per-site and per-language prompt customization. |
| Add AI validation to fields | [AI Validations](ai-validations.md) | **Status: DEPRECATED** — moving to standalone `drupal/ai_validations` (1.0.0-alpha1, pre-stable as of Jun 2026; keep using in-core until stable). Use when you need AI-powered field validation constraints with the Field Validation module (>=3.0.0-beta3). |
| Add action buttons to field widgets | [Field Widget Actions](field-widget-actions.md) | Use this guide when adding action buttons to field widgets on entity edit forms. The `field_widget_actions` module is AI-agnostic — it provides the framework; other modules provide the actual AI plugins. |
| Monitor AI usage and costs in production | [AI Observability](ai-observability.md) | Use `ai_observability` for production monitoring and audit trails. Use [AI Logging](ai-logging.md) only for local development debugging (it is deprecated). |
| Log AI requests for local debugging | [AI Logging](ai-logging.md) | **Status: DEPRECATED** — use [AI Observability](ai-observability.md) for production monitoring. `ai_logging` is development/debugging only and stores AI requests as `ai_log` entities in the database. |
| Test AI operations interactively | [AI API Explorer](ai-api-explorer.md) | Use `ai_api_explorer` for interactive testing of AI operations during development. **Do not enable on production.** Use [Operation Types](operation-types.md) for the actual PHP API. |
| Add guardrails (pre/post processing) | [Guardrails System](guardrails-system.md) | Pre/post process AI requests: block unsafe input, filter PII, or inject context. Required for user-facing features. 1.4 adds multiple guardrail sets per input, global site-wide enforcement, and StreamableGuardrailInterface for mid-stream redaction. |
| Use short-term memory plugins | [Short-Term Memory](short-term-memory.md) | Use short-term memory plugins when you need to manage conversation context within a session beyond the default history mechanism in `ai_assistant_api`. For most cases, set `allow_history` on the `ai_assistant` config entity instead. |
| Work with prompts and prompt types | [Prompt System](prompt-system.md) | Use the prompt system when you need reusable, deployable prompts with variable substitution. For one-off prompts in code, string interpolation is simpler. |
| Subscribe to AI events | [Events System](events-system.md) | Use events when you need to intercept AI requests or responses across all operations without modifying providers. Changed in 1.4: AiExceptionEvent fires when a provider throws — subscribers can rewrite the error or inject a recovery output to prevent re-throwing. |
| Handle AI-specific exceptions | [Exceptions](exceptions.md) | Use this guide when handling errors from AI provider calls. Always catch specific exceptions before the generic AiExceptionInterface. Changed in 1.4: ProviderProxy also dispatches AiExceptionEvent before re-throwing — subscribe to inject fallback output instead of surfacing errors to users. |
| Work with enums, DTOs, structured output | [Enums & DTOs](enums-and-dtos.md) | Filter models by AiModelCapability, enforce structured output via StructuredOutputSchema, or track token costs via TokenUsageDto. New in 1.4: ChatWithPdf capability. Deprecated: setChatStrictSchema() — set strict: TRUE on StructuredOutputSchema. |
| Follow security best practices | [Security](security.md) | Use this guide before deploying any user-facing AI feature. All items in the checklist are required for production. |
| Plan migrations from deprecated modules | [Deprecated Modules](deprecated-modules.md) | Use this guide when planning migrations away from deprecated sub-modules. As of AI Core 1.4.7 all deprecations remain in place — removal is planned for AI 2.0.0, which is not yet released. |
| Identify gaps in official documentation | [Documentation Gaps](documentation-gaps.md) | Undocumented features verified against 1.4.2 source. 1.4 gaps: ChatProcessor, global guardrails, AiExceptionEvent. 1.4.2 gaps: ai_file, ai.file_manager, AiFileProviderInterface, ChatWithPdf, restrict_to_topic, StreamableGuardrailInterface. |
