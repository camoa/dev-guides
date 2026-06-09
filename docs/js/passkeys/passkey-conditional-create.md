---
description: Silent post-login passkey registration using mediation:conditional — boost passkey adoption without interrupting the user's post-login flow.
tldr: Trigger immediately after a complete password-based sign-in (not magic links or OTP). Abort any active autofill controller first. Pass mediation:'conditional' to suppress the blocking modal. Never render error UI for InvalidStateError or NotAllowedError in this flow.
drupal_version: ""
---

# Conditional Create (Silent Post-Login Registration)

## When to Use

> Use immediately after a verified, complete password-based sign-in to silently register a passkey in the background. Uses `mediation: 'conditional'` to suppress the modal passkey prompt and boost adoption without interrupting the post-login flow.

## Decision

| Precondition | Required |
|---|---|
| Full password-based sign-in completed | Yes |
| All MFA factors completed | Yes |
| Active authenticated session established | Yes |
| Magic link, SMS OTP, or federated sign-in | Do NOT trigger — this flow only for password sign-ins |

## Pattern

```js
import 'webauthn-polyfills';

async function silentRegisterPasskey(loginAbortController) {
  // Step 1: abort any active autofill controller
  loginAbortController.abort();

  // Step 2: feature-detect conditionalCreate
  const caps = await PublicKeyCredential.getClientCapabilities();
  if (caps.conditionalCreate !== true) return; // Not supported — exit silently

  const optionsJSON = await optionsFetch({ conditional: true });
  const publicKey = PublicKeyCredential.parseCreationOptionsFromJSON(optionsJSON);

  let credential;
  try {
    credential = await navigator.credentials.create({ publicKey, mediation: 'conditional' });
  } catch (e) {
    // Silently swallow — never render error UI for conditional flows
    if (['InvalidStateError', 'NotAllowedError', 'AbortError'].includes(e.name)) return;
    console.error('Unexpected conditional create error:', e);
    return;
  }

  // Segregated try/catch for server verification
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

**Server**: When verifying a conditional-create credential, pass `requireUserPresence: false` to your server-side library. Strict UP verification must remain active for explicit (non-conditional) registration flows.

## Common Mistakes

- **Triggering after magic link, OTP, or federated sign-in** → This flow upgrades password-based sign-ins only; other flows haven't verified a local credential
- **Not aborting the autofill controller first** → Browser blocks concurrent `credentials.create()` and `credentials.get()`; silent abort or `NotAllowedError` results
- **Omitting `mediation: 'conditional'`** → Browser shows a full blocking modal, interrupting the post-login flow
- **Rendering error UI on `InvalidStateError` or `NotAllowedError`** → These are expected silent outcomes; never surface them to the user
- **Not relaxing UP server-side for conditional requests** → Valid conditional credentials rejected at verification

## See Also

- [passkey-registration](passkey-registration.md) — explicit registration ceremony
- [passkey-authentication](passkey-authentication.md) — the `loginAbortController` aborted in Step 1 comes from the autofill flow there
- Reference: [MDN getClientCapabilities()](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/getClientCapabilities_static)
