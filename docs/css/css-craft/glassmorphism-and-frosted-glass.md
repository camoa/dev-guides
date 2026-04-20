---
description: Create frosted glass / blurred panel effects with backdrop-filter — blur values, dark mode, extended header technique, and accessibility fallbacks
tldr: "Use frosted glass when there is rich, colorful content behind the element — navigation bars over hero images, floating cards over gradients. On a plain white background it just looks like a blurry rectangle."
---

# Glassmorphism and Frosted Glass

## When to Use

> Use frosted glass when there is rich, colorful content behind the element — navigation bars over hero images, floating cards over gradients. On a plain white background it just looks like a blurry rectangle. Ask: "What is behind this?"

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Standard frosted panel | `backdrop-filter: blur(12px)` + semi-transparent bg | 97% browser support as of 2024 |
| Headers that miss nearby content | Extended backdrop with `mask-image` trim | `backdrop-filter` only blurs directly behind; mask extends the capture area |
| Accessibility fallback | `@media (prefers-reduced-transparency: reduce)` | Solid background when user reduces transparency |
| Mobile performance concern | Reduce blur to 6-8px; limit to 2-3 elements per viewport | Blur is exponentially more expensive past 15px |
| Contrast over complex backgrounds | Add `text-shadow` or increase bg opacity | Frosted glass alone may fail WCAG contrast on busy images |

### Professional vs Cheap Frosted Glass

| Quality | Blur | Background Opacity | Result |
|---------|------|--------------------|--------|
| **Professional** | 10-16px | 0.6-0.8 | Depth without distraction |
| **Premium/minimal** | 20-24px | 0.4-0.6 | Airy, high-end feel |
| **Cheap** | 4px | 0.9 | Barely visible, might as well be opaque |
| **Overwhelming** | 40px+ | 0.2 | Background completely unreadable |

## Pattern

**Standard frosted panel:**
```css
.glass-panel {
  background: hsl(0 0% 100% / 0.7);
  backdrop-filter: blur(12px) saturate(1.5);
  -webkit-backdrop-filter: blur(12px) saturate(1.5);
  border: 1px solid hsl(0 0% 100% / 0.2);
  border-radius: 12px;
}
[data-theme="dark"] .glass-panel {
  background: hsl(220 20% 15% / 0.75);
  border-color: hsl(0 0% 100% / 0.08);
}
```

**Extended backdrop for sticky headers:**
```css
.sticky-header { position: sticky; top: 0; isolation: isolate; z-index: 100; }
.sticky-header::before {
  content: ''; position: absolute; inset: 0;
  height: 200%; /* Expand to capture content above fold line */
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  mask-image: linear-gradient(to bottom, black 0% 50%, transparent 50% 100%);
  pointer-events: none; z-index: -1;
}
```

**Reduced transparency fallback:**
```css
@media (prefers-reduced-transparency: reduce) {
  .glass-panel { background: hsl(0 0% 98%); backdrop-filter: none; -webkit-backdrop-filter: none; }
  [data-theme="dark"] .glass-panel { background: hsl(220 20% 18%); }
}
```

## Common Mistakes

- **Wrong**: `backdrop-filter` on a solid-background page — **Right**: There is nothing to blur; it just looks grey
- **Wrong**: Missing `-webkit-backdrop-filter` — **Right**: Required for Safari even in 2025
- **Wrong**: Blur values above 20px on mobile — **Right**: Exponentially more expensive; profile on a real mid-range device
- **Wrong**: 10+ glass elements per viewport — **Right**: 3-5 glass elements is negligible; 10+ causes lag on mid-range phones
- **Wrong**: Animating `backdrop-filter` blur values — **Right**: Does not run on compositor thread; causes main-thread jank
- **Wrong**: No contrast check — **Right**: Semi-transparent backgrounds over images frequently fail WCAG 1.4.3

## See Also

- [Elevation and Shadows](elevation-and-shadows.md) — complement glass panels with shadow depth
- [Animation Performance](animation-performance.md) — why animating `backdrop-filter` is expensive
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-transparency` media feature
- Reference: [Josh W. Comeau: Next-Level Frosted Glass](https://www.joshwcomeau.com/css/backdrop-filter/)
- Reference: [MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
