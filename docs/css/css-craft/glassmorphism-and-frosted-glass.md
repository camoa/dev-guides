---
description: Create frosted glass / blurred panel effects with backdrop-filter — blur values, dark mode, extended header technique, and accessibility fallbacks
tldr: "Use frosted glass when there is rich, colorful content behind the element — navigation bars over hero images, floating cards over gradients. On a plain white background it just looks like a blurry rectangle."
---

# Glassmorphism and Frosted Glass

## When to Use
Frosted glass works when there is rich, colorful content behind the element — navigation bars over hero images, floating cards over gradients, overlays above media. On a plain white background it just looks like a blurry rectangle. Ask: "What is behind this?" If the answer is "nothing interesting," use an opaque surface instead.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Standard frosted panel | `backdrop-filter: blur(12px)` + semi-transparent bg | 97% browser support as of 2024 |
| Better blur capture (headers that miss nearby content) | Extended backdrop with `mask-image` trim | `backdrop-filter` only blurs directly behind; mask trick extends the capture area |
| Accessibility fallback | `@media (prefers-reduced-transparency: reduce)` | Solid background when user reduces transparency |
| Mobile performance concern | Reduce blur to 6-8px; limit to 2-3 elements per viewport | Blur is exponentially more expensive past 15px |
| Contrast over complex backgrounds | Add `text-shadow` or increase bg opacity | Frosted glass alone may fail WCAG contrast on busy images |

## Professional vs Cheap Frosted Glass

| Quality | Blur | Background opacity | Color tint | Result |
|---|---|---|---|---|
| **Professional** | 10-16px | 0.6-0.8 | Slightly warm/cool tint | Depth without distraction |
| **Premium/minimal** | 20-24px | 0.4-0.6 | White or brand-tinted | Airy, high-end feel |
| **Cheap** | 4px | 0.9 | None | Barely visible, might as well be opaque |
| **Overwhelming** | 40px+ | 0.2 | Saturated color | Background completely unreadable |

## Pattern

**Standard frosted panel:**

```css
.glass-panel {
  --glass-blur: 12px;
  --glass-bg-alpha: 0.7;
  --glass-border-alpha: 0.2;

  background: hsl(0 0% 100% / var(--glass-bg-alpha));
  backdrop-filter: blur(var(--glass-blur)) saturate(1.5);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.5);
  border: 1px solid hsl(0 0% 100% / var(--glass-border-alpha));
  border-radius: 12px;
}

[data-theme="dark"] .glass-panel {
  background: hsl(220 20% 15% / 0.75);
  border-color: hsl(0 0% 100% / 0.08);
}
```

**Extended backdrop for headers** — `backdrop-filter` only blurs pixels directly behind the element, missing nearby content that scrolls close. The mask trick expands the blurred area then trims it:

```css
.sticky-header {
  position: sticky;
  top: 0;
  isolation: isolate; /* New stacking context */
  z-index: 100;
}

.sticky-header::before {
  content: '';
  position: absolute;
  inset: 0;
  /* Expand height 2x to capture content above the fold line */
  height: 200%;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  /* Mask: show top half (the actual header), hide bottom half */
  mask-image: linear-gradient(to bottom, black 0% 50%, transparent 50% 100%);
  pointer-events: none;
  z-index: -1;
}
```

**Accessibility — reduced transparency fallback:**

```css
@media (prefers-reduced-transparency: reduce) {
  .glass-panel {
    background: hsl(0 0% 98%);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    border-color: hsl(0 0% 80%);
  }

  [data-theme="dark"] .glass-panel {
    background: hsl(220 20% 18%);
    border-color: hsl(0 0% 30%);
  }
}
```

## Common Mistakes
- Using `backdrop-filter` on a solid-background page — there is nothing to blur; it just looks grey
- Missing `-webkit-backdrop-filter` — required for Safari (even in 2025)
- Blur values above 20px on mobile — exponentially more expensive; profile on a real mid-range device
- Applying to 10+ elements per viewport — 3-5 glass elements is negligible; 10+ causes lag on mid-range phones
- Animating `backdrop-filter` blur values — does not run on the compositor thread; causes main-thread jank
- No contrast check — semi-transparent backgrounds over images frequently fail WCAG 1.4.3; add `text-shadow` or increase opacity

## See Also
- [Elevation and Shadows](elevation-and-shadows.md) — complement glass panels with shadow depth
- [Animation Performance](animation-performance.md) — why animating `backdrop-filter` is expensive
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-transparency` media feature
- Reference: [Josh W. Comeau: Next-Level Frosted Glass](https://www.joshwcomeau.com/css/backdrop-filter/)
- Reference: [MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)
