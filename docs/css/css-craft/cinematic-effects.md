---
description: Cinematic CSS effects — border beam, glow, aurora, neon, shimmer sweep, particles, and perspective grid for focal hero moments
tldr: "Use cinematic effects on hero sections, primary CTAs, and feature highlights — one or two per page maximum. Do not use on navigation, body copy, form fields, dashboards, or secondary CTAs."
---

# Cinematic Effects

## When to Use
Cinematic effects are decorative CSS flourishes that create dramatic visual impact — the difference between a polished landing page and a memorable one. These are NOT everyday craft patterns. They belong on: hero sections, primary CTAs, feature highlights, and dark-mode-first product pages.

**The less-is-more rule:** Maximum 1-2 cinematic effects per page. Stacking a border beam, glow, aurora background, AND neon text on the same viewport is visual noise. Pick one focal point — the effect is the signal; everything else is noise.

## Decision: When to Apply (and When Not To)

| Context | Use Cinematic Effects? | Why |
|---|---|---|
| Hero section headline or CTA | Yes | The page's single focal moment |
| Primary action button | Yes, one effect only | Draws the eye to the conversion point |
| Feature highlight card | Yes, subtle only | Differentiates without distracting |
| Navigation, headers | No | Users need nav to be calm and scannable |
| Body copy, long-form content | No | Animated backgrounds ruin readability |
| Form fields and inputs | No | Focus states need clarity, not drama |
| Secondary or tertiary CTAs | No | Reserve for the single primary action |
| Data tables, dashboards | No | Analytical contexts need calm interfaces |

## Decision: Which Effect for Which Design Style

| Effect | Kinematic / Dark UI | Retro / Y2K | Memphis | Minimal / Swiss | Wabi-Sabi |
|---|---|---|---|---|---|
| Border Beam | Excellent fit | Good fit | Poor fit | Never | Never |
| Glow (box/text) | Excellent fit | Good fit | Poor fit | Never | Never |
| Aurora background | Excellent fit | Poor fit | Poor fit | Never | Never |
| Neon text/borders | Poor fit | Excellent fit | Good fit | Never | Never |
| Shimmer sweep | Excellent fit | Good fit | Poor fit | Sparing | Never |
| Particles / meteors | Good fit | Good fit | Poor fit | Never | Never |
| Perspective grid | Poor fit | Excellent fit | Poor fit | Never | Never |

**Minimal / Swiss and Wabi-Sabi design systems:** These philosophies reject decorative effects by definition. Introducing cinematic effects breaks the system's foundational premise. If a client pushes for "more excitement," solve it with typography scale and whitespace — not effects.

---

## Border Beam

**What it is:** A beam of light that travels along the border of a container, created with a conic-gradient on the border itself. Popularized by Magic UI and shadcn ecosystem components.

**Performance:** `@property` angle animation → compositor-safe. The conic-gradient background is repainted when the angle changes, but on a single element this is acceptable. Not suitable for 10+ simultaneous instances.

**Pattern — `@property` conic-gradient approach (recommended):**

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

**Pattern — pseudo-element fallback (wider support, no `@property`):**

