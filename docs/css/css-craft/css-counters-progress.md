---
description: CSS counters and progress — animated progress rings, CSS-only counting numbers, step indicators, and scroll-driven progress
tldr: "Use `@property` + `counter()` for animated counting numbers and SVG `stroke-dashoffset` for progress rings — both without JavaScript counting libraries."
---

# CSS Counters & Progress

## When to Use

> Use `@property` + `counter()` for animated counting numbers and SVG `stroke-dashoffset` for progress rings — both without JavaScript counting libraries.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Circular progress ring | SVG circle + `stroke-dashoffset` driven by CSS variable | Animatable, accessible |
| Horizontal progress bar | `scaleX()` + CSS variable for percentage | Compositor-safe animation |
| Step indicator (1 of 5) | CSS counters + `:nth-child` styling | Pure CSS, semantic |
| Animated counting number | `@property` + `counter()` + animation | CSS-only counting effect |
| Scroll-driven progress | `animation-timeline: scroll()` on scaleX | See [Scroll-Aware Components](scroll-aware-components.md) |

## Pattern

```css
/* CSS-only animated counter */
@property --num {
  syntax: "<integer>";
  initial-value: 0;
  inherits: false;
}
.counter {
  --num: 0;
  animation: count-up 2s ease-out forwards;
  counter-set: num var(--num);
  font-variant-numeric: tabular-nums;
}
.counter::after { content: counter(num); }
@keyframes count-up {
  to { --num: 847; }
}

/* Step indicator */
.steps { display: flex; counter-reset: step; }
.step { counter-increment: step; flex: 1; text-align: center; }
.step::before {
  content: counter(step);
  display: grid; place-content: center;
  width: 32px; height: 32px;
  border-radius: 50%;
  background: oklch(92% 0 0);
  margin: 0 auto 0.5rem;
  transition: background 0.3s, color 0.3s;
}
.step.is-active::before { background: var(--color-primary); color: white; }
.step.is-complete::before { background: var(--color-primary); color: white; content: "✓"; }
```

For the SVG progress ring, set `stroke-dasharray` and `stroke-dashoffset` using `calc(3.1416 * diameter)` and drive the offset from a `--progress` CSS custom property (0–1).

## Common Mistakes

- **Using JS counting libraries** when `@property` + `counter()` works — CSS-only counting is smoother and lighter
- **Forgetting `font-variant-numeric: tabular-nums`** on counters — digits shift width as they change
- **Animating `width` for progress bars** — use `transform: scaleX()` for 60fps

## See Also

- [Scroll-Aware Components](scroll-aware-components.md) → scroll-driven progress
- [Skeleton and Loading States](skeleton-and-loading-states.md) → loading indicators
- Reference: [MDN: @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
