---
description: DeepChat + Drupal OAuth auth — architecture, CSRF lifecycle, configuration, pitfalls, and debugging
guide-meta:
  concepts:
    - DeepChat Drupal auth
    - OAuth CSRF flow
    - CSRF token lifecycle
    - DeepChat interceptors
    - SSE streaming auth
  not:
    - DeepChat setup (see nextjs/deepchat-nextjs)
    - Drupal Simple OAuth module
  requires:
    - nextjs/deepchat-nextjs
  complements:
    - drupal/security
    - nextjs/next-drupal
  specializes: ""
  category: nextjs
---

# DeepChat + Drupal OAuth Auth

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the architecture and component stack | [Architecture Overview](oauth-csrf-overview.md) | Use this guide when integrating `deep-chat-react` in a Next.js frontend against Drupal's AI chatbot module with OAuth Bearer token authentication. Use the [Authentication Flow](dual-authentication-flow.md) guide when you need to trace the… |
| Trace the OAuth + CSRF authentication flow step by step | [Authentication Flow](dual-authentication-flow.md) | Use this guide to understand why OAuth and CSRF must work together and to trace each request in the flow. Use [CSRF Token Lifecycle](csrf-token-lifecycle.md) to understand the internal token mechanics. |
| Understand how CSRF tokens are generated and why validation fails | [CSRF Token Lifecycle](csrf-token-lifecycle.md) | Use this guide to understand the internals of `CsrfTokenGenerator::get()` and `validate()`. Use [Common Pitfalls](common-pitfalls.md) for actionable fixes when validation fails. |
| Configure deep-chat-react with interceptors and SSE streaming | [DeepChat Configuration](deepchat-configuration.md) | Use this guide to configure `deep-chat-react` in Next.js with the proxy pattern. Use [Reference Implementation](reference-implementation.md) for the complete working example including the Next.js route handler. |
| Fix CSRF token errors and session context mismatches | [Common Pitfalls](common-pitfalls.md) | Use this guide when CSRF validation is failing (`csrf_token URL query argument is invalid`) or chat requests return 403. Use [Debugging Checklist](debugging-checklist.md) for systematic curl-based diagnosis. |
| Debug CSRF failures with curl and Drupal logs | [Debugging Checklist](debugging-checklist.md) | Use this guide when diagnosing `csrf_token URL query argument is invalid` or 403 errors in production. Use [Common Pitfalls](common-pitfalls.md) for known causes and fixes. |
| See a complete working Next.js proxy + Drupal controller example | [Reference Implementation](reference-implementation.md) | Use this guide as the canonical working example for DeepChat + Drupal OAuth integration. Start here when building from scratch or verifying your implementation against a known-good pattern. |