```css
.border-beam-fallback {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.border-beam-fallback::before {
  content: '';
  position: absolute;
  inset: -2px; /* Same as border-width */
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
  inset: 2px; /* Mask the interior */
  background: hsl(220 15% 10%);
  border-radius: calc(12px - 2px);
  z-index: -1;
}

@keyframes beam-spin {
  to { transform: rotate(1turn); }
}
```

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  .border-beam { animation: none; }
  /* Show a static gradient border instead */
  .border-beam {
    background:
      hsl(220 15% 10%) padding-box,
      linear-gradient(135deg, hsl(250 80% 70%), hsl(320 70% 65%)) border-box;
  }
}
```

**Style compatibility:** Best on dark surfaces — the beam is nearly invisible on white or light grey backgrounds. Dark cards, feature panels, pricing cards.

**Professional vs overdone:**
- Professional: 3-6s rotation, single thin beam (10-20% arc), subtle color
- Overdone: <1s rotation (epileptic), 50%+ arc coverage (the whole border glows = no beam, just a border), multiple simultaneous border-beam cards

> **See also:** [Gradient Craft](gradient-craft.md) — the `@property` + dual `background-clip` technique this builds on

---

## Glow Effects

**What it is:** Aura/halo effects around elements or text using stacked `box-shadow` or `filter: drop-shadow()`, and stacked `text-shadow` for type.

**Performance:** Static glow = paint-only (acceptable). Animated glow (`box-shadow` changing blur/spread) = repaint on every frame. Prefer animating `opacity` on the glow layer, not the shadow itself.

**Pattern — box glow:**

```css
.glow-card {
  --glow-color: hsl(250 80% 65%);

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

**Pattern — glow on hover (performance-safe approach using pseudo-element opacity):**

```css
.glow-hover {
  position: relative;
}

/* The glow lives on a pseudo-element — animate opacity, not shadow */
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

.glow-hover:hover::after {
  opacity: 1;
}
```

**Pattern — text glow (neon-adjacent, dark backgrounds only):**

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

**Common mistakes:**
- Animating `box-shadow` blur radius directly → repaint per frame; use opacity on a pseudo-element instead
- Glow on light backgrounds → the effect is invisible or muddy; glow only works where there is contrast to bloom against
- Too many glow elements on one page → the eye has nowhere to rest; glow is attention-grabbing, so it should mark exactly one thing

---

## Aurora / Northern Lights Background

**What it is:** A flowing, multi-color background that resembles the aurora borealis — achieved with blurred colored blob elements (filter blur technique) or animated radial/mesh gradients. Used for hero backgrounds, feature section backgrounds, and dark-mode "premium" product pages.

**Performance:** `filter: blur()` on large elements is the most expensive effect in this guide. A 400px div with `filter: blur(60px)` will trigger full repaint across the blur radius area on every animation frame. Limit to 2-4 blob elements, avoid blur values above 80px, never animate the blur radius — only animate `transform` and `opacity`.

**Pattern — filter blur blob technique:**

```css
.aurora-wrapper {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  background: hsl(230 30% 8%); /* Dark base */
}

.aurora-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.7;
  will-change: transform; /* Promote to own layer */
}

.aurora-blob--1 {
  width: 600px;
  height: 600px;
  background: hsl(270 70% 50%);
  top: -20%;
  left: -10%;

  @media (prefers-reduced-motion: no-preference) {
    animation: aurora-drift-1 18s ease-in-out infinite alternate;
  }
}

.aurora-blob--2 {
  width: 500px;
  height: 400px;
  background: hsl(200 80% 45%);
  top: 30%;
  right: -15%;

  @media (prefers-reduced-motion: no-preference) {
    animation: aurora-drift-2 22s ease-in-out infinite alternate;
  }
}

@keyframes aurora-drift-1 {
  from { transform: translate(0, 0) rotate(0deg); }
  to   { transform: translate(80px, 40px) rotate(30deg); }
}

@keyframes aurora-drift-2 {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(-60px, 30px) scale(1.1); }
}
```

**Pattern — `@property` animated hue gradient (lighter-weight alternative):**

> **Feature reference:** See [Gradient Craft](gradient-craft.md) for the `@property` animated gradient pattern. Apply it as a radial mesh background for a lighter aurora approximation.

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

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  .aurora-blob { animation: none; }
  .aurora-gradient { animation: none; }
  /* Static version remains — the colors stay, the motion stops */
}
```

**Common mistakes:**
- Blur values above 80px on mobile → exponential GPU cost; 40-60px is the practical ceiling
- Animating `filter: blur()` values → do not change blur radius in keyframes; only `transform` and `opacity`
- More than 4 blur blobs → performance collapses on mid-range devices; 2-3 is the effective maximum
- Aurora on light or neutral backgrounds → the effect needs a dark surface to bloom against; it looks grey on white

---

## Neon Effects

**What it is:** Electric neon sign aesthetics — text or borders that appear to emit colored light, achieved through stacked `text-shadow` or `box-shadow` layers building from tight inner glow to wide diffuse halo. Optional: flicker animation using opacity keyframes.

**Performance:** Static neon = paint-only (acceptable). The neon flicker keyframe is fast because it animates `text-shadow` between two states — not a gradual change, but a snap. Prefer the `@keyframes` flicker over `opacity` transitions for the authentic electrical cut-off feel.

**Pattern — neon text:**

```css
.neon-text {
  --neon-color: hsl(150 90% 55%);
  --neon-white: hsl(0 0% 100%);

  color: var(--neon-white);
  text-shadow:
    0 0  4px var(--neon-white),
    0 0 10px var(--neon-white),
    0 0 21px var(--neon-color),
    0 0 42px var(--neon-color),
    0 0 82px hsl(150 90% 55% / 0.7),
    0 0 92px hsl(150 90% 55% / 0.5);
}
```

**Pattern — neon border:**

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

**Pattern — neon flicker animation:**

```css
.neon-flicker {
  @media (prefers-reduced-motion: no-preference) {
    animation: neon-flicker 2.5s linear infinite;
  }
}

