---
description: Map Figma variables to Tailwind tokens via automated pipeline
---

# Figma to Tailwind Mapping

## When to Use

> Use this when your design team maintains tokens in Figma variables and you need to consume them in a Tailwind project.

## Decision

| Export Method | Output Format | Target | Automation |
|---|---|---|---|
| Tokens Studio plugin | .tokens.json (W3C DTCG) | Style Dictionary → Tailwind | Pipeline required |
| Export Variables plugin | CSS, SCSS, Tailwind | Direct use | Manual or CI |
| Layout plugin | @theme {} blocks | Tailwind v4 native | Direct import |
| Figma REST API | JSON | Custom transform | Full automation |

## Pattern

**Workflow**

1. **Export from Figma**

Use one of these approaches:
- **Tokens Studio plugin** -- exports .tokens.json in W3C DTCG format
- **Export Variables plugin** -- exports directly to CSS, SCSS, or Tailwind format
- **Layout plugin** -- Tailwind v4 native export with @theme {} blocks
- **Figma REST API** -- GET /v1/files/:key/variables/local for programmatic access

2. **Transform to Tailwind format**

Map Figma variable collections to @theme blocks. DTCG JSON { "color": { "primary": { "$value": "#3b82f6" } } } becomes --color-primary: #3b82f6; in @theme {}.

3. **Automate with Style Dictionary**

```javascript
// style-dictionary.config.mjs
export default {
  source: ['tokens/**/*.tokens.json'],
  platforms: {
    tailwind: {
      transformGroup: 'css',
      buildPath: 'src/css/',
      files: [{ destination: 'tokens.css', format: 'css/theme-variables' }],
    },
  },
};
```

4. **Validate** -- build the project and verify utility classes are generated, CSS variables resolve correctly in DevTools, and no naming collisions exist.

## Common Mistakes

- **Wrong**: Manually copying Figma color values. **Right**: Automate the pipeline so token updates propagate automatically.
- **Wrong**: Exporting Figma modes (light/dark) as separate token files without a merge strategy. **Right**: Map modes to DaisyUI theme variants or CSS prefers-color-scheme media queries.

## See Also

- [W3C Design Tokens Format](w3c-design-tokens-format.md)
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- Reference: https://figmafy.com/figma-variables-to-code-tokens-to-tailwind-css-vars/
