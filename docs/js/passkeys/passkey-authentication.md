---
description: Passkey sign-in flows — conditional autofill (mediation:conditional on page load) and explicit button trigger, with abort controller lifecycle management.
tldr: Run initConditionalAutofill() on DOMContentLoaded with mediation:'conditional'. Button flow must abort the autofill controller first, then re-arm autofill after exiting. Signal signalUnknownCredential only on HTTP 404 — not on any other server error. Store userVerification level server-side to prevent client manipulation.
drupal_version: ""
---

# Passkey Authentication

## When to Use

> Use to authenticate returning users with a stored passkey. The conditional autofill flow surfaces passkey suggestions in the username field without extra UI. The button flow provides an explicit trigger for users who know they have passkeys registered.

## Decision

| If the user... | Use | Mechanism |
|---|---|---|
| Focuses the username field on sign-in | Conditional autofill flow | `mediation: 'conditional'` on page load, `autocomplete="username webauthn"` on input |
| Clicks "Sign in with passkey" button | Button trigger flow | Abort autofill controller, invoke `credentials.get()` without mediation |
| Is on a page without a sign-in form | Button trigger flow | Same — explicit trigger only |

## Pattern

**HTML annotation** — `autocomplete="username webauthn"` activates passkey autofill suggestions:

```html
<input type="text" name="username"
       autocomplete="username webauthn"
       autofocus />
```

**Conditional autofill flow:**

```js
import 'webauthn-polyfills';
let autofillAbortController = new AbortController();

async function initConditionalAutofill() {
  const caps = await PublicKeyCredential.getClientCapabilities();
  if (!caps.conditionalGet) return;

  const publicKey = PublicKeyCredential.parseRequestOptionsFromJSON(await optionsFetch());
  try {
    const credential = await navigator.credentials.get({
      publicKey,
      mediation: 'conditional',
      signal: autofillAbortController.signal,
    });
    const encoded = credential.toJSON();
    const res = await loginVerifyFetch(encoded);
    if (!res.ok && res.status === 404 && PublicKeyCredential.signalUnknownCredential) {
      await PublicKeyCredential.signalUnknownCredential({ rpId: 'example.com', credentialId: encoded.id });
    }
  } catch (err) {
    if (['NotAllowedError', 'AbortError'].includes(err.name)) return;
  }
}

window.addEventListener('DOMContentLoaded', initConditionalAutofill);
```

**Button flow** — abort autofill first, then re-arm after exit:

```js
async function triggerButtonAuth() {
  autofillAbortController.abort();
  autofillAbortController = new AbortController();

  const publicKey = PublicKeyCredential.parseRequestOptionsFromJSON(await optionsFetch());
  let credential;
  try {
    credential = await navigator.credentials.get({ publicKey, signal: autofillAbortController.signal });
  } catch (err) {
    if (err.name === 'NotAllowedError') { /* user cancelled — no UI */ }
    initConditionalAutofill(); // Re-arm autofill after button flow exits
    return;
  }

  const encoded = credential.toJSON();
  try {
    const res = await loginVerifyFetch(encoded);
    if (!res.ok && res.status === 404 && PublicKeyCredential.signalUnknownCredential) {
      await PublicKeyCredential.signalUnknownCredential({ rpId: 'example.com', credentialId: encoded.id });
    }
  } catch (err) { console.error('Verification error:', err); }
}
```

**Server options**: `allowCredentials: []` requests discoverable credentials. Store `userVerification` level in the session — never return it to the client. Return HTTP `404` when a credential ID is not found — the client uses this to trigger `signalUnknownCredential`.

## Common Mistakes

- **Not aborting autofill before the button trigger** → Two concurrent `credentials.get()` calls collide; both can silently fail
- **Passing `credential.rawId` (ArrayBuffer) to `signalUnknownCredential`** → Must pass `encoded.id`, the Base64URL string from `credential.toJSON().id`
- **Calling `signalUnknownCredential` on any server error** → Only call on HTTP `404`; other codes indicate server bugs, not orphaned credentials
- **Missing `autocomplete="username webauthn"` on the input** → Autofill suggestions never appear even with `mediation: 'conditional'` active
- **Not re-arming autofill after button flow exits** → Autofill suggestions are gone until the next page load if user cancels
- **`userVerification` level in the client response** → Allows a client to downgrade UV requirements

## See Also

- [passkey-conditional-create](passkey-conditional-create.md) — the `autofillAbortController` created here is the `loginAbortController` aborted there
- [passkey-management](passkey-management.md) — Signal API synchronization
- Reference: [MDN parseRequestOptionsFromJSON()](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/parseRequestOptionsFromJSON_static)
