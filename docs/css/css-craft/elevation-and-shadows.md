---
description: Add realistic multi-layer shadows to cards, modals, and dropdowns — tinted shadow system with dark mode support
tldr: "Use elevation shadows when components need visual depth — cards resting on a surface, modals floating above content, dropdowns popping over elements. Shadows establish spatial relationships in a flat medium."
---

# Elevation and Shadows

## When to Use
When components need visual depth — cards resting on a surface, modals floating above content, dropdowns popping over elements. Shadows establish spatial relationships in a flat medium.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Card at rest on a surface | Elevation 1 (2 shadow layers) | Subtle lift, not attention-grabbing |
| Card on hover or dropdown | Elevation 2 (3 shadow layers) | Medium lift suggests interactivity |
| Modal, dialog, popover | Elevation 3 (5 shadow layers) | High lift for top-layer content |
| Dark mode depth | Tonal elevation (lightness shift) | Shadows are imperceptible on dark backgrounds |
| Irregular/clipped shapes | `filter: drop-shadow()` | `box-shadow` ignores `clip-path` |
| Diffuse glow effect | Pseudo-element with `filter: blur()` | Softer than any `box-shadow` configuration |

## Pattern

**Layered shadow system** — multiple shadows with progressive blur and offset simulate real light. Shadow color uses the background hue, not pure black:

```css
:root {
  --shadow-color: 220deg 60% 50%;
  --shadow-strength: 0.1;
}

/* Elevation 1 — Cards at rest */
.elevation-1 {
  box-shadow:
    0 0.5px 1px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.04)),
    0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.02));
}

/* Elevation 2 — Hover, dropdowns */
.elevation-2 {
  box-shadow:
    0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.04)),
    0 2px 4px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.03)),
    0 4px 8px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.02));
}

/* Elevation 3 — Modals, popovers */
.elevation-3 {
  box-shadow:
    0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.04)),
    0 2px 4px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.03)),
    0 4px 8px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.02)),
    0 8px 16px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.01)),
    0 16px 32px hsl(var(--shadow-color) / var(--shadow-strength));
}
```

**Dark mode tonal elevation** — surfaces lighten as they rise (MD3 pattern):

```css
:root {
  --surface-0: hsl(220 15% 10%);   /* Lowest — darkest */
  --surface-1: hsl(220 15% 13%);   /* +3% lightness */
  --surface-2: hsl(220 15% 15%);   /* +5% */
  --surface-3: hsl(220 15% 17%);   /* +7% */
  --surface-4: hsl(220 15% 19%);   /* +9% */
  --surface-5: hsl(220 15% 22%);   /* +12% — highest */
}

/* Dark mode: combine tonal + subtle shadow */
[data-theme="dark"] {
  --shadow-color: 220deg 40% 2%;
  --shadow-strength: 0.25;
}

[data-theme="light"] {
  --shadow-color: 220deg 60% 50%;
  --shadow-strength: 0.07;
}
```

**Alternative depth techniques:**

```css
/* drop-shadow respects clip-path and irregular shapes */
.irregular-shape {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  filter: drop-shadow(0 4px 8px hsl(0 0% 0% / 0.15));
}

/* Pseudo-element blur — softer, more diffuse glow */
.soft-shadow {
  position: relative;
}
.soft-shadow::after {
  content: '';
  position: absolute;
  inset: 5%;
  z-index: -1;
  background: inherit;
  filter: blur(20px);
  opacity: 0.4;
  border-radius: inherit;
}
```

## Common Mistakes
- Pure black shadows (`rgba(0,0,0,0.2)`) — tinted shadows matching the background hue look far more natural
- Single shadow layer for elevated elements — real light produces multiple penumbra layers at different distances
- Using `box-shadow` on elements with `clip-path` — the shadow is clipped; use `filter: drop-shadow()` instead
- Same shadow values in dark and light modes — dark mode needs higher `--shadow-strength` (0.25+) because dark backgrounds absorb shadow
- Animating `box-shadow` directly on many elements simultaneously — each shadow triggers repaint; consider `filter: drop-shadow()` or `::after` pseudo-element technique for better performance

## See Also
- [Micro-Interactions](micro-interactions.md) — hover shadow transitions
- [Animation Performance](animation-performance.md) — `box-shadow` repaint cost
- Reference: [Josh W. Comeau: Designing Beautiful Shadows](https://www.joshwcomeau.com/css/designing-shadows/)
- Reference: [MD3 Elevation](https://m3.material.io/styles/elevation/applying-elevation)
