---
description: Choose the right Tailwind installation path for your build tool — Vite plugin, PostCSS, or CLI.
tldr: "Use when setting up Tailwind in a new or existing project. Choose Vite plugin for Vite-based projects; PostCSS for everything else."
---

# Installation & Integration

## When to Use

> Setting up Tailwind in a new or existing project, choosing the right integration path.

## Steps

1. **Choose your integration method** — Vite plugin is the recommended path for Vite-based projects; PostCSS for everything else
   ```bash
   # Vite (React, SvelteKit, Solid, etc.)
   npm install tailwindcss @tailwindcss/vite

   # PostCSS (Next.js, Angular, Nuxt, generic)
   npm install tailwindcss @tailwindcss/postcss postcss

   # CLI (no build tool, simple projects)
   npm install tailwindcss @tailwindcss/cli
   ```

2. **Configure the build tool**
   ```ts
   // vite.config.ts — Vite plugin
   import tailwindcss from '@tailwindcss/vite';
   export default { plugins: [tailwindcss()] };
   ```
   ```js
   // postcss.config.mjs — PostCSS
   export default { plugins: { '@tailwindcss/postcss': {} } };
   ```

3. **Add the CSS import** to your main stylesheet
   ```css
   @import "tailwindcss";
   /* Your @theme customizations follow here */
   ```

4. **For Next.js specifically** — add `@import "tailwindcss"` to `app/globals.css`; the PostCSS plugin handles the rest. Next.js 13+ App Router works out of the box.

5. **Verify** by adding a Tailwind class to any element (`text-red-500`) and confirming styles apply.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Choosing integration | Using Vite | Use `@tailwindcss/vite` plugin (faster, zero PostCSS config) |
| Choosing integration | Not using Vite | Use `@tailwindcss/postcss` |
| Content detection missing classes | Using dynamic class strings | Add `@source` directives or move to static class maps |
| Deploying to CDN (no build step) | Prototyping only | Use Play CDN via `<script src="https://cdn.tailwindcss.com">` — never for production |

## Common Mistakes

- **Using the v3 package name `tailwindcss` as a PostCSS plugin in v4** — install `@tailwindcss/postcss` separately
- **Forgetting the `@import "tailwindcss"` in the CSS file** — the plugin alone doesn't inject styles
- **Using `postcss-import` separately in v4** — not needed, built-in

## See Also

- [Tailwind v3 vs v4](tailwind-v3-vs-v4.md)
- [v4 Configuration](v4-configuration.md)
- Reference: https://tailwindcss.com/docs/installation
