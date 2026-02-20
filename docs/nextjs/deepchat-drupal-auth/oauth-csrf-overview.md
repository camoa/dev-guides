---
description: Architecture overview for DeepChat + Next.js + Drupal OAuth — component stack and key file locations
drupal_version: "11.x"
---

# Architecture Overview

## When to Use

> Use this guide when integrating `deep-chat-react` in a Next.js frontend against Drupal's AI chatbot module with OAuth Bearer token authentication. Use the [Authentication Flow](dual-authentication-flow.md) guide when you need to trace the request sequence step by step.

## Decision

| Question | Answer |
|----------|--------|
| Does deep-chat call Drupal directly? | No — all requests proxy through Next.js API routes |
| Who owns CSRF token management? | Next.js proxy (fetches token per request, passes as query param) |
| Does OAuth create a PHP session automatically? | No — session must be started explicitly in `setSession()` |

## Pattern

```
Browser (deep-chat-react)
  → POST /api/deepchat (Next.js)
    → POST /api/deepchat/session (Drupal) — get CSRF token + start session
    → POST /api/deepchat?token=<csrf> (Drupal) — send chat request
```

Three-layer stack:

| Layer | Responsibility |
|-------|---------------|
| Browser | deep-chat-react component — renders chat, calls Next.js proxy |
| Next.js | Two route handlers: `/api/deepchat/session` and `/api/deepchat` |
| Drupal | `ai_chatbot` module — session controller + CSRF-protected chat endpoint |

## Common Mistakes

- **Wrong**: Pointing `deep-chat` `connect.url` directly at Drupal → **Right**: Always proxy through Next.js to centralize token management
- **Wrong**: Skipping the session endpoint and calling `/api/deepchat` directly → **Right**: Always fetch CSRF token first via session endpoint

## See Also

- [Authentication Flow](dual-authentication-flow.md)
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/ai_chatbot.routing.yml`
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/src/Controller/DeepChatApi.php`
- Reference: `/frontend/app/api/deepchat/route.ts`
