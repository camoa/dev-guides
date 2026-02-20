---
description: Build semantic spacing and layout tokens for consistent vertical rhythm
---

# Spacing & Layout Token System

## When to Use

> Use this when building semantic spacing and layout tokens for consistent vertical rhythm, grid gaps, and container widths.

## Decision

| Token Type | Pattern | Example |
|---|---|---|
| Base spacing unit | --spacing | --spacing: 0.25rem (1 = 4px, 2 = 8px, etc.) |
| Custom spacing | --spacing-{name} | --spacing-gutter: 1.5rem |
| Responsive gaps | @utility with breakpoint variants | gap-xs: gap-1 md:gap-2 |
| Responsive margins | @utility with breakpoint variants | mb-sm: mb-4 lg:mb-8 |
| Grid column templates | --grid-cols-{name} | --grid-cols--66x33: minmax(0, 2fr) minmax(0, 1fr) |
| Container widths | @utility container-{size} | container-md: px-4 lg:px-2 xl:px-0 max-w-5xl |

## Pattern

**Base Spacing Multiplier**

Tailwind v4 uses --spacing as a base unit. All numeric spacing utilities are multiples of this value.

```css
@theme {
  --spacing: 0.25rem; /* 1 = 4px, 2 = 8px, 4 = 16px, etc. */
}
```

**Semantic Spacing Utilities (from UI Suite DaisyUI starterkit)**

```css
/* Responsive semantic gaps */
@utility gap-xs { @apply gap-1 md:gap-2; }
@utility gap-sm { @apply gap-2 md:gap-4; }
@utility gap-md { @apply gap-4 md:gap-6; }
@utility gap-lg { @apply gap-6 md:gap-8; }
@utility gap-xl { @apply gap-8 md:gap-12; }

/* Responsive semantic margins */
@utility mb-xs { @apply mb-2 lg:mb-4; }
@utility mb-sm { @apply mb-4 lg:mb-8; }
@utility mb-md { @apply mb-6 lg:mb-12; }
@utility mb-lg { @apply mb-8 lg:mb-16; }
```

**Custom Grid Tokens (from UI Suite DaisyUI starterkit)**

```css
@theme {
  --grid-cols--66x33: minmax(0, 2fr) minmax(0, 1fr);
  --grid-cols--33x66: minmax(0, 1fr) minmax(0, 2fr);
}

@utility grid-2-66x33 {
  @apply grid-cols-1 md:grid-cols-(--grid-cols--66x33);
}
```

**Semantic Container Widths (from starterkit)**

```css
@utility container-md { @apply px-4 lg:px-2 xl:px-0 max-w-5xl mx-auto; }
@utility container-lg { @apply px-4 xl:px-0 max-w-6xl mx-auto; }
```

## Common Mistakes

- **Wrong**: Using fixed pixel values everywhere. **Right**: Reference --spacing or custom spacing tokens for consistency.
- **Wrong**: Creating one-off responsive utilities per component. **Right**: Define semantic responsive utilities once, reuse everywhere.

## See Also

- [UI Suite DaisyUI Starterkit Patterns](ui-suite-daisyui-starterkit-patterns.md)
- [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md)
- Reference: ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/css/utilities/
