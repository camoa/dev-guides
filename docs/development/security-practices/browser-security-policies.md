---
description: Browser security policy deployment — CSP enforcement workflow (report-only to enforce), Trusted Types for DOM-sink XSS, cross-origin isolation (COOP+COEP), Fetch Metadata resource isolation, and Clear-Site-Data on logout.
tldr: Deploy CSP through three phases — report-only discovery (days to weeks, not hours), analyze violations filtering extension noise, then enforce only when violations near zero. Trusted Types blocks DOM-sink XSS at runtime but requires framework/widget support audit before enforcement — third-party widgets that write raw strings to innerHTML will throw. COEP requires every embedded subresource to serve Cross-Origin-Resource-Policy or the browser blocks it.
drupal_version: ""
---

# Browser Security Policies

## When to Use

> Apply when hardening an existing web application incrementally against client-side attacks. Section 12.0 covers which security headers to set; this section covers the deployment workflow for safely enforcing CSP, protecting DOM sinks with Trusted Types, enabling cross-origin isolation, verifying request origin with Fetch Metadata, and wiping browser state at logout.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Roll out CSP without breaking the app | Report-Only → Analyze → Enforce workflow | Strict CSP applied blindly breaks inline scripts silently for users |
| Block DOM-sink XSS at runtime | Trusted Types (`require-trusted-types-for 'script'`) | Enforces safe DOM writes even when XSS payloads bypass other defenses |
| Enable SharedArrayBuffer or WebAssembly multi-threading | Cross-origin isolation (COOP + COEP) | Browsers require `crossOriginIsolated = true` for these APIs |
| Reject suspicious cross-site subresource requests server-side | Fetch Metadata resource-isolation policy | `Sec-Fetch-*` headers cannot be forged by cross-site scripts |
| Wipe all browser state on logout | `Clear-Site-Data` response header | Clears cookies, localStorage, sessionStorage, and cache in one response |

## Pattern

**CSP — Phase 1: Report-Only discovery (run for days to weeks):**

```http
Reporting-Endpoints: csp-endpoint="https://reports.example/csp"
Content-Security-Policy-Report-Only: script-src 'nonce-{RANDOM}' 'strict-dynamic' 'report-sample'; object-src 'none'; base-uri 'none'; report-to csp-endpoint;
```

`'report-sample'` includes the first 40 characters of violating code in each report. The `'strict-dynamic'`, `https:`, and `'unsafe-inline'` tokens form a backwards-compatibility ladder: modern browsers honor `'strict-dynamic'` and ignore the others; older browsers fall back to `https:` then `'unsafe-inline'`.

**Phase 2 — Analyze reports:**

| Violation pattern | Action |
|---|---|
| Many inline-script violations | Add server-rendered nonces to `<script>` tags; use hashes for static/cached HTML (SPAs) |
| Third-party analytics violations | Use `'strict-dynamic'` with a nonce so the loader propagates trust to its children. Never add the analytics domain to a URL allowlist |
| Trusted Types violations on specific sinks | Refactor those sinks before enforcing |

**Phase 3 — Enforce (only when violations near zero):**

```http
Reporting-Endpoints: csp-endpoint="https://reports.example/csp"
Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic' 'report-sample'; object-src 'none'; base-uri 'none'; report-to csp-endpoint;
```

Keep `report-to` on the enforced header so regressions remain visible.

**Trusted Types — incremental rollout:**

```javascript
// 1. Audit sinks via report-only first
// 2. Refactor sinks to use safe DOM APIs (textContent, createElement)
// 3. For unavoidable sinks, route through a named policy:
if (window.trustedTypes && trustedTypes.createPolicy) {
  const policy = trustedTypes.createPolicy('default', {
    createHTML: (input) => DOMPurify.sanitize(input)
  });
  el.innerHTML = policy.createHTML(untrustedContent);
}
// 4. Move to global enforcement only after violations drop to zero
```

**Cross-origin isolation (only when SharedArrayBuffer or WASM threading is needed):**

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Every embedded subresource must serve `Cross-Origin-Resource-Policy: cross-origin` or the browser blocks it. Use Report-Only headers to discover breakage before enforcing. Note: `COOP: same-origin` severs `window.opener` references — audit OAuth popups and payment gateway flows.

**Chromium-only alternative (Chrome 142+):**

```http
Document-Isolation-Policy: isolate-and-credentialless
```

Strips credentials from non-CORS cross-origin requests instead of blocking them. Not implemented in other browsers.

**Fetch Metadata resource-isolation middleware:**

```javascript
app.use((req, res, next) => {
  const site = req.get('Sec-Fetch-Site');
  if (!site) return next(); // Legacy browsers: fail open

  if (['same-origin', 'same-site', 'none'].includes(site)) return next();

  // Allow top-level navigation GET requests (ordinary link clicks)
  const mode = req.get('Sec-Fetch-Mode');
  const dest = req.get('Sec-Fetch-Dest');
  if (site === 'cross-site' && mode === 'navigate' &&
      req.method === 'GET' && !['object', 'embed'].includes(dest)) {
    return next();
  }

  return res.status(403).send('Forbidden');
});
```

Prevent CDNs from caching a blocked response: `Vary: Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site`

**Clear-Site-Data on logout (server-side response header):**

```http
Clear-Site-Data: "cookies", "storage", "cache"
```

Clears cookies, localStorage, sessionStorage, and HTTP cache in one response. All modern browsers support it.

## Common Mistakes

- **Deploying enforced CSP without report-only first** → Strict policies silently break inline scripts for real users; run report-only for days to weeks
- **URL allowlists in CSP** → `script-src https://cdn.example.com` is bypassed via open redirects or JSONP on the allowlisted domain; use nonces or hashes
- **Trusted Types without framework and widget support audit** → Third-party widgets writing raw strings to DOM sinks will throw at assignment time
- **COEP without CORP on every embedded subresource** → A single third-party image lacking `Cross-Origin-Resource-Policy` blocks the entire page
- **Missing `Vary` header on Fetch Metadata-protected endpoints** → CDNs may cache a 403 and serve it to legitimate users
- **Only deleting the session cookie on logout** → localStorage, sessionStorage, and cached responses persist; `Clear-Site-Data` closes all state at once

## See Also

- [Security Headers](security-headers.md) — 12.0 which headers to set and recommended values
- [XSS Prevention Patterns](xss-prevention-patterns.md) — CSP basics, nonce generation, DOMPurify
- [Cross-Site Scripting (XSS)](cross-site-scripting-xss.md) — safe DOM APIs (textContent vs innerHTML)
- Reference: [W3C Trusted Types specification](https://w3c.github.io/trusted-types/dist/spec/)
- Reference: [MDN Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)
- Reference: [Fetch Metadata — web.dev](https://web.dev/articles/fetch-metadata)
- Reference: [MDN Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data)
