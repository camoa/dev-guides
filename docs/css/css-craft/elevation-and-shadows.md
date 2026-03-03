---
description: Add realistic multi-layer shadows to cards, modals, and dropdowns — tinted shadow system with dark mode support
---

# Elevation and Shadows

## When to Use

> Use elevation shadows when components need visual depth — cards resting on a surface, modals floating above content, dropdowns popping over elements. Shadows establish spatial relationships in a flat medium.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Card at rest on a surface | Elevation 1 (2 shadow layers) | Subtle lift, not attention-grabbing |
| Card on hover or dropdown | Elevation 2 (3 shadow layers) | Medium lift suggests interactivity |
| Modal, dialog, popover | Elevation 3 (5 shadow layers) | High lift for top-layer content |
| Dark mode depth | Tonal elevation (lightness shift) | Shadows are imperceptible on dark backgrounds |
| Irregular/clipped shapes | `filter: drop-shadow()` | `box-shadow` ignores `clip-path` |
| Diffuse glow effect | Pseudo-element with `filter: blur()` | Softer than any `box-shadow` configuration |

## Pattern

Layered shadow system — multiple shadows with progressive blur simulate real light. Shadow color uses the background hue, not pure black:

```css
:root {
  --shadow-color: 220deg 60% 50%;
  --shadow-strength: 0.1;
}

.elevation-1 {
  box-shadow:
    0 0.5px 1px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.04)),
    0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.02));
}

.elevation-2 {
  box-shadow:
    0 1px 2px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.04)),
    0 2px 4px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.03)),
    0 4px 8px hsl(var(--shadow-color) / calc(var(--shadow-strength) + 0.02));
}

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
[data-theme="dark"]  { --shadow-color: 220deg 40% 2%;  --shadow-strength: 0.25; }
[data-theme="light"] { --shadow-color: 220deg 60% 50%; --shadow-strength: 0.07; }
```

**For clipped/irregular shapes** — `box-shadow` is clipped; use `filter: drop-shadow()` instead:

```css
.irregular-shape {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  filter: drop-shadow(0 4px 8px hsl(0 0% 0% / 0.15));
}
```

## Common Mistakes

- **Wrong**: Pure black shadows `rgba(0,0,0,0.2)` — **Right**: Tint shadows to the background hue for natural results
- **Wrong**: Single shadow layer — **Right**: Real light produces multiple penumbra layers at different distances
- **Wrong**: `box-shadow` on elements with `clip-path` — **Right**: Use `filter: drop-shadow()` on a wrapper
- **Wrong**: Same shadow in dark and light modes — **Right**: Dark mode needs `--shadow-strength: 0.25+`
- **Wrong**: Animating `box-shadow` on many elements simultaneously — **Right**: Use `filter: drop-shadow()` or a `::after` pseudo-element

## See Also

- [Micro-Interactions](micro-interactions.md) — hover shadow transitions
- [Animation Performance](animation-performance.md) — `box-shadow` repaint cost
- Reference: [Josh W. Comeau: Designing Beautiful Shadows](https://www.joshwcomeau.com/css/designing-shadows/)
- Reference: [MD3 Elevation](https://m3.material.io/styles/elevation/applying-elevation)
