---
description: Mesh gradients, animated gradients with @property, grainy noise overlays, and gradient borders that work with border-radius
tldr: "Use gradient craft techniques for mesh-like layered backgrounds, animated color transitions, grainy texture overlays, and gradient borders. Avoid animating mesh gradients directly — each radial gradient triggers repaint; use a static mesh…"
---

# Gradient Craft

## When to Use
CSS gradients have evolved well past `linear-gradient(to bottom, #fff, #000)`. This section covers production craft for gradients: mesh-like radial layering, animated gradients via `@property`, grainy/noisy texture overlays, and gradient borders — all using CSS custom properties for themeable, maintainable results.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Smooth multi-color background (mesh-like) | Layered `radial-gradient()` with no repeat | Multiple radial blobs create organic mesh appearance |
| Animated gradient that transitions colors | `@property` registered color tokens | Without `@property`, gradient colors cannot be interpolated |
| Grainy/noisy gradient texture | SVG `<feTurbulence>` filter + CSS `background` layering | CSS-only noise effect; no image files |
| Gradient border with border-radius | `background-clip` two-background trick | `border-image` breaks with `border-radius`; the clip trick works |
| Animated gradient border | `@property` + gradient border pattern | Register gradient stop as `@property` then animate it |

## Pattern

**Mesh gradient** — layered radial gradients create organic blob-like depth:

```css
.mesh-bg {
  --mesh-1: hsl(250 80% 70%);
  --mesh-2: hsl(320 70% 65%);
  --mesh-3: hsl(190 80% 60%);
  --mesh-4: hsl(40 90% 65%);

  background:
    radial-gradient(ellipse at 20% 30%, var(--mesh-1) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, var(--mesh-2) 0%, transparent 55%),
    radial-gradient(ellipse at 60% 80%, var(--mesh-3) 0%, transparent 60%),
    radial-gradient(ellipse at 10% 80%, var(--mesh-4) 0%, transparent 50%),
    hsl(240 30% 15%); /* Base color */
}
```

Adjust `ellipse at X% Y%` positions per project. Keep stops at `0%` to `transparent 50-65%` — this creates the soft, overlapping blob look.

**Animated gradient via `@property`:**

> **Feature reference:** See [modern-css → at-property](../modern-css/at-property.md) for registration syntax. See [Modern CSS Craft Patterns](modern-css-craft-patterns.md) for the button gradient pattern.

```css
@property --grad-hue {
  syntax: "<number>";
  initial-value: 250;
  inherits: false;
}

.animated-bg {
  background: linear-gradient(
    135deg,
    hsl(var(--grad-hue) 80% 60%),
    hsl(calc(var(--grad-hue) + 60) 80% 60%)
  );

  @media (prefers-reduced-motion: no-preference) {
    animation: hue-cycle 6s linear infinite;
  }
}

@keyframes hue-cycle {
  to { --grad-hue: 610; } /* 250 + 360 = full hue cycle */
}
```

**Grainy gradient** — adds organic texture to flat gradients using an inline SVG filter:

```css
/* In <head> or a hidden element — the filter definition */
/*
  <svg style="display:none">
    <filter id="grain">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    </filter>
  </svg>
*/

.grainy-gradient {
  --gradient: linear-gradient(135deg, hsl(250 70% 40%), hsl(320 60% 50%));

  background: var(--gradient);
  position: relative;
  isolation: isolate;
}

/* Noise overlay — blends multiplicatively to add grain */
.grainy-gradient::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 256px 256px;
  mix-blend-mode: overlay;
  opacity: 0.4;
  pointer-events: none;
}
```

**Gradient border with border-radius** — the `border-image` approach breaks border-radius; this two-background trick works:

```css
.gradient-border {
  --border-width: 2px;
  --border-radius: 12px;
  --border-grad: linear-gradient(135deg, hsl(250 80% 60%), hsl(320 80% 60%));

  background:
    linear-gradient(hsl(var(--surface-hsl)), hsl(var(--surface-hsl))) padding-box,
    var(--border-grad) border-box;
  border: var(--border-width) solid transparent;
  border-radius: var(--border-radius);
}
```

The key: two backgrounds on the same element. `padding-box` clips the first background to the padding box (solid fill). `border-box` extends the second background into the border area. The `transparent` border creates a window into the gradient background.

**Animated gradient border:**

```css
@property --border-angle {
  syntax: "<angle>";
  initial-value: 135deg;
  inherits: false;
}

.animated-border {
  background:
    hsl(220 15% 10%) padding-box,
    conic-gradient(from var(--border-angle), hsl(250 80% 60%), hsl(320 80% 60%), hsl(250 80% 60%)) border-box;
  border: 2px solid transparent;
  border-radius: 12px;

  @media (prefers-reduced-motion: no-preference) {
    animation: rotate-border 3s linear infinite;
  }
}

@keyframes rotate-border {
  to { --border-angle: 495deg; } /* 135 + 360 */
}
```

## Common Mistakes
- Using `border-image` with `border-radius` — `border-image` ignores `border-radius`; use the two-background technique instead
- Animating gradient stop colors without `@property` — browsers snap between values without interpolation
- Grainy gradient with high noise opacity (>0.6) — the grain overwhelms the gradient; 0.2-0.4 opacity is the sweet spot
- Animating mesh gradients — each radial gradient triggers repaint; an animated mesh can bring mid-range devices to their knees; prefer static mesh with a subtle CSS overlay animation
- Missing `isolation: isolate` on the grain overlay pattern — the `mix-blend-mode: overlay` on the `::after` pseudo-element will blend against the wrong stacking context

## See Also
- [Modern CSS Craft Patterns](modern-css-craft-patterns.md) — `@property` gradient button animation
- [Text Effects](text-effects.md) — gradient fills on text using `background-clip`
- [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) — `mix-blend-mode` for grain overlay
- [Animation Performance](animation-performance.md) — why animating gradients is expensive
- Reference: [CSS-Tricks: Grainy Gradients](https://css-tricks.com/grainy-gradients/)
- Reference: [CSS-Tricks: Gradient Borders](https://css-tricks.com/gradient-borders-in-css/)
- Reference: [WebKit Blog: background-clip: border-area](https://webkit.org/blog/16214/background-clip-border-area/)
