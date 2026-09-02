---
description: "Browser security policy deployment — CSP enforcement workflow (report-only to enforce), Trusted Types for DOM-sink XSS, cross-origin isolation (COOP+COEP), Fetch Metadata resource isolation, and Clear-Site-Data on logout."
tldr: "Deploy CSP through three phases — report-only discovery (days to weeks, not hours), analyze violations filtering extension noise, then enforce only when violations have dropped to near zero. Trusted Types blocks DOM-sink XSS at runtime but requires framework/widget support audit before enforcement — third-party widgets that write raw strings to innerHTML will throw. COEP requires every embedded subresource to serve Cross-Origin-Resource-Policy or the browser blocks it."
drupal_version: ""
---

# Browser Security Policies

## When to Use

> Apply these policies when hardening an existing web application incrementally against client-side attacks. Section 12.0 covers which security headers to set and their recommended values; this section covers the deployment workflow for safely enforcing CSP, protecting DOM sinks with Trusted Types, enabling cross-origin isolation via COOP + COEP, verifying request origin with Fetch Metadata, and wiping browser state at logout.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Roll out CSP without breaking the app | Report-Only → Analyze → Enforce workflow | Strict CSP applied blindly breaks inline scripts silently for users |
| Block DOM-sink XSS at runtime | Trusted Types (`require-trusted-types-for 'script'`) | Enforces safe DOM writes even when XSS payloads bypass other defenses |
| Enable SharedArrayBuffer or WebAssembly multi-threading | Cross-origin isolation (COOP + COEP) | Browsers require `crossOriginIsolated = true` for these APIs |
| Reject suspicious cross-site subresource requests server-side | Fetch Metadata resource-isolation policy | `Sec-Fetch-*` headers cannot be forged by cross-site scripts |
| Wipe all browser state on logout | `Clear-Site-Data` response header | Clears cookies, localStorage, sessionStorage, and cache in one response |

## CSP Enforcement Workflow

**Phase 1 — Report-Only (discovery).** Wire up a reporting endpoint and ship the report-only header. Set server-side on every response. Run for days to weeks — long enough to cover real traffic patterns, not just synthetic testing.

```http
Reporting-Endpoints: csp-endpoint="https://reports.example/csp"
Content-Security-Policy-Report-Only: script-src 'nonce-{RANDOM}' 'strict-dynamic' 'report-sample'; object-src 'none'; base-uri 'none'; report-to csp-endpoint;
```

The `'report-sample'` token includes the first 40 characters of violating code in each report, making triage far easier. The `'strict-dynamic'`, `https:`, and `'unsafe-inline'` tokens form a backwards-compatibility ladder: modern browsers honor `'strict-dynamic'` (nonce-propagating) and ignore the others; older browsers fall back to `https:` then `'unsafe-inline'`.

**Phase 2 — Analyze reports.** Filter noise (browser extensions, antivirus, crawlers) from real violations. Ignore low-volume reports — they are typically false positives. Focus on high-frequency patterns from modern user-agents:

| Violation pattern | Action |
|---|---|
| Many inline-script violations | Add server-rendered nonces to `<script>` tags; use hashes for static/cached HTML (SPAs) |
| Third-party analytics violations | Use `'strict-dynamic'` with a nonce so the loader propagates trust to its children. Never add the analytics domain to a URL allowlist — open redirects on that domain bypass the entire policy |
| Trusted Types violations on specific sinks | Refactor those sinks (see Trusted Types below) before enforcing |

**Phase 3 — Enforce.** Switch from `Content-Security-Policy-Report-Only` to `Content-Security-Policy` only when violations have dropped to near zero. Keep `report-to` on the enforced header so regressions remain visible.

```http
Reporting-Endpoints: csp-endpoint="https://reports.example/csp"
Content-Security-Policy: script-src 'nonce-{RANDOM}' 'strict-dynamic' 'report-sample'; object-src 'none'; base-uri 'none'; report-to csp-endpoint;
```

**Key directives to prioritize:** `script-src` with nonces or hashes is the core XSS defense. `base-uri 'none'` blocks `<base>` tag hijacking. `form-action 'self'` prevents form submissions to attacker-controlled origins. Avoid `default-src 'self'` as a broad catch-all — it complicates deployment with little security value beyond a strict `script-src`.

## Trusted Types

Trusted Types enforces safe DOM writes at runtime. The browser blocks string assignments to dangerous sinks — `.innerHTML`, `document.write`, `.outerHTML`, `eval` — unless the value passes through a named Trusted Types policy object. This protects against DOM-sink XSS even when other defenses have been bypassed.

**Incremental rollout — do not enforce globally on day one:**

1. Find every offending sink via report-only: `Content-Security-Policy-Report-Only: require-trusted-types-for 'script'`
2. Refactor sinks to use safe DOM APIs (`textContent`, `createElement`) — see section 5.0 for patterns
3. For unavoidable sinks, route through a named policy:

