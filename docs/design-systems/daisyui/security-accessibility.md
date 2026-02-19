---
description: DaisyUI accessibility gaps, required ARIA attributes, keyboard navigation status, and security considerations
---

# Security and Accessibility

## When to Use

> Every component implementation. Accessibility and security are part of shipping correct code, not optional steps.

## What DaisyUI Provides Automatically

| Feature | Status | Notes |
|---------|--------|-------|
| Focus-visible outlines | Yes | All interactive components |
| `prefers-reduced-motion` | Yes | Transitions/animations disabled via media query |
| `prefers-color-scheme: dark` | Yes | Auto-applies if configured with `--prefersdark` |
| High-contrast mode (Windows) | Partial | `forced-colors` queries in checkbox, radio, tab — not all components |
| ARIA roles | No | DaisyUI does NOT add any ARIA roles or attributes |
| Keyboard navigation | Partial | See table below |

## ARIA Gaps — You Must Add These

| Component | Required ARIA / HTML attributes |
|-----------|--------------------------------|
| `.modal` | `role="dialog"` `aria-modal="true"` `aria-labelledby="title-id"` |
| `.dropdown` | Trigger: `aria-expanded` `aria-haspopup` `aria-controls`. Content: `role="menu"` |
| `.alert` | `role="alert"` (or `role="status"` for non-urgent) |
| `.tabs` (radio input method) | Each `<input>` needs `aria-label` |
| `.rating` | Each `<input>` needs `aria-label` (e.g., "3 stars") |
| `.accordion / .collapse` | `aria-expanded` on toggle, `aria-controls` pointing to content |
| `.breadcrumbs` | Wrap in `<nav aria-label="Breadcrumb">` |
| `.steps` | Add `aria-current="step"` on active step |

## Keyboard Navigation Status

| Component | Tab | Enter/Space | Arrows | Escape |
|-----------|-----|-------------|--------|--------|
| `.btn` | Yes | Yes (native) | — | — |
| `.dropdown` | Yes | Opens via CSS focus | No (JS needed) | No (JS needed) |
| `.modal` (CSS-only checkbox) | Leaks focus | No | — | No |
| `.modal` + `<dialog>` element | Trapped | Yes | — | Yes |
| `.menu` items | Yes | Yes | No | — |
| `.tabs` (radio method) | Yes | Yes | Yes (native radio) | — |
| `.checkbox` `.toggle` `.radio` | Yes | Yes | Yes (groups) | — |

## Pattern

**Critical: Modal focus trapping.** The CSS-only checkbox modal does NOT trap focus. Solutions:

1. Use `<dialog>` element with `showModal()` — browsers trap focus natively (recommended)
2. Use Radix UI Dialog primitive in React — handles trapping, escape key, ARIA
3. Add a focus trap library

```html
<!-- Native dialog element — correct approach -->
<dialog class="modal" id="my-modal">
  <div class="modal-box">
    <h2 id="modal-title" class="text-lg font-bold">Title</h2>
    <p>Content.</p>
    <div class="modal-action">
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

- **XSS via `data-theme`:** If setting `data-theme` from user input, always sanitize against your known theme list before setting the attribute
- **Modal content injection:** DaisyUI modal framing creates false legitimacy for phishing content — always escape user-provided HTML in modal bodies
- **SVG injection:** DaisyUI doesn't sanitize icon content. Use dedicated icon libraries (lucide-react, heroicons) rather than dynamic SVG strings from user input

## Common Mistakes

- **Wrong**: Shipping modal without `role="dialog"` — **Right**: Screen reader users will not know a dialog has appeared
- **Wrong**: Dropdown without `aria-expanded` — **Right**: Keyboard users cannot tell if the menu is open
- **Wrong**: Relying solely on DaisyUI's focus styles for accessibility — **Right**: Focus styles indicate focus; they do not manage focus flow

## See Also

- [Actions Components](actions-components.md) — modal implementation patterns
- [DaisyUI and React](daisyui-react.md) — Radix UI for accessible dialogs in React
- Reference: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
- Reference: https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/
