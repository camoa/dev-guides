---
description: Handle prefers-reduced-motion, focus rings, and forced-colors — WCAG-compliant motion alternatives and keyboard accessibility patterns
tldr: "Apply reduced-motion handling to every animation pattern. WCAG 2.1 SC 2.3.3 requires it."
---

# Accessibility and Motion

## When to Use
Every motion pattern in this guide must accommodate users who experience motion sickness, vestibular disorders, or seizure conditions. This is not optional — WCAG 2.1 SC 2.3.3 requires it.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Reduced motion for all animations | `@media (prefers-reduced-motion: reduce)` | System-level user preference |
| Alternative to killing all motion | Replace transform-based with opacity crossfade | Users still get state feedback without spatial motion |
| Keyboard focus indicator | `:focus-visible` with 2px 3:1 contrast ring | Only shows for keyboard nav, not mouse clicks |
| High contrast mode support | `@media (forced-colors: active)` | Windows High Contrast, some assistive tech |
| JS-side motion detection | `matchMedia('(prefers-reduced-motion: reduce)')` | Skip IntersectionObserver animations |

## Pattern

**Option A — Universal kill switch** (quick but removes all feedback):
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Option B (preferred) — Crossfade replacement** (users still get visual feedback, just without spatial motion):
```css
@media (prefers-reduced-motion: reduce) {
  .reveal {
    transform: none;
    transition: opacity var(--duration-moderate) var(--ease-standard);
  }

  .card:hover {
    transform: none;
    box-shadow: none;
    filter: brightness(1.05);
  }

  .scroll-reveal {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

**JavaScript detection:**
```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
);

if (prefersReducedMotion.matches) {
  // Skip IntersectionObserver setup, or set duration to 0
}

// Listen for mid-session preference changes
prefersReducedMotion.addEventListener('change', (e) => {
  document.documentElement.classList.toggle('reduce-motion', e.matches);
});
```

**Focus-visible pattern:**
```css
/* Standard — outline with offset */
:focus-visible {
  outline: 2px solid var(--color-focus, currentColor);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}

/* Advanced — double ring that follows border-radius */
:where(a, button, input, textarea, select, [tabindex]):focus-visible {
  outline: none;
  box-shadow:
    0 0 0 2px var(--color-background),     /* Gap ring */
    0 0 0 4px var(--color-focus, currentColor); /* Focus ring */
}

/* Forced colors mode fallback — box-shadow is invisible */
@media (forced-colors: active) {
  :focus-visible {
    outline: 2px solid LinkText;
    outline-offset: 2px;
    box-shadow: none;
  }
}
```

## WCAG Checklist for CSS Craft

| Requirement | WCAG | Rule |
|---|---|---|
| Respect `prefers-reduced-motion` | 2.3.3 | Replace spatial motion with crossfade, not removal |
| Focus indicator contrast | 1.4.11 | 3:1 minimum contrast, 2px minimum thickness |
| Auto-playing animation >5s | 2.2.2 | Must have pause/stop controls |
| Motion as sole state indicator | 1.3.3 | Never — always pair with color, icon, or text change |
| Hover content must be keyboard accessible | 1.4.13 | Match `:hover` interactions with `:focus-visible` |
| Forced colors support | 1.4.11 | Functional indicators must survive `forced-colors: active` |
| Flashing content | 2.3.1 | No more than 3 flashes per second |

## Common Mistakes
- Using `prefers-reduced-motion` as a kill switch only — users lose ALL feedback; replace motion with crossfade instead
- `:focus-visible` ring that disappears on dark backgrounds — test on both light and dark themes
- `box-shadow` focus ring without `forced-colors` fallback — `box-shadow` is invisible in Windows High Contrast mode
- Hover-only interactions with no keyboard equivalent — screen readers and keyboard users cannot access hover content
- Removing `outline` globally (`* { outline: none }`) — destroys keyboard navigation; use `:focus:not(:focus-visible)` instead

## See Also
- [Micro-Interactions](micro-interactions.md) — hover/focus patterns that need accessibility treatment
- [Entrance Animations](entrance-animations.md) — scroll reveal reduced-motion alternatives
- Reference: [Pope Tech: Accessible Animation and Movement](https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/)
- Reference: [Piccalilli: Focus Ring Problem](https://piccalil.li/blog/taking-a-shot-at-the-double-focus-ring-problem-using-modern-css/)
- Reference: [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
