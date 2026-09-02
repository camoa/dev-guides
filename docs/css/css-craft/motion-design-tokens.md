---
description: Set up a consistent easing and duration token system for all UI animations — MD3-aligned curves, 50ms duration increments
tldr: "Use motion tokens when you need a shared vocabulary for animation timing and easing across a project. Without tokens, developers pick arbitrary values (`300ms ease`, `0.5s linear`) creating inconsistent, untuneable motion."
---

# Motion Design Tokens

## When to Use
Every project needs a shared vocabulary for animation timing and easing. Without tokens, developers pick arbitrary values (`300ms ease`, `0.5s linear`) creating inconsistent, untuneable motion.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| General UI transitions (hover, color) | `--ease-standard` + `--duration-normal` | Neutral curve, snappy timing |
| Element entering the screen | `--ease-decel` or `--ease-emphasized-decel` | Decelerating curves feel like arriving |
| Element leaving the screen | `--ease-accel` or `--ease-emphasized-accel` | Accelerating curves feel like departing |
| Micro-feedback (checkbox, ripple) | `--ease-standard` + `--duration-instant` | Must feel instantaneous |
| Page-level transitions | `--ease-emphasized-decel` + `--duration-slow` | Larger motion needs more time and expression |

## Pattern

MD3-aligned easing values with semantic duration names in 50ms increments:

```css
:root {
  /* === Easing Curves (MD3-aligned) === */
  --ease-standard:          cubic-bezier(0.2, 0, 0, 1);
  --ease-decel:             cubic-bezier(0, 0, 0, 1);
  --ease-accel:             cubic-bezier(0.3, 0, 1, 1);
  --ease-emphasized-decel:  cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-emphasized-accel:  cubic-bezier(0.3, 0, 0.8, 0.15);

  /* === Duration Scale (50ms increments) === */
  --duration-instant:   50ms;   /* Ripple start, micro-feedback */
  --duration-quick:    100ms;   /* Checkbox, toggle */
  --duration-fast:     150ms;   /* Hover/active state */
  --duration-normal:   200ms;   /* Small component transitions */
  --duration-moderate: 300ms;   /* Modal appear, popover enter */
  --duration-slow:     400ms;   /* Page-level, larger motion */
  --duration-slower:   500ms;   /* Complex choreography */
}
```

**Duration selection rule:** The larger the element or the further it travels, the longer the duration — but never exceed 600ms for a single element.

## Common Mistakes
- Using `ease` (CSS default) everywhere — it has a slow start that feels sluggish; use `--ease-standard` instead
- Using `linear` for UI transitions — linear motion looks robotic; reserve it for progress indicators and infinite loops
- Durations over 600ms for single elements — users perceive the interface as slow past this threshold
- Hardcoding `300ms ease-out` instead of tokens — impossible to tune the feel of an entire site later
- Using the same easing for enter and exit — enter should decelerate, exit should accelerate

## See Also
- [Micro-Interactions](micro-interactions.md) — applying tokens to hover/active/focus states
- [Quick Reference: Recommended Defaults](quick-reference-recommended-defaults.md) — complete copy-paste token set
- Reference: [MD3 Easing and Duration](https://m3.material.io/styles/motion/easing-and-duration)
- Reference: [MD3 Easing Tokens & Specs](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs)
- Reference: [NNGroup: Animation Duration](https://www.nngroup.com/articles/animation-duration/)
