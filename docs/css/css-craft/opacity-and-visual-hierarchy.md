---
description: Create text and UI hierarchy with alpha channels — primary/secondary/tertiary opacity tokens, state overlays, color-mix() for token-based transparency
tldr: "Use color alpha for text hierarchy (primary/secondary/tertiary weight) without changing font size or weight. Use `color-mix()` to create semi-transparent versions of existing tokens."
---

# Opacity and Visual Hierarchy

## When to Use
Text and UI elements at uniform opacity look flat and unprioritized. Design systems use alpha-channel hierarchy to create primary/secondary/tertiary visual weight without changing font size or weight.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Text hierarchy (primary/secondary/tertiary) | Color alpha channel (`hsl(... / 0.7)`) | Does not affect child elements |
| Semi-transparent overlay from an existing token | `color-mix(in srgb, var(--token) 32%, transparent)` | Works with any color token, no hardcoded rgba |
| Hover/focus/pressed state overlay | State overlay alpha tokens (0.08/0.12/0.16) | MD3-standard, subtle, consistent |
| Disabled element | `--alpha-disabled: 0.38` on color + no pointer events | Universally recognized disabled pattern |
| Modal backdrop scrim | `color-mix(in srgb, var(--color-text) 32%, transparent)` | Dims background without hardcoded colors |

## Pattern

**Text hierarchy via color alpha** (NOT the `opacity` property):

```css
:root {
  /* Alpha values — consistent across major design systems */
  --alpha-primary:     1.0;    /* Headlines, body, primary labels */
  --alpha-secondary:   0.7;    /* Subtitles, descriptions, metadata */
  --alpha-tertiary:    0.5;    /* Captions, hints, timestamps */
  --alpha-disabled:    0.38;   /* Disabled labels, inactive controls */
  --alpha-placeholder: 0.5;    /* Input placeholders */

  /* State overlay alpha */
  --state-hover:    0.08;      /* Surface hover overlay */
  --state-focus:    0.12;      /* Surface focus overlay */
  --state-pressed:  0.16;      /* Surface active/pressed overlay */
  --state-dragged:  0.16;
  --state-disabled: 0.38;      /* Disabled element opacity */

  /* Structural */
  --divider:        0.12;      /* Divider lines */
  --overlay-scrim:  0.32;      /* Modal backdrop */
}

/* Light mode text */
[data-theme="light"] {
  --text-primary:   hsl(220 15% 10% / var(--alpha-primary));
  --text-secondary: hsl(220 10% 20% / var(--alpha-secondary));
  --text-tertiary:  hsl(220 10% 30% / var(--alpha-tertiary));
}

/* Dark mode text */
[data-theme="dark"] {
  --text-primary:   hsl(0 0% 100% / 0.87);
  --text-secondary: hsl(0 0% 100% / 0.6);
  --text-tertiary:  hsl(0 0% 100% / 0.38);
}
```

**`color-mix()` for token-based alpha** — create semi-transparent versions of existing tokens without hardcoding rgba values:

```css
.scrim {
  background: color-mix(in srgb, var(--color-text) 32%, transparent);
}

.divider {
  border-color: color-mix(in srgb, var(--color-text) 12%, transparent);
}

.hover-overlay {
  background: color-mix(in srgb, var(--color-primary) 8%, transparent);
}
```

> **Feature reference:** See [modern-css → color-mix](../modern-css/color-mix.md) for `color-mix()` syntax and browser support.

## Common Mistakes
- Using the `opacity` property for text hierarchy — `opacity` affects ALL children (icons, badges, nested elements); use color alpha instead
- Hardcoding `rgba(0,0,0,0.7)` for secondary text — breaks when the theme changes; use tokens with alpha channels
- Skipping the disabled state alpha — disabled elements without reduced opacity are not recognizable as disabled
- Same alpha values in dark and light modes — dark mode text on dark backgrounds needs different alpha values (0.87/0.6/0.38 vs 1.0/0.7/0.5)
- Using `color-mix()` without understanding the percentage — `color-mix(in srgb, black 8%, transparent)` means 8% of the first color, 92% transparent

## See Also
- [Elevation and Shadows](elevation-and-shadows.md) — shadow alpha for depth
- [Accessibility and Motion](accessibility-and-motion.md) — contrast requirements for reduced alpha text
- Reference: [MD3 State Layers](https://m3.material.io/foundations/interaction/states/state-layers)
- Reference: [Workday Canvas: Opacity Tokens](https://canvas.workday.com/styles/tokens/opacity)
