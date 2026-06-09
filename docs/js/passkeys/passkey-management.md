---
description: Passkey management UI — listing, renaming, deleting credentials with Signal API synchronization and AAGUID provider registry lookup.
tldr: Call signalAllAcceptedCredentials on page load and after every delete to keep password manager vaults in sync. All Signal API calls require Base64URL strings — never ArrayBuffer rawId. Gate every Signal API call with feature detection; Firefox does not support it. AAGUID is UX-only — never use it for access control.
drupal_version: ""
---

# Passkey Management

## When to Use

> Use to build a credentials panel in account settings where users can view, rename, and delete their registered passkeys. The Signal API methods keep password manager vaults synchronized with your server's credential state after every change.

## Decision

| Signal API method | When to call |
|---|---|
| `signalAllAcceptedCredentials` | On page load and after every delete |
| `signalCurrentUserDetails` | After username or display name update |
| `signalUnknownCredential` | When server rejects a credential (HTTP 404 or verification failure) |

**Browser support:** Chrome 132+, Edge 132+, Safari 26+ (Sep 2025). Not supported in Firefox. Always feature-detect.

## Pattern

**Credential row must render:** provider icon, provider/custom name, registration date, last used date, rename button, delete button.

**Signal API synchronization:**

```js
async function syncAcceptedCredentials(credentialsList) {
  if (!PublicKeyCredential.signalAllAcceptedCredentials) return;
  await PublicKeyCredential.signalAllAcceptedCredentials({
    rpId: 'example.com',
    userId: base64UrlUserId,          // Base64URL string — NOT ArrayBuffer
    allAcceptedCredentialIds: credentialsList.map(c => c.id),
  });
}

// Sync on page load
window.addEventListener('DOMContentLoaded', async () => {
  const list = await (await listFetch()).json();
  renderUI(list);
  await syncAcceptedCredentials(list);
});

// Sync after deletion
async function performDelete(credentialId) {
  const res = await deleteFetch(credentialId);
  if (res.ok) {
    const updatedList = await (await listFetch()).json();
    renderUI(updatedList);
    await syncAcceptedCredentials(updatedList);
  }
}
```

**AAGUID registry lookup:**

```js
// Registry: https://raw.githubusercontent.com/passkeydeveloper/passkey-authenticator-aaguids/refs/heads/main/combined_aaguid.json
// Vendor locally or fetch at build time — do not fetch at runtime from raw GitHub

import aaguids from './aaguids.json' with { type: 'json' };

function resolveProvider(aaguid) {
  if (aaguid === '00000000-0000-0000-0000-000000000000') {
    return { name: 'Unknown passkey provider', icon: undefined };
  }
  const provider = aaguids[aaguid];
  return { name: provider?.name ?? 'Unknown passkey provider', icon: provider?.icon_light };
}
```

**Server — IDOR prevention on rename/delete:**

```js
router.delete('/api/credential/:id', checkAuth, async (req, res) => {
  const cred = await db.findCredentialById(req.params.id);
  if (!cred || cred.passkeyUserId !== req.user.id) {
    return res.status(404).json({ error: 'Credential not found.' });
  }
  await db.deleteCredential(req.params.id);
  res.json({ success: true });
});
```

## Common Mistakes

- **Passing raw ArrayBuffer IDs to Signal API** → All credential IDs and user IDs must be Base64URL strings; `rawId` (ArrayBuffer) throws `TypeError`
- **Not calling `signalAllAcceptedCredentials` on page load** → Password managers learn about deletions only when a sync fires; stale passkeys appear after server-side removal
- **Signal API calls without feature detection** → Throws `TypeError` in Firefox; always guard with `if (PublicKeyCredential.signalXxx)`
- **Looking up the zero AAGUID in the registry** → Always returns undefined; check for all-zeros before lookup and use a fallback string
- **No ownership check on rename/delete** → IDOR vulnerability; any authenticated user could mutate another user's credentials
- **Using AAGUID for access control or security decisions** → AAGUID is UX-only; not cryptographically verified for platform passkeys

## See Also

- [passkey-registration](passkey-registration.md) — `aaguid` and `transports` fields set at registration time
- [passkey-reauthentication](passkey-reauthentication.md) — step-up verification before sensitive actions
- [authentication-best-practices](../../development/security-practices/authentication-best-practices.md) — session security and access control
- Reference: [passkey-authenticator-aaguids registry](https://github.com/passkeydeveloper/passkey-authenticator-aaguids)
