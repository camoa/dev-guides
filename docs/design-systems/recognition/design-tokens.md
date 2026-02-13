---
description: Extract color, typography, spacing, and surface tokens from any design system source
---

# Foundation Layer: Design Tokens

## When to Use

> Use this guide when analyzing ANY design system source and need to identify foundational values. Use before analyzing components — tokens are the foundation layer.

## Decision

| If You See... | It's Probably... | Token Category |
|---------------|------------------|----------------|
| Numbered scales (50-950) | Tailwind-style palette | Reference tokens (primitives) |
| Semantic names (primary, surface, on-surface) | Material Design 3 style | Semantic tokens |
| `--color-*` CSS custom properties | Token implementation | Token variables |
| RGB/Hex values in JSON with `$type: "color"` | W3C DTCG format | Standard tokens |
| OKLCH/OKLAB values | Modern color space | Perceptually uniform tokens |
| Font sizes with ratio progression (1.25×, 1.333×) | Modular scale | Typography tokens |
| Values divisible by 8 (8, 16, 24, 32) | 8px base system | Spacing tokens |
| `box-shadow`, `--shadow-*` | Composite values | Surface tokens |

## Pattern

**3-Layer Token Hierarchy:**

```
Reference Tokens (Primitives)
  ↓
Semantic Tokens (Context)
  ↓
Component Tokens (Application)
```

**Color Token Example:**

```css
/* Reference tokens */
--color-blue-500: #0052CC;

/* Semantic tokens */
--color-primary: var(--color-blue-500);

/* Component tokens */
--button-background: var(--color-primary);
```

**Typography Scale Recognition:**

| Ratio Name | Multiplier | When to Use |
|------------|------------|-------------|
| Minor Third | 1.200 | Subtle hierarchy, dense content |
| Major Third | 1.250 | **Most common** — balanced hierarchy |
| Perfect Fourth | 1.333 | Strong hierarchy, spacious layouts |

**Spacing Scale Recognition:**

| Base Unit | Example Values | System Type |
|-----------|----------------|-------------|
| 8px | 8, 16, 24, 32, 40, 48 | 8px linear |
| 4px | 4, 8, 12, 16, 20, 24 | 4px linear |

## Common Mistakes

- **Wrong**: Using raw tokens directly in components → **Right**: Use 3-layer hierarchy (reference → semantic → component) for rebranding flexibility
- **Wrong**: HSL-based palettes with uneven brightness → **Right**: OKLCH provides perceptual uniformity (yellow-500 and blue-500 have same visual weight)
- **Wrong**: Missing theme variants → **Right**: Light/dark swap token values, not component styles
- **Wrong**: Confusing font-size with line-height → **Right**: Separate token categories (dimension vs ratio)
- **Wrong**: Ad-hoc spacing values (13px, 19px) → **Right**: Consistent scale from base unit (8px, 16px, 24px)

## See Also

- [Component Classification](./component-classification.md)
- [HTML/CSS Analysis](./html-css-analysis.md)
- Reference: [W3C Design Tokens Format](https://www.designtokens.org/tr/drafts/format/)
- Reference: [OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)
- Reference: [Design Tokens & Theming 2025](https://materialui.co/blog/design-tokens-and-theming-scalable-ui-2025)
