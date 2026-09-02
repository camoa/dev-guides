---
description: Install and configure DaisyUI with Tailwind v4 (CSS-first) or Tailwind v3 (JS config)
tldr: "Setting up DaisyUI in a new or existing Tailwind project."
---

# Installation and Configuration

## When to Use

> Setting up DaisyUI in a new or existing Tailwind project.

## Decision: Install Method

| If you're using... | Install method | Config location |
|---|---|---|
| Tailwind v4 (CSS-first) | `@plugin "daisyui"` in CSS | `globals.css` / main CSS entry |
| Tailwind v3 (JS config) | `plugins: [require('daisyui')]` | `tailwind.config.js` |
| CDN (no build step) | `<link href="https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css">` | No config |

## Pattern: Tailwind v4 — Current Standard

```css
/* globals.css */
@import "tailwindcss";
@plugin "daisyui";

/* Optional: customize which themes are active */
@plugin "daisyui" {
  themes: light --default, dark --prefersdark, cupcake;
  logs: false;
}
```

```bash
npm install daisyui
```

## Pattern: Tailwind v3 — Legacy

```js
// tailwind.config.js
module.exports = {
  plugins: [require('daisyui')],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
    logs: false,
  },
}
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `themes` | `["light --default", "dark --prefersdark"]` | Which themes to include. Use `"all"` for all 35+. Use `--default` flag for the root default. Use `--prefersdark` to apply on `prefers-color-scheme: dark` |
| `logs` | `true` | Console log on build. Set `false` in CI |
| `prefix` | `""` | Class prefix. `prefix: "d-"` makes `.d-btn`, `.d-card`. Avoids conflicts with other libraries |
| `root` | `":root"` | Where theme CSS variables are applied |
| `include` / `exclude` | — | Array of component names to include or exclude. `exclude: ["drawer", "hero"]` trims unused CSS |

## Selective Component Loading

```css
/* Only load specific components (reduces CSS output) */
@plugin "daisyui" {
  exclude: carousel, countdown, diff, mockup;
}
```

Source: `node_modules/daisyui/functions/pluginOptionsHandler.js` — the `include`/`exclude` arrays filter component registration at build time.

## Common Mistakes

- Installing DaisyUI with Tailwind v4 using v3 JS config — v4 requires `@plugin` in CSS
- Including all themes when you only need 2-3 — each theme adds ~25 CSS variable declarations; `themes: "all"` adds 35 themes (negligible CSS size, but adds build time noise)
- Forgetting the `--default` flag — without it, no theme applies to `:root` and all components render with no color

## See Also

- [DaisyUI vs Alternatives](daisyui-vs-alternatives.md)
- [Theming System](theming-system.md)
- Reference: `design-system-tailwind.md` Section 2 — Tailwind v4 CSS-first installation
