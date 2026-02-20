---
description: DaisyUI v5 semantic color roles and component mapping
---

# DaisyUI v5 Color Token System

## When to Use

> Use this when building with DaisyUI v5 (used by UI Suite DaisyUI in Drupal). DaisyUI adds a semantic color layer on top of Tailwind's raw color palette, mapping brand intentions to CSS variables.

## Decision

| Role | Purpose | Components That Use It |
|---|---|---|
| primary | Main brand action color | Buttons, links, active states, CTAs |
| secondary | Supporting brand color | Secondary buttons, badges, accents |
| accent | Highlight/emphasis color | Decorative elements, highlights |
| neutral | Dark neutral for contrast areas | Navbar, footer, dark sections |
| base-100/200/300 | Page background shades (light to dark) | Page bg, card bg, input bg, dividers |
| base-content | Default text color on base backgrounds | Body text, headings, icons |
| info | Informational feedback | Info alerts, tooltips, badges |
| success | Positive feedback | Success alerts, confirmation states |
| warning | Caution feedback | Warning alerts, validation hints |
| error | Negative/destructive feedback | Error messages, destructive actions |

## Pattern

**The -content Pair Pattern**

Every semantic color has a -content pair used as the foreground when that color is the background. DaisyUI applies it automatically (e.g., btn-primary uses --color-primary-content for text).

```css
--color-primary: oklch(45% 0.3 240);         /* dark bg */
--color-primary-content: oklch(97% 0.01 240); /* light text */
```

If you omit a -content color, DaisyUI auto-generates one based on lightness. For brand-critical colors, define explicitly.

## Common Mistakes

- **Wrong**: Using base-100 for all backgrounds. **Right**: Use base-100/200/300 progression for visual hierarchy (page, card, input).
- **Wrong**: Defining only primary/secondary/accent and skipping feedback colors. **Right**: Define info/success/warning/error for consistent state messaging.

## See Also

- [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md)
- [Brand Color Mapping Workflow](brand-color-mapping-workflow.md)
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- Reference: https://daisyui.com/docs/colors/
