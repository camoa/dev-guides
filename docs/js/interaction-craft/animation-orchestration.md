---
description: "Sequence, cancel, and coordinate JS animations — when to use CSS transitions, WAAPI element.animate(), or requestAnimationFrame loops"
tldr: "Use CSS transitions for simple state changes. Use WAAPI (`element.animate()`) when you need JS-driven values, sequencing, or mid-animation cancellation."
---

# Animation Orchestration

## When to Use

> When CSS transitions are not enough — you need to sequence animations, respond to mid-animation interruptions, coordinate multiple elements' timing, or build a custom animation loop with JavaScript control.

## Decision: CSS vs WAAPI vs rAF Loop

| If you need... | Use... | Why |
|---|---|---|
| Simple state transitions (hover, toggle) | CSS `transition` | Simplest; GPU-composited; browser optimizes |
| Predefined keyframe animation | CSS `@keyframes` | Declarative; no JS; best for looping or self-contained sequences |
| Dynamic values (from JS variables, user input) | WAAPI (`element.animate()`) | CSS cannot use JS values; WAAPI can |
| Sequence: A completes then B starts | WAAPI with `.finished` promise | `animation.finished` resolves when done; chain with `await` |
| Interrupt/cancel a running animation | WAAPI `.cancel()` or `.reverse()` | CSS cannot be interrupted mid-animation and reversed cleanly |
| Custom physics, particle systems, canvas | `requestAnimationFrame` loop | Full control; runs every display frame |
| Coordinating CSS class adds with timing | `setTimeout` + `transitionend` event | Add class, wait for transition, then do next step |

## Pattern: WAAPI Basics

```javascript
// Play an animation imperatively
const anim = element.animate(
  [
    { opacity: 0, transform: 'translateY(20px)' },
    { opacity: 1, transform: 'translateY(0)' },
  ],
  { duration: 300, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)', fill: 'forwards' }
);

// Cancel before completion
anim.cancel();

// Reverse mid-animation (for hover-out)
anim.reverse();

// Wait for completion before doing next action
await anim.finished;
doNextStep();
```

## Pattern: Promise-Based Sequencing

```javascript
async function animateSequence(elements) {
  for (const el of elements) {
    await el.animate(
      [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 250, easing: 'ease-out', fill: 'forwards' }
    ).finished;
    // Each element waits for the previous to complete
  }
}

// Parallel with stagger (don't await — start all, then wait for last)
async function animateStagger(elements, staggerMs = 75) {
  const animations = elements.map((el, i) =>
    el.animate(
      [{ opacity: 0 }, { opacity: 1 }],
      { duration: 300, delay: i * staggerMs, fill: 'forwards' }
    )
  );
  await animations.at(-1).finished; // Wait for last to complete
}
```

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

## Pattern: JS + CSS Coordination

```javascript
// Add class, then remove after transition completes
function animateIn(element) {
  element.classList.add('is-entering');
  element.addEventListener('transitionend', () => {
    element.classList.remove('is-entering');
    element.classList.add('is-visible');
  }, { once: true });
}

// Cross-fade between two elements
async function crossFade(outEl, inEl) {
  outEl.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 200, fill: 'forwards' });
  await inEl.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, fill: 'forwards' }).finished;
  outEl.style.display = 'none';
}
```

## WAAPI Key Properties

| Property | Values | Notes |
|---|---|---|
| `fill` | `'none'`, `'forwards'`, `'backwards'`, `'both'` | `'forwards'` keeps end state applied after finish |
| `easing` | Any CSS easing string | Same values as CSS `transition-timing-function` |
| `iterations` | Number or `Infinity` | `Infinity` for infinite loops |
| `direction` | `'normal'`, `'reverse'`, `'alternate'` | Use `'alternate'` for ping-pong loops |
| `delay` | ms | Positive = start delay; use for stagger |
| `composite` | `'replace'`, `'add'`, `'accumulate'` | `'add'` for layering animations on same property |

## Common Mistakes

- **Using `fill: 'forwards'` without calling `.cancel()` later** — WAAPI holds a reference to the element; can cause memory leaks in SPAs
- **`await animation.finished` without error handling** — `.finished` rejects if `.cancel()` is called; wrap in try/catch
- **Using rAF loop for simple transitions** — overkill; CSS transitions are simpler and GPU-composited
- **Sequencing with `setTimeout` guesses** — fragile timing that drifts; use `.finished` promise instead
- **Forgetting `prefers-reduced-motion` check** — WAAPI animations bypass CSS `@media (prefers-reduced-motion)`; check manually

```javascript
// Always check reduced motion before WAAPI animations
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const duration = prefersReduced ? 0 : 300;
element.animate(keyframes, { duration, fill: 'forwards' });
```

## See Also

- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — coordinating IntersectionObserver with WAAPI
- [Spring Physics and Advanced Easing](../../css/css-craft/spring-physics-and-advanced-easing.md) — easing values to use in WAAPI options
- [Animation Performance](../../css/css-craft/animation-performance.md) — compositor-safe properties for WAAPI keyframes
- Reference: [MDN: Using the Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API)
- Reference: [CSS-Tricks: CSS Animations vs Web Animations API](https://css-tricks.com/css-animations-vs-web-animations-api/)
