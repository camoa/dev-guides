---
description: Step-by-step OAuth + CSRF authentication flow for DeepChat + Drupal — dual-auth challenge and sequence
drupal_version: "11.x"
---

# Authentication Flow

## When to Use

> Use this guide to understand why OAuth and CSRF must work together and to trace each request in the flow. Use [CSRF Token Lifecycle](csrf-token-lifecycle.md) to understand the internal token mechanics.

## Decision

| Auth Mechanism | Purpose | Creates PHP Session? |
|---------------|---------|---------------------|
| OAuth Bearer token | Identifies user, grants `access deepchat api` permission | No — stateless by design |
| Session-based CSRF | Validates token matches seed stored in session | Requires explicit `$session->start()` |

**Key rule**: OAuth alone is not enough. You must explicitly start a PHP session before generating the CSRF token, then maintain that session through the API call.

## Pattern

17-step sequence (abbreviated):

```
1. Browser loads chat
2. Next.js calls auth() → gets access_token
3. Next.js: POST /api/deepchat/session (Bearer: access_token)
4. Drupal validates Bearer token
5. Drupal: $session->start()        ← creates PHP session
6. Drupal: generates random seed, stores in session
7. Drupal: computes CSRF token (HMAC of seed + key + salt)
8. Drupal returns token (plain text)
9. Next.js stores token, marks session ready
10. Browser: user sends message
11. Browser → Next.js: POST /api/deepchat
12. Next.js → Drupal: POST /api/deepchat?token=<csrf> (Bearer: same access_token)
13. Drupal validates Bearer token (permission check)
14. Drupal CsrfAccessCheck: get seed from session, compute expected token, hash_equals()
15. If valid: process AI request
16. Stream SSE response back through Next.js
17. Browser renders AI response
```

**Three timing requirements:**
1. PHP session from step 5 must persist through step 14
2. Same Bearer token used for both requests (steps 3 and 12)
3. Token value in `get()` and `validate()` must match (`"api/deepchat"`)

## Common Mistakes

- **Wrong**: Using different OAuth clients for session fetch and API call → **Right**: Call `auth()` once, reuse same `accessToken` for both requests
- **Wrong**: Assuming `_csrf_token: TRUE` route requirement is optional → **Right**: It is enforced by `CsrfAccessCheck` and will 403 without a valid token

## See Also

- [Architecture Overview](oauth-csrf-overview.md)
- [CSRF Token Lifecycle](csrf-token-lifecycle.md)
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfAccessCheck.php`
- Drupal docs: [CSRF Access Checking](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/csrf-access-checking)
