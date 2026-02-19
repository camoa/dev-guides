---
description: Connect Figma or Style Dictionary token pipelines to Tailwind configuration and maintain design-to-code consistency.
---

# Design System Integration

## When to Use

> Use when connecting a design tool (Figma) or token management system to Tailwind configuration — keeping design and implementation in sync.

## Decision

| Tool/Need | Approach |
|-----------|----------|
| Figma Variables → Tailwind tokens | Tailwind Tokens Figma plugin or manual export |
| Token JSON → multiple outputs (CSS, JS, SCSS) | Style Dictionary |
| Manual sync (small team) | Export Figma Variables as CSV, maintain `@theme` manually |
| Monorepo token sharing | CSS `@import` of shared `theme.css` |
| Token validation in CI | `npx style-dictionary build` in pipeline |

## Pattern — Style Dictionary Integration

```json
// tokens/colors.json
{
  "color": {
    "brand": {
      "500": { "value": "oklch(0.65 0.18 260)", "type": "color" },
      "600": { "value": "oklch(0.55 0.20 260)", "type": "color" }
    }
  }
}
```

```js
// style-dictionary.config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      prefix: 'color',
      buildPath: 'src/styles/',
      files: [{ destination: '_tokens.css', format: 'css/variables' }],
    },
  },
};
```

```css
/* styles.css — reference generated tokens inside @theme */
@import "tailwindcss";
@import "./_tokens.css";

@theme inline {
  --color-brand-500: var(--color-brand-500);
}
```

## Naming Conventions for Cross-Tool Consistency

| Design tool naming | Tailwind token naming | Generated utility |
|--------------------|-----------------------|-------------------|
| `color/brand/500` | `--color-brand-500` | `bg-brand-500` |
| `spacing/4` | `--spacing-4` | `p-4`, `m-4`, `gap-4` |
| `radius/md` | `--radius-md` | `rounded-md` |
| `shadow/card` | `--shadow-card` | `shadow-card` |
| `font/display` | `--font-display` | `font-display` |

Use Tailwind's namespace pattern in your design tool. Tokens named with `/` separators in Figma map cleanly to `--namespace-*` patterns with forward slashes converted to hyphens.

## Common Mistakes

- **Wrong**: Naming tokens by component (`--button-background`) instead of role (`--color-primary`). **Right**: Component-named tokens don't reuse across components; semantic/role tokens do.
- **Wrong**: Hand-translating hex values without an automated pipeline. **Right**: Drift starts immediately; automate the sync.
- **Wrong**: Not locking token names to a versioned contract. **Right**: A designer renaming `brand-blue` to `cobalt` in Figma breaks all downstream consumers without a versioning strategy.

## See Also

- [Design Token Mapping](design-token-mapping.md)
- [Performance Optimization](performance-optimization.md)
- Design System Recognition Guide (separate guide — identify tokens first)
- Reference: https://styledictionary.com/
- Reference: https://www.figma.com/community/plugin/1513618945140968492
