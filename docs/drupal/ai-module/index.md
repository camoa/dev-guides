---
description: Drupal AI module — provider abstraction, AI operations, agents, automators, chatbot API, CKEditor, vector search/RAG, guardrails, and all 14 sub-modules
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
  specializes: ""
  category: drupal
---

# Drupal AI Module

Provider-agnostic AI abstraction for Drupal 11. Covers provider setup, all 15 operation types, agents, automators, the DeepChat chatbot, CKEditor integration, vector search/RAG, guardrails, and the complete sub-module ecosystem.

| I need to... | Guide |
|-------------|-------|
| Understand the AI module architecture and request lifecycle | [Core Architecture](core-architecture.md) |
| Work with AI providers (Anthropic, OpenAI, Ollama, etc.) | [Provider System](provider-system.md) |
| Call an AI operation (chat, embeddings, TTS, etc.) | [Operation Types](operation-types.md) |
| Build a REST chat API or embed a chatbot | [AI Chatbot (DeepChat)](ai-chatbot-deepchat.md) |
| Create AI assistants with action plugins | [AI Assistant API](ai-assistant-api.md) |
| Build autonomous AI agents | [AI Agents](ai-agents.md) |
| Create custom tools/functions for agents | [Function Calling](function-calling.md) |
| Auto-generate field content on entity save | [AI Automators](ai-automators.md) |
| Add AI features to CKEditor 5 | [AI CKEditor](ai-ckeditor.md) |
| Set up vector search / RAG | [AI Search (Vector/RAG)](ai-search-vector-rag.md) |
| Translate content with AI | [AI Translate](ai-translate.md) |
| Add AI validation to fields | [AI Validations](ai-validations.md) |
| Add action buttons to field widgets | [Field Widget Actions](field-widget-actions.md) |
| Monitor AI usage and costs in production | [AI Observability](ai-observability.md) |
| Log AI requests for local debugging | [AI Logging](ai-logging.md) |
| Test AI operations interactively | [AI API Explorer](ai-api-explorer.md) |
| Add guardrails (pre/post processing) | [Guardrails System](guardrails-system.md) |
| Use short-term memory plugins | [Short-Term Memory](short-term-memory.md) |
| Work with prompts and prompt types | [Prompt System](prompt-system.md) |
| Subscribe to AI events | [Events System](events-system.md) |
| Handle AI-specific exceptions | [Exceptions](exceptions.md) |
| Work with enums, DTOs, structured output | [Enums & DTOs](enums-and-dtos.md) |
| Follow security best practices | [Security](security.md) |
| Plan migrations from deprecated modules | [Deprecated Modules](deprecated-modules.md) |
| Identify gaps in official documentation | [Documentation Gaps](documentation-gaps.md) |
