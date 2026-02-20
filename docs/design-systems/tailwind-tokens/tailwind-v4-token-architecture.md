---
description: Tailwind v4 @theme block architecture and utility class generation
---

# Tailwind v4 Token Architecture

## When to Use

> Use @theme {} when starting a new Tailwind v4 project or migrating from v3. Tailwind v4 is CSS-first -- the @theme block IS your design token definition.

## Decision

| Need | Choose | Why |
|---|---|---|
| Token that generates utility classes | @theme | Creates both CSS variable and utility classes |
| Variable that should NOT generate utilities | :root | Pure CSS variable, no Tailwind utility generation |
| Custom tokens extending defaults | @theme { --color-brand: ... } | Adds to existing tokens |
| Clean slate, remove all defaults | @theme { --color-*: initial; } | Resets all default values first |

## Pattern

```css
/* app.css -- Tailwind v4 token definition */
@import "tailwindcss";

@theme {
  --color-brand: oklch(55% 0.3 240);
  --color-brand-light: oklch(75% 0.2 240);
  --font-display: "Inter", system-ui, sans-serif;
  --breakpoint-3xl: 1920px;
  --spacing-18: 4.5rem;
  --radius-pill: 9999px;
}
```

This single block creates:
- CSS variables: `var(--color-brand)`, `var(--font-display)`, etc.
- Utility classes: `bg-brand`, `text-brand-light`, `font-display`, `3xl:*`, `p-18`, `rounded-pill`

**Key Principle**: @theme variables generate utility classes. Regular :root CSS variables do not.

```css
/* Generates bg-surface, text-surface utilities */
@theme {
  --color-surface: oklch(98% 0.01 240);
}

/* Does NOT generate utilities -- just a CSS variable */
:root {
  --app-header-height: 64px;
}
```

## Common Mistakes

- **Wrong**: Using :root for tokens that need utility classes. **Right**: Use @theme for utility-generating tokens, :root for structural variables.
- **Wrong**: Importing tailwindcss after @theme block. **Right**: @import "tailwindcss"; must come first.

## See Also

- [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md)
- [Custom Token Definition](custom-token-definition.md)
- Reference: https://tailwindcss.com/docs/theme
