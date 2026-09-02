---
description: "Animate display, overlay, and other discrete properties — entry/exit animations for dialogs and popovers"
tldr: "Use `transition-behavior: allow-discrete` when you need to animate properties that were previously impossible to transition — `display`, `overlay`, `content-visibility`. Pair with `@starting-style` for entry animations."
---

# Discrete Property Animations

## When to Use

> When you need to transition properties that were previously impossible to animate — `display`, `overlay`, `content-visibility`, or `mix-blend-mode`. This works with `@starting-style` to create entry/exit animations for elements toggling `display: none`.

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

/* Entry state */
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

**How `allow-discrete` works:** For a discrete property like `display`, the browser swaps the value at 50% of the transition duration. Combined with `@starting-style`, this means:
1. Element enters with `display: none` → `display: block` swap happens at time 0 (start)
2. Opacity/transform animate from `@starting-style` values to final values
3. On exit, opacity/transform animate to exit values, then `display` swaps to `none` at 50%

**The `overlay` property:** Keeps elements in the top layer (above all other content) during exit transitions. Without transitioning `overlay`, a dialog would snap behind content immediately when closing.

**Browser support:** Chrome 117+, Edge 117+, Safari 17.5+, Firefox 129+ (Firefox does not animate `display` itself but handles `@starting-style` opacity/transform). Baseline Newly Available.

## Common Mistakes

- Forgetting to transition both `display` AND `overlay` — without `overlay`, top-layer elements (dialogs, popovers) snap behind content during exit
- Using `allow-discrete` as a standalone property — it's a value for `transition-behavior`, not a property: `transition-behavior: allow-discrete` or inline as `display 0.3s allow-discrete`
- Not providing `@starting-style` — without it, the entry state is the same as the final state (no animation on entry)
- Expecting discrete transitions on non-show/hide changes — `display: flex` → `display: grid` cannot be animated

## See Also

- [@starting-style](starting-style-transitions.md) → the entry-state companion for discrete animations
- [Popover API](popover-api.md) → the primary use case for discrete transitions
- [interpolate-size](interpolate-size.md) → for animating height to `auto`, the other half of an accordion transition
- Reference: [Chrome: Entry/exit animations](https://developer.chrome.com/blog/entry-exit-animations)
