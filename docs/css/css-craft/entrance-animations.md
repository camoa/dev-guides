---
description: Animate elements in as they scroll into view — IntersectionObserver vs CSS scroll-driven, stagger timing, professional distance ranges
---

# Entrance Animations

## When to Use

> Use entrance animations for content appearing on scroll to signal freshness and guide the eye. Use IntersectionObserver for wide browser support and precise control; use scroll-driven `animation-timeline: view()` for pure CSS progressive enhancement.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Wide browser support (all modern) | IntersectionObserver + CSS class toggle | Works everywhere, fire-once control |
| No JavaScript dependency | Scroll-driven `animation-timeline: view()` | Pure CSS, progressive enhancement |
| Staggered card grid reveals | IntersectionObserver + `transition-delay` | Precise control over stagger timing |
| Parallax-like scroll effects | `animation-timeline: scroll()` | Ties animation progress to scroll position |

### Professional vs Cheap Entrance Quality

| Quality | Translate Distance | Duration | Easing |
|---------|--------------------|----------|--------|
| **Professional** | 16-24px | 300-500ms | ease-out / decel |
| **Subtle/premium** | 8-12px | 250-350ms | ease-out |
| **Cheap/amateurish** | 50px+ | 800ms+ | linear or ease |
| **Distracting** | Any with bounce | 1000ms+ | ease-in-out with overshoot |

Stagger timing: 50-100ms delay per item, 75ms sweet spot for card grids, max total stagger 400ms.

## Pattern

**IntersectionObserver:**
```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity var(--duration-slow) var(--ease-emphasized-decel),
    transform var(--duration-slow) var(--ease-emphasized-decel);
}
.reveal.is-visible { opacity: 1; transform: translateY(0); }
.reveal-stagger > .reveal:nth-child(1) { transition-delay: 0ms; }
.reveal-stagger > .reveal:nth-child(2) { transition-delay: 75ms; }
.reveal-stagger > .reveal:nth-child(3) { transition-delay: 150ms; }
```

```javascript
const observer = new IntersectionObserver(
  (entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target); // Fire once
    }
  }),
  { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
);
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
```

**CSS-only scroll-driven (no JavaScript):**
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
@supports not (animation-timeline: view()) {
  .scroll-reveal { opacity: 1; transform: none; }
}
```

## Common Mistakes

- **Wrong**: Translate distance of 50px+ — **Right**: 16-24px is the professional range
- **Wrong**: No `@supports` fallback for scroll-driven — **Right**: Unsupported browsers show invisible content
- **Wrong**: Forgetting `observer.unobserve()` — **Right**: Without it elements re-animate every scroll
- **Wrong**: Total stagger exceeding 400ms — **Right**: Early items feel frozen while late ones arrive
- **Wrong**: Animating above-the-fold content on load — **Right**: Content visible on load should not animate in

## See Also

- [Motion Design Tokens](motion-design-tokens.md) — duration and easing values
- [Animation Performance](animation-performance.md) — `transform` + `opacity` are compositor-only
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling
- [Modern CSS Craft Patterns](modern-css-craft-patterns.md) — scroll-driven progress bar pattern
- [Parallax Effects](parallax-effects.md) — scroll-driven depth without entrance animation
- Reference: [Chrome: Scroll-Driven Animations](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)
