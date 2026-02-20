---
description: Step-by-step debugging guide for CSRF failures in DeepChat + Drupal OAuth — curl commands, log inspection, session verification
drupal_version: "11.x"
---

# Debugging Checklist

## When to Use

> Use this guide when diagnosing `csrf_token URL query argument is invalid` or 403 errors in production. Use [Common Pitfalls](common-pitfalls.md) for known causes and fixes.

## Decision

| Symptom | Check | Tool |
|---------|-------|------|
| 401 on any request | OAuth token invalid or expired | Step 1: curl against `/jsonapi/user/user` |
| Session endpoint returns no `Set-Cookie` | Session not being created | Step 2: curl with `-v` |
| Token is wrong length | CSRF generation failed | Step 3: `wc -c` on token |
| API call returns 403 | Token invalid or wrong context | Step 4: curl with cookie jar |
| Random failures | Mixed session cookies | Step 4 + clear `SESS*` cookies |
| Works with cookie jar, fails without | Cookie not being sent by browser | Browser DevTools — Application → Cookies |

## Pattern

**Step 1: Verify OAuth works**

```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://your-drupal.com/jsonapi/user/user
# Expect: 200 with user data
```

**Step 2: Verify session creation**

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -v \
  https://your-drupal.com/api/deepchat/session
# Expect: 200, body = 43-char token, headers include Set-Cookie: SESS*
```

**Step 3: Verify token format**

```bash
echo "$TOKEN_VALUE" | wc -c  # Should be 44 (43 + newline)
echo "$TOKEN_VALUE" | grep -E '^[A-Za-z0-9_-]{43}$'  # Should match
```

**Step 4: Test API with cookie jar**

```bash
# 1. Get token, save cookie
curl -X POST -H "Authorization: Bearer $TOKEN" -c cookies.txt -v \
  https://your-drupal.com/api/deepchat/session

# 2. Use token with cookie
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"assistant_id":"test","messages":[{"role":"user","text":"Hello"}]}' \
  "https://your-drupal.com/api/deepchat?token=$TOKEN_VALUE"
```

**Step 5: Check Drupal logs**

```bash
drush config:set system.logging error_level verbose -y && drush cr
drush watchdog:tail --extended
# Look for: "csrf_token URL query argument is invalid", session start messages
```

**Step 6: Add Drupal debug logging**

```php
// In setSession() temporarily:
\Drupal::logger('ai_chatbot')->info('Session ID: @id, started: @s', [
  '@id' => $session->getId(),
  '@s'  => $session->isStarted() ? 'YES' : 'NO',
]);
```

**Step 7: Add Next.js proxy logging**

```typescript
console.log('[DeepChat Proxy] access_token:', session?.accessToken?.substring(0, 10));
console.log('[DeepChat Proxy] CSRF token:', csrfToken?.substring(0, 10));
console.log('[DeepChat Proxy] Drupal status:', drupalResponse.status);
if (!drupalResponse.ok) console.error(await drupalResponse.text());
```

## Common Mistakes

- **Wrong**: Testing without `-b cookies.txt` and assuming cookie-less curl proves the issue → **Right**: Test both with and without cookie jar — difference isolates session persistence
- **Wrong**: Comparing only against Drupal's native JS (`deepchat-init.js`) which uses cookie auth — **Right**: Native JS uses cookie auth (no session setup needed); OAuth flow requires explicit session creation

## See Also

- [Common Pitfalls](common-pitfalls.md)
- [CSRF Token Lifecycle](csrf-token-lifecycle.md)
- [Reference Implementation](reference-implementation.md)
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/js/deepchat-init.js`
