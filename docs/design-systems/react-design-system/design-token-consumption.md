---
description: Connect design tokens to React components using CSS custom properties and Tailwind v4 CSS-first @theme inline configuration.
tldr: "Use when connecting design tokens (colors, spacing, typography scales) from a design tool or token file into React components. Tailwind v4 changes the approach significantly — there is no `tailwind.config.ts`."
---

# Design Token Consumption

## When to Use

> When connecting design tokens (colors, spacing, typography scales) from a design tool or token file into React components.

> **Tailwind v4 (installed: 4.2.0) changes this significantly.** There is no `tailwind.config.ts` in Tailwind v4. All theme configuration is done in CSS using `@theme inline { }`. The v3 JS config approach is superseded. See patterns below.

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

Tailwind v3 reference (for v3 projects — not this install):
```ts
// tailwind.config.ts (v3 only — does not apply to Tailwind v4)
export default {
  theme: {
    extend: {
      colors: {
        primary: 'hsl(var(--color-primary) / <alpha-value>)',
      },
    },
  },
};
```

## Common Mistakes

- Using `tailwind.config.ts` in a Tailwind v4 project → v4 ignores it; use `@theme inline { }` in CSS instead
- Hard-coding hex values in Tailwind classes → bypasses the token system; changes require find-and-replace across all components
- Importing JSON token files into JS and applying as inline styles → loses Tailwind utility integration and dark mode
- Creating a React Context just to distribute token values → CSS custom properties already cascade; Context adds unnecessary re-renders
- Using Tailwind arbitrary values (`bg-[#0070f3]`) for design token colors → breaks the token abstraction; define in `@theme inline` then use the generated utility
- In Tailwind v4: defining colors without the `--color-` prefix → only `--color-*` variables generate `bg-*` / `text-*` utilities; `--primary` alone won't generate `bg-primary`

## See Also

- [Variant Management](variant-management.md)
- [TypeScript Patterns](typescript-patterns.md)
- Reference: Installed `globals.css` — `src/app/globals.css`
- Reference: [Tailwind v4 docs](https://tailwindcss.com/docs/upgrade-guide)
- Reference: [shadcn/ui theming](https://ui.shadcn.com/docs/theming)
- Reference: [UXPin — Managing Global Styles with Design Tokens](https://www.uxpin.com/studio/blog/managing-global-styles-in-react-with-design-tokens/)
