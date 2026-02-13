---
description: W3C token format, WCAG accessibility, and atomic design methodology standards
---

# Standards & Specifications

## When to Use

> Use when validating token structure against W3C standards. Use when implementing design token systems or ensuring cross-tool compatibility.

## Decision

| Standard | When to Apply | Compliance Check |
|----------|---------------|------------------|
| **W3C DTCG Token Format** | Implementing token system | JSON with `$value`, `$type` properties |
| **WCAG 2.2 Color Contrast** | All color tokens | 4.5:1 normal text, 3:1 large text (Level AA) |
| **Atomic Design Methodology** | Component classification | 5-stage hierarchy (atoms → pages) |

## Pattern

**W3C DTCG Token Format (2025.10 Stable Version):**

```json
{
  "token-name": {
    "$value": "value-here",
    "$type": "color",
    "$description": "Optional description"
  }
}
```

**Required:**
- `$value` property
- Token name as parent object key

**Optional:**
- `$type` (can inherit from group)
- `$description`
- `$deprecated`
- `$extensions` (vendor-specific)

**Supported Types:**
- **Primitives**: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number
- **Composites**: shadow (color, offsetX, offsetY, blur, spread), border (width, style, color), typography (fontFamily, fontSize, fontWeight, lineHeight), gradient, transition

**File Format:**
- Format: JSON
- MIME: `application/design-tokens+json` or `application/json`
- Extensions: `.tokens` or `.tokens.json`

**References:**
- Curly brace: `{group.token}`
- JSON Pointer: `#/path/to/target`

**WCAG 2.2 Color Contrast Requirements:**

| Level | Normal Text | Large Text (18pt+ or 14pt+ bold) | UI Components |
|-------|-------------|----------------------------------|---------------|
| **AA (Standard)** | 4.5:1 minimum | 3:1 minimum | 3:1 against adjacent |
| **AAA (Enhanced)** | 7:1 minimum | 4.5:1 minimum | N/A |

**Exceptions:**
- Incidental text (inactive controls, decorative)
- Logotypes and brand names

**WCAG 2.2 Update:**
- Color contrast moved from Level AA to **Level A** (strengthened requirement)

**Atomic Design Methodology (Brad Frost 2013, Evolved 2025):**

**Five-Stage Hierarchy:**

| Stage | Description | 2025 Evolution |
|-------|-------------|----------------|
| **Atoms** | Foundational building blocks (HTML elements) | Design tokens as foundation layer (not in original) |
| **Molecules** | Simple groups (2-3 atoms) | Semantic naming preferred over strict categorization |
| **Organisms** | Complex components (multiple molecules/atoms) | Behavioral patterns emphasized |
| **Templates** | Page-level layouts (content structure) | Flexible interpretation encouraged |
| **Pages** | Template instances with real content | Purpose-driven classification |

## Common Mistakes

- **Wrong**: Custom token format incompatible with tools → **Right**: Use W3C DTCG standard for cross-tool compatibility (Figma, Style Dictionary, Tokens Studio)
- **Wrong**: Color pairs that fail WCAG contrast → **Right**: Validate all text/background combinations (4.5:1 minimum for normal text)
- **Wrong**: Rigid atomic design enforcement → **Right**: Use as mental model, not rigid rulebook (labels aid communication, not dogma)
- **Wrong**: Missing composite token structure → **Right**: Shadows, borders, typography use composite format with multiple properties

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Validation Checklist](./validation-checklist.md)
- Reference: [W3C Design Tokens Format](https://www.designtokens.org/tr/drafts/format/)
- Reference: [WCAG 2.1 Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- Reference: [Atomic Design](https://atomicdesign.bradfrost.com/)
- Reference: [Atomic Design in 2025: Flexible Practice](https://medium.com/design-bootcamp/atomic-design-in-2025-from-rigid-theory-to-flexible-practice-91f7113b9274)
