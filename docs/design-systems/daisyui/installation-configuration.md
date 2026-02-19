---
description: Install and configure DaisyUI with Tailwind v4 (CSS-first) or Tailwind v3 (JS config)
---

# Installation and Configuration

## When to Use

> Setting up DaisyUI in a new or existing Tailwind project.

## Decision

| If you're using... | Install method | Config location |
|--------------------|----------------|-----------------|
| Tailwind v4 (CSS-first) | `@plugin "daisyui"` in CSS | `globals.css` / main CSS entry |
| Tailwind v3 (JS config) | `plugins: [require('daisyui')]` | `tailwind.config.js` |
| CDN (no build step) | `<link href="https://cdn.jsdelivr.net/npm/daisyui@5/daisyui.css">` | No config |

## Pattern

**Tailwind v4 — current standard:**

```css
/* globals.css */
@import "tailwindcss";
@plugin "daisyui";

/* Optional: customize active themes */
@plugin "daisyui" {
  themes: light --default, dark --prefersdark, cupcake;
  logs: false;
}
```

```bash
npm install daisyui
```

**Tailwind v3 — legacy:**

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
| `themes` | `["light --default", "dark --prefersdark"]` | Which themes to include. `"all"` for all 35+. `--default` sets root default. `--prefersdark` triggers on `prefers-color-scheme: dark` |
| `logs` | `true` | Console log on build. Set `false` in CI |
| `prefix` | `""` | Class prefix. `prefix: "d-"` makes `.d-btn`, `.d-card` |
| `root` | `":root"` | Where theme CSS variables are applied |
| `include` / `exclude` | — | Array of component names to include or exclude |

**Selective component loading (reduces CSS output):**

```css
@plugin "daisyui" {
  exclude: carousel, countdown, diff, mockup;
}
```

Source: `node_modules/daisyui/functions/pluginOptionsHandler.js`

## Common Mistakes

- **Wrong**: Installing DaisyUI with Tailwind v4 using v3 JS config — **Right**: v4 requires `@plugin` in CSS
- **Wrong**: Including all themes when you only need 2-3 — **Right**: Specify only your needed themes to reduce build noise
- **Wrong**: Omitting `--default` flag — **Right**: Without it, no theme applies to `:root` and all components render with no color

## See Also

- [DaisyUI vs Alternatives](daisyui-vs-alternatives.md)
- [Theming System](theming-system.md)
- Reference: `design-system-tailwind.md` Section 2 — Tailwind v4 CSS-first installation
