---
description: Handle prefers-reduced-motion, focus rings, and forced-colors — WCAG-compliant motion alternatives and keyboard accessibility patterns
tldr: "Apply reduced-motion handling to every animation pattern. WCAG 2.1 SC 2.3.3 requires it."
---

# Accessibility and Motion

## When to Use

> Apply reduced-motion handling to every animation pattern. WCAG 2.1 SC 2.3.3 requires it. Replace motion with crossfade — do not use a kill switch that removes all feedback.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Reduced motion for all animations | `@media (prefers-reduced-motion: reduce)` | System-level user preference |
| Alternative to killing all motion | Replace transform-based with opacity crossfade | Users still get state feedback without spatial motion |
| Keyboard focus indicator | `:focus-visible` with 2px 3:1 contrast ring | Only shows for keyboard nav, not mouse clicks |
| High contrast mode support | `@media (forced-colors: active)` | Windows High Contrast, some assistive tech |
| JS-side motion detection | `matchMedia('(prefers-reduced-motion: reduce)')` | Skip IntersectionObserver animations |

## Pattern

**Option A — Kill switch** (quick but removes all feedback):
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Option B (preferred) — Crossfade replacement:**
```css
@media (prefers-reduced-motion: reduce) {
  .reveal { transform: none; transition: opacity var(--duration-moderate) var(--ease-standard); }
  .card:hover { transform: none; filter: brightness(1.05); }
  .scroll-reveal { animation: none; opacity: 1; transform: none; }
}
```

**JavaScript detection:**
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (prefersReducedMotion.matches) { /* skip animations */ }
prefersReducedMotion.addEventListener('change', (e) => {
  document.documentElement.classList.toggle('reduce-motion', e.matches);
});
```

**Focus-visible with forced-colors fallback:**
```css
:where(a, button, input, [tabindex]):focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-background), 0 0 0 4px var(--color-focus, currentColor);
}
@media (forced-colors: active) {
  :focus-visible { outline: 2px solid LinkText; outline-offset: 2px; box-shadow: none; }
}
```

### WCAG Checklist

| Requirement | WCAG | Rule |
|-------------|------|------|
| `prefers-reduced-motion` | 2.3.3 | Replace spatial motion with crossfade, not removal |
| Focus indicator contrast | 1.4.11 | 3:1 minimum, 2px minimum thickness |
| Auto-playing animation >5s | 2.2.2 | Must have pause/stop controls |
| Motion as sole state indicator | 1.3.3 | Never — pair with color, icon, or text |
| Hover content keyboard accessible | 1.4.13 | Match `:hover` with `:focus-visible` |
| Forced colors | 1.4.11 | Functional indicators must work in `forced-colors: active` |
| Flashing content | 2.3.1 | No more than 3 flashes per second |

## Common Mistakes

- **Wrong**: `prefers-reduced-motion` as kill switch only — **Right**: Replace with crossfade; users lose all feedback with kill switch
- **Wrong**: Focus ring invisible on dark backgrounds — **Right**: Test on both light and dark themes
- **Wrong**: `box-shadow` focus ring without `forced-colors` fallback — **Right**: `box-shadow` is invisible in Windows High Contrast mode
- **Wrong**: Hover-only interactions — **Right**: Always add keyboard equivalents for screen reader and keyboard users
- **Wrong**: `* { outline: none }` globally — **Right**: Use `:focus:not(:focus-visible)` to hide outline for mouse only

## See Also

- [Micro-Interactions](micro-interactions.md) — hover/focus patterns that need accessibility treatment
- [Entrance Animations](entrance-animations.md) — scroll reveal reduced-motion alternatives
- Reference: [Pope Tech: Accessible Animation and Movement](https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/)
- Reference: [Piccalilli: Focus Ring Problem](https://piccalil.li/blog/taking-a-shot-at-the-double-focus-ring-problem-using-modern-css/)
- Reference: [MDN: prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion)
