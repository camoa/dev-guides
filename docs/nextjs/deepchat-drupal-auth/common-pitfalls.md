---
description: Common CSRF and session pitfalls in DeepChat + Drupal OAuth — mismatched auth contexts, missing session start, wrong token placement
drupal_version: "11.x"
---

# Common Pitfalls

## When to Use

> Use this guide when CSRF validation is failing (`csrf_token URL query argument is invalid`) or chat requests return 403. Use [Debugging Checklist](debugging-checklist.md) for systematic curl-based diagnosis.

## Decision

| Pitfall | Root Cause | Fix |
|--------|-----------|-----|
| Token from wrong session context | `getDrupalForUser()` vs `auth()` use different token handling | Call `auth()` once; use same `accessToken` for both requests |
| CSRF always fails for OAuth users | No `$session->start()` in `setSession()` | Add `if (!$session->isStarted()) $session->start();` |
| 403 even with correct token | Token passed in header or body, not query param | Use `?token=<csrf>` query parameter |
| Works in incognito, fails otherwise | Stale `SESS*` cookies from previous sessions | Clear cookies; use consistent auth flow |
| Token valid, but API call fails sometimes | Token value mismatch (query params included in route path) | Use `"api/deepchat"` — no leading slash, no query params |
| Different `getDrupalForUser()` instances | Internal token refresh between calls | Use one `auth()` call per request lifecycle |

## Pattern

**Wrong: mixed auth clients**

```typescript
// BAD
const drupal = await getDrupalForUser();
const token = await (await drupal.fetch('/api/deepchat/session')).text();
const session = await auth();
await fetch(`/api/deepchat?token=${token}`, {
  headers: { 'Authorization': `Bearer ${session.accessToken}` }
});
```

**Right: single Bearer token throughout**

```typescript
// GOOD
const session = await auth();
const accessToken = session.accessToken;

const token = await (await fetch(`${baseUrl}/api/deepchat/session`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${accessToken}` },
})).text();

await fetch(`${baseUrl}/api/deepchat?token=${encodeURIComponent(token)}`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
});
```

**Wrong: missing session start (Drupal)**

```php
// BAD
public function setSession(Request $request): Response {
  return new Response($this->csrfTokenGenerator->get("api/deepchat"));
}
```

**Right: explicit session start**

```php
// GOOD
public function setSession(Request $request): Response {
  $session = $request->getSession();
  if (!$session->isStarted()) $session->start();
  $session->set('deepchat', 'true');
  return new Response($this->csrfTokenGenerator->get("api/deepchat"));
}
```

## Common Mistakes

- **Wrong**: `X-CSRF-Token` header or `body.token` → **Right**: Query param only (`?token=...`) — the route uses `_csrf_token: 'TRUE'` which reads from `$request->query->get('token')`
- **Wrong**: Creating multiple `getDrupalForUser()` instances within one request → **Right**: One `auth()` call, one `accessToken`, used for all requests in that lifecycle

## See Also

- [CSRF Token Lifecycle](csrf-token-lifecycle.md)
- [Debugging Checklist](debugging-checklist.md)
- [Reference Implementation](reference-implementation.md)
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/ai_chatbot.routing.yml`
