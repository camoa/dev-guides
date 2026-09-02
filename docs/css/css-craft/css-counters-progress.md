---
description: CSS counters and progress — animated progress rings, CSS-only counting numbers, step indicators, and scroll-driven progress
tldr: "Use `@property` + `counter()` for animated counting numbers and SVG `stroke-dashoffset` for progress rings — both without JavaScript counting libraries."
---

# CSS Counters & Progress

## When to Use
When a client wants animated counters, progress rings, step indicators, or number displays — without JavaScript counting libraries.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Circular progress ring | SVG circle + `stroke-dashoffset` driven by CSS variable | Animatable, accessible |
| Horizontal progress bar | `scaleX()` + CSS variable for percentage | Compositor-safe animation |
| Step indicator (1 of 5) | CSS counters + `:nth-child` styling | Pure CSS, semantic |
| Animated counting number | `@property` + `counter()` + animation | CSS-only counting effect |
| Scroll-driven progress | `animation-timeline: scroll()` on scaleX | See [Scroll-Aware Components](scroll-aware-components.md) |

## Pattern: Circular Progress Ring
```css
.progress-ring {
  --progress: 0.75; /* 0 to 1 */
  --size: 120px;
  --stroke: 8px;
  width: var(--size);
  height: var(--size);
}

.progress-ring circle {
  fill: none;
  stroke-width: var(--stroke);
  r: calc(var(--size) / 2 - var(--stroke));
  cx: calc(var(--size) / 2);
  cy: calc(var(--size) / 2);
  /* Circumference = 2πr */
  stroke-dasharray: calc(3.1416 * (var(--size) - var(--stroke) * 2));
  stroke-dashoffset: calc(
    3.1416 * (var(--size) - var(--stroke) * 2) * (1 - var(--progress))
  );
  transform: rotate(-90deg);
  transform-origin: center;
  transition: stroke-dashoffset 1s var(--ease-emphasized-decel);
}

.progress-ring__bg { stroke: oklch(92% 0 0); }
.progress-ring__fill { stroke: var(--color-primary); stroke-linecap: round; }
```

## Pattern: CSS-Only Animated Counter
```css
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

.counter::after {
  content: counter(num);
}

@keyframes count-up {
  to { --num: 847; } /* Target number */
}

/* Scroll-triggered: start counting when in view */
.counter--scroll {
  animation: count-up 1s linear forwards;
  animation-timeline: view();
  animation-range: entry 50% entry 100%;
}
```

## Pattern: Step Indicator
```css
.steps {
  display: flex;
  counter-reset: step;
}

.step {
  counter-increment: step;
  flex: 1;
  text-align: center;
}

.step::before {
  content: counter(step);
  display: grid;
  place-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: oklch(92% 0 0);
  margin: 0 auto 0.5rem;
  transition: background 0.3s, color 0.3s;
}

.step.is-complete::before {
  background: var(--color-primary);
  color: white;
  content: "✓";
}

.step.is-active::before {
  background: var(--color-primary);
  color: white;
}
```

## Common Mistakes
- **Using JS counting libraries** when `@property` + `counter()` works — CSS-only counting is smoother and lighter
- **Forgetting `font-variant-numeric: tabular-nums`** on counters — without it, digits shift as they change width
- **Animating `width` for progress bars** — use `transform: scaleX()` for 60fps

## See Also
- [Scroll-Aware Components](scroll-aware-components.md) → scroll-driven progress
- [Skeleton and Loading States](skeleton-and-loading-states.md) → loading indicators
- Reference: [MDN: @property](https://developer.mozilla.org/en-US/docs/Web/CSS/@property)
