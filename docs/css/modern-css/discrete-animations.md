---
description: Animate display, overlay, and other discrete properties — entry/exit animations for dialogs and popovers
drupal_version: "11.x"
---

# Discrete Property Animations

## When to Use

> Use `transition-behavior: allow-discrete` when you need to animate properties that were previously impossible to transition — `display`, `overlay`, `content-visibility`. Pair with `@starting-style` for entry animations. Use `overlay` transition to keep top-layer elements (dialogs, popovers) visible during exit.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Animate dialog open/close | `transition-behavior: allow-discrete` + `@starting-style` | Full entry+exit animation |
| Keep element in top layer during exit | Transition `overlay` | Prevents element from snapping behind content |
| Animate popover entry | `allow-discrete` on `display` + `overlay` | Combined with Popover API |
| Animate display swap (flex→grid) | Not possible | Discrete transitions only handle show/hide (none↔block) |

## Pattern

```css
/* Dialog with entry and exit animations */
dialog {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease,
              transform 0.3s ease,
              display 0.3s allow-discrete,
              overlay 0.3s allow-discrete;
}

dialog[open] {
  opacity: 1;
  transform: translateY(0);
}

@starting-style {
  dialog[open] {
    opacity: 0;
    transform: translateY(20px);
  }
}

/* Popover with discrete transitions */
[popover] {
  opacity: 0;
  scale: 0.95;
  transition: opacity 0.2s, scale 0.2s,
              display 0.2s allow-discrete,
              overlay 0.2s allow-discrete;
}

[popover]:popover-open {
  opacity: 1;
  scale: 1;
}

@starting-style {
  [popover]:popover-open {
    opacity: 0;
    scale: 0.95;
  }
}
```

For a discrete property like `display`, the browser swaps the value at 50% of the transition duration. On entry, `display` swaps to `block` at time 0 so opacity/transform can animate from `@starting-style` values. On exit, opacity/transform animate to exit values, then `display` swaps to `none` at 50%.

The `overlay` property keeps elements in the top layer (above all other content) during exit transitions. Without transitioning `overlay`, a dialog snaps behind content immediately when closing.

**Browser support:** Chrome 117+, Edge 117+, Safari 17.5+, Firefox 129+. Firefox handles `@starting-style` but does not animate `display` itself. Baseline Newly Available.

## Common Mistakes

- **Wrong**: Transitioning `display` but not `overlay` → **Right**: Without `overlay`, top-layer elements (dialogs, popovers) snap behind content during exit
- **Wrong**: `allow-discrete` as a standalone property → **Right**: It is a value for `transition-behavior`, or used inline: `display 0.3s allow-discrete`
- **Wrong**: No `@starting-style` → **Right**: Without it, there is no entry animation (element starts in its final state)
- **Wrong**: Expecting to animate `display: flex` → `display: grid` → **Right**: Discrete transitions only handle show/hide, not value swaps

## See Also

- [@starting-style & Discrete Transitions](starting-style-transitions.md) — the entry-state companion for discrete animations
- [Popover API](popover-api.md) — primary use case for discrete transitions
- [interpolate-size](interpolate-size.md) — for animating height to auto
- Reference: [Chrome: Entry/exit animations](https://developer.chrome.com/blog/entry-exit-animations)
