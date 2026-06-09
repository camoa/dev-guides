---
description: Build accessible forms with persistent labels, programmatically linked errors, and validation timing that feels natural rather than premature.
tldr: Use `<label for="id">` for every input, `aria-describedby` for hints, `aria-errormessage`+`aria-invalid` for errors; bridge CSS `:user-invalid` to `aria-invalid` via JS so errors only announce after the user has interacted with the field.
---

# Forms Accessibility

## When to Use

> Build accessible forms by ensuring each control has a persistent label, hints and errors are programmatically linked, and validation feedback is timed to feel natural rather than premature or delayed.

## Decision

| Need | Pattern | Anti-pattern |
|---|---|---|
| Persistent label | `<label for="id">` | `placeholder` (disappears; low contrast) |
| Supplementary hint | `aria-describedby="hint-id"` | Packing hint into the label |
| Required field | `required` attribute | `aria-required="true"` alone |
| Error message linked to field | `aria-errormessage="error-id"` + `aria-invalid="true"` | `aria-describedby` only |
| Auto-fill support | `autocomplete="email"` / `"given-name"` / etc. | Missing autocomplete on personal-info fields |
| Hint placement | Above the input | Below (autocomplete popovers cover it) |

## Pattern: Label and Error Structure

```html
<label for="email">Email address</label>
<span id="email-hint">We'll use this to send your confirmation.</span>
<input type="email" id="email" required autocomplete="email"
  aria-describedby="email-hint" aria-errormessage="email-error">
<span id="email-error" class="error-msg" role="alert">
  Please enter a valid email address.
</span>
```

## Pattern: Bridge `:user-invalid` to `aria-invalid`

CSS `:invalid` fires the moment a required field exists but is empty — before the user has typed. `:user-invalid` (Baseline 2023) applies only after the user has interacted. Bridge the gap with JS:

```css
.error-msg { display: none; color: #d93025; }
input:user-invalid ~ .error-msg { display: block; }
input:user-invalid { border-color: #d93025; }
```

```javascript
const updateAriaState = (event) => {
  const input = event.target;
  if (!input.matches?.('input, textarea, select')) return;
  if (input.matches(':user-invalid')) {
    input.setAttribute('aria-invalid', 'true');
  } else {
    input.removeAttribute('aria-invalid');
  }
};

// blur/focus don't bubble — use capture phase
document.addEventListener('blur', updateAriaState, true);
document.addEventListener('focus', updateAriaState, true);
document.addEventListener('input', (event) => {
  const input = event.target;
  if (!input.matches?.('input, textarea, select')) return;
  if (input.getAttribute('aria-invalid') === 'true') updateAriaState(event);
});
```

Feature-detect before using:
```javascript
if (!CSS.supports('selector(:user-invalid)')) {
  // Load fallback — track interaction state manually
}
```

## Common Mistakes

- **Wrong**: Placeholder as label → **Right**: Placeholder vanishes on input, fails contrast, is not reliably announced
- **Wrong**: Error announced via `aria-live` before user has interacted → **Right**: Use `:user-invalid` bridge or equivalent timing
- **Wrong**: `aria-required="true"` alongside `required` → **Right**: `required` implies `aria-required`; redundant
- **Wrong**: Triggering form submission or page navigation on focus change → **Right**: WCAG 3.2.1 violation; breaks users who tab through fields
- **Wrong**: Hint text placed below input → **Right**: Autocomplete popovers obscure hints below; move hints above the input

## See Also

- [Live Regions](live-regions.md) — centralized announcer patterns
- [Accessible Names](accessible-names.md) — label/for association and `aria-describedby`
- Reference: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-invalid
- Reference: https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid
