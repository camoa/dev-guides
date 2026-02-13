---
description: Industry-leading design system examples and token structure patterns
---

# Reference Design Systems

## When to Use

> Use when comparing your analysis to established design systems. Use when learning patterns from industry-leading systems or needing examples of token structures.

## Decision

| Design System | Best For | Token Approach | Component Style |
|--------------|----------|----------------|-----------------|
| **Tailwind CSS** | Utility-first development | Numbered scales (50-950), OKLCH | No predefined components |
| **Material Design 3** | Google-style interfaces | Semantic tokens, dynamic color | Component-rich library |
| **Shopify Polaris** | E-commerce applications | 4px base, multiplier naming | Opinionated components |
| **IBM Carbon** | Enterprise applications | Layer-based theming | Productive vs Expressive |
| **Radix UI** | Headless/unstyled primitives | User-applied tokens | Logic separated from style |
| **shadcn/ui** | Copy-paste components | Tailwind-based | Styled Radix primitives |

## Pattern

**Color System Patterns:**

| System | Scale | Notable Features |
|--------|-------|------------------|
| **Tailwind CSS** | 50-950 (11 steps) | OKLCH color space, 22 color families |
| **Material Design 3** | Semantic roles | On-surface, on-primary semantic pairs, dynamic color |
| **Open Props** | 0-12 (13 steps) | Sub-atomic styles, OKLCH colors |
| **IBM Carbon** | Theme tokens | Elevation-based theming, layer system |

**Spacing System Patterns:**

| System | Base Unit | Scale Type | Naming |
|--------|-----------|------------|--------|
| **Material Design** | 8px | Linear (8dp increments) | Numeric |
| **Shopify Polaris** | 4px | `space-2` = 8px | Multiplier |
| **Atlassian** | 8px | Limited set (8, 16, 24, 32) | Pixel values |
| **Tailwind CSS** | 0.25rem (4px) | `4` = 16px, `8` = 32px | Numeric × 4px |
| **GitLab Pajamas** | 8px | Geometric + augmented | Numeric |

**Typography Patterns:**

| System | Type Scale | Font Family | Notable Features |
|--------|------------|-------------|------------------|
| **Material Design** | Headline, Title, Body, Label | Roboto | Scale names, not sizes |
| **Tailwind CSS** | xs, sm, base, lg, xl, 2xl-9xl | System fonts | Utility classes |
| **IBM Carbon** | Productive vs Expressive | IBM Plex | Two type sets for contexts |
| **Open Props** | 00-8 (9 sizes) | System fonts | Fluid typography support |

**Component Hierarchy Examples:**

**Tailwind CSS (Utility-First):**
- No predefined components
- Atoms = HTML elements + utility classes
- Molecules/organisms = user-defined patterns

**Material Design 3 (Component-Rich):**
- Atoms: Button, Icon, Text field
- Molecules: Search bar, List item, Card
- Organisms: App bar, Navigation drawer, Bottom sheet

**Radix UI (Headless/Primitives):**
- Unstyled primitives (atoms)
- Logic separated from presentation
- User applies styling layer

**shadcn/ui (Styled Primitives):**
- Built on Radix primitives
- Pre-styled with Tailwind
- Copy-paste component approach

**W3C Design Tokens Community Group (DTCG):**

- **Specification**: Design Tokens Format Module 2025.10
- **Status**: First stable version (October 2025)
- **Format**: JSON with `$value`, `$type`, `$description`
- **Token Types**: Color, Dimension, Font family, Font weight, Duration, Cubic Bézier, Number
- **Composite Types**: Shadow, Border, Typography, Gradient, Transition

## Common Mistakes

- **Wrong**: Copying systems without understanding context → **Right**: Learn patterns, adapt to your needs (Material Design for consumer apps, Carbon for enterprise)
- **Wrong**: Mixing incompatible patterns → **Right**: Tailwind utility-first doesn't mix well with Material component-rich approach
- **Wrong**: Ignoring W3C DTCG standard → **Right**: Use standardized token format for cross-tool compatibility

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Standards & Specifications](./standards-specifications.md)
- Reference: [Tailwind CSS](https://tailwindcss.com/docs/colors)
- Reference: [Material Design 3](https://m3.material.io/)
- Reference: [IBM Carbon](https://carbondesignsystem.com/)
- Reference: [Atlassian Design](https://atlassian.design/)
- Reference: [Radix UI](https://www.radix-ui.com/)
- Reference: [shadcn/ui](https://ui.shadcn.com/)
