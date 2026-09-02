---
description: Apply @starting-style, @property, scroll-driven animations, and view transitions for polished UI craft — application patterns with feature cross-references
tldr: "Use this guide for applying modern CSS features to craft and polish. Feature syntax and browser support live in [modern-css.md](../modern-css/index.md)."
---

# Modern CSS Craft Patterns

## When to Use
When applying modern CSS features covered in `modern-css.md` for craft and polish purposes. This section shows the **application patterns** — the feature syntax and browser support live in the feature reference guide.

## Decision
| If you need... | Use... | Cross-reference |
|---|---|---|
| Dialog/popover entry animation from `display: none` | `@starting-style` entry pattern | [modern-css → starting-style-transitions](../modern-css/starting-style-transitions.md) |
| Animated gradient hover | `@property` registered custom property | [modern-css → at-property](../modern-css/at-property.md) |
| Reading progress bar tied to scroll | `animation-timeline: scroll()` | [modern-css → scroll-driven-animations](../modern-css/scroll-driven-animations.md) |
| Smooth page-to-page transitions | View Transitions API | [modern-css → view-transitions](../modern-css/view-transitions.md) |
| Token-based semi-transparent colors | `color-mix()` with transparent | [modern-css → color-mix](../modern-css/color-mix.md) |
| Dynamic hover color shift | Relative color syntax in oklch | [modern-css → relative-color](../modern-css/relative-color.md) |

## Pattern

**Dialog entry with @starting-style:**

> **Feature reference:** See [modern-css → starting-style-transitions](../modern-css/starting-style-transitions.md) for `@starting-style` syntax and browser support.

```css
dialog {
  opacity: 1;
  translate: 0 0;
  transition:
    opacity var(--duration-moderate) var(--ease-emphasized-decel),
    translate var(--duration-moderate) var(--ease-emphasized-decel),
    display var(--duration-moderate) allow-discrete,
    overlay var(--duration-moderate) allow-discrete;

  @starting-style {
    opacity: 0;
    translate: 0 -1rem;
  }
}

/* Exit state */
dialog:not([open]) {
  opacity: 0;
  translate: 0 -1rem;
}
```

Three required pieces: `@starting-style` block for entry state, `transition-behavior: allow-discrete` on `display`, and `overlay` transition for top-layer elements.

**Gradient animation with @property:**

> **Feature reference:** See [modern-css → at-property](../modern-css/at-property.md) for `@property` syntax and browser support.

```css
@property --gradient-start {
  syntax: "<color>";
  initial-value: #6366f1;
  inherits: false;
}

@property --gradient-end {
  syntax: "<color>";
  initial-value: #8b5cf6;
  inherits: false;
}

.gradient-btn {
  background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
  transition:
    --gradient-start var(--duration-moderate) var(--ease-standard),
    --gradient-end var(--duration-moderate) var(--ease-standard);
}

.gradient-btn:hover {
  --gradient-start: #4f46e5;
  --gradient-end: #7c3aed;
}
```

Without `@property` registration, browsers cannot interpolate custom properties — the gradient would snap instead of transitioning.

**Scroll-driven reading progress bar:**

> **Feature reference:** See [modern-css → scroll-driven-animations](../modern-css/scroll-driven-animations.md) for `animation-timeline` syntax and browser support.

```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--color-primary);
  transform-origin: 0 0;
  animation: grow-width linear;
  animation-timeline: scroll(root);
  z-index: 1000;
}

@keyframes grow-width {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

@supports not (animation-timeline: scroll()) {
  .progress-bar { display: none; }
}
```

Uses `scaleX` instead of `width` for compositor-only performance. See [Animation Performance](animation-performance.md).

**View transitions for page navigation:**

> **Feature reference:** See [modern-css → view-transitions](../modern-css/view-transitions.md) for View Transitions API syntax and browser support.

```css
/* Cross-document MPA — enable on both pages */
@view-transition { navigation: auto; }

/* Named element morphing */
.hero-image { view-transition-name: hero; }

::view-transition-old(hero) {
  animation: fade-out var(--duration-moderate) var(--ease-accel);
}
::view-transition-new(hero) {
  animation: fade-in var(--duration-moderate) var(--ease-decel);
}

/* Reduce motion: crossfade only */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(hero),
  ::view-transition-new(hero) {
    animation-duration: var(--duration-fast);
  }
}
```

**Dynamic hover with relative color syntax:**

> **Feature reference:** See [modern-css → relative-color](../modern-css/relative-color.md) for relative color syntax and browser support.

```css
.button:hover {
  /* Darken primary color by reducing lightness */
  background: oklch(from var(--color-primary) calc(l - 0.1) c h);
}

.card {
  /* Muted background — low chroma version of primary */
  background: oklch(from var(--color-primary) 95% calc(c * 0.3) h);
}
```

## Common Mistakes
- Missing `overlay` transition on `@starting-style` for top-layer elements — the element pops to top-layer before animating
- Forgetting `@property` registration before animating custom properties — browsers snap the value instead of interpolating
- Using `width` animation for progress bar instead of `scaleX` — triggers layout on every scroll frame
- View transition names must be unique per page — two elements with the same `view-transition-name` cause a conflict
- No `@supports` or `@media` fallbacks — users on unsupported browsers get broken/invisible content

## See Also
- [Entrance Animations](entrance-animations.md) — scroll-driven reveal patterns
- [Animation Performance](animation-performance.md) — why `scaleX` over `width`
- [Accessibility and Motion](accessibility-and-motion.md) — reduced-motion for view transitions
- Reference: [modern-css](../modern-css/index.md) — feature syntax and browser support for all referenced features
