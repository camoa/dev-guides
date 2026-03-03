---
description: Apply @starting-style, @property, scroll-driven animations, and view transitions for polished UI craft — application patterns with feature cross-references
---

# Modern CSS Craft Patterns

## When to Use

> Use this guide for applying modern CSS features to craft and polish. Feature syntax and browser support live in [modern-css.md](../modern-css/index.md). This guide covers the application patterns.

## Decision

| Situation | Choose | Cross-reference |
|-----------|--------|-----------------|
| Dialog/popover entry from `display: none` | `@starting-style` entry pattern | [modern-css → starting-style-transitions](../modern-css/starting-style-transitions.md) |
| Animated gradient hover | `@property` registered custom property | [modern-css → at-property](../modern-css/at-property.md) |
| Reading progress bar tied to scroll | `animation-timeline: scroll()` | [modern-css → scroll-driven-animations](../modern-css/scroll-driven-animations.md) |
| Smooth page-to-page transitions | View Transitions API | [modern-css → view-transitions](../modern-css/view-transitions.md) |
| Token-based semi-transparent colors | `color-mix()` with transparent | [modern-css → color-mix](../modern-css/color-mix.md) |
| Dynamic hover color shift | Relative color syntax in oklch | [modern-css → relative-color](../modern-css/relative-color.md) |

## Pattern

**Dialog entry with @starting-style:**
```css
dialog {
  opacity: 1; translate: 0 0;
  transition:
    opacity var(--duration-moderate) var(--ease-emphasized-decel),
    translate var(--duration-moderate) var(--ease-emphasized-decel),
    display var(--duration-moderate) allow-discrete,
    overlay var(--duration-moderate) allow-discrete;
  @starting-style { opacity: 0; translate: 0 -1rem; }
}
dialog:not([open]) { opacity: 0; translate: 0 -1rem; }
```

Three required pieces: `@starting-style` block, `transition-behavior: allow-discrete` on `display`, and `overlay` transition for top-layer elements.

**Gradient animation with @property:**
```css
@property --gradient-start { syntax: "<color>"; initial-value: #6366f1; inherits: false; }
@property --gradient-end   { syntax: "<color>"; initial-value: #8b5cf6; inherits: false; }

.gradient-btn {
  background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
  transition:
    --gradient-start var(--duration-moderate) var(--ease-standard),
    --gradient-end var(--duration-moderate) var(--ease-standard);
}
.gradient-btn:hover { --gradient-start: #4f46e5; --gradient-end: #7c3aed; }
```

**Scroll-driven reading progress bar:**
```css
.progress-bar {
  position: fixed; top: 0; left: 0;
  width: 100%; height: 3px;
  background: var(--color-primary);
  transform-origin: 0 0;
  animation: grow-width linear;
  animation-timeline: scroll(root);
  z-index: 1000;
}
@keyframes grow-width { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@supports not (animation-timeline: scroll()) { .progress-bar { display: none; } }
```

Uses `scaleX` instead of `width` — compositor-only. See [Animation Performance](animation-performance.md).

**View transitions for page navigation:**
```css
@view-transition { navigation: auto; }
.hero-image { view-transition-name: hero; }
::view-transition-old(hero) { animation: fade-out var(--duration-moderate) var(--ease-accel); }
::view-transition-new(hero) { animation: fade-in var(--duration-moderate) var(--ease-decel); }
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(hero), ::view-transition-new(hero) { animation-duration: var(--duration-fast); }
}
```

**Dynamic hover with relative color syntax:**
```css
.button:hover { background: oklch(from var(--color-primary) calc(l - 0.1) c h); }
.card { background: oklch(from var(--color-primary) 95% calc(c * 0.3) h); }
```

## Common Mistakes

- **Wrong**: Missing `overlay` transition on `@starting-style` for top-layer — **Right**: Element pops to top-layer before animating without it
- **Wrong**: Forgetting `@property` registration before animating — **Right**: Browsers snap unregistered custom properties instead of interpolating
- **Wrong**: `width` animation for progress bar — **Right**: Use `scaleX` for compositor-only performance
- **Wrong**: Duplicate `view-transition-name` values — **Right**: Names must be unique per page
- **Wrong**: No `@supports` or `@media` fallbacks — **Right**: Unsupported browsers show broken/invisible content

## See Also

- [Entrance Animations](entrance-animations.md) — scroll-driven reveal patterns
- [Animation Performance](animation-performance.md) — why `scaleX` over `width`
- [Accessibility and Motion](accessibility-and-motion.md) — reduced-motion for view transitions
- Reference: [modern-css.md](../modern-css/index.md) — feature syntax and browser support for all referenced features
