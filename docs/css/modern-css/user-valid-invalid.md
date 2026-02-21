---
description: Form validation styling only after user interaction with :user-valid/:user-invalid
---

# :user-valid and :user-invalid

## When to Use

> Use `:user-invalid` and `:user-valid` for form validation styling that only appears after the user has interacted with a field. Use `:invalid` / `:valid` only when immediate page-load validation is intentional.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Error state after user leaves a field | `:user-invalid` | Only activates after significant interaction |
| Success state after user fills correctly | `:user-valid` | Same — interaction-gated |
| Immediate validation on page load | `:invalid` / `:valid` | Still available; rarely good UX |
| Validation after form submit attempt | `:invalid` + JS submit handler adding a class | `:user-invalid` doesn't trigger on submit, only on blur |

## Pattern

```css
/* Bad UX — error shown on page load before user touches anything */
input:invalid {
  border-color: red;
}

/* Correct — error only after user has interacted and left the field */
input:user-invalid {
  border-color: oklch(55% 0.2 30); /* red */
  background: oklch(97% 0.03 30);
}

input:user-valid {
  border-color: oklch(55% 0.2 140); /* green */
}

/* With error message using :has() */
.form-group:has(input:user-invalid) .error-message {
  display: block;
}

.form-group:has(input:user-valid) .error-message {
  display: none;
}
```

**What counts as "significant interaction":** the user must have focused the field AND left it (blur), or the containing form must have been submitted. Typing alone does not trigger `:user-invalid` / `:user-valid`.

**Browser support:** Chrome 119, Firefox 88 (had it first, in 2021), Safari 16.5. Baseline 2023. Safe to use.

## Common Mistakes

- **Wrong**: Expecting `:user-invalid` to fire on form submit → **Right**: It does not in most implementations; add a class via JS submit handler to trigger `:invalid` styles on submit
- **Wrong**: Using `:user-valid` on optional fields → **Right**: An empty optional field matches `:user-valid` because empty is valid for optional inputs; consider only using success styling on required fields
- **Wrong**: Worrying that `:user-invalid` won't clear when corrected → **Right**: It resets to `:user-valid` when the field becomes valid — this is the desired behavior

## See Also

- [:has() — Parent & Sibling Selection](has-selector.md)
- Reference: [MDN :user-invalid](https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid)