/* Flicker snaps on/off — no interpolation, that's intentional */
@keyframes neon-flicker {
  0%, 18%, 22%, 25%, 53%, 57%, 100% {
    text-shadow:
      0 0 4px #fff, 0 0 10px #fff,
      0 0 21px hsl(150 90% 55%),
      0 0 42px hsl(150 90% 55%);
    opacity: 1;
  }
  20%, 24%, 55% {
    text-shadow: none;
    opacity: 0.8;
  }
}
```

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  .neon-flicker { animation: none; }
  /* Static neon glow remains */
}

/* WCAG note: neon text on dark backgrounds — verify 4.5:1 contrast ratio.
   White (#fff) on very dark backgrounds passes easily.
   Colored neon text alone may fail — always pair with white or near-white text color */
```

**Style compatibility:** Retro/Y2K, Memphis, cyberpunk, nightlife aesthetics. Completely wrong for corporate, healthcare, finance, or any context requiring trust signals.

**Professional vs overdone:**
- Professional: 1 neon element per section, matched to the brand palette, used for a label or border accent
- Overdone: Every heading is neon, multiple colors competing, flicker on multiple elements simultaneously (seizure risk — WCAG 2.3.1 limits flashing to 3 times/second)

---

## Shimmer Sweep

**What it is:** A moving light highlight that sweeps across a surface — buttons, cards, or banners — to convey premium quality or draw attention to an interactive element. Distinct from skeleton shimmer (which signals loading). This is a deliberate decorative flourish.

**Performance:** The safest shimmer uses a `pseudo-element` with `translateX` — compositor-only. Avoid `background-position` animation for this effect (paint-only). The `@property` approach (animated gradient stop) works but requires repaint.

**Pattern — pseudo-element translateX sweep (compositor-only, recommended):**

```css
.shimmer-btn {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.shimmer-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 60%;
  height: 100%;
  background: linear-gradient(
    105deg,
    transparent 20%,
    hsl(0 0% 100% / 0.25) 50%,
    transparent 80%
  );
  pointer-events: none;

  @media (prefers-reduced-motion: no-preference) {
    animation: shimmer-sweep 2.5s ease-in-out infinite;
    animation-delay: 1s; /* Pause before sweeping */
  }
}

@keyframes shimmer-sweep {
  0%   { transform: translateX(0%); }
  100% { transform: translateX(350%); }
}
```

**Pattern — on-hover only (less distracting, recommended for CTAs):**

```css
.shimmer-hover::after {
  opacity: 0;
  animation: none;
  transition: opacity var(--duration-fast) var(--ease-standard);
}

.shimmer-hover:hover::after {
  opacity: 1;
  animation: shimmer-sweep 0.6s ease-out forwards;
}
```

**Common mistakes:**
- Continuous infinite shimmer on every card in a grid → attention overload; use hover-triggered shimmer instead
- `background-position` animation for shimmer → paint-only; use `translateX` on a pseudo-element
- Shimmer without `overflow: hidden` → the gradient bleeds outside the element bounds
- Shimmer on form inputs or navigation → users read it as loading state; reserve for hero CTAs and feature cards

---

## Particles and Meteor Effects

**What it is:** CSS-only animated shooting stars, floating particles, or meteor trails using pseudo-elements, `nth-child` offsets, and `@keyframes`. No JavaScript, no canvas. Used for dark-mode hero backgrounds and space/night-sky aesthetics.

**Performance:** CSS particles work by styling individual DOM elements — each with its own animation. Keep particle counts under 20. Above 20 elements animating simultaneously on low-end mobile, performance degrades noticeably. These are NOT compositor-safe if they animate `opacity` alongside `transform` (both are compositor-safe independently; combining them is fine). The risk is element count, not the properties.

