---
description: HTML form structure and semantics — correct element choices, labeling rules, and button patterns that unlock native browser behaviour for autofill and validation.
tldr: Wrap all controls in <form>, use fieldset+legend for groups, always associate <label for> with <input id>. Never disable the submit button for validation — keyboard users cannot trigger invalid events. Use method="POST" for mutations. Labels above inputs, never placeholder-as-label.
drupal_version: ""
---

# Form Structure & Semantics

## When to Use

> Apply these structural rules to every form you build. Correct semantics unlock native browser behaviour — autofill, built-in validation, assistive technology compatibility — at no extra cost.

## Decision

| Need | Pattern | Why |
|------|---------|-----|
| Data collection | `<form>` wrapping all controls | Required for autofill, submit, screen reader context |
| Mutations / sensitive data | `method="POST"` | GET exposes data in browser history, server logs, referrer headers |
| Idempotent queries | `method="GET"` | Bookmarkable, shareable (search forms) |
| Related controls | `<fieldset>` + `<legend>` | Group semantics for AT; replaces generic `<div>` grouping |

**Selection control decision matrix:**

| Options count | Choice type | Use | Rationale |
|---|---|---|---|
| 1–5 | Single (exclusive) | `<input type="radio">` | All choices immediately visible |
| 6+ | Single (exclusive) | `<select>` | Space conservation |
| 10+ / dynamic | Single (exclusive) | `<input list="…">` (`<datalist>`) | Fuzzy search |
| Any count | Multi-select | `<input type="checkbox">` | Non-exclusive toggles |

## Pattern

```html
<form action="/subscribe" method="POST">
  <input type="hidden" name="csrf_token" value="{{ secure_token }}">

  <fieldset>
    <legend>Contact preference</legend>
    <label for="email">Email address</label>
    <input type="email" id="email" name="email"
           autocomplete="email" aria-describedby="email-hint" required>
    <span id="email-hint" class="hint">We'll send a confirmation.</span>
  </fieldset>

  <button type="submit">Subscribe</button>
</form>
```

**Labeling rules:**
- Always associate `<label for="…">` with `<input id="…">`. Never omit labels.
- Place labels **above** the input — faster scanning, works with zoom and mobile keyboards.
- The vertical gap between label and input must be **smaller** than the gap between form groups (Gestalt Proximity).
- Use `aria-describedby` to link help text or error containers.
- Use `aria-live="polite"` on error containers that are dynamically populated.
- Visually hide labels with `.visually-hidden` (`clip-path: inset(50%)`, not `display: none`).

**Button rules:**
- Use `<button type="submit">` for primary submission. Never a `<div>` or `<span>`.
- Use specific language: "Save address", "Pay $49.00" — not "Continue" or "Submit".
- **Do not disable the submit button** for validation — keyboard users cannot trigger native error display.
- **Disable after a valid submission click** to prevent double-posts.

## Common Mistakes

- **`<div>` for form controls** → no semantic role, no keyboard access, autofill blind
- **`placeholder` as label** → disappears on input, fails contrast requirements, breaks AT
- **`method="GET"` for password/payment** → credentials in URL, browser history, server logs
- **Disabling submit button for validation** → keyboard users cannot trigger `invalid` events
- **Splitting name into First/Last** → autofill mismatch, name truncation, international exclusion
- **Inline `onclick="…"` handlers** → violates CSP; use `addEventListener`

## See Also

- [Autocomplete & Autofill](autocomplete-and-autofill.md) — complete token vocabulary
- [Native Validation](native-validation.md) — Constraint Validation API and error UX
- Reference: MWG `forms.md` sections 1, 2, 5, 8
