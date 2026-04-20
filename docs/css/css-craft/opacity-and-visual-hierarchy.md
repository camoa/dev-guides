---
description: Create text and UI hierarchy with alpha channels — primary/secondary/tertiary opacity tokens, state overlays, color-mix() for token-based transparency
tldr: "Use color alpha for text hierarchy (primary/secondary/tertiary weight) without changing font size or weight. Use `color-mix()` to create semi-transparent versions of existing tokens."
---

# Opacity and Visual Hierarchy

## When to Use

> Use color alpha for text hierarchy (primary/secondary/tertiary weight) without changing font size or weight. Use `color-mix()` to create semi-transparent versions of existing tokens. Use `opacity` only for entire element fade, never for text hierarchy.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Text hierarchy (primary/secondary/tertiary) | Color alpha channel `hsl(... / 0.7)` | Does not affect child elements |
| Semi-transparent overlay from a token | `color-mix(in srgb, var(--token) 32%, transparent)` | Works with any color token, no hardcoded rgba |
| Hover/focus/pressed state overlay | State overlay alpha tokens (0.08/0.12/0.16) | MD3-standard, subtle, consistent |
| Disabled element | `--alpha-disabled: 0.38` on color + no pointer events | Universally recognized disabled pattern |
| Modal backdrop scrim | `color-mix(in srgb, var(--color-text) 32%, transparent)` | Dims background without hardcoded colors |

## Pattern

**Text hierarchy via color alpha** (NOT the `opacity` property):

```css
:root {
  --alpha-primary:     1.0;    /* Headlines, body, primary labels */
  --alpha-secondary:   0.7;    /* Subtitles, descriptions, metadata */
  --alpha-tertiary:    0.5;    /* Captions, hints, timestamps */
  --alpha-disabled:    0.38;   /* Disabled labels, inactive controls */
  --state-hover:       0.08;
  --state-focus:       0.12;
  --state-pressed:     0.16;
  --divider:           0.12;
  --overlay-scrim:     0.32;
}

[data-theme="light"] {
  --text-primary:   hsl(220 15% 10% / var(--alpha-primary));
  --text-secondary: hsl(220 10% 20% / var(--alpha-secondary));
  --text-tertiary:  hsl(220 10% 30% / var(--alpha-tertiary));
}

[data-theme="dark"] {
  --text-primary:   hsl(0 0% 100% / 0.87);
  --text-secondary: hsl(0 0% 100% / 0.6);
  --text-tertiary:  hsl(0 0% 100% / 0.38);
}
```

**`color-mix()` for token-based alpha:**

```css
.scrim    { background: color-mix(in srgb, var(--color-text) 32%, transparent); }
.divider  { border-color: color-mix(in srgb, var(--color-text) 12%, transparent); }
.hover-overlay { background: color-mix(in srgb, var(--color-primary) 8%, transparent); }
```

## Common Mistakes

- **Wrong**: Using the `opacity` property for text hierarchy — **Right**: `opacity` affects ALL children; use color alpha instead
- **Wrong**: Hardcoding `rgba(0,0,0,0.7)` for secondary text — **Right**: Use tokens with alpha channels that adapt when theme changes
- **Wrong**: Skipping the disabled state alpha — **Right**: Disabled elements without reduced opacity are not recognizable
- **Wrong**: Same alpha values in dark and light modes — **Right**: Dark mode uses 0.87/0.6/0.38; light mode uses 1.0/0.7/0.5
- **Wrong**: `color-mix(in srgb, black 8%, transparent)` confusion — **Right**: The percentage means 8% of first color, 92% transparent

## See Also

- [Elevation and Shadows](elevation-and-shadows.md) — shadow alpha for depth
- [Accessibility and Motion](accessibility-and-motion.md) — contrast requirements for reduced alpha text
- Reference: [MD3 State Layers](https://m3.material.io/foundations/interaction/states/state-layers)
- Reference: [Workday Canvas: Opacity Tokens](https://canvas.workday.com/styles/tokens/opacity)
