---
description: Hover effects cookbook — button lift, ghost fill, card lift, link underline reveal, image overlay, icon circle, table row, 3D tilt, and magnetic hover patterns
tldr: "Use this guide when you need the right hover/active/focus effect for a specific UI element. This is the cookbook companion to [Micro-Interactions](micro-interactions.md), which covers the underlying principles and easing tokens."
drupal_version: "11.x"
---

# Hover Effects Collection

## When to Use

> Use this guide when you need the right hover/active/focus effect for a specific UI element. This is the cookbook companion to [Micro-Interactions](micro-interactions.md), which covers the underlying principles and easing tokens.

## Decision

| Element | Recommended Effect | Why |
|---|---|---|
| Button (primary) | Lift + shadow increase + brightness | Feels clickable, provides feedback |
| Button (secondary/ghost) | Background fill on hover | Reveals affordance without being heavy |
| Card (clickable) | Lift + shadow + slight scale | Clearly interactive |
| Card (non-clickable) | None or very subtle shadow | Don't imply clickability |
| Navigation link | Underline reveal or background slide | Clear focus indication |
| Image | Zoom in container + overlay | Shows interactivity, reveals action |
| Icon button | Background circle reveal | Common pattern (MD3, GitHub, etc.) |
| Table row | Background highlight | Helps track across columns |
| Tag/chip | Brightness change | Lightweight for small elements |

## Pattern

### Button Lift
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

### Ghost Button Background Fill
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

### Card Hover (Lift + Border + Image Zoom)
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

.card__image { overflow: hidden; }

.card__image img {
  transition: transform var(--duration-medium2) var(--ease-standard);
}

.card:hover .card__image img { transform: scale(1.05); }
```

### Link Underline Reveal
```css
.link {
  text-decoration: none;
  background-image: linear-gradient(currentColor, currentColor);
  background-size: 0% 2px;
  background-position: left bottom;
  background-repeat: no-repeat;
  transition: background-size var(--duration-fast) var(--ease-standard);
  padding-bottom: 2px;
}

.link:hover { background-size: 100% 2px; }

/* Slide from center variant */
.link--center { background-position: center bottom; }
```

### Image Overlay on Hover
```css
.image-card { position: relative; overflow: hidden; }

.image-card__overlay {
  position: absolute;
  inset: 0;
  background: oklch(0% 0 0 / 0);
  display: grid;
  place-content: center;
  transition: background var(--duration-medium1) var(--ease-standard);
}

.image-card:hover .image-card__overlay { background: oklch(0% 0 0 / 0.5); }

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

### Icon Button Circle Reveal
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

.icon-btn:hover { background: color-mix(in oklch, currentColor 8%, transparent); }
.icon-btn:active { background: color-mix(in oklch, currentColor 16%, transparent); }
```

### Table Row Highlight
```css
.table tbody tr {
  transition: background var(--duration-instant) var(--ease-standard);
}

.table tbody tr:hover { background: oklch(97% 0 0); }

@media (prefers-color-scheme: dark) {
  .table tbody tr:hover { background: oklch(20% 0 0); }
}
```

## Performance Rules

1. **Safe to animate on hover**: `transform`, `opacity`, `filter`, `box-shadow`, `background-color`, `border-color`, `clip-path`
2. **Avoid on hover**: `width`, `height`, `top`, `left`, `margin`, `padding` — causes layout reflow
3. **Duration**: hover-in 150–200ms, hover-out 100–150ms (faster out feels snappier)
4. **Active press**: always ≤75ms with `scale(0.97)` feedback

## Common Mistakes

- **Wrong**: Adding hover effects to decorative elements → **Right**: Only add to interactive elements — hover implies clickability
- **Wrong**: Hover effect with no focus-visible equivalent → **Right**: Every hover effect needs a keyboard `:focus-visible` match
- **Wrong**: `translateY(-8px)` on card hover → **Right**: Keep to 2-4px maximum; more feels cartoonish
- **Wrong**: Same transition duration for enter and exit → **Right**: Hover-out should be 25-50% shorter than hover-in
- **Wrong**: Movement effects with no reduced-motion fallback → **Right**: Replace movement with opacity/color changes under `prefers-reduced-motion`

## See Also

- [Micro-Interactions](micro-interactions.md) — easing tokens and interaction principles
- [3D Transforms](3d-transforms.md) — mouse-tracked 3D tilt with JavaScript
- [Elevation and Shadows](elevation-and-shadows.md) — shadow token system for hover states
- [Accessibility and Motion](accessibility-and-motion.md) — reduced motion alternatives
