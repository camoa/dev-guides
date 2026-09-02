---
description: Springy, bouncy animations without JavaScript — CSS linear() easing, generator tools, fallbacks, and when JS springs are better
tldr: "Use CSS `linear()` for spring-like bounce in drawers, modals, toggle switches, and toasts. Use JS spring libraries when animations are frequently interrupted — CSS springs handle interrupts unnaturally because they require a fixed duration."
---

# Spring Physics and Advanced Easing

## When to Use
Standard cubic-bezier curves are limited to one acceleration and one deceleration — they cannot overshoot or bounce. The CSS `linear()` function breaks this constraint by specifying dozens of discrete points on a timing curve, enabling spring-like bounce and snappy overshoot natively in CSS. Use for interactive elements that benefit from physical character: drawers, modals, toggle switches, notification toasts.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Bouncy spring in CSS only | `linear()` with overshoot values (>1.0) | ~88% browser support; GPU-composited like any CSS transition |
| Spring that responds to interrupts naturally | JS spring library (Motion, React Spring) | CSS cannot model physics mid-animation; interrupted springs feel wrong in CSS |
| Subtle overshoot (1-2% past target) | `linear()` with a few values slightly above 1.0 | Simple spring feel without a full generator |
| Complex physics (friction, velocity) | JS spring library | CSS `linear()` requires a fixed duration |
| Browser support for all users | Cubic-bezier as `@supports` fallback | `linear()` has no IE/old Safari support |

## When CSS linear() Falls Short

CSS spring physics has a fundamental limitation: all transitions require a fixed duration. A real spring's duration depends on the velocity and mass of the object — it resolves when it reaches equilibrium. In CSS, an interrupted spring (hover before animation completes) applies a "reversing shortening factor" that proportionally reduces duration. This produces an unnatural snap that doesn't match spring physics. If animations are frequently interrupted (e.g., rapidly hovering in and out), a JS spring library will feel significantly better.

## Pattern

**Simple spring — subtle overshoot:**

```css
:root {
  /* Store in a token — reuse across all springy elements */
  --ease-spring-subtle: linear(
    0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%,
    1.017, 1.077, 1.108, 1.121 24.4%, 1.106, 1.081 27.2%, 1.057, 1.036,
    1.021 32.4%, 1.013, 1.007, 1.003, 1.001 39.5%, 1
  );
  --ease-spring-subtle-duration: 500ms;

  /* Fallback for non-supporting browsers */
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

**Bouncy spring — more dramatic:**

```css
:root {
  --ease-spring-bouncy: linear(
    0, 0.004, 0.016, 0.035, 0.063, 0.098, 0.141, 0.191, 0.25, 0.316, 0.391,
    0.475, 0.568, 0.67, 0.782, 0.905, 1.041, 1.19, 1.353, 1.531, 1.726,
    1.938, 2.169, 2.42, 2.69, 2.98, 1.316, 0.987, 0.812, 0.723, 0.680,
    0.667, 0.672, 0.690, 0.715, 0.743, 0.770, 0.794, 0.814, 0.829, 0.839,
    0.845, 0.847 72.1%, 0.848, 0.846, 0.842, 0.838, 0.833, 0.829, 0.826,
    0.823, 0.822, 0.821, 0.821, 0.822, 0.823, 0.825, 0.827, 0.829, 0.831,
    0.833, 0.835, 0.836, 0.837, 0.838, 0.839, 0.839, 0.839, 0.839, 1
  );
}

.toggle-switch {
  transition: transform 600ms var(--ease-spring-bouncy);
}
```

**Practical usage — toggle with spring feel:**

```css
.notification-toast {
  transform: translateY(100%);
  opacity: 0;
  transition:
    transform var(--ease-spring-subtle-duration) var(--ease-spring-subtle),
    opacity var(--duration-fast) var(--ease-decel);
}

.notification-toast.is-visible {
  transform: translateY(0);
  opacity: 1;
}
```

## Generating spring values

Do not write `linear()` values by hand. Use a generator tool:
- **Josh W. Comeau's Spring Generator**: https://www.joshwcomeau.com/animation/linear-timing-function/ (interactive playground)
- **CSS Springs Generator**: https://www.kvin.me/css-springs/how-to-use (stiffness/damping → CSS output)

These tools convert spring parameters (stiffness, damping, mass) into optimized `linear()` point lists. Store the output as CSS custom properties so you only compute them once.

## Common Mistakes
- Writing `linear()` values by hand — the curves need 30-70 data points for convincing springs; always use a generator
- Using springy animations for form inputs or data-heavy UIs — users want direct feedback, not a physics lesson; reserve bounce for personality moments
- No `@supports` fallback — `linear()` with many values is unparseable in older browsers; the transition silently fails
- Animating `height` or `width` with spring easing — layout-triggering + spring physics = jank on every bounce; use `transform: scaleY()` instead
- Using `--ease-spring-bouncy` for exit animations — bouncy exits feel wrong; enter with bounce, exit with standard ease-out

## See Also
- [Motion Design Tokens](motion-design-tokens.md) — where to store spring tokens alongside cubic-bezier curves
- [Animation Performance](animation-performance.md) — `linear()` runs on the compositor like any timing function
- [Accessibility and Motion](accessibility-and-motion.md) — spring bounce is a vestibular trigger; always reduce to static transitions
- Reference: [Josh W. Comeau: Springs and Bounces in Native CSS](https://www.joshwcomeau.com/animation/linear-timing-function/)
- Reference: [Chrome: CSS linear() Easing Function](https://developer.chrome.com/docs/css-ui/css-linear-easing-function)
- Reference: [PQINA: CSS Spring Animation with linear()](https://pqina.nl/blog/css-spring-animation-with-linear-easing-function)
