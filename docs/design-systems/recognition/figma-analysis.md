---
description: Extract design tokens and components from Figma design files
---

# Figma Analysis

## When to Use

> Use when analyzing Figma design files to extract design systems. Use when mapping Figma components to atomic hierarchy or documenting from Figma source.

## Decision

| Figma Feature | Token/Component Type | Recognition |
|--------------|---------------------|-------------|
| **Variables** (color, number, string, boolean) | Design tokens | Local variables panel (Design tab) |
| **Styles** (color, text, effect, grid) | Legacy tokens | Pre-variable era token system |
| **Component** (single level, e.g., `Button`) | Atom | Single element, no nested components |
| **Component** (two levels, e.g., `Form/Field`) | Molecule | Compound element |
| **Component** (three+ levels, e.g., `Nav/Header/Desktop`) | Organism | Complex section |
| **Component Set** (purple diamond icon) | Variant system | Same component, different states |
| **Auto-Layout** (blue outline) | Spacing tokens | Gap/padding values |
| **Layout Grid** | Layout system | Column count, gutter, margin |

## Pattern

**Figma Variables as Design Tokens (since June 2023):**

```
Variable Types:
- Color: Fill, stroke, effect colors
- Number: Spacing, sizing, opacity
- String: Text content, font names
- Boolean: Show/hide states

Naming: color/primary, spacing/md, border-radius/lg
Collections: Light, Dark, Brand A, Brand B
```

**Component Hierarchy Mapping:**

```
Components (Assets Panel)
├── Atoms (single level)
│   ├── Button
│   ├── Input
│   └── Icon
├── Molecules (two levels)
│   ├── Form/Field
│   ├── Search/Bar
│   └── Nav/Item
└── Organisms (three+ levels)
    ├── Navigation/Header/Desktop
    ├── Navigation/Footer/Desktop
    └── Content/Hero/Section
```

**Component Sets & Variants:**

```
Button Component Set
- Properties:
  - Size: sm, md, lg
  - State: default, hover, active
  - Type: primary, secondary
- Variants: All combinations
  - sm/primary/default
  - md/secondary/hover
  - lg/primary/active
```

Recognition: Purple diamond with 4 smaller diamonds, Properties panel shows variant dimensions

**Auto-Layout Spacing Extraction:**

Blue outline when selected indicates auto-layout:
- **Spacing between items**: Gap token value (8px, 16px, 24px)
- **Padding**: Inset spacing token (8px, 16px)
- **Direction**: Horizontal or vertical stacking
- **Resizing**: Hug contents or Fill container

**Layout Grid Analysis:**

Grid types and breakpoint system:
- **Desktop**: 12 columns, 24px gutter, 80px margin
- **Tablet**: 8 columns, 16px gutter, 40px margin
- **Mobile**: 4 columns, 16px gutter, 20px margin

**Component Nesting Hierarchy:**

```
1. Select component
2. Expand layers panel
3. Look for purple diamond icons (instances)
4. Count nested components:
   - No instances → Atom
   - 2-3 atom instances → Molecule
   - Molecule instances or many atoms → Organism
   - Full-frame with organisms → Template
```

## Common Mistakes

- **Wrong**: Variants as separate components → **Right**: Variants are states of same component (Button/Primary and Button/Secondary are variants, not separate atoms)
- **Wrong**: Missing variable collections → **Right**: Modern Figma uses variables (not just styles) for tokens
- **Wrong**: Ignoring auto-layout spacing → **Right**: Auto-layout gap/padding values ARE spacing tokens
- **Wrong**: Frames classified as components → **Right**: Frames are containers; components are reusable elements with purple diamond icon

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [HTML/CSS Analysis](./html-css-analysis.md)
- Reference: [Figma Components and Variants 2025](https://medium.com/@ashish.garg25/2025-figma-walkthrough-components-and-variants-5f1c1de507b5)
- Reference: [Token-Based Component Library in Figma](https://designilo.com/2025/07/10/how-to-build-a-token-based-component-library-in-figma/)
