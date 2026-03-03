---
description: Springy, bouncy animations without JavaScript — CSS linear() easing, generator tools, fallbacks, and when JS springs are better
---

# Spring Physics and Advanced Easing

## When to Use

> Use CSS `linear()` for spring-like bounce in drawers, modals, toggle switches, and toasts. Use JS spring libraries when animations are frequently interrupted — CSS springs handle interrupts unnaturally because they require a fixed duration.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Bouncy spring in CSS only | `linear()` with overshoot values (>1.0) | ~88% browser support; GPU-composited |
| Spring that responds to interrupts naturally | JS spring library (Motion, React Spring) | CSS cannot model physics mid-animation |
| Subtle overshoot (1-2% past target) | `linear()` with a few values slightly above 1.0 | Simple spring feel without a full generator |
| Complex physics (friction, velocity) | JS spring library | CSS `linear()` requires fixed duration |
| Browser support for all users | Cubic-bezier as `@supports` fallback | `linear()` has no IE/old Safari support |

### CSS linear() Limitation

CSS spring physics requires a fixed duration. A real spring's duration depends on velocity and mass. If an animation is interrupted mid-way, CSS applies a "reversing shortening factor" that produces an unnatural snap. For rapidly-interrupted animations (hover in/out quickly), a JS spring library will feel significantly better.

## Pattern

**Simple spring — subtle overshoot:**
```css
:root {
  --ease-spring-subtle: linear(
    0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%,
    1.017, 1.077, 1.108, 1.121 24.4%, 1.106, 1.081 27.2%, 1.021 32.4%, 1
  );
  --ease-spring-subtle-duration: 500ms;
  @supports not (animation-timing-function: linear(0, 1)) {
    --ease-spring-subtle: cubic-bezier(0.2, 0, 0, 1);
    --ease-spring-subtle-duration: 300ms;
  }
}
.springy-modal {
  transition:
    transform var(--ease-spring-subtle-duration) var(--ease-spring-subtle),
    opacity var(--duration-moderate) var(--ease-emphasized-decel);
}
```

**Toast with spring entrance:**
```css
.notification-toast {
  transform: translateY(100%); opacity: 0;
  transition:
    transform var(--ease-spring-subtle-duration) var(--ease-spring-subtle),
    opacity var(--duration-fast) var(--ease-decel);
}
.notification-toast.is-visible { transform: translateY(0); opacity: 1; }
```

### Generating Spring Values

Do not write `linear()` values by hand — they need 30-70 data points for convincing springs. Use a generator:

- [Josh W. Comeau's Spring Generator](https://www.joshwcomeau.com/animation/linear-timing-function/) — interactive playground
- [CSS Springs Generator](https://www.kvin.me/css-springs/how-to-use) — stiffness/damping to CSS output

Store the output as CSS custom properties so you only compute them once.

## Common Mistakes

- **Wrong**: Writing `linear()` values by hand — **Right**: Always use a generator; curves need 30-70 data points
- **Wrong**: Springy animations for form inputs or data-heavy UIs — **Right**: Users want direct feedback; reserve bounce for personality moments
- **Wrong**: No `@supports` fallback — **Right**: `linear()` with many values is unparseable in older browsers; transition silently fails
- **Wrong**: Animating `height` or `width` with spring easing — **Right**: Layout-triggering + spring physics = jank on every bounce; use `scaleY()`
- **Wrong**: `--ease-spring-bouncy` for exit animations — **Right**: Bouncy exits feel wrong; enter with bounce, exit with standard ease-out

## See Also

- [Motion Design Tokens](motion-design-tokens.md) — where to store spring tokens alongside cubic-bezier curves
- [Animation Performance](animation-performance.md) — `linear()` runs on the compositor like any timing function
- [Accessibility and Motion](accessibility-and-motion.md) — spring bounce is a vestibular trigger; reduce to static transitions
- Reference: [Josh W. Comeau: Springs and Bounces in Native CSS](https://www.joshwcomeau.com/animation/linear-timing-function/)
- Reference: [Chrome: CSS linear() Easing Function](https://developer.chrome.com/docs/css-ui/css-linear-easing-function)
- Reference: [PQINA: CSS Spring Animation with linear()](https://pqina.nl/blog/css-spring-animation-with-linear-easing-function)
