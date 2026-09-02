---
description: Animate elements in as they scroll into view — IntersectionObserver vs CSS scroll-driven, stagger timing, professional distance ranges
tldr: "Use entrance animations for content appearing on scroll to signal freshness and guide the eye. Use IntersectionObserver for wide browser support and precise control; use scroll-driven `animation-timeline: view()` for pure CSS progressive…"
---

# Entrance Animations

## When to Use
Content appearing on scroll should animate in to signal freshness and guide the eye. Two approaches: JavaScript IntersectionObserver (wider support, more control) and CSS-only scroll-driven animations (no JS, progressive enhancement).

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Wide browser support (all modern) | IntersectionObserver + CSS class toggle | Works everywhere, fire-once control |
| No JavaScript dependency | Scroll-driven `animation-timeline: view()` | Pure CSS, progressive enhancement |
| Staggered card grid reveals | IntersectionObserver + `transition-delay` | Precise control over stagger timing |
| Parallax-like scroll effects | `animation-timeline: scroll()` | Ties animation progress to scroll position |

## Professional vs Cheap Entrance Quality

| Quality | Translate Distance | Duration | Easing |
|---|---|---|---|
| **Professional** | 16-24px | 300-500ms | ease-out / decel |
| **Subtle/premium** | 8-12px | 250-350ms | ease-out |
| **Cheap/amateurish** | 50px+ | 800ms+ | linear or ease |
| **Distracting** | Any with bounce | 1000ms+ | ease-in-out with overshoot |

**Stagger timing rules:**
- Between sequential items: 50-100ms delay per item
- Sweet spot for card grids: 75ms
- Max total stagger: ~400ms (after that, early items feel frozen while late items are still arriving)

## Pattern

**IntersectionObserver approach:**

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity var(--duration-slow) var(--ease-emphasized-decel),
    transform var(--duration-slow) var(--ease-emphasized-decel);
}

.reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Staggered children */
.reveal-stagger > .reveal:nth-child(1) { transition-delay: 0ms; }
.reveal-stagger > .reveal:nth-child(2) { transition-delay: 75ms; }
.reveal-stagger > .reveal:nth-child(3) { transition-delay: 150ms; }
.reveal-stagger > .reveal:nth-child(4) { transition-delay: 225ms; }
```

```javascript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target); // Fire once
      }
    });
  },
  { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
```

**CSS-only scroll-driven reveal (no JavaScript):**

```css
@keyframes reveal-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.scroll-reveal {
  animation: reveal-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}

/* Fallback for browsers without scroll-driven support */
@supports not (animation-timeline: view()) {
  .scroll-reveal {
    opacity: 1;
    transform: none;
  }
}
```

> **Feature reference:** See [modern-css → scroll-driven-animations](../modern-css/scroll-driven-animations.md) for `animation-timeline`, `animation-range` syntax and browser support.

**Accessibility note:** Both approaches must respect `prefers-reduced-motion` — replace transform-based reveals with opacity-only crossfade or show content immediately. See [Accessibility and Motion](accessibility-and-motion.md).

## Common Mistakes
- Translate distance of 50px+ — feels like content is flying in from offscreen; 16-24px is the professional range
- No `@supports` fallback for scroll-driven animations — unsupported browsers show invisible content
- Forgetting `observer.unobserve()` — elements re-animate every time they scroll in and out
- Total stagger exceeding 400ms — early items feel frozen while waiting for late items
- Not testing entrance animations on page load — above-the-fold content should not animate in (it was never "off-screen")

## See Also
- [Motion Design Tokens](motion-design-tokens.md) — duration and easing values
- [Animation Performance](animation-performance.md) — `transform` + `opacity` are compositor-only
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling
- [Modern CSS Craft Patterns](modern-css-craft-patterns.md) — scroll-driven progress bar pattern
- [Parallax Effects](parallax-effects.md) — scroll-driven depth without entrance animation
- Reference: [Chrome: Scroll-Driven Animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)
