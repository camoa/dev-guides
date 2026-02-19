---
description: Configure Tailwind v3 using tailwind.config.js — understand extend vs override, content paths, and preset sharing.
---

# v3 Configuration: tailwind.config.js

## When to Use

> Use for projects running Tailwind v3, or when using `@config` in v4 to load a JS config during gradual migration.

## Decision

| Situation | Approach | Effect |
|-----------|----------|--------|
| Add new color without losing defaults | `theme.extend.colors` | Merges; `bg-red-500` still works |
| Replace all colors with brand-only set | `theme.colors` (no extend) | Removes all defaults |
| Add custom spacing step | `theme.extend.spacing` | Keeps defaults, adds yours |
| Change all breakpoints | `theme.screens` (no extend) | Replaces default breakpoint system |

## Pattern

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,ts,jsx,tsx,vue,twig,php}',
    './templates/**/*.twig',
  ],
  theme: {
    // Override (replaces entire key — no defaults)
    screens: {
      sm: '640px', md: '768px', lg: '1024px', xl: '1280px',
    },
    extend: {
      // Extend (merges with existing defaults)
      colors: {
        brand: { 500: '#4f46e5', 600: '#4338ca' },
      },
      fontFamily: {
        display: ['Inter', 'sans-serif'],
      },
      spacing: { 18: '4.5rem' },
      borderRadius: { xl: '0.75rem' },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

## CSS Entry File

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom component classes */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-brand-500 text-white rounded-lg font-semibold;
    @apply hover:bg-brand-600 focus-visible:outline focus-visible:outline-2;
  }
}
```

## Presets (Sharing Configs Across Projects)

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

- **Wrong**: `theme.colors` instead of `theme.extend.colors` — overwrites all defaults, breaking `bg-white`, `text-gray-500`, etc. **Right**: Always use `theme.extend` unless intentionally replacing the entire scale.
- **Wrong**: `./src/**/*` in content glob — scans binary files, slowing scanning. **Right**: Always include file extensions.
- **Wrong**: Looking for v4 features (`@utility`, container queries built-in) in a v3 project — requires plugins in v3.

## See Also

- [v4 Configuration](v4-configuration.md)
- [Design Token Mapping](design-token-mapping.md)
- Reference: https://v3.tailwindcss.com/docs/configuration
