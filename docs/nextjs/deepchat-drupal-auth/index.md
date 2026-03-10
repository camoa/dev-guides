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

| I need to... | Guide |
|-------------|-------|
| Understand the architecture and component stack | [Architecture Overview](oauth-csrf-overview.md) |
| Trace the OAuth + CSRF authentication flow step by step | [Authentication Flow](dual-authentication-flow.md) |
| Understand how CSRF tokens are generated and why validation fails | [CSRF Token Lifecycle](csrf-token-lifecycle.md) |
| Configure deep-chat-react with interceptors and SSE streaming | [DeepChat Configuration](deepchat-configuration.md) |
| Fix CSRF token errors and session context mismatches | [Common Pitfalls](common-pitfalls.md) |
| Debug CSRF failures with curl and Drupal logs | [Debugging Checklist](debugging-checklist.md) |
| See a complete working Next.js proxy + Drupal controller example | [Reference Implementation](reference-implementation.md) |
