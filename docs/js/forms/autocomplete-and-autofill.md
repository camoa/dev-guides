---
description: HTML autocomplete token vocabulary for identity, address, payment, and authentication fields — enabling browser and password manager autofill on every form.
tldr: Add autocomplete to every input, select, and textarea. Autofill requires a stable name/id, a <form> wrapper, a submit button, and a recognised token. Use autocomplete="username" on sign-in email inputs so password managers link them to stored credentials. Never use autocomplete="off" on password fields.
drupal_version: ""
---

# Autocomplete & Autofill

## When to Use

> Add `autocomplete` to every `<input>`, `<select>`, and `<textarea>` in every form. Browser autofill is the single highest-impact improvement to form completion rates — users abandon forms that require retyping data they've entered before.

## Decision

**Prerequisites for autofill to work:**
1. The input has a stable `name` or `id` — not randomly generated on each page load
2. The input is inside a `<form>` element
3. The form has a `<button type="submit">` or `<input type="submit">`
4. The `autocomplete` attribute is present and uses a recognised token

**Identity tokens:**

| Token | Field | Notes |
|-------|-------|-------|
| `name` | Full name (single field) | Use a single name input for global audiences |
| `email` | Email address | Use `type="email"` |
| `tel` | Phone number | Single input (never split) |
| `username` | Email used as login ID | Use on email inputs in sign-in/sign-up — password managers recognise this regardless of `type` |

**Address tokens:**

| Token | Field | Notes |
|-------|-------|-------|
| `street-address` | Full address as one block | Use `<textarea>` for international compatibility |
| `address-level2` | City | |
| `address-level1` | State / province | |
| `postal-code` | ZIP / postal code | Use `inputmode="numeric"` not `type="number"` |
| `country` | Country code | |

Prefix with `shipping` or `billing` for multi-address forms: `autocomplete="shipping address-line1"`.

**Payment tokens:**

| Token | Field | Notes |
|-------|-------|-------|
| `cc-number` | Card number | Single input; `inputmode="numeric"` |
| `cc-name` | Name on card | Allow Unicode pattern |
| `cc-exp` | Expiry (MM/YY) | Place format hint **above** the input |
| `cc-csc` | Security code | `inputmode="numeric"`; not `type="password"` |

**Authentication tokens:**

| Token | Field | Notes |
|-------|-------|-------|
| `username` | Email used as login | Password managers recognise even with `type="email"` |
| `current-password` | Existing password (sign-in) | Signals browser to autofill stored password |
| `new-password` | New password (sign-up/reset) | Signals browser to offer a generated strong password |

## Pattern

**Sign-up form:**

```html
<form method="post" action="/register">
  <input type="hidden" name="csrf_token" value="{{ token }}">
  <label for="name">Full name</label>
  <input id="name" name="name" type="text" autocomplete="name"
         pattern="[\p{L}\.\- ]+" required>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" autocomplete="username" required>
  <label for="new-password">Password</label>
  <input id="new-password" name="new-password" type="password"
         autocomplete="new-password" minlength="8" required>
  <button type="submit">Create account</button>
</form>
```

**Sign-in form:**

```html
<form method="post" action="/login">
  <input type="hidden" name="csrf_token" value="{{ token }}">
  <label for="email">Email</label>
  <input id="email" name="email" type="email"
         autocomplete="username" required enterkeyhint="next">
  <label for="password">Password</label>
  <input id="password" name="password" type="password"
         autocomplete="current-password" required enterkeyhint="done">
  <button type="submit">Sign in</button>
</form>
```

**Address form** — use `<textarea>` for street address; handles multi-line international formats that split inputs cannot.

**Payment form** — use a **single input** for card numbers; splitting into groups breaks autofill entirely.

## Common Mistakes

- **Missing `autocomplete` on any field** → browser cannot autofill; abandonment rate increases
- **`autocomplete="off"` on a password field** → prevents password managers from saving; security regression
- **`autocomplete="email"` on sign-in email** → wrong; use `"username"` so password managers link it to stored credentials
- **`autocomplete="new-password"` on a sign-in form** → browser suggests a new password on top of an existing credential
- **Split first/last name inputs** → autofill must guess token mapping; frequently fails
- **Split card number into groups** → autofill cannot fill a single card number across multiple inputs
- **Blocking password paste** → reduces security; violates NCSC guidance

## See Also

- [Input Types & Modes](input-types-and-modes.md) — `type` and `inputmode` for every field
- [Autofill Visual Feedback](autofill-visual-feedback.md) — styling autofilled fields with `:autofill`
- Reference: MWG `autofill-address-form.md`, `autofill-payment-form.md`, `autofill-sign-in-form.md`, `autofill-sign-up-form.md`
