---
description: Passkey step-up reauthentication before sensitive operations — constraining allowCredentials to the current user and verifying ownership server-side.
tldr: Populate allowCredentials with the current user's credential IDs — never leave it empty for reauthentication or any user's passkey can satisfy the challenge on a shared device. After signature verification, explicitly assert the credential belongs to req.user.id. Button-only trigger — never autofill.
drupal_version: ""
---

# Passkey Reauthentication (Step-Up Verification)

## When to Use

> Use to re-verify the signed-in user's identity before a sensitive operation (password change, financial transaction, account deletion). Unlike sign-in, reauthentication constrains the passkey prompt to the current user's registered credentials.

## Decision

| Dimension | Sign-In (Authentication) | Reauthentication |
|---|---|---|
| `allowCredentials` | `[]` — discoverable, any user | Array of the current user's credential IDs |
| Session state | Not yet authenticated | Active authenticated session required |
| Trigger | Autofill or button | Button only — no autofill |
| Server ownership check | Not applicable | MUST verify returned credential belongs to `req.user.id` |

## Pattern

**Server — generate constrained options:**

```js
router.post('/api/reauth/options', enforceActiveSession, async (req, res) => {
  const userPasskeys = await db.findCredentialsByUserId(req.user.id);
  const options = {
    challenge: serverBase64UrlChallenge,
    rpId: 'example.com',
    allowCredentials: userPasskeys.map(cred => ({
      type: 'public-key',
      id: cred.id,
      transports: cred.transports,  // Speeds up authenticator resolution
    })),
  };
  req.session.reauthChallenge = serverBase64UrlChallenge;
  return res.json(options);
});

// After signature verification:
if (storedCredential.passkeyUserId !== req.user.id) {
  return res.status(403).json({ error: 'Credential does not belong to the active user.' });
}
```

**Client — button trigger only:**

```js
import 'webauthn-polyfills';
let reauthAbortController = new AbortController();

async function triggerReauth() {
  reauthAbortController.abort();
  reauthAbortController = new AbortController();

  const optionsJSON = await (await fetch('/api/reauth/options', { method: 'POST' })).json();
  const publicKey = PublicKeyCredential.parseRequestOptionsFromJSON(optionsJSON);

  try {
    const credential = await navigator.credentials.get({ publicKey, signal: reauthAbortController.signal });
    const encoded = credential.toJSON();
    const res = await fetch('/api/reauth/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(encoded),
    });
    if (res.ok) showTransactionSuccessUI();
    else if (res.status === 404 && PublicKeyCredential.signalUnknownCredential) {
      await PublicKeyCredential.signalUnknownCredential({ rpId: 'example.com', credentialId: encoded.id });
    }
  } catch (err) {
    if (err.name === 'NotAllowedError') { /* user cancelled — no UI */ }
  }
}

document.getElementById('reauth-btn').addEventListener('click', triggerReauth);
```

## Common Mistakes

- **`allowCredentials: []` in reauthentication** → Becomes a discoverable flow; on a shared device, any user's passkey satisfies the challenge, breaking session integrity
- **No server-side ownership check** → A valid passkey belonging to user B can satisfy a reauthentication for user A if the server only checks the signature
- **Attaching reauthentication to form autofill** → Reauthentication is always explicit and button-initiated; never surface passkey suggestions proactively
- **Full sign-out and re-sign-in instead of step-up** → Unnecessary session disruption; reauthentication is exactly the mechanism to avoid this

## See Also

- [passkey-management](passkey-management.md) — managing the credentials used in `allowCredentials`
- [passkeys-overview](passkeys-overview.md) — prerequisites and environment setup
- [authentication-best-practices](../../development/security-practices/authentication-best-practices.md) — sensitive-action patterns, session management, MFA step-up
- Reference: [MDN parseRequestOptionsFromJSON()](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential/parseRequestOptionsFromJSON_static)
