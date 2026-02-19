---
description: Choose the right Tailwind installation path for your build tool — Vite plugin, PostCSS, or CLI.
---

# Installation & Integration

## When to Use

> Use when setting up Tailwind in a new or existing project. Choose Vite plugin for Vite-based projects; PostCSS for everything else.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Choosing integration | Using Vite | Use `@tailwindcss/vite` plugin (faster, zero PostCSS config) |
| Choosing integration | Not using Vite | Use `@tailwindcss/postcss` |
| Content detection missing classes | Using dynamic class strings | Add `@source` directives or move to static class maps |
| Deploying to CDN (no build step) | Prototyping only | Use Play CDN — never for production |

## Pattern

```bash
# Vite (React, SvelteKit, Solid, etc.)
npm install tailwindcss @tailwindcss/vite

# PostCSS (Next.js, Angular, Nuxt, generic)
npm install tailwindcss @tailwindcss/postcss postcss

# CLI (no build tool, simple projects)
npm install tailwindcss @tailwindcss/cli
```

```ts
// vite.config.ts — Vite plugin
import tailwindcss from '@tailwindcss/vite';
export default { plugins: [tailwindcss()] };
```

```js
// postcss.config.mjs — PostCSS
export default { plugins: { '@tailwindcss/postcss': {} } };
```

```css
/* Main stylesheet — add this import */
@import "tailwindcss";
/* Your @theme customizations follow here */
```

For Next.js: add `@import "tailwindcss"` to `app/globals.css`; the PostCSS plugin handles the rest.

## Common Mistakes

- **Wrong**: Using the v3 package name `tailwindcss` as a PostCSS plugin in v4. **Right**: Install `@tailwindcss/postcss` separately.
- **Wrong**: Forgetting the `@import "tailwindcss"` in the CSS file — the plugin alone doesn't inject styles.
- **Wrong**: Adding `postcss-import` separately in v4. **Right**: Not needed; it's built-in.

## See Also

- [Tailwind v3 vs v4](tailwind-v3-vs-v4.md)
- [v4 Configuration](v4-configuration.md)
- Reference: https://tailwindcss.com/docs/installation
