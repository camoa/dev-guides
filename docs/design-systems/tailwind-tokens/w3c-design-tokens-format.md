---
description: W3C Design Tokens (DTCG) format for vendor-neutral token interchange
---

# W3C Design Tokens Format

## When to Use

> Use this when you need a vendor-neutral interchange format for sharing tokens across tools (Figma, Style Dictionary, Tailwind, native apps). The DTCG specification reached its first stable version (2025.10) in October 2025.

## Decision

| Token Type | $type Value | Example $value |
|---|---|---|
| Color | color | "oklch(55% 0.3 240)" |
| Dimension | dimension | "0.5rem" |
| Font family | fontFamily | ["Inter", "system-ui", "sans-serif"] |
| Font weight | fontWeight | "600" |
| Duration | duration | "200ms" |
| Cubic bezier | cubicBezier | [0.4, 0, 0.2, 1] |
| Shadow | shadow | { offsetX, offsetY, blur, spread, color } |
| Border | border | { color, width, style } |
| Typography | typography | { fontFamily, fontSize, lineHeight, ... } |

## Pattern

**Token File Structure**

Files use .tokens.json extension and application/design-tokens+json media type.

```json
{
  "color": {
    "primary": {
      "$value": "oklch(55% 0.3 240)",
      "$type": "color",
      "$description": "Main brand action color"
    },
    "primary-content": {
      "$value": "oklch(98% 0.01 240)",
      "$type": "color"
    }
  },
  "spacing": {
    "sm": { "$value": "0.5rem", "$type": "dimension" },
    "md": { "$value": "1rem", "$type": "dimension" },
    "lg": { "$value": "1.5rem", "$type": "dimension" }
  },
  "font-family": {
    "sans": {
      "$value": ["Inter", "system-ui", "sans-serif"],
      "$type": "fontFamily"
    }
  },
  "border-radius": {
    "field": { "$value": "0.5rem", "$type": "dimension" },
    "box": { "$value": "1rem", "$type": "dimension" }
  }
}
```

**Token Aliases**

Tokens reference other tokens with curly braces: "$value": "{color.blue-500}". This creates a dependency chain resolved at build time by tools like Style Dictionary.

**Composite Types**

Shadow example:

```json
{
  "shadow": {
    "card": {
      "$value": { "offsetX": "0px", "offsetY": "2px", "blur": "8px",
                  "spread": "0px", "color": "{color.neutral}" },
      "$type": "shadow"
    }
  }
}
```

**Conversion to Tailwind v4**

Use Style Dictionary or a simple script to flatten DTCG JSON into @theme variables:

```javascript
// dtcg-to-tailwind.mjs
import { readFileSync } from 'fs';
const tokens = JSON.parse(readFileSync('tokens.tokens.json', 'utf8'));

function toThemeVars(obj, prefix = '') {
  let vars = [];
  for (const [key, val] of Object.entries(obj)) {
    const path = prefix ? `${prefix}-${key}` : key;
    if (val.$value !== undefined) vars.push(`  --${path}: ${val.$value};`);
    else vars.push(...toThemeVars(val, path));
  }
  return vars;
}
console.log(`@theme {\n${toThemeVars(tokens).join('\n')}\n}`);
```

## Common Mistakes

- **Wrong**: Using custom $type values not in the spec. **Right**: Stick to official types for tool compatibility.
- **Wrong**: Circular alias references. **Right**: Maintain a directed acyclic graph of token dependencies.

## See Also

- [Figma to Tailwind Mapping](figma-to-tailwind-mapping.md)
- [Token Naming Conventions](token-naming-conventions.md)
- Reference: https://www.designtokens.org/tr/drafts/format/
