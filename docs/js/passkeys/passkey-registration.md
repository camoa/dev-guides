---
description: Passkey registration ceremony — database schema, server options, client credential creation, and the segregated try/catch pattern for signal API safety.
tldr: Use residentKey:required for discoverable credentials. Segregate try/catch into two blocks — the inner wraps credentials.create() (abort on catch, never signal), the outer wraps the server fetch (signal signalUnknownCredential on rejection). Missing this split causes signalUnknownCredential to fire on user-cancel events.
drupal_version: ""
---

# Passkey Registration

## When to Use

> Use when adding a passkey creation flow — either as an explicit "Create passkey" button in account settings (management flow, allows security keys) or as a promotion shown after a successful password sign-in (promotion flow, platform authenticators only). A single server endpoint can handle both via a `promotion` flag.

## Decision

| Context | `authenticatorAttachment` | Security keys allowed? |
|---|---|---|
| Promotion after password sign-in | `"platform"` | No — platform authenticator only |
| Account settings / security panel | Omit entirely | Yes |

## Pattern

```typescript
interface StoredPasskeyCredential {
  id: string;                                    // Base64URL credential ID (primary key)
  passkeyUserId: string;                         // App user ID
  credentialPublicKey: string;                   // Base64URL public key for verification
  credentialDeviceType: 'singleDevice' | 'multiDevice';
  credentialBackedUp: boolean;
  aaguid: string;                                // Provider identifier — UX display only
  transports: string[];                          // Required for excludeCredentials
  counter: number;                               // Replay-attack prevention
  registeredAt: number;                          // Unix epoch
}
```

```js
import 'webauthn-polyfills';

async function registerPasskey(isPromotion = false) {
  const caps = await PublicKeyCredential.getClientCapabilities();
  if (!caps.passkeyPlatformAuthenticator || !caps.conditionalGet) return;

  const publicKey = PublicKeyCredential.parseCreationOptionsFromJSON(
    await optionsFetch({ promotion: isPromotion })
  );

  let credential;
  try {
    // Inner block — ONLY wraps credentials.create()
    credential = await navigator.credentials.create({ publicKey });
  } catch (err) {
    if (err.name === 'InvalidStateError') alert('Passkey already exists.');
    // NotAllowedError / AbortError = user cancelled — no UI needed
    return; // Do NOT call signalUnknownCredential here — no credential was persisted
  }

  // Outer block — wraps server verification
  const encoded = credential.toJSON();
  try {
    const res = await registerVerifyFetch(encoded);
    if (!res.ok && PublicKeyCredential.signalUnknownCredential) {
      await PublicKeyCredential.signalUnknownCredential({ rpId: 'example.com', credentialId: encoded.id });
    }
  } catch {
    if (PublicKeyCredential.signalUnknownCredential) {
      await PublicKeyCredential.signalUnknownCredential({ rpId: 'example.com', credentialId: encoded.id });
    }
  }
}
```

**Server options** must set `residentKey: "required"`, `requireResidentKey: true`, and populate `excludeCredentials` from existing credentials. Use `authenticatorAttachment: "platform"` only for promotion flows.

## Common Mistakes

- **Not segregating try/catch** → Catching server errors in the WebAuthn catch block fires `signalUnknownCredential` on user-cancel events, signalling credentials that were never created
- **`signalUnknownCredential` from the WebAuthn catch** → No credential exists server-side; only call signal after a server-side rejection of a successfully-created credential
- **`excludeCredentials` omitted** → Allows registering duplicate passkeys; `InvalidStateError` never fires without it
- **`residentKey: "required"` omitted** → Credential is not discoverable; will not appear in autofill
- **`userVerification: "preferred"` without `requireUserVerification: false` server-side** → Authenticators without screen locks trigger spurious 400 errors
- **`authenticatorAttachment: "platform"` in a security-panel flow** → Blocks external FIDO2 security keys

## See Also

- [passkeys-overview](passkeys-overview.md) — prerequisites
- [passkey-conditional-create](passkey-conditional-create.md) — silent post-login registration
- [passkey-management](passkey-management.md) — AAGUID registry lookup for provider name/icon
- Reference: [MDN parseCreationOptionsFromJSON()](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/parseCreationOptionsFromJSON_static)
