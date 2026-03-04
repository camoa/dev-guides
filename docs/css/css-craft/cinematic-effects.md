---
description: Cinematic CSS effects — border beam, glow, aurora, neon, shimmer sweep, particles, and perspective grid for focal hero moments
---

# Cinematic Effects

## When to Use

> Use cinematic effects on hero sections, primary CTAs, and feature highlights — one or two per page maximum. Do not use on navigation, body copy, form fields, dashboards, or secondary CTAs.

## Decision

### When to Apply

| Context | Use? | Why |
|---------|------|-----|
| Hero section headline or CTA | Yes | The page's single focal moment |
| Primary action button | Yes, one effect only | Draws the eye to the conversion point |
| Feature highlight card | Yes, subtle only | Differentiates without distracting |
| Navigation, headers | No | Users need nav to be calm and scannable |
| Body copy, long-form content | No | Animated backgrounds ruin readability |
| Form fields and inputs | No | Focus states need clarity, not drama |
| Secondary or tertiary CTAs | No | Reserve for the single primary action |
| Data tables, dashboards | No | Analytical contexts need calm interfaces |

### Which Effect for Which Design Style

| Effect | Kinematic / Dark UI | Retro / Y2K | Memphis | Minimal / Swiss | Wabi-Sabi |
|--------|---------------------|-------------|---------|-----------------|-----------|
| Border Beam | Excellent fit | Good fit | Poor fit | Never | Never |
| Glow (box/text) | Excellent fit | Good fit | Poor fit | Never | Never |
| Aurora background | Excellent fit | Poor fit | Poor fit | Never | Never |
| Neon text/borders | Poor fit | Excellent fit | Good fit | Never | Never |
| Shimmer sweep | Excellent fit | Good fit | Poor fit | Sparing | Never |
| Particles / meteors | Good fit | Good fit | Poor fit | Never | Never |
| Perspective grid | Poor fit | Excellent fit | Poor fit | Never | Never |

## Pattern

### Border Beam (`@property` approach — recommended)

```css
@property --beam-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.border-beam {
  background:
    hsl(220 15% 10%) padding-box,
    conic-gradient(from var(--beam-angle), transparent 80%, hsl(250 80% 70%) 90%, transparent 100%) border-box;
  border: 2px solid transparent;
  border-radius: 12px;

  @media (prefers-reduced-motion: no-preference) {
    animation: beam-rotate 3s linear infinite;
  }
}

@keyframes beam-rotate {
  to { --beam-angle: 360deg; }
}
```

### Border Beam (pseudo-element fallback — no `@property`)

```css
.border-beam-fallback {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.border-beam-fallback::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: conic-gradient(from 0deg, transparent 80%, hsl(250 80% 70%) 90%, transparent);
  border-radius: inherit;
  z-index: -1;

  @media (prefers-reduced-motion: no-preference) {
    animation: beam-spin 3s linear infinite;
  }
}

.border-beam-fallback::after {
  content: '';
  position: absolute;
  inset: 2px;
  background: hsl(220 15% 10%);
  border-radius: calc(12px - 2px);
  z-index: -1;
}

@keyframes beam-spin {
  to { transform: rotate(1turn); }
}
```

### Glow

```css
.glow-card {
  box-shadow:
    0 0 20px hsl(250 80% 65% / 0.3),
    0 0 40px hsl(250 80% 65% / 0.2),
    0 0 80px hsl(250 80% 65% / 0.1);
}

/* Pulsing glow — animate opacity, NOT shadow values */
.glow-pulse {
  @media (prefers-reduced-motion: no-preference) {
    animation: glow-breathe 3s ease-in-out infinite;
  }
}

@keyframes glow-breathe {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.6; }
}
```

### Glow on hover (performance-safe: pseudo-element opacity)

```css
.glow-hover {
  position: relative;
}

.glow-hover::after {
  content: '';
  position: absolute;
  inset: -8px;
  background: radial-gradient(ellipse, hsl(250 80% 65% / 0.4), transparent 70%);
  border-radius: inherit;
  opacity: 0;
  transition: opacity var(--duration-normal) var(--ease-standard);
  pointer-events: none;
  z-index: -1;
}

.glow-hover:hover::after { opacity: 1; }
```

### Text glow

```css
.text-glow {
  --glow: hsl(180 80% 60%);
  color: hsl(180 80% 90%);
  text-shadow:
    0 0 4px  var(--glow),
    0 0 10px var(--glow),
    0 0 20px var(--glow),
    0 0 40px hsl(180 80% 60% / 0.5);
}
```

### Aurora background (filter blur blobs)

