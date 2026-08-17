---
description: Passkeys prerequisites and environment checklist before writing any WebAuthn code — HTTPS requirements, RP ID rules, discoverable credential settings, and server library selection.
tldr: "Verify HTTPS context, consistent RP ID, and residentKey:required before writing passkey code. Use getClientCapabilities() to gate UI. Server-side: pick a vetted library (SimpleWebAuthn for JS/TS); never hand-roll WebAuthn crypto."
drupal_version: ""
---

# Passkeys Prerequisites & Overview

## When to Use

> Read this section before writing any passkey code to verify your environment satisfies WebAuthn requirements, select the correct server-side verification library, and identify which implementation flow maps to each use case.

## Decision

| Requirement | Rule | Failure if violated |
|---|---|---|
| Secure Context | Production MUST run on `https://`. `http://localhost` is the only exception | `SecurityError` on `credentials.create()` / `credentials.get()` |
| RP ID binding | `rpId` must equal the domain or a registrable suffix of the current origin | `SecurityError`; credentials become permanently unresolvable |
| Discoverable credentials | Registration MUST set both `residentKey: "required"` and `requireResidentKey: true` | Passkeys will not appear in autofill or username-less sign-in |
| Challenge entropy | Generate a cryptographically random challenge server-side per request | Replay attacks; signature verification must fail without verified challenge |

| Goal | Use |
|---|---|
| User explicitly creates a passkey (settings panel, post-signup) | [passkey-registration](passkey-registration.md) |
| Silent passkey creation after password sign-in | [passkey-conditional-create](passkey-conditional-create.md) |
| Returning user authenticates (autofill or button) | [passkey-authentication](passkey-authentication.md) |
| User views, renames, or deletes their passkeys | [passkey-management](passkey-management.md) |
| Step-up re-verification before a sensitive action | [passkey-reauthentication](passkey-reauthentication.md) |

## Pattern

```js
import 'webauthn-polyfills';

// Gate all passkey UI on capability detection at page load
const caps = await PublicKeyCredential.getClientCapabilities();
if (!caps.passkeyPlatformAuthenticator || !caps.conditionalGet) {
  showPasswordFallbackUI();
}
```

`getClientCapabilities()` — Baseline since 2025-02-06 (Chrome 133, Edge 133, Firefox 135, Safari 17.4). The polyfill handles older versions.

## Server Library Matrix

| Language | Library |
|---|---|
| JavaScript / TypeScript | SimpleWebAuthn — github.com/MasterKale/SimpleWebAuthn |
| Python | py_webauthn — github.com/duo-labs/py_webauthn |
| Java | java-webauthn-server (Yubico) |
| .NET | fido2-net-lib |
| Go | go-webauthn |
| Ruby | webauthn-ruby |
| PHP | webauthn-framework — github.com/web-auth/webauthn-framework |

These libraries apply server-side only. On the client, always call native browser APIs directly.

## Common Mistakes

- **`http://` in production** → `SecurityError`; HTTPS is mandatory. `localhost` exception is development-only
- **Inconsistent RP ID** → Define `rpId` as a single constant shared across endpoints; any mismatch orphans credentials permanently
- **Client-side WebAuthn wrapper libraries** → Wrappers abstract away `mediation`, `AbortController`, and error handling. Use native APIs; use the server library only server-side
- **Skipping `getClientCapabilities()` before rendering passkey UI** → Passkey buttons appear on browsers that cannot use them

## See Also

- [passkey-registration](passkey-registration.md) — credential creation ceremony
- [passkey-authentication](passkey-authentication.md) — sign-in flows
- [authentication-best-practices](../../development/security-practices/authentication-best-practices.md) — passwords, MFA, session management
- Reference: [MDN Web Authentication API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API)
- Reference: [W3C WebAuthn Level 3 Spec](https://www.w3.org/TR/webauthn-3/)
- Reference: [webauthn-polyfills (npm)](https://www.npmjs.com/package/webauthn-polyfills)
