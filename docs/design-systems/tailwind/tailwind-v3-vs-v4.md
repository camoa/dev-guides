---
description: Choose between Tailwind v3 and v4 based on browser requirements, project stage, and framework integration needs.
---

# Tailwind v3 vs v4

## When to Use

> Use v4 for new projects targeting modern browsers. Use v3 when you need legacy browser support or have an existing stable v3 project.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| New project, modern browser support | v4 | CSS-first config, built-in container queries, 180x faster incremental builds, native CSS features |
| Legacy browser support (Safari <16.4) | v3 | v4 requires `@property`, `color-mix()` — unavailable in older browsers |
| Existing v3 project, stable team | Stay on v3 | Upgrade effort rarely pays off mid-project; plan for v4 on next major version |
| Shared design system across monorepo | v4 | CSS `@theme` blocks are portable, importable; v3 configs require JS module sharing |
| Using Vite/Next.js/SvelteKit | v4 | First-party framework plugins eliminate PostCSS complexity |
| Needing container queries today | v4 | Built-in; v3 requires `@tailwindcss/container-queries` plugin |

## Pattern

```css
/* v4: single import, CSS-first config */
@import "tailwindcss";

@theme {
  --color-brand: oklch(0.65 0.18 260);
  --font-display: "Inter", sans-serif;
}
```

```js
// v3: JS config file (tailwind.config.js)
module.exports = {
  content: ['./src/**/*.{html,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: { brand: '#4f46e5' },
      fontFamily: { display: ['Inter', 'sans-serif'] },
    },
  },
};
```

## v3 → v4 Key Changes

| Aspect | v3 | v4 |
|--------|----|----|
| Config | `tailwind.config.js` | `@theme {}` in CSS |
| Import | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| Content scanning | Manual `content: []` paths | Automatic (respects `.gitignore`) |
| PostCSS plugin | `tailwindcss` | `@tailwindcss/postcss` |
| Container queries | Plugin required | Built-in |
| Colors | sRGB hex | oklch (wider P3 gamut) |
| `!important` modifier | `!flex` (prefix) | `flex!` (suffix) |
| CSS variables in arbitrary | `bg-[--color]` | `bg-(--color)` |
| Browser minimum | IE11+ (configurable) | Safari 16.4, Chrome 111, Firefox 128 |
| Custom utilities | `@layer utilities {}` | `@utility name {}` |
| Upgrade path | — | `npx @tailwindcss/upgrade` |

## Common Mistakes

- **Wrong**: Starting v4 without checking browser requirements — Safari 16.4+ rules out some enterprise environments. **Right**: Verify target browser matrix before choosing v4.
- **Wrong**: Running the v4 upgrade tool and committing without reviewing the diff — utilities are renamed (shadow-sm → shadow-xs, etc.). **Right**: Audit each renamed utility after `npx @tailwindcss/upgrade`.
- **Wrong**: Mixing v3 `@tailwind` directives with v4's `@import "tailwindcss"`. **Right**: Pick one; they are not interchangeable.

## See Also

- [Installation & Integration](installation-integration.md)
- Reference: https://tailwindcss.com/blog/tailwindcss-v4
- Reference: https://tailwindcss.com/docs/upgrade-guide
