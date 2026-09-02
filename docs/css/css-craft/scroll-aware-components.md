---
description: Scroll-aware components — shrinking headers, reading progress bars, back-to-top buttons, and scroll fade-ins without JavaScript
tldr: "Use scroll-driven animations when a client wants headers that shrink on scroll, progress indicators, or scroll-triggered reveals — all without JavaScript scroll listeners."
---

# Scroll-Aware Components

## When to Use
When a client wants headers that shrink on scroll, elements that change appearance when stuck, scroll progress indicators, or scroll-triggered class changes — all without JavaScript scroll listeners.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Sticky header with shadow when scrolled | Scroll-driven animation on header | No JS scroll listener |
| Shrinking header on scroll | `animation-timeline: scroll()` on height/padding | Smooth interpolation |
| Reading progress bar | `animation-timeline: scroll(root)` on width | Classic pattern, zero JS |
| Parallax speed difference | `animation-timeline: scroll()` on `translateY` | See [Parallax Effects](parallax-effects.md) |
| Back-to-top button on scroll | Scroll-driven opacity animation | Appears after scrolling down |
| Stuck header detection | `@container scroll-state(stuck)` (Chrome 133+) | See [Modern CSS: Container Scroll-State](../modern-css/container-scroll-state.md) |

## Pattern: Sticky Header with Scroll Shadow
```css
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  animation: header-shadow linear;
  animation-timeline: scroll(root);
  animation-range: 0px 100px; /* First 100px of scroll */
}

@keyframes header-shadow {
  from {
    box-shadow: 0 0 0 oklch(0% 0 0 / 0);
    backdrop-filter: blur(0);
  }
  to {
    box-shadow: 0 2px 12px oklch(0% 0 0 / 0.1);
    backdrop-filter: blur(12px);
  }
}
```

## Pattern: Shrinking Header
```css
.header {
  animation: shrink-header linear;
  animation-timeline: scroll(root);
  animation-range: 0px 200px;
}

@keyframes shrink-header {
  from {
    padding-block: 1.5rem;
  }
  to {
    padding-block: 0.5rem;
  }
}

.header__logo {
  animation: shrink-logo linear;
  animation-timeline: scroll(root);
  animation-range: 0px 200px;
}

@keyframes shrink-logo {
  from { height: 48px; }
  to { height: 32px; }
}
```

## Pattern: Reading Progress Bar
```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--color-primary);
  transform-origin: left;
  animation: reading-progress linear;
  animation-timeline: scroll(root);
  z-index: 1000;
}

@keyframes reading-progress {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

## Pattern: Back-to-Top Button
```css
.back-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  opacity: 0;
  translate: 0 20px;
  animation: show-back-to-top linear;
  animation-timeline: scroll(root);
  animation-range: 300px 400px; /* Show after 300px scroll */
  animation-fill-mode: both;
}

@keyframes show-back-to-top {
  to {
    opacity: 1;
    translate: 0 0;
  }
}
```

## Pattern: Fade-In Sections on Scroll
```css
.section {
  animation: scroll-fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
}

@keyframes scroll-fade-in {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**Browser support:** Scroll-driven animations: Chrome 115+, Safari 18+. Firefox behind flag. For Firefox fallback, the elements remain in their final state (visible, full-size) — functional but not animated.

## Common Mistakes
- **Using `animation-timeline: scroll()` without `linear` timing** — scroll-driven animations should use `linear` timing function; the scroll position IS the timing
- **Forgetting `animation-fill-mode: both`** for show/hide patterns — without it, the element reverts when outside the range
- **Animating layout properties** (height, padding) in scroll animations — use `transform: scaleY()` or `clip-path` for performance

## See Also
- [Parallax Effects](parallax-effects.md) → scroll speed differences
- [Entrance Animations](entrance-animations.md) → view() timeline reveals
- [Animation Performance](animation-performance.md) → compositor-safe properties
