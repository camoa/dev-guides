---
description: HTML input type, inputmode, and enterkeyhint selection — give mobile users the correct on-screen keyboard and activate built-in browser validation without JavaScript.
tldr: Use type="text" + inputmode="numeric" for card numbers and ZIP codes — never type="number" which strips leading zeros and adds spinners. Set enterkeyhint on every field in multi-step forms. Pattern performs a full match; allow spaces and international characters users naturally type.
drupal_version: ""
---

# Input Types & Modes

## When to Use

> Choose `type`, `inputmode`, and `enterkeyhint` on every `<input>` to give mobile users the correct on-screen keyboard and to activate built-in browser validation — no JavaScript required for basic constraints.

## Decision

| Data | `type` | `inputmode` | Notes |
|------|--------|-------------|-------|
| Email address | `email` | — | Browser validates format; gives `@` keyboard on mobile |
| Phone number | `tel` | — | Gives numeric dialpad; no format enforcement |
| URL | `url` | — | Gives `.com` key on mobile |
| PIN / ZIP / numeric ID | `text` | `numeric` | No spinner controls, preserves leading zeros |
| Currency / decimal | `text` | `decimal` | Decimal keyboard without increment/decrement |
| Password | `password` | — | Browser autofill recognises this type |
| Search | `search` | `search` | Shows clear button |
| Card number | `text` | `numeric` | **Never `type="number"`** — strips leading zeros, adds spinner |
| Date | `date` | — | Native date picker |
| Free text | `text` | `text` | Default |

**Baseline status:** `inputmode` — Widely available (Baseline 2021).

| `enterkeyhint` value | Displays as | Use when |
|---|---|---|
| `next` | "Next" | Moving to next field in multi-step form |
| `done` | "Done" | Final input in the form |
| `search` | "Search" | Search input |
| `send` | "Send" | Message / email composition |
| `go` | "Go" | URLs, navigation targets |

## Pattern

```html
<!-- Correct: type="text" + inputmode for numeric data without spinner issues -->
<label for="zip">ZIP code</label>
<input type="text" id="zip" name="zip"
       autocomplete="postal-code"
       inputmode="numeric"
       pattern="\d{5}"
       enterkeyhint="next"
       maxlength="5"
       required>

<!-- Correct: card number as single text field -->
<label for="cc-number">Card number</label>
<input type="text" id="cc-number" name="cc-number"
       autocomplete="cc-number"
       inputmode="numeric"
       maxlength="19"
       pattern="[\d ]{13,19}"
       required>
```

**`pattern` rules:**
- Performs a **full match** (implied `^…$`).
- Allow spaces and formatting characters users naturally type (card numbers, phone numbers); strip server-side.
- Use Unicode letter classes (`[\p{L}…]`) for names — Latin-only patterns exclude international users.
- Place visible format hints **above** the input — autocomplete popovers obscure hints placed below.

## Common Mistakes

- **`type="number"` for card number or ZIP** → strips leading zeros, adds increment/decrement spinner, breaks paste
- **`type="number"` for phone number** → strips leading `+`, breaks international formats
- **Missing `enterkeyhint` on multi-step forms** → mobile users see generic "Return"
- **`pattern` with Latin-only character class for name fields** → rejects valid international names
- **Format hint placed below the input** → mobile keyboard or autocomplete popover obscures it

## See Also

- [Autocomplete & Autofill](autocomplete-and-autofill.md) — `autocomplete` token for every field listed here
- [Native Validation](native-validation.md) — using `pattern`, `required`, `minlength` with the Constraint Validation API
- Reference: MWG `forms.md` §3, `autofill-payment-form.md`
