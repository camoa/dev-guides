---
description: Ensure every interactive element is keyboard-reachable with a visible focus indicator and correct Enter/Space key behavior.
tldr: Every action reachable by mouse must be reachable by keyboard; use `:focus-visible` with sufficient contrast; never use positive `tabindex` values — they destroy predictable tab order; `aria-hidden="true"` on a focusable element creates an invisible focus trap.
---

# Keyboard and Focus

## When to Use

> Keyboard accessibility is required for all interactive elements — every action a mouse user can take must be reachable and operable by keyboard alone, with a visible focus indicator.

## Decision

| Need | Pattern | Notes |
|---|---|---|
| Single interactive element | Native `<button>` / `<a>` | Browser handles Tab, Enter, Space |
| Tab order matches visual layout | DOM order = visual order | Avoid CSS `order` diverging from source order |
| Visible focus ring | `:focus-visible` with sufficient contrast | Never just `outline: none` |
| Element reachable by Tab | `tabindex="0"` (or implicit from native element) | Assign ARIA role if not a native element |
| Element focusable only by script | `tabindex="-1"` then `.focus()` | Skip-link targets, dialog on open |
| Custom widget arrow key navigation | Roving tabindex in JS | See [Keyboard Navigation Craft](../../js/interaction-craft/keyboard-navigation-craft.md) |
| Focus trap for modal | `<dialog>.showModal()` → browser handles it | See [Native Dialog](native-dialog.md) |
| Toggle button state | `aria-expanded` / `aria-pressed` | Set programmatically when state changes |

**Positive `tabindex` is always wrong:** `tabindex="1"` creates a separate, earlier focus sequence that breaks the natural DOM order. Restructure the DOM if the visual order differs.

**`aria-hidden` on focusable elements:** Never set `aria-hidden="true"` on an element that can receive keyboard focus — it becomes an invisible, unreachable focus trap for AT users.

## Pattern

```css
/* Explicit :focus-visible — high contrast, never removed */
:where(a:any-link, button, [tabindex]):focus-visible {
  outline: 3px solid #ff0055;
  outline-offset: 3px;
}
```

```javascript
// Custom widget: Enter on keydown, Space on keyup (matches native button)
customWidget.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') toggleState();
  if (e.key === ' ') e.preventDefault(); // Block scroll
});
customWidget.addEventListener('keyup', (e) => {
  if (e.key === ' ') toggleState();
});

function toggleState() {
  const expanded = customWidget.getAttribute('aria-expanded') === 'true';
  customWidget.setAttribute('aria-expanded', String(!expanded));
}
```

## Common Mistakes

- **Wrong**: `outline: none` with no replacement → **Right**: Focus position becomes invisible for keyboard users; always provide a visible replacement
- **Wrong**: Positive `tabindex` values → **Right**: Destroys predictable tab order; use `tabindex="0"` only
- **Wrong**: Skip-link target missing `tabindex="-1"` → **Right**: `<main>` is not natively focusable; `.focus()` silently fails without it
- **Wrong**: Toggling element visibility with CSS only → **Right**: Keyboard focus can land on visually hidden interactive elements; use `hidden`, `inert`, or `display: none`

## See Also

- [Native Dialog](native-dialog.md) — browser-native focus management in modals
- Reference: [Keyboard Navigation Craft](../../js/interaction-craft/keyboard-navigation-craft.md) — roving tabindex, focus trap, focus restoration
- Reference: https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
