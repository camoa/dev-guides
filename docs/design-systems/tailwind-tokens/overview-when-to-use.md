---
description: When to use this guide and which extraction method to choose
---

# Overview & When to Use

## When to Use

> Use this guide when you have a Tailwind-based design system and need to extract tokens for a Drupal theme (CSS variables for DaisyUI / UI Suite DaisyUI), a Figma design system (token import/export), documentation (design token catalog), or multi-platform use (web + native).

## Decision

| Source | Target | Method |
|---|---|---|
| Tailwind v4 @theme {} | CSS variables | Already CSS variables -- direct use |
| Tailwind v4 @theme {} | DaisyUI theme | Map namespace variables to DaisyUI semantic tokens |
| Tailwind v3 tailwind.config.js | CSS variables | Extract via resolveConfig() then generate :root block |
| Tailwind classes in markup | Token catalog | Parse class usage patterns to identify active tokens |
| DaisyUI v5 theme | CSS variables | Built-in: --color-*, --radius-*, --border, etc. |
| Figma variables | Tailwind v4 config | Export JSON, map to @theme {} block |
| Figma variables | Tailwind v3 config | Export JSON, map to tailwind.config.js extend |
| Any token source | W3C Design Tokens | Convert to .tokens.json (DTCG 2025.10 spec) |
| CSS variables | Drupal SDC props | Map token names to component prop schema |

## Pattern

**Tailwind v3 vs v4: Key Differences for Tokens**

| Aspect | Tailwind v3 | Tailwind v4 |
|---|---|---|
| Configuration | tailwind.config.js (JavaScript) | @theme {} in CSS |
| Token format | JS object keys | CSS custom properties |
| Extraction | resolveConfig() + script | Read CSS directly |
| Color format | hex, rgb, hsl | oklch (default), any CSS color |
| Build tool | PostCSS plugin | Standalone engine (Lightning CSS) |
| Token access at runtime | Requires extraction step | Native var() references |

## See Also

- [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md)
- [Tailwind v3 Token Extraction](tailwind-v3-token-extraction.md)
- Reference: https://tailwindcss.com/docs/theme
