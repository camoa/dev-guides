---
description: Mesh gradients, animated gradients with @property, grainy noise overlays, and gradient borders that work with border-radius
---

# Gradient Craft

## When to Use

> Use gradient craft techniques for mesh-like layered backgrounds, animated color transitions, grainy texture overlays, and gradient borders. Avoid animating mesh gradients directly — each radial gradient triggers repaint; use a static mesh with a subtle overlay animation instead.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Smooth multi-color background (mesh-like) | Layered `radial-gradient()` with no repeat | Multiple radial blobs create organic mesh appearance |
| Animated gradient that transitions colors | `@property` registered color tokens | Without `@property`, gradient colors cannot be interpolated |
| Grainy/noisy gradient texture | SVG `<feTurbulence>` filter + CSS `background` layering | CSS-only noise effect; no image files |
| Gradient border with border-radius | `background-clip` two-background trick | `border-image` breaks with `border-radius` |
| Animated gradient border | `@property` + gradient border pattern | Register gradient angle as `@property` then animate it |

## Pattern

**Mesh gradient:**
```css
.mesh-bg {
  background:
    radial-gradient(ellipse at 20% 30%, hsl(250 80% 70%) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, hsl(320 70% 65%) 0%, transparent 55%),
    radial-gradient(ellipse at 60% 80%, hsl(190 80% 60%) 0%, transparent 60%),
    radial-gradient(ellipse at 10% 80%, hsl(40 90% 65%) 0%, transparent 50%),
    hsl(240 30% 15%);
}
```

**Animated gradient via @property:**
```css
@property --grad-hue { syntax: "<number>"; initial-value: 250; inherits: false; }
.animated-bg {
  background: linear-gradient(135deg, hsl(var(--grad-hue) 80% 60%), hsl(calc(var(--grad-hue) + 60) 80% 60%));
  @media (prefers-reduced-motion: no-preference) { animation: hue-cycle 6s linear infinite; }
}
@keyframes hue-cycle { to { --grad-hue: 610; } } /* 250 + 360 = full cycle */
```

**Grainy gradient — SVG noise overlay:**
```css
.grainy-gradient { background: linear-gradient(135deg, hsl(250 70% 40%), hsl(320 60% 50%)); position: relative; isolation: isolate; }
.grainy-gradient::after {
  content: ''; position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E");
  background-size: 256px 256px; mix-blend-mode: overlay; opacity: 0.4; pointer-events: none;
}
```

**Gradient border with border-radius:**
```css
.gradient-border {
  background:
    linear-gradient(hsl(var(--surface-hsl)), hsl(var(--surface-hsl))) padding-box,
    linear-gradient(135deg, hsl(250 80% 60%), hsl(320 80% 60%)) border-box;
  border: 2px solid transparent;
  border-radius: 12px;
}
```

**Animated gradient border:**
```css
@property --border-angle { syntax: "<angle>"; initial-value: 135deg; inherits: false; }
.animated-border {
  background:
    hsl(220 15% 10%) padding-box,
    conic-gradient(from var(--border-angle), hsl(250 80% 60%), hsl(320 80% 60%), hsl(250 80% 60%)) border-box;
  border: 2px solid transparent; border-radius: 12px;
  @media (prefers-reduced-motion: no-preference) { animation: rotate-border 3s linear infinite; }
}
@keyframes rotate-border { to { --border-angle: 495deg; } } /* 135 + 360 */
```

## Common Mistakes

- **Wrong**: `border-image` with `border-radius` — **Right**: `border-image` ignores `border-radius`; use the two-background technique
- **Wrong**: Animating gradient stop colors without `@property` — **Right**: Browsers snap between values without interpolation
- **Wrong**: Grainy gradient with noise opacity >0.6 — **Right**: 0.2-0.4 opacity is the sweet spot
- **Wrong**: Animating mesh gradients — **Right**: Each radial gradient triggers repaint; prefer static mesh with a subtle overlay animation
- **Wrong**: Missing `isolation: isolate` on the grain pattern — **Right**: `mix-blend-mode: overlay` on `::after` blends against wrong stacking context

## See Also

- [Modern CSS Craft Patterns](modern-css-craft-patterns.md) — `@property` gradient button animation
- [Text Effects](text-effects.md) — gradient fills on text using `background-clip`
- [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) — `mix-blend-mode` for grain overlay
- [Animation Performance](animation-performance.md) — why animating gradients is expensive
- Reference: [CSS-Tricks: Grainy Gradients](https://css-tricks.com/grainy-gradients/)
- Reference: [CSS-Tricks: Gradient Borders](https://css-tricks.com/gradient-borders-in-css/)
- Reference: [WebKit Blog: background-clip: border-area](https://webkit.org/blog/16214/background-clip-border-area/)
