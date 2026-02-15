---
description: Defense-in-depth XSS protections including Content Security Policy (CSP), HTML sanitization libraries, template auto-escaping, and HTTPOnly cookies.
---

# XSS Prevention Patterns

## When to Use

Implement these defense-in-depth XSS protections in addition to (not instead of) input validation and output encoding.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Allow NO HTML in user content | Output escaping only | Simplest, most secure |
| Allow SOME HTML formatting | HTML sanitization library (Bleach, DOMPurify) | Allowlist-based sanitization |
| Restrict script sources | Content Security Policy (CSP) | Mitigates impact when XSS bypasses other defenses |
| Protect session cookies | HTTPOnly + Secure + SameSite flags | Prevents JavaScript access to cookies |
| Auto-escape templates | Modern framework (React, Vue, Django) | Reduces human error |

## Content Security Policy (CSP)

**CSP is the most powerful XSS mitigation.** Even if attacker injects `<script>` tag, CSP can prevent execution.

**CSP enforcement levels:**

```http
# Level 1: Block inline scripts, only allow scripts from specific domains
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com

# Level 2: Stricter - use nonces or hashes for inline scripts
Content-Security-Policy: script-src 'nonce-{random}' 'strict-dynamic'

# Level 3: Most strict - no inline scripts at all
Content-Security-Policy: script-src 'self'; object-src 'none'; base-uri 'none'
```

**Nonce-based CSP (recommended for 2025+):**

```php
// Generate random nonce for each request
$nonce = base64_encode(random_bytes(16));

// Set CSP header with nonce
header("Content-Security-Policy: script-src 'nonce-{$nonce}'");

// Allow only scripts with matching nonce
echo "<script nonce='{$nonce}'>alert('Allowed');</script>";
echo "<script>alert('Blocked - no nonce');</script>";  // Blocked by CSP
```

**CSP Report-Only mode (for testing):**

```http
# Test CSP without blocking, just report violations
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

**Major 2026 CSP enforcement:** SharePoint Online and Microsoft Entra ID enforcing CSP in March-October 2026. Prepare now by auditing inline scripts.

## HTML Sanitization Libraries

**When users need formatted text (bold, links, lists):**

```javascript
// DOMPurify (JavaScript) - client or server-side with jsdom
import DOMPurify from 'dompurify';

function sanitizeUserHTML(dirty) {
    const clean = DOMPurify.sanitize(dirty, {
        ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li'],
        ALLOWED_ATTR: ['href', 'title']
    });
    return clean;
}

// Input: "<p>Hello</p><script>alert('XSS')</script>"
// Output: "<p>Hello</p>"
```

```python
# Bleach (Python) - HTML sanitization
import bleach

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li']
ALLOWED_ATTRS = {'a': ['href', 'title']}

def sanitize_user_html(dirty):
    clean = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
    return clean
```

**Sanitization library selection criteria:**

- Regularly updated (XSS bypass techniques evolve)
- Uses allowlist approach (not blocklist)
- Handles mutation XSS (browser re-parsing)
- Well-tested against OWASP XSS vectors

## Template Auto-Escaping

**Frameworks with built-in XSS protection:**

```jsx
// React - auto-escapes by default
function UserProfile({ username }) {
    return <div>{username}</div>;  {/* Safe - auto-escaped */}
}

// Vue.js - auto-escapes
<template>
    <div>{{ username }}</div>  <!-- Safe - auto-escaped -->
</template>

// Django templates - auto-escapes
<div>{{ username }}</div>  {# Safe - auto-escaped #}
```

**But you must STILL escape in non-HTML contexts:**

```jsx
// React - NOT auto-escaped in attribute event handlers
<div onClick={() => eval(userInput)}>Bad</div>  {/* XSS! */}

// Correct approach - use data attributes + event listeners
<div data-user-id={userId} onClick={handleClick}>Good</div>
```

## HTTPOnly Cookies

**Session cookies MUST have HTTPOnly flag:**

```php
// Good: HTTPOnly prevents JavaScript access
setcookie('session_id', $session_value, [
    'httponly' => true,
    'secure' => true,      // Only send over HTTPS
    'samesite' => 'Lax',   // CSRF protection
]);

// Bad: JavaScript can read cookie (XSS steals session)
setcookie('session_id', $session_value);
```

```javascript
// Express.js (Node.js)
app.use(session({
    cookie: {
        httpOnly: true,
        secure: true,        // Only HTTPS
        sameSite: 'lax'      // CSRF protection
    }
}));
```

**XSS impact with/without HTTPOnly:**

- **Without HTTPOnly:** XSS -> `document.cookie` -> attacker gets session -> account hijacked
- **With HTTPOnly:** XSS -> `document.cookie` returns empty -> attacker can't steal session (but can still perform actions as user)

## Pattern

```text
Defense-in-Depth XSS Prevention Stack:
1. Input validation - allowlist patterns
2. Output encoding - context-specific escaping
3. HTML sanitization - DOMPurify/Bleach for formatted text
4. Template auto-escaping - framework default protection
5. Content Security Policy - restrict script sources
6. HTTPOnly cookies - prevent cookie theft
7. Security headers - X-Content-Type-Options: nosniff
```

## Common Mistakes

- **CSP with 'unsafe-inline'** — Defeats the purpose. `script-src 'unsafe-inline'` allows ALL inline scripts including XSS. Use nonces instead
- **CSP with overly broad allowlist** — `script-src *` or `script-src https:` allows too many sources. Be specific
- **Not testing CSP in Report-Only mode first** — CSP can break functionality. Test with `Content-Security-Policy-Report-Only` before enforcing
- **Sanitizing input instead of output** — Sanitize at output time (just before display), not at input time
- **Trusting sanitization libraries blindly** — DOMPurify and Bleach are excellent but not perfect. Keep libraries updated
- **Using eval() or Function() with user data** — NEVER use `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` with untrusted data

## See Also

- Previous: [Cross-Site Scripting (XSS)](cross-site-scripting-xss.md) | Next: [SQL Injection Prevention](sql-injection-prevention.md)
- Reference: [Content Security Policy (CSP) - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
- Reference: [DOMPurify](https://github.com/cure53/DOMPurify)
- Reference: [Bleach (Python)](https://bleach.readthedocs.io/)
