---
description: Recognize design patterns and components from UI screenshots without source access
---

# Screenshot Analysis

## When to Use

> Use when analyzing UI screenshots to extract design patterns. Use when recognizing components without access to source files, or documenting a competitor's design system from visual inspection.

## Decision

| Visual Pattern | Indicates | Component Type |
|----------------|-----------|----------------|
| **Consistent spacing** | Intentional grouping | Molecule/Organism |
| **Visual container** (border/shadow/background) | Component boundary | Molecule/Organism |
| **Repeated patterns** | Reusable component | Atom/Molecule |
| **Color consistency** | Semantic token usage | Token system |
| **Typographic hierarchy** | Type scale | Token system |

## Pattern

**Visual Boundary Recognition:**

```
1. Identify major sections
   - Header, main content, sidebar, footer

2. Mark visual boundaries
   - Boxes, cards, panels, groups

3. Note repeated patterns
   - Same component used multiple times

4. Observe spacing
   - Consistent gaps indicate spacing system
```

**Color Sampling Process:**

1. **Identify all unique colors** in screenshot
2. **Group similar shades** — from same color family
3. **Count shade variations** — 3-11 shades suggests structured palette
4. **Note semantic usage** — Primary actions (blue), errors (red), success (green)

**Spacing Measurement:**

| Measured Gap | Likely Base Unit | System Type |
|--------------|------------------|-------------|
| 8, 16, 24, 32, 40, 48 | 8px | 8px linear |
| 4, 8, 12, 16, 20, 24 | 4px | 4px linear |
| 8, 16, 32, 64 | 8px | 8px geometric |

**Component Recognition in Screenshots:**

**Atoms:**
- Buttons (rectangular with text, consistent styling)
- Inputs (text fields with borders)
- Icons (small, monochromatic graphics)
- Badges (small labels with background)
- Avatars (circular profile images)

**Molecules:**
- Search bars (input + icon/button)
- Form fields (label + input + error)
- Cards (container with image + text + button)
- Nav items (icon + text link)

**Organisms:**
- Headers (top section with logo + nav + actions)
- Footers (bottom section with links + info)
- Card grids (multiple cards in grid layout)
- Forms (multiple form fields grouped)
- Data tables (rows/columns with headers)

**Design System Fingerprints:**

| Visual Pattern | Likely System | Key Indicators |
|----------------|---------------|----------------|
| **Material Design** | Google | FAB, elevation shadows, Roboto font, ripple effects |
| **Bootstrap** | Twitter | 12-column grid alignment, 0.25rem corners, blue primary (#0d6efd) |
| **Tailwind** | Labs | Utility-first appearance, slate/zinc grays, 0.375rem corners |
| **Shopify Polaris** | Shopify | Green primary, tight spacing, Inter font, subtle borders |

## Common Mistakes

- **Wrong**: Guessing spacing values → **Right**: Always measure spacing/sizes when possible (use screenshot in design tool)
- **Wrong**: Missing subtle backgrounds/borders → **Right**: Subtle visual boundaries define component boundaries
- **Wrong**: Ignoring repeated patterns → **Right**: Same visual pattern = reusable component
- **Wrong**: Overlooking shadows/elevation → **Right**: Shadow depth indicates hierarchy level (Material Design elevation)

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Reference Design Systems](./reference-systems.md)
- Reference: [Computer Vision for UI Testing](https://www.techrxiv.org/users/898550/articles/1282199)
- Reference: [AI-Assisted Visual Testing](https://www.deepakkamboj.com/blog/ai-assisted-visual-testing/)
