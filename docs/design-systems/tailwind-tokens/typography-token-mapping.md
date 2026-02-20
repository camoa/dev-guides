---
description: Map typography decisions to Tailwind v4 and DaisyUI token systems
---

# Typography Token Mapping

## When to Use

> Use this when mapping typography decisions (font families, sizes, weights) into the Tailwind v4 / DaisyUI token system.

## Decision

| Typography Element | Token Namespace | Example |
|---|---|---|
| Font family | --font-{name} | --font-sans, --font-display |
| Font weight | --font-weight-{name} | --font-weight-semibold |
| Font size | --text-{name} | --text-lg, --text-title-xl |
| Line height | --leading-{name} | --leading-tight |
| Letter spacing | --tracking-{name} | --tracking-wide |

## Pattern

**Font Family in @theme**

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@400;700&display=swap');

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-serif: "Merriweather", ui-serif, Georgia, serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
  --font-display: "Inter", system-ui, sans-serif;
}
```

This generates utilities: font-sans, font-serif, font-mono, font-display.

**Custom Type Scale**

The UI Suite DaisyUI starterkit defines a semantic type scale. This pattern is recommended:

```css
@theme {
  /* Title scale -- for headings */
  --text-title-2xl: 2.625rem;
  --text-title-xl: 2.25rem;
  --text-title-lg: 1.75rem;
  --text-title-md: 1.375rem;
  --text-title-sm: 1.125rem;
  --text-title-xs: 1rem;
  --text-title-2xs: 0.875rem;

  /* Copy scale -- for body text */
  --text-copy-2xl: 1.375rem;
  --text-copy-xl: 1.125rem;
  --text-copy-lg: 1rem;
  --text-copy-md: 0.875rem;
  --text-copy-sm: 0.75rem;
  --text-copy-xs: 0.625rem;
}
```

Creates utilities like text-title-xl, text-copy-md.

**Semantic Utility Aliases**

```css
@utility title-xl {
  @apply text-title-xl;
}
@utility copy-md {
  @apply text-copy-md;
}
```

## Common Mistakes

- **Wrong**: Defining heading sizes in @layer base with fixed pixel values. **Right**: Define tokens in @theme, apply via utilities or @layer base referencing the tokens.
- **Wrong**: Loading Google Fonts via link AND @import. **Right**: Pick one. @import in CSS is simpler for Vite/PostCSS pipelines.

## See Also

- [UI Suite DaisyUI Starterkit Patterns](ui-suite-daisyui-starterkit-patterns.md)
- [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md)
- Reference: ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/css/utilities/typography.pcss
