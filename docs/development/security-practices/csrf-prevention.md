---
description: CSRF attack mechanics and prevention using SameSite cookies, CSRF tokens, double submit cookie pattern, and Origin/Referer validation.
---

# CSRF Prevention

## When to Use

Protect ALL state-changing operations: POST/PUT/DELETE requests, password changes, money transfers, profile updates, admin actions. GET requests should NEVER change state (by design, GET = read-only).

## How CSRF Attacks Work

```text
1. User logs into bank.com, receives session cookie
2. User visits evil.com (different tab, same browser)
3. evil.com contains hidden form:
   <form action="https://bank.com/transfer" method="POST">
       <input name="to" value="attacker_account">
       <input name="amount" value="10000">
   </form>
   <script>document.forms[0].submit();</script>
4. Form submits to bank.com with user's session cookie (automatic)
5. Bank processes transfer as legitimate request (user is authenticated)
6. Money transferred to attacker
```

**Why it works:** Browsers automatically include cookies with requests to matching domains, even from other sites.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| CSRF protection (modern apps) | **SameSite cookies + CSRF tokens** | Double protection |
| CSRF protection (legacy browsers) | CSRF tokens (synchronizer token pattern) | SameSite not supported in old browsers |
| API authentication | Token-based auth (JWT, API keys) instead of cookies | No automatic credential inclusion |
| Simple protection | SameSite=Lax cookies | Blocks CSRF for POST/PUT/DELETE (not GET) |
| Strict protection | SameSite=Strict cookies | Blocks CSRF completely (but breaks legitimate cross-site navigation) |

## Pattern

**SameSite cookies (primary defense for 2025+):**

```php
// PHP - SameSite=Lax (recommended default)
setcookie('session_id', $session_value, [
    'httponly' => true,
    'secure' => true,
    'samesite' => 'Lax',  // Browser won't send cookie on POST from other sites
]);
```

```javascript
// Express.js (Node.js)
app.use(session({
    cookie: {
        httpOnly: true,
        secure: true,
        sameSite: 'lax'
    }
}));
```

**CSRF tokens (defense in depth):**

```python
# Django - automatic CSRF protection
<form method="POST">
    {% csrf_token %}
    <input name="email" value="{{ user.email }}">
    <button type="submit">Update</button>
</form>
# Django validates token automatically - returns 403 if missing/invalid
```

```php
// PHP - manual CSRF token implementation
session_start();
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
?>
<form method="POST" action="/update-profile">
    <input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">
    <button type="submit">Update</button>
</form>
<?php
// Validate token on submission
if ($_POST['csrf_token'] !== $_SESSION['csrf_token']) {
    die('CSRF token validation failed');
}
```

```javascript
// React SPA - CSRF token in header
function updateProfile(email) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    return fetch('/api/update-profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        },
        body: JSON.stringify({ email })
    });
}
```

**Double submit cookie pattern (stateless CSRF protection):**

```javascript
// Server sets CSRF token as cookie
response.cookie('csrf_token', token, {
    httpOnly: false,  // JavaScript must read it
    secure: true,
    sameSite: 'lax'
});

// Client reads cookie and submits as header
const csrfToken = getCookie('csrf_token');
fetch('/api/update', {
    method: 'POST',
    headers: { 'X-CSRF-Token': csrfToken },
    body: JSON.stringify(data)
});

// Server validates: header value === cookie value
// Attacker can't read cookies from other domains (same-origin policy)
```

## Defense Layers

**Recommended 2025+ approach (multiple layers):**

1. **SameSite=Lax cookies** — blocks most CSRF attacks
2. **CSRF tokens** — catches edge cases (SameSite bypass, old browsers)
3. **Origin/Referer validation** — supplementary check
4. **Re-authentication for sensitive actions** — password change, money transfer require password re-entry

## Common Mistakes

- **Using only SameSite cookies** — SameSite has edge cases and browser inconsistencies. Use tokens too
- **CSRF protection on GET requests** — GET should never change state. If your GET endpoints modify data, that's the real problem
- **Checking Referer header only** — Referer can be stripped by proxies, privacy extensions, HTTPS to HTTP transitions
- **Not protecting JSON APIs** — CSRF affects JSON APIs too. SameSite cookies + custom header required
- **Weak token generation** — Use cryptographically secure random. NOT Math.random() or predictable patterns
- **Token reuse across sessions** — Generate new token per session or per request
- **SameSite=None without reason** — `SameSite=None` disables protection. Only use for legitimate cross-site embedding

## See Also

- Previous: [SQL Injection Prevention](sql-injection-prevention.md) | Next: [Authentication Best Practices](authentication-best-practices.md)
- Reference: [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- Reference: [SameSite cookies explained](https://web.dev/articles/samesite-cookies-explained)
