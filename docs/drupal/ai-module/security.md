---
description: AI module security — permissions, checklist, prompt injection, XSS, CSRF, and agent security
tldr: "Use this guide before deploying any user-facing AI feature. All items in the checklist are required for production."
drupal_version: "11.x"
---

# AI Module Security

## When to Use

> Use this guide before deploying any user-facing AI feature. All items in the checklist are required for production.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| User-facing chat | Guardrails enabled | Prompt injection can bypass instructions |
| Agent with entity access | Property Restrictions | Prevents writing to unintended entity types |
| Monitoring AI usage | `ai_observability` | Audit trail without DB overhead |
| MCP tools on production | Do not use | Tool description injection risk |

## Security Checklist

- [ ] Tools check `$this->currentUser->hasPermission()` before operations
- [ ] Agent `max_loops` set conservatively (3-5)
- [ ] Tool Property Restrictions configured (entity types, bundles)
- [ ] `ai_observability` enabled for audit trail
- [ ] XSS protection: responses sanitized with `Xss::filter()`
- [ ] CSRF tokens required for DeepChat API
- [ ] Guardrails enabled for user-facing AI features
- [ ] No MCP tools on critical production sites
- [ ] Separate high-privilege agents from user-facing ones
- [ ] Prompt injection awareness: any user content is a vector

## Permissions Reference

| Permission | Module | Description |
|------------|--------|-------------|
| `access deepchat api` | ai_chatbot | REST API access |
| `administer ai_assistant` | ai_assistant_api | Manage assistants |
| `administer ai_automator` | ai_automators | Manage automators |
| `use ai ckeditor` | ai_ckeditor | CKEditor AI features |
| `access ai prompt` | ai_api_explorer | API testing UI (dev only) |
| `create ai content translation` | ai_translate | Trigger translation |
| `administer ai observability` | ai_observability | Monitoring config |

## Prompt Injection

Any user-controlled content that reaches the AI context is a potential injection vector:
- Entity titles, body text, field values, user names
- URL parameters passed as context
- Messages from other users in multi-user assistants

**Mitigation**: Use Guardrails for pre-processing; write explicit instructions in system prompts; separate high-privilege agents from user-facing ones.

## `search_api_bypass_access` Warning

Using `search_api_bypass_access` in RAG queries leaks entity access-controlled content into AI responses. Always query with proper access control unless you have confirmed all indexed content is public.

## Common Mistakes

- **Wrong**: Exposing agent tools without permission checks → **Right**: Any user who can chat with the agent inherits tool permissions
- **Wrong**: Using `search_api_bypass_access` carelessly → **Right**: Leaks access-controlled content into AI responses
- **Wrong**: Not using guardrails on user-facing features → **Right**: Prompt injection can bypass agent instructions

## See Also

- [Guardrails System](guardrails-system.md)
- [AI Agents](ai-agents.md)
- [AI Chatbot](ai-chatbot-deepchat.md)
- Reference: https://project.pages.drupalcode.org/ai/
