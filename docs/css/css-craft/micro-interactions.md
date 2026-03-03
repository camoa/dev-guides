---
description: Polish hover, active, and focus states on buttons, cards, links, and toggles — the difference between a flat prototype and a production interface
---

# Micro-Interactions

## When to Use

> Use micro-interactions on every interactive element (buttons, cards, links, toggles). These are the difference between a flat prototype and a production interface. Every element needs hover, active, and focus states.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Card hover lift | `translateY(-2px)` + shadow increase | Subtle lift implies interactivity |
| Button press feedback | `scale(0.97)` with instant duration | Physical "push" feeling |
| Link hover indicator | Background-image underline reveal | Smoother than `text-decoration` transitions |
| Icon hover | `filter: brightness(1.08)` | Avoids layout shift, works on any element |
| Toggle state | `background-color` + `transform` | Color signals state, transform signals motion |

### Professional vs Cheap Quality

| Quality | Translate | Duration | Easing | Effect |
|---------|-----------|----------|--------|--------|
| **Professional** | 2-4px | 150-200ms | ease-out / standard | Subtle, responsive, confident |
| **Subtle/premium** | 1-2px | 100-150ms | ease-out | Barely perceptible, high-end feel |
| **Cheap/amateur** | 10px+ | 800ms+ | linear or ease | Floaty, distracting, uncontrolled |
| **Distracting** | Any with bounce | 1000ms+ | ease-in-out with overshoot | Calls attention to the animation |

## Pattern

**Card hover:**
```css
.card {
  transition:
    transform var(--duration-normal) var(--ease-standard),
    box-shadow var(--duration-normal) var(--ease-standard);
}
.card:hover { transform: translateY(-2px); }
.card:active { transform: translateY(0) scale(0.98); transition-duration: var(--duration-quick); }
```

**Button press:**
```css
.btn {
  transition:
    background-color var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard);
}
.btn:hover { filter: brightness(1.08); transform: translateY(-1px); }
.btn:active { transform: scale(0.97); transition-duration: var(--duration-instant); }
```

**Link underline reveal:**
```css
.link {
  text-decoration: none;
  background-image: linear-gradient(currentColor, currentColor);
  background-position: 0% 100%;
  background-repeat: no-repeat;
  background-size: 0% 1px;
  transition: background-size var(--duration-normal) var(--ease-standard);
}
.link:hover { background-size: 100% 1px; }
```

All hover interactions must have `:focus-visible` equivalents. See [Accessibility and Motion](accessibility-and-motion.md).

## Common Mistakes

- **Wrong**: Animating hover with no active state — **Right**: Always add an active state; the element feels unresponsive without it
- **Wrong**: Same duration for hover-in and active — **Right**: Active must use `--duration-instant` for press feedback
- **Wrong**: `translateY(-10px)` on hover — **Right**: 2-4px is the professional range
- **Wrong**: Missing `transition` on the base state — **Right**: Without it, hover snaps on and eases off (or vice versa)
- **Wrong**: `margin-top` or `top` for hover lift — **Right**: Use `transform: translateY()` to avoid layout jank

## See Also

- [Motion Design Tokens](motion-design-tokens.md) — the easing and duration values used here
- [Elevation and Shadows](elevation-and-shadows.md) — shadow values for hover lift
- [Animation Performance](animation-performance.md) — why `transform` instead of `top`
- [Accessibility and Motion](accessibility-and-motion.md) — reduced-motion alternatives
