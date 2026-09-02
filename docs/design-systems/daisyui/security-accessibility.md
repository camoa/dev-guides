---
description: DaisyUI accessibility gaps, required ARIA attributes, keyboard navigation status, and security considerations
tldr: "Every component implementation. Accessibility and security are part of shipping correct code, not optional steps."
---

# Security and Accessibility

## When to Use

> Every component implementation. Accessibility and security are not optional steps — they are part of shipping correct code.

## What DaisyUI Provides Automatically

| Feature | Status | Notes |
|---------|--------|-------|
| Focus-visible outlines | Yes | All interactive components have `focus-visible` outlines |
| `prefers-reduced-motion` | Yes | Transitions/animations disabled via media query |
| `prefers-color-scheme: dark` | Yes | Dark theme auto-applies if configured with `--prefersdark` |
| High-contrast mode (Windows) | Partial | `forced-colors` media queries in checkbox, radio, tab — not all components |
| Print styles | Partial | Checkbox/radio have print-specific rendering |
| ARIA roles | No | DaisyUI does NOT add any ARIA roles/attributes |
| Keyboard navigation | Partial | See table below |

## ARIA Gaps — You Must Add These

DaisyUI is a CSS library. It adds classes and styles, but zero JavaScript and zero ARIA. You are responsible for:

| Component | Required ARIA / HTML attributes |
|-----------|--------------------------------|
| `.modal` | `role="dialog"` `aria-modal="true"` `aria-labelledby="title-id"` |
| `.dropdown` | Trigger: `aria-expanded` `aria-haspopup` `aria-controls`. Content: `role="menu"` |
| `.alert` | `role="alert"` (or `role="status"` for non-urgent) |
| `.tabs` (radio input method) | Each `<input>` needs `aria-label` — DaisyUI uses `attr(aria-label)` for visible text |
| `.rating` | Each `<input>` needs `aria-label` (e.g., "3 stars") |
| `.accordion / .collapse` | `aria-expanded` on toggle, `aria-controls` pointing to content |
| `.breadcrumbs` | Wrap in `<nav aria-label="Breadcrumb">` |
| `.steps` | Add `aria-current="step"` on active step |

## Keyboard Navigation Status

| Component | Tab | Enter/Space | Arrows | Escape |
|-----------|-----|-------------|--------|--------|
| `.btn` | Yes | Yes (native button) | — | — |
| `.dropdown` | Yes | Opens on focus (via CSS) | No (JS needed) | No (JS needed) |
| `.modal` (CSS-only) | Leaks | No | — | No |
| `.modal` + dialog element | Trapped | Yes | — | Yes |
| `.menu` items | Yes | Yes | No | — |
| `.tabs` (radio method) | Yes | Yes | Yes (native radio) | — |
| `.checkbox` `.toggle` `.radio` | Yes | Yes | Yes (groups) | — |

## Critical Gap: Modal Focus Trapping

**Critical gap: Modal focus trapping.** The CSS-only modal (checkbox method) does NOT trap focus. A keyboard user can tab past the modal into background content. Solutions:

1. Use `<dialog>` element with `showModal()` — browsers trap focus natively
2. Use Radix UI Dialog primitive (recommended for React) — handles trapping, escape, ARIA
3. Add a focus trap library

```html
<!-- Correct modal with native dialog element -->
<dialog class="modal" id="my-modal">
  <div class="modal-box">
    <h2 id="modal-title" class="text-lg font-bold">Title</h2>
    <p>Content.</p>
    <div class="modal-action">
      <!-- autofocus first actionable element -->
      <button class="btn" onclick="document.getElementById('my-modal').close()" autofocus>
        Close
      </button>
    </div>
  </div>
</dialog>

<button class="btn btn-primary" onclick="document.getElementById('my-modal').showModal()">
  Open
</button>
```

## Security Considerations

DaisyUI has minimal direct security surface — it's CSS. Security risks come from how you use the components:

- **XSS via `data-theme` attribute:** If you set `data-theme` from user input without sanitization, an attacker could set arbitrary attribute values. DaisyUI only reads `data-theme` for CSS variable application — no script execution — but it could be combined with other injection vectors. Always sanitize theme names against your known theme list before setting as an attribute
- **Modal content injection:** DaisyUI's modal is a fixed-position overlay. If you render user-provided HTML inside a modal without sanitization, the modal framing creates false legitimacy for phishing content. Always escape user content in modal bodies
- **SVG in badge/card content:** DaisyUI doesn't sanitize icon content. SVG injection through `innerHTML` can execute scripts. Use dedicated icon libraries (lucide-react, heroicons) rather than dynamic SVG strings

## Common Mistakes

- Shipping modal without `role="dialog"` — screen reader users will not know a dialog has appeared
- Using dropdown without `aria-expanded` — keyboard users cannot tell if the menu is open
- Relying on DaisyUI's focus styles as the only accessibility measure — they style focus, but don't manage focus flow

## See Also

- [Actions Components](actions-components.md) — modal implementation with `<dialog>` element
- [DaisyUI and React](daisyui-react.md) — Radix UI for accessible dialogs in React
- Reference: `react-design-system.md` Section 7 — Radix UI for accessible dialogs in React
- Reference: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- Reference: https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/
