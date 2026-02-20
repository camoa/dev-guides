---
description: Design system recognition — 9. reference design systems
---

## 9. Reference Design Systems

### When to Use This Section
- You're comparing your analysis to established design systems
- You need examples of token structures and component hierarchies
- You're learning patterns from industry-leading systems

### 9.1 Modern Design System Examples

**Reference Sources:**
- Tailwind CSS: [https://tailwindcss.com/docs/colors](https://tailwindcss.com/docs/colors)
- Material Design 3: [Mastering Material 3 in Jetpack Compose](https://medium.com/@hiren6997/mastering-material-3-in-jetpack-compose-the-2025-guide-1c1bd5acc480)
- Shopify Polaris: [https://polaris-react.shopify.com/](https://polaris-react.shopify.com/)
- GitHub Primer: [https://primer.style/](https://primer.style/)
- IBM Carbon: [https://carbondesignsystem.com/](https://carbondesignsystem.com/)
- Atlassian Design: [https://atlassian.design/](https://atlassian.design/)
- Open Props: [https://open-props.style/](https://open-props.style/)
- Radix UI: [https://www.radix-ui.com/](https://www.radix-ui.com/)
- shadcn/ui: [https://ui.shadcn.com/](https://ui.shadcn.com/)

### 9.2 Design System Patterns

**Color System Patterns:**

| System | Approach | Scale | Notable Features |
|--------|----------|-------|------------------|
| **Tailwind CSS** | Numbered scales | 50-950 (11 steps) | OKLCH color space, 22 color families |
| **Material Design 3** | Semantic tokens | Dynamic color roles | On-surface, on-primary semantic pairs |
| **Open Props** | CSS custom properties | 0-12 (13 steps) | Sub-atomic styles, OKLCH colors |
| **IBM Carbon** | Layer-based | Theme tokens | Elevation-based theming |

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
| **IBM Carbon** | Productive vs Expressive | IBM Plex | Two type sets for different contexts |
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

### 9.3 Token Standard References

**W3C Design Tokens Community Group (DTCG):**
- **Specification:** Design Tokens Format Module 2025.10
- **Status:** First stable version (October 2025)
- **Format:** JSON with `$value`, `$type`, `$description` properties
- **URL:** [https://www.designtokens.org/tr/drafts/format/](https://www.designtokens.org/tr/drafts/format/)

**Token Types Supported:**
- Color, Dimension, Font family, Font weight, Duration
- Cubic Bézier, Number
- Composite: Shadow, Border, Typography, Gradient, Transition

**Tool Support:**
- Figma, Penpot, Sketch, Framer
- Knapsack, Supernova, zeroheight
- Style Dictionary, Tokens Studio, Terrazzo

**Reference:** [Design Tokens Specification Reaches First Stable Version](https://designzig.com/design-tokens-specification-reaches-first-stable-version-with-w3c-community-group/)
