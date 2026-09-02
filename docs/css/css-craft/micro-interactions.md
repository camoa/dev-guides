---
description: Polish hover, active, and focus states on buttons, cards, links, and toggles — the difference between a flat prototype and a production interface
tldr: "Use micro-interactions on every interactive element (buttons, cards, links, toggles). These are the difference between a flat prototype and a production interface."
---

# Micro-Interactions

## When to Use
Every interactive element (buttons, cards, links, toggles) needs hover, active, and focus states. These are the difference between a flat prototype and a production interface.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Card hover lift | `translateY(-2px)` + shadow increase | Subtle lift implies interactivity |
| Button press feedback | `scale(0.97)` with instant duration | Physical "push" feeling |
| Link hover indicator | Background-image underline reveal | Smoother than `text-decoration` transitions |
| Icon hover | `filter: brightness(1.08)` | Avoids layout shift, works on any element |
| Toggle state | `background-color` + `transform` | Color signals state, transform signals motion |

## Professional vs Cheap Quality

| Quality | Translate | Duration | Easing | Effect |
|---|---|---|---|---|
| **Professional** | 2-4px | 150-200ms | ease-out / standard | Subtle, responsive, confident |
| **Subtle/premium** | 1-2px | 100-150ms | ease-out | Barely perceptible, high-end feel |
| **Cheap/amateur** | 10px+ | 800ms+ | linear or ease | Floaty, distracting, uncontrolled |
| **Distracting** | Any with bounce | 1000ms+ | ease-in-out with overshoot | Calls attention to the animation itself |

## Pattern

**Card hover:**
```css
.card {
  transition:
    transform var(--duration-normal) var(--ease-standard),
    box-shadow var(--duration-normal) var(--ease-standard);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow:
    0 4px 6px hsl(var(--shadow-color) / 0.1),
    0 8px 15px hsl(var(--shadow-color) / 0.1);
}

.card:active {
  transform: translateY(0) scale(0.98);
  transition-duration: var(--duration-quick);
}
```

**Button press:**
```css
.btn {
  transition:
    background-color var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.btn:hover {
  filter: brightness(1.08);
  transform: translateY(-1px);
}

.btn:active {
  transform: scale(0.97);
  transition-duration: var(--duration-instant);
}
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

.link:hover {
  background-size: 100% 1px;
}
```

**Accessibility note:** All hover interactions must have `:focus-visible` equivalents. Active press (`scale(0.97)`) should use `--duration-instant` so it never feels laggy. See [Accessibility and Motion](accessibility-and-motion.md) for `prefers-reduced-motion` handling.

## Common Mistakes
- Animating only hover with no active state — the element feels unresponsive when clicked
- Using the same duration for hover-in and active — active must be faster (instant) for press feedback
- `translateY(-10px)` on hover — too much movement; 2-4px is the professional range
- Missing `transition` declaration on the base state — the hover snaps on and eases off (or vice versa)
- Using `margin-top` or `top` instead of `transform` for hover lift — triggers layout, causes jank

## See Also
- [Motion Design Tokens](motion-design-tokens.md) — the easing and duration values used here
- [Elevation and Shadows](elevation-and-shadows.md) — shadow values for hover lift
- [Animation Performance](animation-performance.md) — why `transform` instead of `top`
- [Accessibility and Motion](accessibility-and-motion.md) — reduced-motion alternatives
