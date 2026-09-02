---
description: Ensure Tailwind produces minimal CSS, builds fast, and doesn't generate unused styles — class detection and bundle size guidance.
tldr: "Use when diagnosing large CSS bundles, slow builds, or missing classes at runtime."
---

# Performance & Optimization

## When to Use

> Ensuring Tailwind produces minimal CSS output, builds quickly, and doesn't generate unused styles.

## Decision

| Performance issue | Solution |
|--------------------|----------|
| CSS bundle too large | Check for dynamic class construction (scanner misses static; safelistings pile up) |
| Build too slow (v4) | Use Vite plugin over PostCSS; v4 is already ~180x faster on incremental |
| Build too slow (v3) | JIT is default since v3.0; ensure `content` paths are as specific as possible |
| Classes not found at runtime | Use static class name lookups, never dynamic string interpolation |
| Unnecessary classes in output | Avoid `@source inline()` safelisting unless required |

## How Class Detection Works (and How to Break It)

Tailwind scans source files as plain text — it finds tokens that look like class names. It **does not execute JavaScript or parse templates**.

```js
// ✗ Dynamic construction — these classes WILL NOT be detected
const cls = `bg-${color}-500`;          // scanner sees "bg-" only
const cls = 'bg-' + shade;              // same problem

// ✓ Static lookup — scanner finds complete class names
const colorMap = {
  blue: 'bg-blue-500 hover:bg-blue-600',
  red:  'bg-red-500  hover:bg-red-600',
};
const cls = colorMap[color];            // ✓ complete strings
```

## Content Path Performance (v3)

```js
// v3: Be specific — overly broad globs scan unnecessary files
content: [
  './src/**/*.{jsx,tsx,ts}', // ✓ specific extensions
  // './src/**/*',           // ✗ scans images, fonts, binaries
],
```

## v4 Automatic Detection

v4 automatically excludes `.gitignore` entries, `node_modules`, binary files, CSS files, and lock files. No manual content configuration. Override only when needed:

```css
@source "../node_modules/@company/ui";      /* include external package */
@source not "../src/generated";            /* exclude generated code */
@import "tailwindcss" source(none);        /* disable auto-detection entirely */
```

## Bundle Size Considerations

- Tailwind v4 generates only the CSS for classes found in source — final bundle for typical apps: 5-20kB gzipped
- Animations and keyframes are only generated when `animate-*` classes appear in source
- The `@layer base` reset (Preflight) adds ~2kB; disable with `@import "tailwindcss/utilities"` if using a different reset
- Container query styles add per-container overhead — use sparingly in deeply nested layouts

## Common Mistakes

- **Safelisting with `@source inline("bg-{red,blue,green}-{100..900..100}")` for every color** — generates thousands of classes; use static lookup maps instead
- **Leaving `node_modules` in v3 content globs** — dramatically slows scanning
- **Expecting v3 JIT to be enabled via `mode: 'jit'`** — JIT is the only mode since v3.0; the config key is a no-op
- **Building production CSS without a minification step** — PostCSS with `cssnano` or the built-in Vite minification is required

## See Also

- [Best Practices & Anti-Patterns](best-practices.md)
- [Design System Integration](design-system-integration.md)
- Reference: https://tailwindcss.com/docs/detecting-classes-in-source-files
