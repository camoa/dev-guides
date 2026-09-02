---
description: Skeleton loading screens and shimmer animations — shimmer vs pulse, explicit dimensions for CLS, dark mode tokens, ARIA markup
tldr: "Use skeleton screens for content-heavy components (cards, feeds, profiles) — they reduce perceived wait by showing the layout shape. Use spinners for actions with indeterminate duration (form submit, file upload)."
---

# Skeleton and Loading States

## When to Use
Skeleton screens show a structural placeholder of the content being loaded — same layout, no real data. They reduce perceived wait time by giving users something to look at that matches the shape of what's coming. Use skeleton screens for content-heavy components (cards, feeds, profiles). Use a spinner for actions with indeterminate duration (form submission, file upload). Never skeleton an entire page — show whatever is available immediately and skeleton only the async parts.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Content placeholder while data loads | Skeleton screen with shimmer | Matches content shape; reduces layout shift |
| Simple loading indicator on a button/icon | CSS `opacity` pulse animation | Low overhead; small scope |
| Skeleton that matches exact content layout | Set explicit dimensions matching real content | Prevents layout shift (CLS) when content swaps in |
| Reduced motion fallback | Replace shimmer with slow pulse | Shimmer sweeps across the screen — motion-sensitive users |
| Dark mode skeleton | CSS custom properties for all skeleton colors | One set of tokens, overridden per theme |

## Pattern

**Shimmer skeleton** — gradient sweeps across to signal active loading:

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
  background: linear-gradient(
    90deg,
    var(--skeleton-bg) 25%,
    var(--skeleton-shine) 50%,
    var(--skeleton-bg) 75%
  );
  background-size: 400% 100%;
  border-radius: 4px;

  @media (prefers-reduced-motion: no-preference) {
    animation: skeleton-shimmer var(--skeleton-speed) ease-in-out infinite;
  }

  @media (prefers-reduced-motion: reduce) {
    animation: skeleton-pulse 2s ease-in-out infinite;
  }
}

@keyframes skeleton-shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}

@keyframes skeleton-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
```

**Card skeleton structure** — explicit dimensions prevent layout shift:

```css
.skeleton-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
}

.skeleton-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.skeleton-title {
  height: 20px;
  width: 60%;
}

.skeleton-body {
  height: 14px;
  width: 100%;
}

.skeleton-body + .skeleton-body {
  width: 80%;
}
```

All `skeleton-*` elements also get the `.skeleton` class above for the animation.

**Accessibility — ARIA markup:**

```html
<div role="status" aria-busy="true" aria-label="Loading article content">
  <div class="skeleton-card">
    <div class="skeleton skeleton-title"></div>
    <div class="skeleton skeleton-body"></div>
    <div class="skeleton skeleton-body"></div>
  </div>
  <span class="visually-hidden">Loading...</span>
</div>
```

When content loads, update `aria-busy="false"` and replace the skeleton markup.

## Common Mistakes
- Skeleton with no explicit dimensions — the layout shifts when content loads, causing CLS score degradation; match skeleton dimensions to real content
- Animating background-position without `background-size: 400%` — the gradient doesn't travel far enough to create the sweep effect
- Applying shimmer animation to fixed/sticky elements — compositing issues on some browsers; keep skeletons in normal document flow
- No ARIA markup — screen readers have no indication something is loading; `role="status"` and `aria-busy` are required
- Using the shimmer animation for reduced-motion users — the sweep across the screen is motion; swap for opacity pulse instead

## See Also
- [Animation Performance](animation-performance.md) — `background-position` animation is paint-only, not compositor; limit element count
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling
- [Opacity and Visual Hierarchy](opacity-and-visual-hierarchy.md) — pulse animation uses opacity tokens
- Reference: [Frontend Hero: CSS Skeleton Loaders](https://frontend-hero.com/how-to-create-skeleton-loader)
- Reference: [MDN: ARIA: status role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/status_role)