```javascript
if (window.trustedTypes && trustedTypes.createPolicy) {
  const policy = trustedTypes.createPolicy('default', {
    createHTML: (input) => DOMPurify.sanitize(input)
  });
  el.innerHTML = policy.createHTML(untrustedContent); // DOMPurify output is now trusted
}
```

4. Move to global enforcement once violations in report-only logs drop to zero: `Content-Security-Policy: require-trusted-types-for 'script'`

**Prerequisite check:** Frameworks and third-party widgets must produce `TrustedHTML` / `TrustedScript` values — not raw strings — before enforcement is safe. If a widget writes strings directly to DOM sinks and does not support Trusted Types, it will throw on assignment. Audit all framework and widget support before enforcing.

## Cross-Origin Isolation

**Only needed when** the application requires `SharedArrayBuffer`, WebAssembly multi-threading, or high-precision `performance.now()` timers. Setting this policy group causes `window.crossOriginIsolated` to return `true`, re-enabling these APIs that browsers restrict by default to mitigate Spectre-class attacks.

**Cross-browser path.** Requires both COOP and COEP together — set server-side:

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

Every embedded subresource — images, fonts, external scripts, media — must also serve `Cross-Origin-Resource-Policy: cross-origin` (or `same-site` for same-eTLD+1 resources), or the browser blocks it from loading. Audit all subresources before enforcing.

**Chromium-only lower-risk alternative (Chrome 142+):**

```http
Document-Isolation-Policy: isolate-and-credentialless
```

This achieves equivalent client-side isolation by stripping credentials from non-CORS cross-origin requests rather than blocking them outright. Evaluate based on target audience — other browsers have not implemented this.

**Before deploying:** Use `Cross-Origin-Opener-Policy-Report-Only` and `Cross-Origin-Embedder-Policy-Report-Only` to discover breakage. Identify OAuth popups and payment gateway flows that rely on cross-origin `window.opener` access — `COOP: same-origin` severs those references.

## Fetch Metadata Resource-Isolation Policy

`Sec-Fetch-Site`, `Sec-Fetch-Mode`, and `Sec-Fetch-Dest` are request headers automatically attached by the browser. They cannot be forged by cross-site scripts. A server-side middleware can use them to reject suspicious cross-origin requests **before** authentication and authorization checks — avoiding timing side-channels that reveal whether a resource or session exists.

```javascript
// Server-side middleware (Express example — adapt to any backend)
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

Prevent intermediate CDNs from caching a policy-blocked response and serving it to legitimate same-origin users:

```http
Vary: Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site
```

**Two cautions before enforcing:** `same-site` trusts all subdomains under your eTLD+1 — if any subdomain hosts user-generated content, accept only `same-origin`. Map all cross-site integrations first (webhooks, SSO handlers, external API callers from different origins) — they will be blocked as `cross-site` unless you add explicit allow rules.

## Clear-Site-Data on Logout

Return this header on the server's logout endpoint response to instruct the browser to wipe all local state in one shot:

```http
Clear-Site-Data: "cookies", "storage", "cache"
```

This is a **server-side response header**, not a JavaScript API. It clears cookies, `localStorage`, `sessionStorage`, and the HTTP cache, closing the session even if client-side cookie deletion fails. All modern browsers support it.

## Common Mistakes

- **Deploying enforced CSP without report-only first** — Strict policies silently break inline scripts for real users. Run report-only long enough to cover actual traffic patterns (days to weeks, not hours)
- **URL allowlists in CSP** — `script-src https://cdn.example.com` is bypassed via open redirects or JSONP endpoints on the allowlisted domain. Use nonces or hashes instead
- **Trusted Types without framework and widget support audit** — Third-party widgets that write raw strings to DOM sinks will throw at assignment time. Audit all dependencies before enforcing
- **COEP without CORP on every embedded subresource** — A single third-party image lacking `Cross-Origin-Resource-Policy` will be blocked, breaking the page. Audit all subresources before enabling COEP
- **Missing `Vary` header on Fetch Metadata-protected endpoints** — CDNs may cache a 403 and serve it to legitimate users, or cache a 200 and serve it to cross-site attackers
- **Only deleting the session cookie on logout** — `localStorage`, `sessionStorage`, and cached responses persist. `Clear-Site-Data` closes all state at once

## See Also

- Previous: [Security Headers](security-headers.md) | Next: [API Security](api-security.md)
- See also: [XSS Prevention Patterns](xss-prevention-patterns.md) — CSP basics, nonce generation, DOMPurify sanitization
- See also: [Cross-Site Scripting (XSS)](cross-site-scripting-xss.md) — safe DOM APIs (textContent vs innerHTML)
- Reference: [W3C Trusted Types specification](https://w3c.github.io/trusted-types/dist/spec/)
- Reference: [MDN Cross-Origin-Embedder-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)
- Reference: [Fetch Metadata request headers — web.dev](https://web.dev/articles/fetch-metadata)
- Reference: [MDN Clear-Site-Data](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Clear-Site-Data)
