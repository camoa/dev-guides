---
description: HTTP security headers configuration including CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy.
---

# Security Headers

## When to Use

Configure security headers on ALL HTTP responses. Headers provide defense-in-depth against XSS, clickjacking, MIME sniffing, and other attacks. As of 2025, X-Content-Type-Options leads adoption at ~50%, with HSTS and X-Frame-Options at ~35%.

## Decision

| Header | Purpose | Recommended Value |
|---|---|---|
| **Content-Security-Policy** | Prevent XSS by restricting script sources | `default-src 'self'; script-src 'nonce-{random}'` |
| **Strict-Transport-Security (HSTS)** | Force HTTPS connections | `max-age=31536000; includeSubDomains; preload` |
| **X-Content-Type-Options** | Prevent MIME sniffing | `nosniff` |
| **X-Frame-Options** | Prevent clickjacking | `DENY` or `SAMEORIGIN` |
| **Referrer-Policy** | Control referer information | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | Disable unnecessary browser features | `geolocation=(), microphone=(), camera=()` |
| **Cross-Origin-Opener-Policy (COOP)** | Isolate browsing context | `same-origin` |
| **Cross-Origin-Resource-Policy (CORP)** | Block cross-origin resource loading | `same-origin` |

## Content-Security-Policy (CSP)

```http
# Strict CSP with nonces (recommended 2025+)
Content-Security-Policy: default-src 'self'; script-src 'nonce-{random}' 'strict-dynamic'; object-src 'none'; base-uri 'none';

# Moderate CSP (if nonces not feasible)
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;
```

**Major 2026 enforcement:** SharePoint Online (March 2026) and Microsoft Entra ID (October 2026) enforcing CSP.

## Strict-Transport-Security (HSTS)

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**HSTS preload list:** Submit your domain to https://hstspreload.org/ for hardcoded HTTPS in browsers.

**Warning:** HSTS with preload is irreversible for months. Test thoroughly first with shorter max-age.

## X-Content-Type-Options

```http
X-Content-Type-Options: nosniff
```

Prevents MIME sniffing attacks where browsers might execute uploaded files as scripts.

## X-Frame-Options

```http
X-Frame-Options: DENY
```

**Clickjacking attack scenario:**

```html
<!-- evil.com embeds your site in invisible iframe -->
<iframe src="https://yourbank.com/transfer" style="opacity:0"></iframe>
<button style="position:absolute;">Click to win!</button>
<!-- User clicks "win" button, actually clicks "transfer" in hidden iframe -->
```

**Modern alternative — CSP frame-ancestors:**

```http
Content-Security-Policy: frame-ancestors 'self' https://trusted.com
```

## Referrer-Policy

```http
Referrer-Policy: strict-origin-when-cross-origin
```

Controls referer information sent with requests. Prevents leaking sensitive URL paths/parameters to external sites.

## Permissions-Policy

```http
Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=(), usb=()
```

## Cross-Origin Policies

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

## Pattern

**Complete security headers (Flask):**

```python
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'nonce-{nonce}' 'strict-dynamic'; object-src 'none'; base-uri 'none';"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    return response
```

**Complete security headers (Nginx):**

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'nonce-$request_id' 'strict-dynamic'; object-src 'none'; base-uri 'none';" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Cross-Origin-Opener-Policy "same-origin" always;
add_header Cross-Origin-Resource-Policy "same-origin" always;
```

## Testing Security Headers

- https://securityheaders.com — Grades A-F based on headers
- https://observatory.mozilla.org — Mozilla Observatory
- https://csp-evaluator.withgoogle.com — CSP validator

## Common Mistakes

- **CSP with 'unsafe-inline' or 'unsafe-eval'** — Defeats the purpose. Use nonces or hashes instead
- **HSTS without HTTPS** — Can't set HSTS over HTTP. Deploy HTTPS first
- **X-Frame-Options and CSP frame-ancestors conflict** — Use CSP frame-ancestors (more flexible)
- **Setting headers only on HTML pages** — Set on ALL responses (CSS, JS, images, API)
- **Permissive CSP in production** — `script-src *` allows everything. Start strict, widen only as needed
- **Not testing headers** — Use securityheaders.com to verify
- **Forgetting 'always' flag in Nginx** — Without `always`, Nginx skips headers on error responses

## See Also

- Previous: [Sensitive Data Protection](sensitive-data-protection.md) | Next: [API Security](api-security.md)
- Reference: [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- Reference: [HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- Reference: [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
