---
description: Ensure Tailwind produces minimal CSS, builds fast, and doesn't generate unused styles — class detection and bundle size guidance.
---

# Performance & Optimization

## When to Use

> Use when diagnosing large CSS bundles, slow builds, or missing classes at runtime.

## Decision

| Performance issue | Solution |
|-------------------|----------|
| CSS bundle too large | Check for dynamic class construction; safelisted classes pile up |
| Build too slow (v4) | Use Vite plugin over PostCSS; v4 is already ~180x faster on incremental |
| Build too slow (v3) | JIT is default since v3.0; ensure `content` paths are as specific as possible |
| Classes not found at runtime | Use static class name lookup maps, never string interpolation |
| Unnecessary classes in output | Avoid `@source inline()` safelisting unless required |

## How Class Detection Works

Tailwind scans source files as plain text. It does not execute JavaScript or parse templates.

```js
// Dynamic construction — these classes WILL NOT be detected
const cls = `bg-${color}-500`;          // scanner sees "bg-" only
const cls = 'bg-' + shade;              // same problem

// Static lookup — scanner finds complete class names
const colorMap = {
  blue: 'bg-blue-500 hover:bg-blue-600',
  red:  'bg-red-500  hover:bg-red-600',
};
const cls = colorMap[color];            // complete strings detected
```

## Content Path Performance (v3)

```js
content: [
  './src/**/*.{jsx,tsx,ts}',  // specific extensions
  // './src/**/*',            // scans images, fonts, binaries — avoid
],
```

## v4 Automatic Detection

v4 auto-excludes `.gitignore` entries, `node_modules`, binary files, CSS files, and lock files. Override only when needed:

```css
@source "../node_modules/@company/ui";   /* include external package */
@source not "../src/generated";          /* exclude generated code */
@import "tailwindcss" source(none);      /* disable auto-detection entirely */
```

## Bundle Size

- Typical v4 app: 5-20kB gzipped
- Animations and keyframes only generated when `animate-*` classes appear in source
- Preflight reset adds ~2kB; disable with `@import "tailwindcss/utilities"` if using a different reset
- Production CSS requires a minification step — PostCSS with `cssnano` or Vite's built-in minification

## Common Mistakes

- **Wrong**: Safelisting every color — `@source inline("bg-{red,blue,green}-{100..900..100}")` generates thousands of classes. **Right**: Use static lookup maps.
- **Wrong**: Leaving `node_modules` in v3 content globs. **Right**: Dramatically slows scanning; exclude explicitly.
- **Wrong**: Setting `mode: 'jit'` in v3 config. **Right**: JIT is the only mode since v3.0; the key is a no-op.
- **Wrong**: Building production CSS without minification. **Right**: Use `cssnano` or Vite's built-in minifier.

## See Also

- [Best Practices](best-practices.md)
- [v4 Configuration](v4-configuration.md)
- Reference: https://tailwindcss.com/docs/detecting-classes-in-source-files
