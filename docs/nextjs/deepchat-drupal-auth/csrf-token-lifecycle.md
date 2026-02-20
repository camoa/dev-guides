---
description: How Drupal CSRF tokens are generated and validated — seed storage, HMAC computation, and root causes of validation failure
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

## Common Mistakes

- **Wrong**: Calling `get()` without starting session first — seed is empty and won't persist → **Right**: Always check `isStarted()` and call `start()` before `get()`
- **Wrong**: Generating token with `"deepchat/api"` but route validates against `"api/deepchat"` → **Right**: Use the route path without leading slash

## See Also

- [Authentication Flow](dual-authentication-flow.md)
- [Common Pitfalls](common-pitfalls.md)
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php`
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfAccessCheck.php`
- API: [CsrfTokenGenerator](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Access!CsrfTokenGenerator.php/class/CsrfTokenGenerator/11.x)
