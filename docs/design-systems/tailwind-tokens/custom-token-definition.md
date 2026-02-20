---
description: Define custom brand tokens and extend Tailwind's default theme
---

# Custom Token Definition

## When to Use

> Use this when you need tokens beyond Tailwind's defaults -- brand colors, custom spacing, project-specific breakpoints, or semantic aliases.

## Decision

| Need | Approach | Example |
|---|---|---|
| Add custom tokens, keep defaults | Add to @theme | @theme { --color-brand: oklch(55% 0.3 240); } |
| Remove defaults, define only custom | Reset first, then define | @theme { --color-*: initial; --color-brand: ...; } |
| Token without utility class | Use @theme inline | @theme inline { --color-surface-elevated: ...; } |
| Semantic alias to existing token | Reference with var() | --color-cta: var(--color-brand); |

## Pattern

**Brand Token Layer**

```css
@theme {
  --color-brand: oklch(55% 0.3 240);
  --color-brand-light: oklch(75% 0.2 240);
  --color-brand-dark: oklch(35% 0.3 240);
  --color-cta: var(--color-brand);       /* Semantic alias */
  --spacing-gutter: 1.5rem;
  --spacing-section: 4rem;
}
```

**@theme inline for Non-Utility Variables**

Use @theme inline for values that should NOT generate utility classes:

```css
@theme inline { --color-surface-elevated: oklch(99% 0.005 240); }
/* var(--color-surface-elevated) works, but no bg-surface-elevated class */
```

## Common Mistakes

- **Wrong**: Adding brand colors to :root instead of @theme. **Right**: Use @theme to get both CSS variables and utility classes.
- **Wrong**: Extending @theme in multiple files without strategy. **Right**: Consolidate all token definitions in one main CSS file or use explicit imports.

## See Also

- [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md)
- [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md)
- Reference: https://tailwindcss.com/docs/theme
