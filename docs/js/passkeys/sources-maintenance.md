---
description: "Source references and maintenance manifest for the passkeys guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: N/A — this guide covers browser WebAuthn APIs and is not Drupal-specific.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| MWG: Passkeys Orientation | `/tmp/mwg/passkeys/passkeys.md` (local MWG source) | passkeys-overview | 2026-06-09 |
| MWG: Passkey Registration | `/tmp/mwg/passkeys/passkey-registration.md` (local MWG source) | passkey-registration | 2026-06-09 |
| MWG: Passkey Conditional Create | `/tmp/mwg/passkeys/passkey-conditional-create.md` (local MWG source) | passkey-conditional-create | 2026-06-09 |
| MWG: Passkey Authentication | `/tmp/mwg/passkeys/passkey-authentication.md` (local MWG source) | passkey-authentication | 2026-06-09 |
| MWG: Passkey Management | `/tmp/mwg/passkeys/passkey-management.md` (local MWG source) | passkey-management | 2026-06-09 |
| MWG: Passkey Reauthentication | `/tmp/mwg/passkeys/passkey-reauthentication.md` (local MWG source) | passkey-reauthentication | 2026-06-09 |
| MDN: Web Authentication API | https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API | passkeys-overview, passkey-registration, passkey-authentication | 2026-06-09 |
| MDN: PublicKeyCredential.getClientCapabilities() | https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/getClientCapabilities_static | passkeys-overview, passkey-registration, passkey-conditional-create, passkey-authentication | 2026-06-09 |
| MDN: parseCreationOptionsFromJSON() | https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/parseCreationOptionsFromJSON_static | passkey-registration, passkey-conditional-create | 2026-06-09 |
| MDN: parseRequestOptionsFromJSON() | https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/parseRequestOptionsFromJSON_static | passkey-authentication, passkey-reauthentication | 2026-06-09 |
| W3C WebAuthn Level 3 Spec | https://www.w3.org/TR/webauthn-3/ | passkeys-overview | 2026-06-09 |
| passkey-authenticator-aaguids Registry | https://github.com/passkeydeveloper/passkey-authenticator-aaguids | passkey-management | 2026-06-09 |
| webauthn-polyfills (npm) | https://www.npmjs.com/package/webauthn-polyfills | All sections (polyfill) | 2026-06-09 |
| SimpleWebAuthn (server library) | https://simplewebauthn.dev/ | passkeys-overview | 2026-06-09 |
| OWASP Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | passkeys-overview, passkey-reauthentication | 2026-06-09 |

## Code Sources

| Module | Relative Path | Guide Sections | Notes |
|--------|---------------|----------------|-------|
| N/A — browser JS APIs only | — | — | No server module code; all client patterns use `navigator.credentials` and `PublicKeyCredential` browser globals |
