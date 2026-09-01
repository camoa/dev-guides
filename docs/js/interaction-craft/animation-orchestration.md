---
description: Sequence, cancel, and coordinate JS animations — when to use CSS transitions, WAAPI element.animate(), or requestAnimationFrame loops
tldr: "Use CSS transitions for simple state changes. Use WAAPI (`element.animate()`) when you need JS-driven values, sequencing, or mid-animation cancellation."
---

# Animation Orchestration

## When to Use

> Use CSS transitions for simple state changes. Use WAAPI (`element.animate()`) when you need JS-driven values, sequencing, or mid-animation cancellation. Use rAF loops only for custom physics or canvas.

## Pattern: requestAnimationFrame Custom Loop

```javascript
class AnimationLoop {
  #rafId = null;
  #startTime = null;

  start(drawFn, duration) {
    this.#startTime = null;
    const tick = (timestamp) => {
      this.#startTime ??= timestamp;
      const elapsed = timestamp - this.#startTime;
      const progress = Math.min(elapsed / duration, 1);
      drawFn(progress);
      if (progress < 1) this.#rafId = requestAnimationFrame(tick);
    };
    this.#rafId = requestAnimationFrame(tick);
  }

  stop() {
    if (this.#rafId) cancelAnimationFrame(this.#rafId);
    this.#rafId = null;
  }
}
```

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple state transitions (hover, toggle) | CSS `transition` | Simplest; GPU-composited; browser optimizes |
| Predefined keyframe animation | CSS `@keyframes` | Declarative; no JS; best for looping sequences |
| Dynamic values from JS variables | WAAPI (`element.animate()`) | CSS cannot use JS values; WAAPI can |
| Sequence: A completes then B starts | WAAPI with `.finished` promise | Chain with `await animation.finished` |
| Interrupt/cancel a running animation | WAAPI `.cancel()` or `.reverse()` | CSS cannot be interrupted mid-animation cleanly |
| Custom physics, particle systems, canvas | `requestAnimationFrame` loop | Full control; runs every display frame |
| CSS class timing coordination | `setTimeout` + `transitionend` event | Add class, wait for transition, then next step |

## Pattern

```javascript
// WAAPI basics
const anim = element.animate(
  [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' }],
  { duration: 300, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)', fill: 'forwards' }
);
anim.cancel();   // Cancel before completion
anim.reverse();  // Reverse mid-animation (hover-out)
await anim.finished; // Wait for completion

// Sequence — each element waits for previous to complete
async function animateSequence(elements) {
  for (const el of elements) {
    await el.animate(
      [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 250, easing: 'ease-out', fill: 'forwards' }
    ).finished;
  }
}

// Stagger — start all, wait for last
async function animateStagger(elements, staggerMs = 75) {
  const anims = elements.map((el, i) =>
    el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: i * staggerMs, fill: 'forwards' })
  );
  await anims.at(-1).finished;
}

// Always check reduced motion for WAAPI (CSS @media doesn't catch it)
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
element.animate(keyframes, { duration: prefersReduced ? 0 : 300, fill: 'forwards' });
```

**WAAPI key properties:**

| Property | Values | Notes |
|---|---|---|
| `fill` | `'none'`, `'forwards'`, `'backwards'`, `'both'` | `'forwards'` keeps end state applied after finish |
| `easing` | Any CSS easing string | Same values as CSS `transition-timing-function` |
| `iterations` | Number or `Infinity` | `Infinity` for infinite loops |
| `direction` | `'normal'`, `'reverse'`, `'alternate'` | `'alternate'` for ping-pong loops |
| `delay` | ms | Positive = start delay; use for stagger |

## Common Mistakes

- **Wrong**: `fill: 'forwards'` without `.cancel()` later → **Right**: WAAPI holds an element reference; causes memory leaks in SPAs
- **Wrong**: `await animation.finished` without error handling → **Right**: `.finished` rejects if `.cancel()` is called; wrap in try/catch
- **Wrong**: rAF loop for simple transitions → **Right**: CSS transitions are simpler and GPU-composited for basic cases
- **Wrong**: Sequencing with `setTimeout` guesses → **Right**: Timing drifts; use `.finished` promise instead
- **Wrong**: Forgetting `prefers-reduced-motion` check for WAAPI → **Right**: WAAPI bypasses CSS `@media (prefers-reduced-motion)`; check manually

## See Also

- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — coordinating IntersectionObserver with WAAPI
- Reference: [MDN: Using the Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API)
- Reference: [CSS-Tricks: CSS Animations vs Web Animations API](https://css-tricks.com/css-animations-vs-web-animations-api/)
