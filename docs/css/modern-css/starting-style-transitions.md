---
description: Animate elements entering from display:none with @starting-style
---

# @starting-style and Discrete Transitions

## When to Use

> Use `@starting-style` with `transition-behavior: allow-discrete` to animate elements entering from `display: none` — dialogs, drawers, popovers. Use a JS animation library when you need complex multi-step choreography.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Animate a dialog or drawer opening | `@starting-style` + `transition-behavior: allow-discrete` | Browser reads start values from `@starting-style` |
| `display: none` → `display: block` with transition | Both `allow-discrete` AND `@starting-style` | Two parts required — display change needs `allow-discrete`, start values need `@starting-style` |
| Animate a popover appearing | Same pattern as dialog | Popovers use top-layer entry same as `<dialog>` |
| Complex orchestrated multi-step animation | JS animation library | CSS discrete transitions are linear; choreography needs JS |

## Pattern

Animating a `<dialog>` open and close:

```css
dialog {
  opacity: 1;
  translate: 0 0;
  transition:
    opacity 0.3s ease,
    translate 0.3s ease,
    display 0.3s allow-discrete,  /* required for display: none transition */
    overlay 0.3s allow-discrete;  /* required to hold top-layer during exit */

  @starting-style {
    /* Values the browser reads BEFORE the element becomes visible */
    opacity: 0;
    translate: 0 -1rem;
  }
}

/* Exit — when dialog is not [open], animate toward these values */
dialog:not([open]) {
  opacity: 0;
  translate: 0 -1rem;
}
```

**Three required pieces for enter/exit animation:**
1. `@starting-style` block — start values for the enter transition
2. `transition-behavior: allow-discrete` on `display` — allows display to be part of transition
3. `transition-behavior: allow-discrete` on `overlay` — keeps top-layer elements visible during exit transition

**Browser support:** Chrome 117, Firefox 129, Safari 17.5. Baseline August 2024. Safe to use.

## Common Mistakes

- **Wrong**: Omitting the `overlay` transition → **Right**: The dialog disappears abruptly during exit because it leaves the top layer before the transition completes
- **Wrong**: Forgetting `@starting-style` → **Right**: Without it, the browser has no starting values and the enter transition does not play
- **Wrong**: Putting animation logic in `@starting-style` → **Right**: `@starting-style` defines start state only; transitions are declared on the element normally
- **Wrong**: Using `@keyframes` animation instead of `transition` → **Right**: `@starting-style` only works with CSS transitions, not `@keyframes`

## See Also

- [Scroll-Driven Animations](scroll-driven-animations.md)
- [View Transitions](view-transitions.md)
- [Popover API](popover-api.md)
- Reference: [MDN @starting-style](https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style)
