---
description: "Form validation styling only after user interaction with :user-valid/:user-invalid"
tldr: "Use `:user-invalid` and `:user-valid` for form validation styling that only appears after the user has interacted with a field. Use `:invalid` / `:valid` only when immediate page-load validation is intentional."
---

# :user-valid and :user-invalid

## When to Use

> For form validation styling that only appears after the user has interacted with a field — as opposed to `:valid` and `:invalid` which fire immediately on page load, showing error states before the user has done anything.

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

**What counts as "significant interaction":** the user must have focused the field AND left it (blur), or the containing form must have been submitted. Typing alone does not trigger `:user-invalid`/`:user-valid`.

**Browser support:** Chrome 119, Firefox 88 (had it first, in 2021), Safari 16.5. Baseline 2023. Safe to use.

## Common Mistakes

- Expecting `:user-invalid` to fire on form submit — it does not in most implementations; add a class via JS submit handler to trigger `:invalid` styles on submit
- Using `:user-valid` on optional fields — an empty optional field matches `:user-valid` because empty is valid for optional inputs; consider only using green success styling on required fields
- Forgetting that `:user-invalid` is reset when the user corrects their input — styles return to `:user-valid` when the field becomes valid, which is the desired behavior

## See Also

- [:has() Parent Selector](has-selector.md) → for showing/hiding error messages based on field state
- Reference: [MDN :user-invalid](https://developer.mozilla.org/en-US/docs/Web/CSS/:user-invalid)
