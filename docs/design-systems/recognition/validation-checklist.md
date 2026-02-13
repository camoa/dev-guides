---
description: Comprehensive checklist to validate design system analysis completeness
---

# Validation Checklist

## When to Use

> Use after completing design system analysis. Use to ensure nothing was missed in recognition process, or when preparing documentation.

## Decision

| Validation Category | Complete When... | Missing Indicator |
|-------------------|------------------|-------------------|
| **Foundation Layer** | All token types extracted (color, typography, spacing, surface) | No token hierarchy documented |
| **Component Hierarchy** | All 5 stages identified (atoms → pages) | Components uncategorized |
| **Source Analysis** | Source-specific patterns documented (CSS/Figma/screenshots) | No source files referenced |
| **Standards Compliance** | W3C DTCG, WCAG 2.2, Atomic Design validated | No compliance notes |
| **Documentation** | All components cataloged, relationships mapped | Incomplete catalog |

## Pattern

**Foundation Layer Validation:**

```
☐ Color tokens extracted
  ☐ Reference/primitive colors
  ☐ Semantic color mappings
  ☐ Theme variations (light/dark)
  ☐ Color space identified (hex, OKLCH, RGB)
  ☐ Contrast ratios meet WCAG 2.2

☐ Typography tokens extracted
  ☐ Type scale identified (ratio or custom)
  ☐ Font families documented
  ☐ Font weights mapped
  ☐ Line height tokens noted
  ☐ Responsive/fluid typography checked

☐ Spacing tokens extracted
  ☐ Base unit identified (4px, 8px, etc.)
  ☐ Scale progression (linear, geometric)
  ☐ Naming convention documented
  ☐ Contextual spacing variants

☐ Surface tokens extracted
  ☐ Border radius values
  ☐ Shadow system identified
  ☐ Elevation levels mapped
  ☐ Border styles/widths
  ☐ Opacity values
```

**Component Hierarchy Validation:**

```
☐ Atoms identified
  ☐ Form elements cataloged
  ☐ Buttons listed
  ☐ Typography atoms
  ☐ Media atoms
  ☐ Indicator atoms

☐ Molecules identified
  ☐ Form field molecules
  ☐ Navigation item molecules
  ☐ Card content molecules
  ☐ All contain 2-3 atoms
  ☐ Single responsibility verified

☐ Organisms identified
  ☐ Header/footer documented
  ☐ Navigation organisms
  ☐ Form organisms
  ☐ Card grids
  ☐ Contains multiple molecules/atoms
  ☐ Distinct interface sections

☐ Templates identified
  ☐ Layout structures documented
  ☐ Content areas defined
  ☐ Grid systems noted
  ☐ Responsive breakpoints
  ☐ Placeholder content confirmed

☐ Pages identified
  ☐ Real content instances
  ☐ Edge cases noted (long headlines, empty states)
  ☐ Variations cataloged (logged in/out, mobile/desktop)
  ☐ Real content confirmed
```

**Source Analysis Validation:**

**HTML/CSS:**
```
☐ CSS custom properties extracted from :root
☐ Token layers identified (primitive → semantic → component)
☐ Component class names mapped to atomic hierarchy
☐ BEM or naming convention documented
☐ Theme variations extracted (dark mode, etc.)
```

**Figma:**
```
☐ Variables/styles extracted
☐ Component hierarchy mapped via naming
☐ Component sets and variants documented
☐ Auto-layout spacing values extracted
☐ Layout grids documented (columns, gutters, margins)
☐ Component nesting analyzed
```

**Screenshots:**
```
☐ Visual boundaries identified
☐ Color palette sampled and grouped
☐ Typography hierarchy measured
☐ Spacing system measured
☐ Components classified by visual pattern
☐ Design system fingerprint identified
```

**Standards Compliance Validation:**

```
☐ W3C DTCG Compliance
  ☐ Token structure uses $value property
  ☐ Token types specified with $type
  ☐ Composite tokens use correct structure
  ☐ Group hierarchy documented
  ☐ File format follows spec (.tokens.json)

☐ WCAG 2.2 Compliance
  ☐ Color contrast ratios validated
  ☐ Level AA minimum met (4.5:1 normal, 3:1 large)
  ☐ Level AAA documented if met
  ☐ UI component contrast checked (3:1)

☐ Atomic Design Compliance
  ☐ All 5 stages represented
  ☐ Classification rationale documented
  ☐ Single responsibility for molecules
  ☐ Templates distinguished from pages
```

**Documentation Completeness:**

```
☐ All design tokens cataloged with values
☐ All components classified (atom/molecule/organism/template/page)
☐ Source files referenced (URLs, file paths)
☐ Design system patterns identified
☐ Edge cases and variations documented
☐ Naming conventions explained
☐ Token hierarchy visualized
☐ Component relationships mapped
☐ Accessibility audit completed
☐ Standards compliance validated
```

## Common Mistakes

- **Wrong**: Skipping edge case documentation → **Right**: Document long headlines, empty states, missing images (pages reveal real-world issues)
- **Wrong**: No source file references → **Right**: Link to original CSS files, Figma URLs, screenshot paths
- **Wrong**: Missing theme variant documentation → **Right**: Document light/dark/high-contrast token swaps
- **Wrong**: Incomplete component catalog → **Right**: Every component categorized and relationships mapped

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Analysis Best Practices](./analysis-best-practices.md)
- [Standards & Specifications](./standards-specifications.md)
