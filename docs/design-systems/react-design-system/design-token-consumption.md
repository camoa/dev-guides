---
description: Connect design tokens to React components using CSS custom properties and Tailwind v4 CSS-first @theme inline configuration.
---

# Design Token Consumption

## When to Use

> Use when connecting design tokens (colors, spacing, typography scales) from a design tool or token file into React components. Tailwind v4 changes the approach significantly — there is no `tailwind.config.ts`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Colors, spacing, radii from design tokens | CSS custom properties (`--token-name`) | Works everywhere; no JS bundle cost; theme-switchable at runtime |
| Token values as Tailwind utility classes (v4) | `@theme inline { --color-primary: ... }` in CSS | v4 CSS-first; Tailwind generates utilities from `@theme` tokens automatically |
| Token values as Tailwind utility classes (v3) | `tailwind.config.ts` `theme.extend.colors` | v3 JS config; generates utility classes from token map |
| Per-component token overrides | CSS custom property on root element | Component-scoped token; avoids global cascade issues |
| Token type safety in TypeScript | `const tokens = { ... } as const;` + derive types | Autocompletion for token names; catches typos at build time |
| Dark mode / theme switching | CSS custom property reassignment under `@media (prefers-color-scheme)` or `[data-theme]` | Zero JS; instant switch; no flash |

## Pattern

Tailwind v4 CSS-first token setup (verified from installed `globals.css`):
```css
/* globals.css — Tailwind v4 pattern */
@import "tailwindcss";  /* replaces @tailwind base/components/utilities */

:root {
  --background: #ffffff;
  --foreground: #171717;
}

/* @theme inline maps CSS custom properties to Tailwind utility classes */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  /* Results in: bg-background, text-foreground, border-background, etc. */
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}
```

Adding design tokens in Tailwind v4:
```css
/* Extend @theme with your design tokens — no tailwind.config.ts needed */
@theme inline {
  --color-primary: oklch(55% 0.2 250);
  --color-primary-foreground: oklch(98% 0 0);
  --radius-md: 0.375rem;
  --spacing-section: 2rem;
}
/* Components use: className="bg-primary text-primary-foreground rounded-md" */
/* Tailwind v4 generates utilities for every --color-*, --radius-*, --spacing-* token */
```

## Common Mistakes

- **Wrong**: Using `tailwind.config.ts` in a Tailwind v4 project → **Right**: v4 ignores it; use `@theme inline { }` in CSS instead
- **Wrong**: Hard-coding hex values in Tailwind classes → **Right**: Define tokens in `@theme inline`; hard-coded values require find-and-replace on change
- **Wrong**: Importing JSON token files into JS and applying as inline styles → **Right**: Loses Tailwind utility integration and dark mode
- **Wrong**: Creating a React Context just to distribute token values → **Right**: CSS custom properties already cascade; Context adds unnecessary re-renders
- **Wrong**: Tailwind arbitrary values (`bg-[#0070f3]`) for design token colors → **Right**: Define in `@theme inline` then use the generated utility
- **Wrong**: Defining colors without the `--color-` prefix in Tailwind v4 → **Right**: Only `--color-*` variables generate `bg-*` / `text-*` utilities

## See Also

- [Variant Management](variant-management.md)
- [TypeScript Patterns](typescript-patterns.md)
- Reference: [Tailwind CSS v4 upgrade guide](https://tailwindcss.com/docs/v4-upgrade)
- Reference: [shadcn/ui Theming](https://ui.shadcn.com/docs/theming)
- Reference: Source — `src/app/globals.css`
