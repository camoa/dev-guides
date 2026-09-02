---
description: HTTP security headers configuration including CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy.
tldr: "Configure security headers on ALL HTTP responses. Headers provide defense-in-depth against XSS, clickjacking, MIME sniffing, and other attacks."
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

**CSP is the most powerful XSS mitigation** (see section 6.0 for details).

```http
# Strict CSP with nonces (recommended 2025+)
Content-Security-Policy: default-src 'self'; script-src 'nonce-{random}' 'strict-dynamic'; object-src 'none'; base-uri 'none';

# Breakdown:
# default-src 'self' - Only load resources from same origin
# script-src 'nonce-{random}' - Only execute scripts with matching nonce
# 'strict-dynamic' - Allow scripts loaded by trusted scripts
# object-src 'none' - Block plugins (Flash, Java applets)
# base-uri 'none' - Prevent <base> tag injection

# Moderate CSP (if nonces not feasible)
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;
```

**Major 2026 enforcement:** SharePoint Online (March 2026) and Microsoft Entra ID (October 2026) enforcing CSP. Migrate inline scripts to external files now.

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

**Prevents MIME sniffing attacks:**

```html
<!-- Attacker uploads image.jpg containing JavaScript -->
<!-- Without nosniff, IE/Chrome might execute it as script -->
<img src="/uploads/image.jpg">

<!-- With nosniff, browser strictly respects Content-Type: image/jpeg -->
<!-- Won't execute as script even if contains JavaScript code -->
```

## X-Frame-Options

**Prevents clickjacking:**

```http
# Don't allow framing at all
X-Frame-Options: DENY

# Allow framing only from same origin
X-Frame-Options: SAMEORIGIN

# Allow specific domain (deprecated - use CSP frame-ancestors instead)
X-Frame-Options: ALLOW-FROM https://trusted.com
```

**Clickjacking attack scenario:**

```html
<!-- evil.com embeds your site in invisible iframe -->
<iframe src="https://yourbank.com/transfer" style="opacity:0"></iframe>
<button style="position:absolute; top:100px; left:200px;">Click to win iPad!</button>

<!-- User clicks "win iPad" button, actually clicks "transfer money" in hidden iframe -->
```

**Modern alternative — CSP frame-ancestors:**

```http
Content-Security-Policy: frame-ancestors 'self' https://trusted.com
```

## Referrer-Policy

**Controls referer information sent with requests:**

```http
# Send full URL to same origin, only origin to cross-origin
Referrer-Policy: strict-origin-when-cross-origin

# Never send referer
Referrer-Policy: no-referrer

# Send origin only
Referrer-Policy: origin
```

**Why it matters:**

```text
User visits: https://yoursite.com/private/patient-records?id=12345&ssn=123-45-6789
User clicks link to: https://external-site.com

Without Referrer-Policy:
  Referer: https://yoursite.com/private/patient-records?id=12345&ssn=123-45-6789
  (Leaks sensitive data in URL!)

With strict-origin-when-cross-origin:
  Referer: https://yoursite.com
  (Only origin, no path/query)
```

## Permissions-Policy

**Disable unnecessary browser features (replaces Feature-Policy):**

```http
Permissions-Policy: geolocation=(), microphone=(), camera=(), payment=(), usb=()

# Allow specific features for specific origins
Permissions-Policy: geolocation=(self "https://maps.example.com"), camera=(self)
```

**2025 growth:** Permissions-Policy adoption increasing as Feature-Policy is deprecated.

## Cross-Origin Policies

**Cross-Origin-Opener-Policy (COOP):**

```http
Cross-Origin-Opener-Policy: same-origin
```

Prevents other sites from gaining window reference to your site (Spectre attacks).

**Cross-Origin-Resource-Policy (CORP):**

```http
Cross-Origin-Resource-Policy: same-origin
```

Prevents other sites from loading your resources (images, scripts, etc.).

**COOP adoption doubled in 2025** from <1% to ~2% of sites.

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

**Complete security headers (PHP):**

```php
header("Content-Security-Policy: default-src 'self'; script-src 'nonce-" . $nonce . "' 'strict-dynamic'; object-src 'none'; base-uri 'none';");
header("Strict-Transport-Security: max-age=31536000; includeSubDomains; preload");
header("X-Content-Type-Options: nosniff");
header("X-Frame-Options: DENY");
header("Referrer-Policy: strict-origin-when-cross-origin");
header("Permissions-Policy: geolocation=(), microphone=(), camera=()");
header("Cross-Origin-Opener-Policy: same-origin");
header("Cross-Origin-Resource-Policy: same-origin");
```

## Testing Security Headers

**Online scanners:**

- https://securityheaders.com — Grades A-F based on headers
- https://observatory.mozilla.org — Mozilla Observatory
- https://csp-evaluator.withgoogle.com — CSP validator

**Browser DevTools:**

```javascript
// Check CSP violations in browser console
document.addEventListener('securitypolicyviolation', (e) => {
    console.log('CSP violation:', e.violatedDirective, e.blockedURI);
});
```

## Common Mistakes

- **CSP with 'unsafe-inline' or 'unsafe-eval'** — Defeats the purpose. Use nonces or hashes instead
- **HSTS without HTTPS** — Can't set HSTS over HTTP (browser ignores it). Deploy HTTPS first
- **X-Frame-Options and CSP frame-ancestors conflict** — Use CSP frame-ancestors (more flexible). If both present, frame-ancestors takes precedence
- **Setting headers only on HTML pages** — Set on ALL responses (CSS, JS, images, API). Attacks can leverage any resource type
- **Permissive CSP in production** — `script-src *` or `default-src *` allows everything. Start strict, widen only as needed
- **Not testing headers** — Use securityheaders.com to verify. Many apps have misconfigurations (typos, syntax errors)
- **Forgetting 'always' flag in Nginx** — Without `always`, Nginx skips headers on error responses. Use `add_header ... always`

## See Also

- Previous: [Sensitive Data Protection](sensitive-data-protection.md) | Next: [API Security](api-security.md)
- See also: [Browser Security Policies](browser-security-policies.md) — CSP enforcement workflow, Trusted Types, cross-origin isolation, Fetch Metadata
- Reference: [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- Reference: [HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- Reference: [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