**Pattern — shooting star / meteor trail:**

```css
.meteor-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.meteor {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  /* Trail: use box-shadow as a tail extending back-left */
  box-shadow: 0 0 0 1px hsl(0 0% 100% / 0.1), -80px 0 8px 2px hsl(0 0% 100% / 0.4);
  opacity: 0;

  @media (prefers-reduced-motion: no-preference) {
    animation: meteor-fall var(--duration, 3s) var(--delay, 0s) linear infinite;
  }
}

/* Stagger meteors with custom properties per element */
.meteor:nth-child(1) { --delay: 0s;    --duration: 3s;   top: 10%; right: 20%; }
.meteor:nth-child(2) { --delay: 1.5s;  --duration: 4s;   top: 25%; right: 40%; }
.meteor:nth-child(3) { --delay: 0.8s;  --duration: 3.5s; top: 5%;  right: 60%; }

@keyframes meteor-fall {
  0%   { transform: translate(0, 0) rotate(-45deg); opacity: 0; }
  5%   { opacity: 1; }
  70%  { opacity: 1; }
  100% { transform: translate(-400px, 400px) rotate(-45deg); opacity: 0; }
}
```

**Pattern — floating particles (ambient, not directional):**

```css
.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: hsl(var(--particle-hue, 250) 70% 70%);
  border-radius: 50%;
  opacity: 0;

  @media (prefers-reduced-motion: no-preference) {
    animation: particle-float var(--dur, 6s) var(--delay, 0s) ease-in-out infinite alternate;
  }
}

@keyframes particle-float {
  0%   { transform: translateY(0) scale(0);   opacity: 0; }
  20%  { opacity: 0.8; }
  50%  { transform: translateY(-40px) scale(1); opacity: 0.6; }
  100% { transform: translateY(-80px) scale(0.5); opacity: 0; }
}
```

**Accessibility note:** Rapid, numerous moving elements are a vestibular trigger. Always wrap particle animations in `prefers-reduced-motion: no-preference`. When motion is reduced, show nothing — particles have no content value without the motion.

**Professional vs overdone:**
- Professional: 8-15 subtle meteors, muted colors, slow durations (3-6s)
- Overdone: 50+ particles, bright white streaks on every frame, durations under 1s

---

## Perspective Grid / Retro Floor

**What it is:** A synthwave/OutRun-style 3D perspective grid using CSS gradients and transforms — a flat div rotated with `perspective` and `rotateX` to create an infinite scrolling floor effect. Used in retro, Y2K, and gaming aesthetics.

**Performance:** The static grid is cheap (two `background-image` gradients). The animation uses `background-position-y` to scroll the grid — this is **paint-only** (not compositor). On desktop this is fine for a single large element; on mobile test explicitly. Avoid on low-end devices by using a static fallback.

> **See also:** [3D Transforms](3d-transforms.md) for `perspective` values guide and `preserve-3d` rules. The grid uses the same perspective system.

**Pattern:**

```css
.retro-grid {
  --grid-color: hsl(280 70% 60% / 0.35);
  --grid-size: 60px;
  --horizon-fade: 30%;

  position: relative;
  height: 50vh;
  overflow: hidden;
  background: hsl(230 40% 8%);
}

.retro-grid__floor {
  position: absolute;
  inset: 0;
  /* Perspective: rotate the floor plane into 3D space */
  transform: perspective(400px) rotateX(55deg);
  transform-origin: center bottom;

  /* Grid lines: horizontal + vertical via layered linear-gradients */
  background-image:
    linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
    linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px);
  background-size: var(--grid-size) var(--grid-size);
  background-position: center 0;

  @media (prefers-reduced-motion: no-preference) {
    animation: grid-scroll 4s linear infinite;
  }
}

/* Distance fog: mask fades the far horizon to transparent */
.retro-grid__floor::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    hsl(230 40% 8%) 0%,      /* Horizon — full fade */
    transparent var(--horizon-fade),
    transparent 100%
  );
}

@keyframes grid-scroll {
  from { background-position: center 0; }
  to   { background-position: center var(--grid-size); }
}
```

**Neon glow on the grid lines:**

