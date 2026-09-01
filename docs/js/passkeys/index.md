---
description: Passkeys / WebAuthn — phishing-resistant passwordless authentication using native browser WebAuthn APIs covering registration, authentication, conditional create, management, and reauthentication.
tracks: []
guide-meta:
  concepts:
    - passkeys
    - WebAuthn
    - FIDO2
    - passwordless authentication
    - credentials.create
    - credentials.get
    - conditional UI
    - mediation conditional
    - signalAllAcceptedCredentials
    - signalUnknownCredential
    - AAGUID
    - authenticator
    - residentKey
    - discoverable credentials
  not:
    - Drupal user authentication
    - OAuth / OIDC flows
    - magic link authentication
    - JWT tokens
  requires:
    - development/security-practices
  complements:
    - js/forms
    - development/security-practices/authentication-best-practices
  category: js
---

# Passkeys / WebAuthn

Native browser WebAuthn APIs for phishing-resistant, passwordless authentication. No client-side wrapper libraries — server-side verification libraries are listed in the overview.

**Polyfill requirement:** Install [`webauthn-polyfills`](https://www.npmjs.com/package/webauthn-polyfills) in every project. The JSON helpers and `getClientCapabilities()` are Baseline Newly Available (2025); the polyfill backfills during the browser adoption window.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Verify HTTPS, RP ID, and server library before writing passkey code | [Passkeys Prerequisites & Overview](passkeys-overview.md) | Verify HTTPS context, consistent RP ID, and residentKey:required before writing passkey code. Use getClientCapabilities() to gate UI. Server-side: pick a vetted library (SimpleWebAuthn for JS/TS); never hand-roll WebAuthn crypto. |
| Register a new passkey from a button or settings panel | [Passkey Registration](passkey-registration.md) | Use residentKey:required for discoverable credentials. Segregate try/catch into two blocks — the inner wraps credentials.create() (abort on catch, never signal), the outer wraps the server fetch (signal signalUnknownCredential on rejection). Missing this split causes signalUnknownCredential to fire on user-cancel events. |
| Silently register a passkey right after a successful password login | [Conditional Create](passkey-conditional-create.md) | Trigger immediately after a complete password-based sign-in (not magic links or OTP). Abort any active autofill controller first. Pass mediation:'conditional' to suppress the blocking modal. Never render error UI for InvalidStateError or NotAllowedError in this flow. |
| Implement passkey sign-in (autofill suggestions or button) | [Passkey Authentication](passkey-authentication.md) | Run initConditionalAutofill() on DOMContentLoaded with mediation:'conditional'. Button flow must abort the autofill controller first, then re-arm autofill after exiting. Signal signalUnknownCredential only on HTTP 404 — not on any other server error. Store userVerification level server-side to prevent client manipulation. |
| Show users their saved passkeys and allow rename or delete | [Passkey Management](passkey-management.md) | Call signalAllAcceptedCredentials on page load and after every delete to keep password manager vaults in sync. All Signal API calls require Base64URL strings — never ArrayBuffer rawId. Gate every Signal API call with feature detection; Firefox does not support it. AAGUID is UX-only — never use it for access control. |
| Re-verify a signed-in user before a sensitive action | [Passkey Reauthentication](passkey-reauthentication.md) | Populate allowCredentials with the current user's credential IDs — never leave it empty for reauthentication or any user's passkey can satisfy the challenge on a shared device. After signature verification, explicitly assert the credential belongs to req.user.id. Button-only trigger — never autofill. |
