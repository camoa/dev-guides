---
description: Architecture overview for DeepChat + Next.js + Drupal OAuth — component stack and key file locations
tldr: "Use this guide when integrating `deep-chat-react` in a Next.js frontend against Drupal's AI chatbot module with OAuth Bearer token authentication. Use the [Authentication Flow](dual-authentication-flow.md) guide when you need to trace the…"
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

## Component Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                     Browser (Client-Side)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  deep-chat-react Component                                 │ │
│  │  - User messages                                           │ │
│  │  - SSE stream rendering                                    │ │
│  │  - requestInterceptor (context injection)                  │ │
│  │  - responseInterceptor (thread tracking)                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                           ↓ HTTP POST                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Next.js Server (Route Handlers)                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  /api/deepchat/session (POST)                              │ │
│  │  - Initialize Drupal session                               │ │
│  │  - Return CSRF token as plain text                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  /api/deepchat (POST)                                      │ │
│  │  - Fetch CSRF token via session endpoint                   │ │
│  │  - Proxy to Drupal /api/deepchat?token=<csrf>             │ │
│  │  - Stream SSE responses back to client                     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                  ↓ Bearer: <access_token>                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              Drupal Backend (AI Module)                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  /api/deepchat/session (POST)                              │ │
│  │  Route: ai_chatbot.session                                 │ │
│  │  Requirements: _permission: 'access deepchat api'          │ │
│  │  Controller: DeepChatApi::setSession()                     │ │
│  │  - Start PHP session if not exists                         │ │
│  │  - Generate CSRF seed in session metadata                  │ │
│  │  - Return token via CsrfTokenGenerator::get("api/deepchat")│ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  /api/deepchat?token=<csrf> (POST)                         │ │
│  │  Route: ai_chatbot.api                                     │ │
│  │  Requirements:                                              │ │
│  │    - _permission: 'access deepchat api'                    │ │
│  │    - _csrf_token: 'TRUE'                                   │ │
│  │  Access Check: CsrfAccessCheck::access()                   │ │
│  │  - Validates token against session seed                    │ │
│  │  - Computes: HMAC(seed + private_key + hash_salt)         │ │
│  │  Controller: DeepChatApi::api()                            │ │
│  │  - Process AI assistant request                            │ │
│  │  - Return JSON or StreamedResponse (SSE)                   │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Key File Locations

**Drupal Backend:**
- `/web/modules/contrib/ai/modules/ai_chatbot/ai_chatbot.routing.yml` - Route definitions with CSRF requirements
- `/web/modules/contrib/ai/modules/ai_chatbot/src/Controller/DeepChatApi.php` - API controller implementing session and chat endpoints
- `/web/modules/contrib/ai/modules/ai_chatbot/js/deepchat-init.js` - Reference implementation for Drupal's native frontend integration
- `/web/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php` - Token generation logic
- `/web/core/lib/Drupal/Core/Access/CsrfAccessCheck.php` - Token validation logic

**Next.js Frontend:**
- `/frontend/app/api/deepchat/route.ts` - Main chat proxy endpoint
- `/frontend/app/api/deepchat/session/route.ts` - Session initialization proxy
- `/frontend/src/components/chat/ChatWorkspace.tsx` - deep-chat-react wrapper component
- `/frontend/src/components/chat/hooks/useChatSession.ts` - Session management hook
- `/frontend/lib/drupal.ts` - next-drupal client configuration with OAuth

---

## Common Mistakes

- **Wrong**: Pointing `deep-chat` `connect.url` directly at Drupal → **Right**: Always proxy through Next.js to centralize token management
- **Wrong**: Skipping the session endpoint and calling `/api/deepchat` directly → **Right**: Always fetch CSRF token first via session endpoint

## See Also

- [Authentication Flow](dual-authentication-flow.md)
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/ai_chatbot.routing.yml`
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/src/Controller/DeepChatApi.php`
- Reference: `/frontend/app/api/deepchat/route.ts`
