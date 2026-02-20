---
description: Complete reference of Tailwind v4 @theme namespaces and generated utilities
---

# Tailwind v4 Namespace Reference

## When to Use

> Use this when you need to know which @theme variable prefix maps to which utility classes. Every namespace corresponds to one or more utility class APIs.

## Decision

| Namespace | Example Variable | Generated Utilities | Token Category |
|---|---|---|---|
| --color-* | --color-primary: oklch(55% 0.3 240) | bg-primary, text-primary, border-primary | Color |
| --font-* | --font-display: "Inter", sans-serif | font-display | Typography (family) |
| --font-weight-* | --font-weight-semibold: 600 | font-semibold | Typography (weight) |
| --text-* | --text-lg: 1.125rem | text-lg | Typography (size) |
| --leading-* | --leading-tight: 1.25 | leading-tight | Typography (line-height) |
| --tracking-* | --tracking-wide: 0.025em | tracking-wide | Typography (letter-spacing) |
| --spacing-* | --spacing-18: 4.5rem | p-18, m-18, w-18, gap-18 | Spacing |
| --spacing | --spacing: 0.25rem | Base multiplier for default scale | Spacing (base unit) |
| --breakpoint-* | --breakpoint-3xl: 1920px | 3xl:* responsive variant | Responsive |
| --container-* | --container-narrow: 640px | max-w-narrow | Layout |
| --radius-* | --radius-pill: 9999px | rounded-pill | Border radius |
| --shadow-* | --shadow-soft: 0 2px 8px ... | shadow-soft | Elevation |
| --inset-shadow-* | --inset-shadow-sm: inset 0 1px ... | inset-shadow-sm | Elevation (inset) |
| --blur-* | --blur-xs: 2px | blur-xs | Filters |
| --drop-shadow-* | --drop-shadow-lg: ... | drop-shadow-lg | Filters |
| --ease-* | --ease-snappy: cubic-bezier(...) | ease-snappy | Animation |
| --animate-* | --animate-fade: fade 0.3s ease | animate-fade | Animation |
| --aspect-* | --aspect-landscape: 16/9 | aspect-landscape | Layout |
| --perspective-* | --perspective-near: 300px | perspective-near | 3D transforms |

## Pattern

**Disabling Default Tokens**

To start from a clean slate and define only your own tokens:

```css
@theme {
  /* Remove all default colors */
  --color-*: initial;
  /* Remove all default spacing */
  --spacing: initial;

  /* Now define only your tokens */
  --color-brand: oklch(55% 0.3 240);
  --spacing: 0.25rem;
}
```

## Common Mistakes

- **Wrong**: Using --bg-primary (property-specific prefix). **Right**: --color-primary (semantic namespace). The --color-* namespace feeds bg-*, text-*, border-*, ring-*, etc.
- **Wrong**: Defining --font-size-lg. **Right**: --text-lg. The namespace for font-size utilities is --text-*.

## See Also

- [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md)
- [Custom Token Definition](custom-token-definition.md)
- Reference: https://tailwindcss.com/docs/theme
