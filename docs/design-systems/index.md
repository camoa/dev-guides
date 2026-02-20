---
description: Design system guides — recognition, Bootstrap mapping, Radix SDC implementation, Radix component reference, Tailwind CSS integration, design token extraction
---

# Design Systems

Guides for the design-to-code pipeline: analyze a design system, map it to Bootstrap or Tailwind, implement in Radix/SDC.

| I need to... | Guide |
|-------------|-------|
| Identify design tokens, components, patterns from any source | [Recognition](recognition/index.md) |
| Map design system patterns to Bootstrap 5.3 | [Bootstrap Mapping](bootstrap/index.md) |
| Implement in Drupal with Radix theme and SDC components | [Radix SDC Mapping](radix-sdc/index.md) |
| Look up Radix 6.x SDC component props, slots, and usage | [Radix Components](radix-components/index.md) |
| Use DaisyUI v5 components, theming, and React integration | [DaisyUI](daisyui/index.md) |
| Implement a design system with Tailwind CSS v4/v3 | [Tailwind CSS](tailwind/index.md) |
| Extract and map design tokens across Tailwind, DaisyUI, Figma, and W3C DTCG | [Tailwind Tokens](tailwind-tokens/index.md) |
| Convert React/JSX components to Drupal Twig templates and SDC | [JSX to Twig](jsx-to-twig/index.md) |

## Workflow

```
1. Recognition → Analyze design (Figma, HTML, screenshots)
2. Bootstrap → Map tokens to variables, components to Bootstrap
   OR Tailwind → Configure @theme, map tokens, use CVA for variants
3. Radix SDC → Build Drupal sub-theme with SDC components
4. Radix Components → Reference for all 57 Radix 6.x SDCs
```
