---
description: Browser Constraint Validation API with :user-invalid/:user-valid — interaction-gated error display that never shows errors on page load, with aria-invalid sync for screen readers.
tldr: Use :user-invalid (not :invalid) so errors appear only after the user has interacted with a field. Bridge to AT with aria-invalid="true" via JS on blur and submit — :user-invalid is CSS-only and invisible to screen readers. Clear setCustomValidity() on the input event or the custom message sticks after correction.
drupal_version: ""
---

# Native Validation

## When to Use

> Use the browser Constraint Validation API with `:user-invalid` / `:user-valid` to provide interaction-gated validation feedback — errors appear only after the user has visited and left a field, not on page load.

## Decision

| Need | API / Pattern | Notes |
|------|---------------|-------|
| Hide errors until user exits a field | `:user-invalid` CSS pseudo-class | Baseline 2023; widely available |
| Show success after correct input | `:user-valid` CSS pseudo-class | Same timing as `:user-invalid` |
| Override browser error bubble text | `setCustomValidity()` + clear on `input` | Empty string clears the custom message |
| Sync visual state with screen readers | `aria-invalid="true"` via JS | `:user-invalid` is CSS-only; AT needs explicit attribute |
| Check validity in JS | `input.checkValidity()` | Returns boolean; populates `ValidityState` |
| Complex async validation | `setCustomValidity()` after fetch | e.g., username availability check |

**Baseline status for `:user-valid` / `:user-invalid`: Widely available** (Baseline 2023-11-02). Chrome 119+, Edge 119+, Firefox 88+, Safari 16.5+.

## Pattern

```html
<label for="email">Email address</label>
<input type="email" id="email" name="email" required
       autocomplete="email"
       aria-describedby="email-hint"
       aria-errormessage="email-error">
<div id="email-error" class="error-msg">Please enter a valid email address.</div>
```

```css
.error-msg { display: none; }
input:user-invalid { border-color: #d93025; background-color: #fce8e6; }
input:user-invalid + .error-msg { display: block; }
input:user-valid  { border-color: #188038; }
```

```javascript
// MANDATORY: JS bridge — :user-invalid is visual only; AT needs aria-invalid
const syncAriaInvalid = (input) => {
  if (!input.checkValidity()) input.setAttribute('aria-invalid', 'true');
  else input.removeAttribute('aria-invalid');
};
form.addEventListener('blur',   (e) => syncAriaInvalid(e.target), true);
form.addEventListener('input',  (e) => { if (e.target.hasAttribute('aria-invalid')) syncAriaInvalid(e.target); });
form.addEventListener('submit', () => form.querySelectorAll('[required]').forEach(syncAriaInvalid));
```

**Custom error messages:**

```javascript
const code = document.getElementById('code');
code.addEventListener('invalid', () => { code.setCustomValidity('Please enter exactly 4 digits.'); });
code.addEventListener('input',   () => { code.setCustomValidity(''); }); // Clear on every input
```

**Validation timing:**

| Trigger | Action | Why |
|---------|--------|-----|
| `input` | Clear existing errors only | Avoid yelling at users mid-type |
| `blur` / `focusout` | Run check, show error | Contextual; user indicated they are done |
| `submit` | Block, show all errors, focus first | Final gate; never the only gate |

**Security note:** Client-side validation is UX only. Always validate and sanitize server-side.

## Common Mistakes

- **`:invalid` instead of `:user-invalid`** → errors shown on every required field immediately on page load
- **No `aria-invalid` sync** → screen readers do not announce error state; `:user-invalid` is invisible to AT
- **`setCustomValidity()` without clearing on `input`** → custom message sticks even after correction
- **Disabling submit button for validation** → keyboard users cannot trigger browser-native error display
- **`aria-errormessage` without the referenced element in the DOM** → AT cannot find the error text

## See Also

- [Form Interaction Craft](../interaction-craft/form-interaction-craft.md) — validation timing, autosave, inline editing
- [user-valid and user-invalid](../../css/modern-css/user-valid-invalid.md) — full CSS coverage, browser support, fallback patterns
- Reference: MWG `required-field-feedback.md`, `validate-input-after-interaction.md`
