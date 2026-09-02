---
description: Hover effects cookbook — button lift, ghost fill, card lift, link underline reveal, image overlay, icon circle, table row, 3D tilt, and magnetic hover patterns
tldr: "Use this guide when you need the right hover/active/focus effect for a specific UI element. This is the cookbook companion to [Micro-Interactions](micro-interactions.md), which covers the underlying principles and easing tokens."
drupal_version: "11.x"
---

# Hover Effects Collection

## When to Use
When you need the right hover/active/focus effect for a specific UI element. This is a consolidated reference of proven hover patterns — the cookbook companion to [Micro-Interactions](micro-interactions.md) which covers the principles.

## Decision: Effect by Element Type

| Element | Recommended Effect | Why |
|---|---|---|
| Button (primary) | Subtle lift + shadow increase + brightness | Feels clickable, provides feedback |
| Button (secondary/ghost) | Background fill on hover | Reveals affordance without being heavy |
| Card (clickable) | Lift + shadow + slight scale | Clearly interactive, not decorative |
| Card (non-clickable) | None or very subtle shadow | Don't imply clickability |
| Navigation link | Underline reveal or background slide | Clear focus indication |
| Image | Zoom in container + overlay | Shows interactivity, reveals action |
| Icon button | Background circle reveal | Common pattern (MD3, GitHub, etc.) |
| Table row | Background highlight | Helps track across columns |
| Tag/chip | Brightness change | Lightweight for small elements |

## Pattern: Button Lift
```css
.btn {
  transition: transform var(--duration-fast) var(--ease-standard),
              box-shadow var(--duration-fast) var(--ease-standard),
              filter var(--duration-fast) var(--ease-standard);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px oklch(0% 0 0 / 0.15);
  filter: brightness(1.08);
}

.btn:active {
  transform: translateY(0) scale(0.97);
  box-shadow: 0 1px 4px oklch(0% 0 0 / 0.1);
  transition-duration: var(--duration-instant);
}
```

## Pattern: Background Fill (Ghost Button)
```css
.btn--ghost {
  background: transparent;
  transition: background var(--duration-fast) var(--ease-standard),
              color var(--duration-fast) var(--ease-standard);
}

.btn--ghost:hover {
  background: color-mix(in oklch, var(--color-primary) 10%, transparent);
}

.btn--ghost:active {
  background: color-mix(in oklch, var(--color-primary) 16%, transparent);
}
```

## Pattern: Card Hover (Lift + Border)
```css
.card {
  transition: transform var(--duration-medium1) var(--ease-standard),
              box-shadow var(--duration-medium1) var(--ease-standard),
              border-color var(--duration-fast) var(--ease-standard);
  border: 1px solid oklch(90% 0 0);
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px oklch(0% 0 0 / 0.12);
  border-color: oklch(80% 0 0);
}

/* Card with image zoom */
.card__image {
  overflow: hidden;
}

.card__image img {
  transition: transform var(--duration-medium2) var(--ease-standard);
}

.card:hover .card__image img {
  transform: scale(1.05);
}
```

## Pattern: Link Underline Reveal
```css
/* Sliding underline from left */
.link {
  text-decoration: none;
  background-image: linear-gradient(currentColor, currentColor);
  background-size: 0% 2px;
  background-position: left bottom;
  background-repeat: no-repeat;
  transition: background-size var(--duration-fast) var(--ease-standard);
  padding-bottom: 2px;
}

.link:hover {
  background-size: 100% 2px;
}

/* Underline slide from center */
.link--center {
  background-position: center bottom;
}
```

## Pattern: Image Overlay on Hover
```css
.image-card {
  position: relative;
  overflow: hidden;
}

.image-card__overlay {
  position: absolute;
  inset: 0;
  background: oklch(0% 0 0 / 0);
  display: grid;
  place-content: center;
  transition: background var(--duration-medium1) var(--ease-standard);
}

.image-card:hover .image-card__overlay {
  background: oklch(0% 0 0 / 0.5);
}

.image-card__overlay-text {
  color: white;
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--duration-fast) var(--ease-decel),
              transform var(--duration-fast) var(--ease-decel);
}

.image-card:hover .image-card__overlay-text {
  opacity: 1;
  transform: translateY(0);
}
```

## Pattern: Icon Button (Circle Reveal)
```css
.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: grid;
  place-content: center;
  background: transparent;
  transition: background var(--duration-fast) var(--ease-standard);
}

.icon-btn:hover {
  background: color-mix(in oklch, currentColor 8%, transparent);
}

.icon-btn:active {
  background: color-mix(in oklch, currentColor 16%, transparent);
}
```

## Pattern: Table Row Highlight
```css
.table tbody tr {
  transition: background var(--duration-instant) var(--ease-standard);
}

.table tbody tr:hover {
  background: oklch(97% 0 0);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  .table tbody tr:hover {
    background: oklch(20% 0 0);
  }
}
```

## Pattern: 3D Tilt on Hover
```css
.tilt-card {
  perspective: 800px;
  transform-style: preserve-3d;
}

.tilt-card__inner {
  transition: transform var(--duration-medium1) var(--ease-standard);
}

/* CSS-only approximation (for JS-tracked mouse position, see 3D Transforms guide) */
.tilt-card:hover .tilt-card__inner {
  transform: rotateX(-3deg) rotateY(3deg) translateZ(10px);
}
```

## Pattern: Magnetic Hover (Scale + Translate)
```css
.magnetic-item {
  transition: transform var(--duration-fast) var(--ease-decel);
}

.magnetic-item:hover {
  transform: scale(1.1);
}

/* Combined with slight movement toward cursor direction */
.magnetic-item:hover:has(+ .magnetic-item) {
  transform: scale(1.1) translateX(-4px); /* Move away from next sibling */
}
```

## Performance Rules for Hover Effects
1. **Safe to animate** on hover: `transform`, `opacity`, `filter`, `box-shadow`, `background-color`, `border-color`, `clip-path`
2. **Avoid animating** on hover: `width`, `height`, `top`, `left`, `margin`, `padding` (causes layout reflow)
3. **Duration**: hover-in 150–200ms, hover-out 100–150ms (faster out feels snappier)
4. **Active press**: always faster than hover (≤75ms) with `scale(0.97)` feedback

## Common Mistakes
- **Hover effects on non-interactive elements** — don't add hover effects to decorative elements; it implies clickability
- **Missing focus-visible styles** — every hover effect needs a keyboard focus equivalent
- **Too much movement** — keep hover `translateY` to 2-4px maximum; more feels cartoonish
- **Same duration for enter and exit** — hover-out should be 25-50% shorter than hover-in
- **Forgetting `prefers-reduced-motion`** — replace movement with opacity/color changes

## See Also
- [Micro-Interactions](micro-interactions.md) → principles and easing tokens
- [3D Transforms](3d-transforms.md) → mouse-tracked 3D tilt with JavaScript
- [Elevation and Shadows](elevation-and-shadows.md) → shadow token system for hover states
- [Accessibility and Motion](accessibility-and-motion.md) → reduced motion alternatives
