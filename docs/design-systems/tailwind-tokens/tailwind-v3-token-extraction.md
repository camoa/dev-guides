---
description: Extract design tokens from Tailwind v3 config files
---

# Tailwind v3 Token Extraction

## When to Use

> Use this when working with a Tailwind v3 project and need to extract tokens as CSS variables or a token catalog.

## Decision

| Task | Approach | Tool |
|---|---|---|
| Extract to CSS variables | resolveConfig() + script | Node.js script |
| Extract to W3C DTCG | resolveConfig() + transform | Style Dictionary |
| Convert v3 config to v4 @theme | resolveConfig() + format | Custom script |
| Audit active tokens | Parse class usage | grep/regex on templates |

## Pattern

**resolveConfig() Extraction**

```javascript
// extract-tokens.mjs
import resolveConfig from 'tailwindcss/resolveConfig.js';
import tailwindConfig from './tailwind.config.js';

const fullConfig = resolveConfig(tailwindConfig);

function extractColors(colors, prefix = '--color') {
  const vars = {};
  for (const [key, value] of Object.entries(colors)) {
    if (typeof value === 'string') vars[`${prefix}-${key}`] = value;
    else if (typeof value === 'object')
      Object.assign(vars, extractColors(value, `${prefix}-${key}`));
  }
  return vars;
}

const tokens = extractColors(fullConfig.theme.colors);
const css = `:root {\n${Object.entries(tokens)
  .map(([k, v]) => `  ${k}: ${v};`).join('\n')}\n}`;
console.log(css);
```

To generate a v4 @theme block from v3, replace :root with @theme in the output.

**Key Differences**

| v3 Extraction | v4 Extraction |
|---|---|
| Requires resolveConfig() import | Read CSS file directly |
| Outputs JS object | Already CSS variables |
| Need build step to generate CSS vars | Native CSS vars at build time |
| fullConfig.theme.colors.blue[500] | var(--color-blue-500) |

## Common Mistakes

- **Wrong**: Shipping resolveConfig to the browser. **Right**: It imports the entire Tailwind module. Use a build script to extract tokens at build time only.
- **Wrong**: Manually copying hex values from tailwind.config.js. **Right**: They may differ from resolved values after extends/overrides merge.

## See Also

- [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md)
- [W3C Design Tokens Format](w3c-design-tokens-format.md)
- Reference: https://tailwindcss.com/docs/configuration
