---
description: How Drupal CSRF tokens are generated and validated — seed storage, HMAC computation, and root causes of validation failure
tldr: "Use this guide to understand the internals of `CsrfTokenGenerator::get()` and `validate()`. Use [Common Pitfalls](common-pitfalls.md) for actionable fixes when validation fails."
drupal_version: "11.x"
---

# CSRF Token Lifecycle

## When to Use

> Use this guide to understand the internals of `CsrfTokenGenerator::get()` and `validate()`. Use [Common Pitfalls](common-pitfalls.md) for actionable fixes when validation fails.

## Decision

| Root Cause | Symptom | Fix |
|-----------|---------|-----|
| No PHP session when `get()` called | Seed empty → not persisted → validation always fails | Call `$session->start()` before `get()` |
| Different session context between requests | Seed in session A not visible in session B | Use same Bearer token for both requests |
| Token value mismatch (`get()` vs `validate()`) | Token wrong → `hash_equals()` returns false | Both must use `"api/deepchat"` (no leading slash, no query params) |
| Stale session cookie conflicts | Works sometimes, fails randomly | Clear `SESS*` cookies; use consistent auth flow |

## Pattern

**Generation (`setSession()`):**

```php
public function setSession(Request $request): Response {
  $session = $request->getSession();
  if (!$session->isStarted()) {
    $session->start();  // CRITICAL: creates PHP session + stores seed
  }
  $session->set('deepchat', 'true');
  return new Response($this->csrfTokenGenerator->get("api/deepchat"));
}
```

**Inside `get()`:**

```php
$seed = $this->sessionMetadata->getCsrfTokenSeed();
if (empty($seed)) {
  $seed = Crypt::randomBytesBase64();  // 43-char random string
  $this->sessionMetadata->setCsrfTokenSeed($seed);
}
return Crypt::hmacBase64($value, $seed . $this->privateKey->get() . Settings::getHashSalt());
```

**Validation (route access check):**

```php
$seed = $this->sessionMetadata->getCsrfTokenSeed();
if (empty($seed)) return FALSE;  // No session = always fail
$expected = $this->computeToken($seed, $value);
return hash_equals($expected, $token);
```

Token format: 43-character URL-safe Base64. Stored seed: `$_SESSION['_sf2_meta']['csrf_token_seed']`.

## Why Validation Fails: Root Causes

## Cause 1: Session Context Lost (Most Common)

**Scenario:**
```
Request 1: POST /api/deepchat/session
  → Creates session A, seed=ABC123
  → Returns token based on ABC123

Request 2: POST /api/deepchat?token=...
  → Different session B created (no seed)
  → Validation fails: no seed in session
```

**Why This Happens:**
- Session cookies not being sent/received properly
- OAuth authentication bypassing session system
- Browser not storing session cookie from first request

**Solution:**
- Ensure same Bearer token used for both requests
- Verify session cookie (SESS\*) is set and sent
- Check `withCredentials` in fetch calls if needed

## Cause 2: Token Value Mismatch

**Scenario:**
```
Token Generation: get("api/deepchat")      → Token X
Token Validation: validate(Token X, "deepchat/api")  → FAIL
```

**Why This Happens:**
- Route path generation differs between generation and validation
- Query parameters included in validation path
- Typo in value parameter

**Solution:**
- Both `get()` and `validate()` must use identical value
- Reference: Drupal uses route path without leading slash
- For `/api/deepchat`, value should be `"api/deepchat"`

## Cause 3: OAuth Session Conflict

**Scenario:**
```
User has both:
  - OAuth Bearer token (stateless)
  - PHP session cookie (stateful)

Drupal sees session cookie → checks CSRF
But session was created by different auth mechanism
Seed doesn't match
```

**Why This Happens:**
- Mixed authentication methods
- Old session cookie from different context
- Session created by standard login, not OAuth flow

**Solution:**
- Use consistent authentication pattern
- Clear old session cookies in development
- Ensure session is created with same user context as API calls

---

## Common Mistakes

- **Wrong**: Calling `get()` without starting session first — seed is empty and won't persist → **Right**: Always check `isStarted()` and call `start()` before `get()`
- **Wrong**: Generating token with `"deepchat/api"` but route validates against `"api/deepchat"` → **Right**: Use the route path without leading slash

## See Also

- [Authentication Flow](dual-authentication-flow.md)
- [Common Pitfalls](common-pitfalls.md)
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php`
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfAccessCheck.php`
- API: [CsrfTokenGenerator](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Access!CsrfTokenGenerator.php/class/CsrfTokenGenerator/11.x)
