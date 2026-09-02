---
description: Configure a Tailwind v4 project using CSS-first @theme blocks — add tokens, override defaults, and define custom utilities.
tldr: "Use when configuring a Tailwind v4 project. All configuration lives in CSS via `@theme` — no JS config file required."
---

# v4 Configuration: CSS-First

## When to Use

> Configuring a Tailwind v4 project — customizing the theme, adding tokens, and extending utilities.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Add new tokens (colors, fonts, etc.) | `@theme { --color-*: value }` | Extends defaults; generates utility classes automatically |
| Remove all default colors, use only yours | `@theme { --color-*: initial; --color-brand: ... }` | Namespace reset prevents default utilities from generating |
| Override a single default breakpoint | `@theme { --breakpoint-sm: 30rem }` | Replaces only that token; others remain |
| Wipe ALL defaults, full custom theme | `@theme { --*: initial; ... }` | Complete blank slate |
| Reference design token in CSS | `var(--color-brand)` | All `@theme` variables are exposed as CSS custom properties |
| Load v3 JS config (gradual migration) | `@config "../../tailwind.config.js"` | Bridges v3 config; not all v3 keys are supported |

## Pattern — Full v4 CSS Config File

```css
@import "tailwindcss";

/* Extend defaults — add tokens without removing defaults */
@theme {
  --color-brand-500: oklch(0.65 0.18 260);
  --color-brand-600: oklch(0.55 0.20 260);
  --font-display: "Inter", "sans-serif";
  --breakpoint-3xl: 120rem;
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Custom utilities (v4 replaces @layer utilities) */
@utility content-auto {
  content-visibility: auto;
}

/* Custom variant */
@custom-variant theme-dark (&:where([data-theme="dark"], [data-theme="dark"] *));

/* Additional source paths (if auto-detection misses them) */
@source "../node_modules/@company/ui-lib";
```

## @theme Namespace Reference

Verified from `node_modules/tailwindcss/theme.css` (v4.2.0):

| Namespace | Generated utilities | Example token |
|-----------|---------------------|---------------|
| `--color-*` | `bg-`, `text-`, `border-`, `ring-`, `fill-`, `stroke-` | `--color-brand: oklch(...)` |
| `--font-*` | `font-family` utilities | `--font-display: "Inter"` |
| `--text-*` | `text-size` utilities; paired `--text-*--line-height` sets line-height automatically | `--text-xl: 1.25rem` |
| `--font-weight-*` | `font-weight` utilities | `--font-weight-semibold: 600` |
| `--tracking-*` | `tracking-` (letter-spacing) utilities | `--tracking-wide: 0.025em` |
| `--leading-*` | `leading-` (line-height) utilities | `--leading-relaxed: 1.625` |
| `--spacing` | Base multiplier for ALL spacing utilities (p-, m-, w-, h-, gap-) | `--spacing: 0.25rem` (4px) |
| `--spacing-*` | Named spacing tokens | `--spacing-18: 4.5rem` |
| `--radius-*` | `rounded-` utilities | `--radius-xs: 0.125rem` through `--radius-4xl: 2rem` |
| `--shadow-*` | `shadow-` utilities | `--shadow-sm`, `--shadow-md`, `--shadow-2xl` |
| `--inset-shadow-*` | `inset-shadow-` utilities | `--inset-shadow-sm: inset 0 2px 4px ...` |
| `--drop-shadow-*` | `drop-shadow-` filter utilities | `--drop-shadow-md: 0 3px 3px ...` |
| `--text-shadow-*` | `text-shadow-` utilities | `--text-shadow-sm`, `--text-shadow-lg` |
| `--blur-*` | `blur-` utilities | `--blur-xs: 4px` through `--blur-3xl: 64px` |
| `--breakpoint-*` | Responsive variants (`sm:`, `lg:`, etc.) | `--breakpoint-3xl: 120rem` |
| `--container-*` | Container query size tokens (`@sm:`, `@lg:`, etc.) | `--container-sm: 24rem` through `--container-7xl: 80rem` |
| `--animate-*` | `animate-` utilities; `@keyframes` live inside `@theme` block | `--animate-slide-in: slide-in 0.3s` |
| `--ease-*` | `ease-` utilities | `--ease-in: cubic-bezier(0.4, 0, 1, 1)` |
| `--perspective-*` | `perspective-` utilities | `--perspective-normal: 500px` |
| `--aspect-*` | `aspect-` utilities | `--aspect-video: 16 / 9` |

**Default color families in v4.2.0**: `red`, `orange`, `amber`, `yellow`, `lime`, `green`, `emerald`, `teal`, `cyan`, `sky`, `blue`, `indigo`, `violet`, `purple`, `fuchsia`, `pink`, `rose`, `slate`, `gray`, `zinc`, `neutral`, `stone`, `black`, `white`. Plus new neutral families: `mauve`, `olive`, `mist`, `taupe`.

**Important internal detail**: Tailwind's built-in defaults use `@theme default { ... }` (with the `default` modifier), meaning user `@theme` blocks automatically override them without needing `initial`. Your custom tokens always win.

## Content Detection (@source)

v4 auto-detects files; explicit configuration only needed when:

```css
@source "../node_modules/@company/ui-lib"; /* external packages */
@source not "../src/legacy";               /* ignore paths */
@import "tailwindcss" source("../src");    /* restrict base path */

/* Force-generate specific classes (safelisting) */
@source inline("hover:bg-brand-{500,600}");
```

## Pattern — Next.js Font Integration (Verified)

This is the pattern generated by `create-next-app` with Tailwind v4. The key is that Next.js injects CSS variable names for font stacks, and `@theme inline` aliases them into Tailwind utilities.

```css
/* globals.css — actual generated pattern from create-next-app */
@import "tailwindcss";

@theme inline {
  /* Next.js font variables → Tailwind font utilities */
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
}
```

```tsx
/* layout.tsx — Next.js loads fonts and sets CSS variables on <body> */
import { Geist, Geist_Mono } from 'next/font/google';

const geistSans = Geist({ variable: '--font-geist-sans', subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
```

The `@theme inline` modifier forces Tailwind to resolve the CSS variable value at utility generation time rather than creating a `var()` reference. Without `inline`, `font-sans` would generate `font-family: var(--font-sans)` which works fine at runtime but doesn't work if you use the font in a CSS context that resolves early.

## Partial Imports (Selective)

Import only specific layers to avoid unused styles:

```css
/* Only the utility classes, no preflight reset */
@import "tailwindcss/utilities";

/* Only preflight reset */
@import "tailwindcss/preflight";

/* Only the theme variables */
@import "tailwindcss/theme";
```

## Common Mistakes

- **Defining `@theme` variables inside nested selectors** — must be top-level; Tailwind validates this
- **Using `var(--font-inter)` inside `@theme` without the `inline` modifier** — use `@theme inline { --font-sans: var(--font-inter) }` to force resolution
- **Forgetting that `--spacing` (singular) is the base multiplier** — while `--spacing-18` adds a named token
- **Assuming your `@theme` values override defaults by adding `!important`** — unnecessary; Tailwind uses `@theme default` for built-ins which user tokens automatically override

## See Also

- [v3 Configuration](v3-configuration.md)
- [Design Token Mapping](design-token-mapping.md)
- Reference: https://tailwindcss.com/docs/theme
- Reference: https://tailwindcss.com/docs/adding-custom-styles
