---
description: Tailwind CSS 4 design tokens — decision guides for extraction, mapping, and multi-platform integration
guide-meta:
  concepts:
    - design token extraction
    - Tailwind v4 @theme
    - DaisyUI color tokens
    - brand color mapping
    - W3C Design Tokens
    - Figma to Tailwind
    - token naming conventions
    - Drupal SDC token integration
  not:
    - Tailwind utility class usage
    - Tailwind configuration setup
    - design system recognition
  requires:
    - design-systems/tailwind
  complements:
    - design-systems/recognition
    - design-systems/daisyui
    - drupal/ui-suite-daisyui
    - drupal/sdc
  specializes: ""
  category: design-systems
---

# Tailwind Tokens

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide which extraction method fits my source and target | [Overview & When to Use](overview-when-to-use.md) | Use this guide when you have a Tailwind-based design system and need to extract tokens for a Drupal theme (CSS variables for DaisyUI / UI Suite DaisyUI), a Figma design system (token import/export), documentation (design token catalog), or… |
| Extract tokens from a Tailwind v4 @theme block | [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md) | Use @theme {} when starting a new Tailwind v4 project or migrating from v3. Tailwind v4 is CSS-first -- the @theme block IS your design token definition. |
| Know all Tailwind v4 @theme namespace categories | [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md) | Use this when you need to know which @theme variable prefix maps to which utility classes. Every namespace corresponds to one or more utility class APIs. |
| Define custom tokens and extend the theme | [Custom Token Definition](custom-token-definition.md) | Use this when you need tokens beyond Tailwind's defaults -- brand colors, custom spacing, project-specific breakpoints, or semantic aliases. |
| Access tokens from CSS, Twig, or JavaScript | [Token Consumption Patterns](token-consumption-patterns.md) | Use this when you need to access design tokens from CSS, Twig templates, JavaScript, or Drupal preprocess functions. |
| Understand DaisyUI v5 semantic color tokens | [DaisyUI v5 Color Token System](daisyui-v5-color-token-system.md) | Use this when building with DaisyUI v5 (used by UI Suite DaisyUI in Drupal). DaisyUI adds a semantic color layer on top of Tailwind's raw color palette, mapping brand intentions to CSS variables. |
| See ALL DaisyUI CSS variables documented | [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md) | Use this when you need to know every CSS variable that DaisyUI v5 provides. This is the complete reference for theming. |
| Map brand colors to DaisyUI theme | [Brand Color Mapping Workflow](brand-color-mapping-workflow.md) | Use when mapping brand guidelines (hex/Pantone) to DaisyUI semantic color roles. Identify primary/secondary/accent from the palette, convert to oklch, then validate every *-content token at 4.5:1 (body text) or 3:1 (large text/UI) — adjust the content token L-channel only, never the brand background. |
| Create a custom DaisyUI theme | [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md) | Use this when you need to create a branded DaisyUI theme for your project. |
| Map typography tokens for DaisyUI/Tailwind | [Typography Token Mapping](typography-token-mapping.md) | Use this when mapping typography decisions (font families, sizes, weights) into the Tailwind v4 / DaisyUI token system. |
| Build semantic spacing/layout tokens | [Spacing & Layout Token System](spacing-layout-token-system.md) | Use this when building semantic spacing and layout tokens for consistent vertical rhythm, grid gaps, and container widths. |
| Extract tokens from a Tailwind v3 config | [Tailwind v3 Token Extraction](tailwind-v3-token-extraction.md) | Use this when working with a Tailwind v3 project and need to extract tokens as CSS variables or a token catalog. |
| Choose the right naming convention | [Token Naming Conventions](token-naming-conventions.md) | Use this when establishing naming conventions for tokens across platforms or when choosing between multiple standards. |
| Map Figma variables to Tailwind tokens | [Figma to Tailwind Mapping](figma-to-tailwind-mapping.md) | Use this when your design team maintains tokens in Figma variables and you need to consume them in a Tailwind project. |
| Export tokens to W3C Design Tokens format | [W3C Design Tokens Format](w3c-design-tokens-format.md) | Use this when you need a vendor-neutral interchange format for sharing tokens across tools (Figma, Style Dictionary, Tailwind, native apps). The DTCG specification reached its first stable version (2025.10) in October 2025. |
| Map tokens to Drupal SDC component props | [Drupal SDC Token Integration](drupal-sdc-token-integration.md) | Use this when mapping design tokens to Drupal Single Directory Component (SDC) props so component consumers can select token-based values. |
| Use tokens in UI Suite DaisyUI starterkit | [UI Suite DaisyUI Starterkit Patterns](ui-suite-daisyui-starterkit-patterns.md) | Use this when building a Drupal theme with UI Suite DaisyUI and need to understand how the starterkit organizes tokens and configuration. |
| Avoid common token extraction mistakes | [Common Mistakes](common-mistakes.md) | Use this to avoid common pitfalls in token extraction, naming, and workflow. |
| Follow token management best practices | [Best Practices](best-practices.md) | Use this as a reference for token architecture, color management, multi-platform strategy, and Drupal/DaisyUI specifics. |