```css
.aurora-wrapper {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: hsl(230 30% 8%);
}

.aurora-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.7;
  will-change: transform;
}

.aurora-blob--1 {
  width: 600px; height: 600px;
  background: hsl(270 70% 50%);
  top: -20%; left: -10%;

  @media (prefers-reduced-motion: no-preference) {
    animation: aurora-drift-1 18s ease-in-out infinite alternate;
  }
}

@keyframes aurora-drift-1 {
  from { transform: translate(0, 0) rotate(0deg); }
  to   { transform: translate(80px, 40px) rotate(30deg); }
}
```

### Aurora (`@property` hue cycle — lighter-weight alternative)

```css
@property --aurora-hue {
  syntax: "<number>";
  initial-value: 250;
  inherits: false;
}

.aurora-gradient {
  background:
    radial-gradient(ellipse at 20% 30%, hsl(var(--aurora-hue) 60% 50% / 0.4), transparent 60%),
    radial-gradient(ellipse at 80% 60%, hsl(calc(var(--aurora-hue) + 60) 70% 45% / 0.3), transparent 55%),
    hsl(230 30% 8%);

  @media (prefers-reduced-motion: no-preference) {
    animation: aurora-hue-cycle 12s linear infinite;
  }
}

@keyframes aurora-hue-cycle {
  to { --aurora-hue: 610; }
}
```

### Neon text

```css
.neon-text {
  --neon-color: hsl(150 90% 55%);

  color: hsl(0 0% 100%);
  text-shadow:
    0 0  4px #fff,
    0 0 10px #fff,
    0 0 21px var(--neon-color),
    0 0 42px var(--neon-color),
    0 0 82px hsl(150 90% 55% / 0.7),
    0 0 92px hsl(150 90% 55% / 0.5);
}
```

### Neon border

```css
.neon-border {
  --neon-color: hsl(300 90% 60%);
  border: 2px solid var(--neon-color);
  border-radius: 8px;
  box-shadow:
    0 0  5px var(--neon-color),
    0 0 10px var(--neon-color),
    0 0 20px hsl(300 90% 60% / 0.6),
    inset 0 0 5px  hsl(300 90% 60% / 0.3),
    inset 0 0 20px hsl(300 90% 60% / 0.1);
}
```

### Neon flicker animation

```css
.neon-flicker {
  @media (prefers-reduced-motion: no-preference) {
    animation: neon-flicker 2.5s linear infinite;
  }
}

/* Snaps on/off — no interpolation, that's intentional */
@keyframes neon-flicker {
  0%, 18%, 22%, 25%, 53%, 57%, 100% {
    text-shadow: 0 0 4px #fff, 0 0 10px #fff, 0 0 21px hsl(150 90% 55%), 0 0 42px hsl(150 90% 55%);
    opacity: 1;
  }
  20%, 24%, 55% { text-shadow: none; opacity: 0.8; }
}
```

### Shimmer sweep (compositor-only, recommended)

```css
.shimmer-btn {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.shimmer-btn::after {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 60%; height: 100%;
  background: linear-gradient(105deg, transparent 20%, hsl(0 0% 100% / 0.25) 50%, transparent 80%);
  pointer-events: none;

  @media (prefers-reduced-motion: no-preference) {
    animation: shimmer-sweep 2.5s ease-in-out infinite;
    animation-delay: 1s;
  }
}

@keyframes shimmer-sweep {
  0%   { transform: translateX(0%); }
  100% { transform: translateX(350%); }
}
```

### Particles / meteor trail

```css
.meteor-container {
  position: absolute; inset: 0;
  overflow: hidden; pointer-events: none;
}

.meteor {
  position: absolute;
  width: 2px; height: 2px;
  background: white; border-radius: 50%;
  box-shadow: 0 0 0 1px hsl(0 0% 100% / 0.1), -80px 0 8px 2px hsl(0 0% 100% / 0.4);
  opacity: 0;

  @media (prefers-reduced-motion: no-preference) {
    animation: meteor-fall var(--duration, 3s) var(--delay, 0s) linear infinite;
  }
}

.meteor:nth-child(1) { --delay: 0s;   --duration: 3s;   top: 10%; right: 20%; }
.meteor:nth-child(2) { --delay: 1.5s; --duration: 4s;   top: 25%; right: 40%; }
.meteor:nth-child(3) { --delay: 0.8s; --duration: 3.5s; top: 5%;  right: 60%; }

@keyframes meteor-fall {
  0%   { transform: translate(0, 0) rotate(-45deg); opacity: 0; }
  5%   { opacity: 1; }
  70%  { opacity: 1; }
  100% { transform: translate(-400px, 400px) rotate(-45deg); opacity: 0; }
}
```

