---
description: Skeleton loading screens and shimmer animations — shimmer vs pulse, explicit dimensions for CLS, dark mode tokens, ARIA markup
tldr: "Use skeleton screens for content-heavy components (cards, feeds, profiles) — they reduce perceived wait by showing the layout shape. Use spinners for actions with indeterminate duration (form submit, file upload)."
---

# Skeleton and Loading States

## When to Use

> Use skeleton screens for content-heavy components (cards, feeds, profiles) — they reduce perceived wait by showing the layout shape. Use spinners for actions with indeterminate duration (form submit, file upload). Never skeleton an entire page.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Content placeholder while data loads | Skeleton screen with shimmer | Matches content shape; reduces layout shift |
| Simple loading indicator | CSS `opacity` pulse animation | Low overhead; small scope |
| Skeleton matching exact content layout | Set explicit dimensions matching real content | Prevents CLS when content swaps in |
| Reduced motion fallback | Replace shimmer with slow pulse | Shimmer sweeps across screen — motion-sensitive users |
| Dark mode skeleton | CSS custom properties for all skeleton colors | One set of tokens, overridden per theme |

## Pattern

**Shimmer skeleton:**
```css
:root {
  --skeleton-bg: hsl(220 15% 90%);
  --skeleton-shine: hsl(220 15% 97%);
  --skeleton-speed: 1.5s;
}
[data-theme="dark"] {
  --skeleton-bg: hsl(220 15% 18%);
  --skeleton-shine: hsl(220 15% 25%);
}

.skeleton {
  background: linear-gradient(90deg, var(--skeleton-bg) 25%, var(--skeleton-shine) 50%, var(--skeleton-bg) 75%);
  background-size: 400% 100%;
  border-radius: 4px;
  @media (prefers-reduced-motion: no-preference) { animation: skeleton-shimmer var(--skeleton-speed) ease-in-out infinite; }
  @media (prefers-reduced-motion: reduce)        { animation: skeleton-pulse 2s ease-in-out infinite; }
}
@keyframes skeleton-shimmer { from { background-position: 200% 0; } to { background-position: -200% 0; } }
@keyframes skeleton-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
```

**Card skeleton structure — explicit dimensions prevent layout shift:**
```css
.skeleton-card { display: flex; flex-direction: column; gap: 12px; padding: 16px; }
.skeleton-avatar { width: 48px; height: 48px; border-radius: 50%; }
.skeleton-title  { height: 20px; width: 60%; }
.skeleton-body   { height: 14px; width: 100%; }
.skeleton-body + .skeleton-body { width: 80%; }
```

All `skeleton-*` elements also get the `.skeleton` class for the animation.

**ARIA markup:**
```html
<div role="status" aria-busy="true" aria-label="Loading article content">
  <div class="skeleton-card">
    <div class="skeleton skeleton-title"></div>
    <div class="skeleton skeleton-body"></div>
  </div>
  <span class="visually-hidden">Loading...</span>
</div>
```

Update `aria-busy="false"` and replace skeleton markup when content loads.

## Common Mistakes

- **Wrong**: Skeleton with no explicit dimensions — **Right**: Match skeleton dimensions to real content; avoids CLS score degradation
- **Wrong**: `background-position` animation without `background-size: 400%` — **Right**: The gradient doesn't travel far enough without it
- **Wrong**: Shimmer on fixed/sticky elements — **Right**: Compositing issues on some browsers; keep skeletons in normal flow
- **Wrong**: No ARIA markup — **Right**: `role="status"` and `aria-busy` are required for screen readers
- **Wrong**: Shimmer for reduced-motion users — **Right**: The sweep is motion; swap for opacity pulse instead

## See Also

- [Animation Performance](animation-performance.md) — `background-position` animation is paint-only; limit element count
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling
- [Opacity and Visual Hierarchy](opacity-and-visual-hierarchy.md) — pulse animation uses opacity tokens
- Reference: [Frontend Hero: CSS Skeleton Loaders](https://frontend-hero.com/how-to-create-skeleton-loader)
- Reference: [MDN: ARIA status role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/status_role)