```css
.retro-grid__floor {
  /* Add filter: drop-shadow for a neon bloom on the grid lines */
  filter: drop-shadow(0 0 6px hsl(280 70% 60% / 0.6));
}
```

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  .retro-grid__floor { animation: none; }
  /* Static perspective grid remains — purely decorative, no content loss */
}
```

**Common mistakes:**
- Missing the horizon fade (the `::after` mask) → grid lines converge to a harsh vanishing point; the fade masks the visual artifact
- `perspective` applied to the floor element itself → must be on a parent or use the `perspective()` function in `transform`; see [3D Transforms](3d-transforms.md)
- Animating `background-size` instead of `background-position` → different visual effect; `background-position` creates the forward-travel illusion
- High `filter: blur()` alongside the grid → the blur is computed after the perspective transform; expensive and visually muddy

---

## Reduced Motion: Cinematic Effects Summary

All cinematic effects must respect `prefers-reduced-motion`. The general rule for this category: **stop the animation, keep the static state.** Unlike entrance animations (which can crossfade instead of translate), cinematic effects usually have no meaningful static alternative to communicate — stopping the motion is the right call.

```css
@media (prefers-reduced-motion: reduce) {
  /* Border beam: static gradient border */
  .border-beam {
    animation: none;
    background:
      hsl(220 15% 10%) padding-box,
      linear-gradient(135deg, hsl(250 80% 70%), hsl(320 70% 65%)) border-box;
  }

  /* Glow: keep static glow, remove pulse */
  .glow-pulse { animation: none; }

  /* Aurora: blobs stay in place (color remains, motion stops) */
  .aurora-blob { animation: none; }

  /* Neon: static glow, no flicker */
  .neon-flicker { animation: none; }

  /* Shimmer: disable entirely (no static alternative makes sense) */
  .shimmer-btn::after,
  .shimmer-hover::after { display: none; }

  /* Particles/meteors: remove entirely */
  .meteor { display: none; }
  .particle { display: none; }

  /* Retro grid: freeze position */
  .retro-grid__floor { animation: none; }
}
```

**WCAG 2.3.1 flicker warning:** The neon flicker animation in this guide is designed to flash at ~2-3 times per second. Do not decrease the animation duration below 1s — that risks the 3 flash/second limit. Test in Axe or a screen reader before shipping.

## Common Mistakes
- Using cinematic effects on body content — reserve for focal moments only; motion on body text is hostile to reading
- Stacking 3+ effects on the same element — a glowing neon border with shimmer sweep and blur bloom is competing with itself
- Forgetting dark surface requirement — glow, aurora, and neon all need dark backgrounds to read as luminous; on light backgrounds they look grey or invisible
- No `prefers-reduced-motion` handling — for effects like neon flicker, this is a WCAG 2.3.1 violation (flashing content)
- Applying `will-change: transform` to all particles preemptively — `will-change` reserves GPU memory per layer; 20 particles × GPU memory reservation = real cost on mobile
- Cinematic effects in production admin UIs, dashboards, or tool interfaces — these design contexts require calm, not drama; save the effects for the marketing site

## See Also
- [Gradient Craft](gradient-craft.md) — `@property` gradient animation used in border beam and aurora
- [3D Transforms](3d-transforms.md) — perspective values and `preserve-3d` used in the retro grid
- [Elevation and Shadows](elevation-and-shadows.md) — layered shadow technique underlying glow effects
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` handling and WCAG 2.3.1 flicker rule
- [Animation Performance](animation-performance.md) — compositor-safe property tier list
- [Skeleton and Loading States](skeleton-and-loading-states.md) — shimmer for loading (different from decorative shimmer sweep)
- Reference: [Magic UI: Border Beam](https://magicui.design/docs/components/border-beam)
- Reference: [CodeTV: Animated CSS Gradient Borders](https://codetv.dev/blog/animated-css-gradient-border)
- Reference: [CSS-Tricks: Neon Text](https://css-tricks.com/how-to-create-neon-text-with-css/)
- Reference: [DEV: Aurora UI with CSS](https://dev.to/albertwalicki/aurora-ui-how-to-create-with-css-4b6g)
- Reference: [Motion.dev: Web Animation Performance Tier List](https://motion.dev/blog/web-animation-performance-tier-list)