### Perspective grid / retro floor

```css
.retro-grid {
  --grid-color: hsl(280 70% 60% / 0.35);
  --grid-size: 60px;
  position: relative; height: 50vh;
  overflow: hidden; background: hsl(230 40% 8%);
}

.retro-grid__floor {
  position: absolute; inset: 0;
  transform: perspective(400px) rotateX(55deg);
  transform-origin: center bottom;
  background-image:
    linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
    linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px);
  background-size: var(--grid-size) var(--grid-size);

  @media (prefers-reduced-motion: no-preference) {
    animation: grid-scroll 4s linear infinite;
  }
}

/* Distance fog */
.retro-grid__floor::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, hsl(230 40% 8%) 0%, transparent 30%, transparent 100%);
}

@keyframes grid-scroll {
  from { background-position: center 0; }
  to   { background-position: center var(--grid-size); }
}
```

### Reduced motion: cinematic effects summary

```css
@media (prefers-reduced-motion: reduce) {
  /* Border beam: static gradient border */
  .border-beam {
    animation: none;
    background:
      hsl(220 15% 10%) padding-box,
      linear-gradient(135deg, hsl(250 80% 70%), hsl(320 70% 65%)) border-box;
  }
  /* Glow: keep static, remove pulse */
  .glow-pulse { animation: none; }
  /* Aurora: blobs stay in place */
  .aurora-blob, .aurora-gradient { animation: none; }
  /* Neon: static glow, no flicker */
  .neon-flicker { animation: none; }
  /* Shimmer: disable entirely */
  .shimmer-btn::after, .shimmer-hover::after { display: none; }
  /* Particles/meteors: remove entirely */
  .meteor, .particle { display: none; }
  /* Retro grid: freeze */
  .retro-grid__floor { animation: none; }
}
```

## Common Mistakes

- **Wrong**: Using cinematic effects on body content, navigation, or form fields → **Right**: Reserve for hero sections and primary CTAs only — one or two focal moments per page
- **Wrong**: Stacking 3+ effects on one element (glow + shimmer + neon border simultaneously) → **Right**: One effect per element — competing effects cancel each other out
- **Wrong**: Glow, aurora, or neon on light backgrounds → **Right**: These effects require dark surfaces to read as luminous; on white or light grey they look grey or invisible
- **Wrong**: Animating `box-shadow` blur radius directly → **Right**: Animate `opacity` on a pseudo-element holding the shadow; direct shadow animation triggers repaint per frame
- **Wrong**: Aurora `filter: blur()` above 80px on mobile → **Right**: 40-60px is the practical ceiling; higher values cause exponential GPU cost on mobile
- **Wrong**: More than 20 particle/meteor elements animating simultaneously → **Right**: Keep under 20; above that, performance degrades on low-end mobile
- **Wrong**: Neon flicker with `animation-duration` below 1s → **Right**: Keep at 2s+ to stay under the WCAG 2.3.1 three-flash-per-second limit
- **Wrong**: `will-change: transform` on all particles preemptively → **Right**: Apply only where needed — each `will-change` reserves GPU memory per layer
- **Wrong**: Cinematic effects in admin UIs, dashboards, or tool interfaces → **Right**: These contexts require calm; save effects for the marketing site

## See Also

- [Gradient Craft](gradient-craft.md) — `@property` + dual `background-clip` technique used in border beam and aurora
- [3D Transforms](3d-transforms.md) — `perspective` values and `preserve-3d` used in the retro grid
- [Elevation and Shadows](elevation-and-shadows.md) — layered shadow technique underlying glow effects
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling and WCAG 2.3.1 flicker rule
- [Animation Performance](animation-performance.md) — compositor-safe property tier list
- [Skeleton and Loading States](skeleton-and-loading-states.md) — shimmer for loading (distinct from decorative shimmer sweep)
- Reference: [Magic UI: Border Beam](https://magicui.design/docs/components/border-beam)
- Reference: [CodeTV: Animated CSS Gradient Borders](https://codetv.dev/blog/animated-css-gradient-border)
- Reference: [CSS-Tricks: Neon Text](https://css-tricks.com/how-to-create-neon-text-with-css/)
- Reference: [DEV: Aurora UI with CSS](https://dev.to/albertwalicki/aurora-ui-how-to-create-with-css-4b6g)
- Reference: [Motion.dev: Web Animation Performance Tier List](https://motion.dev/blog/web-animation-performance-tier-list)
