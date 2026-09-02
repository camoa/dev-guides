---
description: Configure Tailwind v3 using tailwind.config.js — understand extend vs override, content paths, and preset sharing.
tldr: "Use for projects running Tailwind v3, or when using `@config` in v4 to load a JS config during gradual migration."
---

# v3 Configuration: tailwind.config.js

## When to Use

> Projects running Tailwind v3, or when migrating an existing v3 codebase. Reference when using `@config` in v4 to load a JS config.

## Pattern — Canonical v3 Config Structure

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  // Required: paths to all files containing Tailwind classes
  content: [
    './src/**/*.{html,js,ts,jsx,tsx,vue,twig,php}',
    './templates/**/*.twig',
  ],
  theme: {
    // Override a default: replaces the entire key
    screens: {
      sm: '640px', md: '768px', lg: '1024px', xl: '1280px',
    },
    extend: {
      // Extend defaults: merges with existing values
      colors: {
        brand: {
          500: '#4f46e5',
          600: '#4338ca',
        },
      },
      fontFamily: {
        display: ['Inter', 'sans-serif'],
      },
      spacing: {
        18: '4.5rem',
      },
      borderRadius: {
        xl: '0.75rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

## Decision: extend vs override

| Situation | Approach | Effect |
|-----------|----------|--------|
| Add new color without losing defaults | `theme.extend.colors` | Merges; `bg-red-500` still works |
| Replace all colors with brand-only set | `theme.colors` (no extend) | Removes all defaults |
| Add custom spacing step | `theme.extend.spacing` | Keeps defaults, adds yours |
| Change all breakpoints | `theme.screens` (no extend) | Replaces default breakpoint system |

## v3 CSS Entry File

```css
/* Replace the deprecated @tailwind directives */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component classes go in @layer components */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-brand-500 text-white rounded-lg font-semibold;
    @apply hover:bg-brand-600 focus-visible:outline focus-visible:outline-2;
  }
}
```

## Presets (Sharing Configs)

```js
// packages/ui-tokens/preset.js — shared across projects
module.exports = {
  theme: {
    extend: {
      colors: { brand: { 500: '#4f46e5' } },
    },
  },
};

// consuming project's tailwind.config.js
module.exports = {
  presets: [require('@company/ui-tokens/preset')],
  content: ['./src/**/*.{html,js}'],
};
```

## Common Mistakes

- **Using `theme.colors` instead of `theme.extend.colors`** — overwrites all Tailwind defaults, breaking `bg-white`, `text-gray-500`, etc.
- **Omitting file extensions in `content` glob** — `./src/**/*` matches binary files, slowing content scanning
- **Checking for v4 features (container queries, `@utility`) in a v3 project** — requires plugins in v3

## See Also

- [v4 Configuration](v4-configuration.md)
- [Design Token Mapping](design-token-mapping.md)
- Reference: https://v3.tailwindcss.com/docs/configuration
