---
description: Styling browser-autofilled fields with the :autofill pseudo-class — inset box-shadow trick for background color override, mandatory focus ring preservation.
tldr: Use box-shadow inset to simulate background-color on autofilled inputs — background-color is blocked by the browser's security model. Always include :autofill:focus-visible with an explicit outline; never remove focus indicators from autofilled fields. Progressive enhancement — no Firefox support.
drupal_version: ""
---

# Autofill Visual Feedback

## When to Use

> Use the `:autofill` pseudo-class to visually distinguish browser-autofilled fields from user-typed fields, guiding users to confirm pre-populated data before submission. This is a progressive enhancement — the form works without it.

## Decision

| Need | Approach | Notes |
|------|----------|-------|
| Tint autofilled background | `box-shadow` inset trick | `background-color` cannot override browser autofill styling |
| Style autofilled border | `border` on `:autofill` | Combine with background change — never color alone |
| Firefox support | No CSS hook available | No `:autofill` in Firefox; form works normally |
| Preserve focus ring | Explicit `:autofill:focus-visible` | Never remove focus outlines without a replacement |

**Baseline status: Limited availability.** Chrome 110+, Edge 110+, Safari 15+. Not supported in Firefox. Treat as progressive enhancement.

## Pattern

```css
/* Use box-shadow inset — background-color is blocked by browser security model */
input:autofill,
input:-webkit-autofill {
  border: 2px solid #2e7d32;
  box-shadow: 0 0 0 100vmax #e8f5e9 inset;
}

/* MANDATORY: Explicit focus indicator for keyboard users when autofill is styled */
input:autofill:focus-visible,
input:-webkit-autofill:focus-visible {
  outline: 3px solid #000;
  outline-offset: 2px;
}
```

**Why `box-shadow` instead of `background-color`:** Browsers apply their own autofill background using a privileged style layer that web CSS cannot override with `background-color`. A large inset `box-shadow` paints over the browser's background from within.

**Accessibility rules:**
- Use **multiple state indicators** — never border colour alone. Combine border thickness change, background shift (via box-shadow), and optionally an icon.
- Never remove `outline` from `:autofill:focus-visible` without a visible replacement.
- Do not use JavaScript to detect or respond to autofill state — the CSS-only `:autofill` pseudo-class is the correct hook.

## Common Mistakes

- **`background-color` on `:autofill`** → overridden by browser's autofill styling; use `box-shadow` inset
- **`:auto-fill` (with hyphen)** → incorrect selector; the property is `:autofill`
- **Colour alone to indicate autofill state** → fails WCAG 1.4.1 (Use of Color)
- **`outline: none` on `:autofill` without replacement** → keyboard users lose focus indicator inside autofilled fields

## See Also

- [Autocomplete & Autofill](autocomplete-and-autofill.md) — how to set up tokens so autofill triggers correctly
- Reference: MWG `autofill-highlight-inputs.md`
