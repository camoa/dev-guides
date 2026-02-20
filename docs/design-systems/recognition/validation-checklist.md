---
description: Design system recognition — 11. validation checklist
---

## 11. Validation Checklist

### When to Use This Section
- You've completed your design system analysis and need to validate
- You're ensuring nothing was missed in the recognition process
- You're preparing documentation of your analysis

### 11.1 Foundation Layer Validation

**Design Tokens Checklist:**

- [ ] **Color tokens extracted**
  - [ ] Reference/primitive colors identified
  - [ ] Semantic color mappings documented
  - [ ] Theme variations (light/dark) noted
  - [ ] Color space identified (hex, OKLCH, RGB)
  - [ ] Contrast ratios meet WCAG 2.2 requirements

- [ ] **Typography tokens extracted**
  - [ ] Type scale identified (ratio or custom)
  - [ ] Font families documented
  - [ ] Font weights mapped
  - [ ] Line height tokens noted
  - [ ] Responsive/fluid typography checked

- [ ] **Spacing tokens extracted**
  - [ ] Base unit identified (4px, 8px, etc.)
  - [ ] Scale progression determined (linear, geometric)
  - [ ] Naming convention documented
  - [ ] Contextual spacing variants noted

- [ ] **Surface tokens extracted**
  - [ ] Border radius values documented
  - [ ] Shadow system identified
  - [ ] Elevation levels mapped
  - [ ] Border styles/widths noted
  - [ ] Opacity values extracted

### 11.2 Component Hierarchy Validation

**Atomic Design Classification Checklist:**

- [ ] **Atoms identified**
  - [ ] Form elements cataloged
  - [ ] Buttons listed
  - [ ] Typography atoms documented
  - [ ] Media atoms noted
  - [ ] Indicator atoms cataloged

- [ ] **Molecules identified**
  - [ ] Form field molecules documented
  - [ ] Navigation item molecules noted
  - [ ] Card content molecules identified
  - [ ] All molecules contain 2-3 atoms
  - [ ] Single responsibility verified for each

- [ ] **Organisms identified**
  - [ ] Header/footer documented
  - [ ] Navigation organisms mapped
  - [ ] Form organisms identified
  - [ ] Card grids noted
  - [ ] Each contains multiple molecules/atoms
  - [ ] Distinct interface sections confirmed

- [ ] **Templates identified**
  - [ ] Layout structures documented
  - [ ] Content areas defined
  - [ ] Grid systems noted
  - [ ] Responsive breakpoints identified
  - [ ] Confirmed placeholder content (not real)

- [ ] **Pages identified**
  - [ ] Real content instances documented
  - [ ] Edge cases noted (long headlines, empty states)
  - [ ] Variations cataloged (logged in/out, mobile/desktop)
  - [ ] Confirmed real content (not placeholders)

### 11.3 Source Analysis Validation

**HTML/CSS Source Checklist:**

- [ ] CSS custom properties extracted from `:root`
- [ ] Token layers identified (primitive → semantic → component)
- [ ] Component class names mapped to atomic hierarchy
- [ ] BEM or naming convention documented
- [ ] Theme variations extracted (dark mode, etc.)

**Figma Source Checklist:**

- [ ] Variables/styles extracted from design file
- [ ] Component hierarchy mapped via naming convention
- [ ] Component sets and variants documented
- [ ] Auto-layout spacing values extracted
- [ ] Layout grids documented (columns, gutters, margins)
- [ ] Component nesting analyzed (atom → molecule → organism)

**Screenshot Source Checklist:**

- [ ] Visual boundaries identified
- [ ] Color palette sampled and grouped
- [ ] Typography hierarchy measured
- [ ] Spacing system measured
- [ ] Components classified by visual pattern
- [ ] Design system fingerprint identified (Material, Bootstrap, etc.)

### 11.4 Standards Compliance Validation

**W3C DTCG Compliance:**

- [ ] Token structure uses `$value` property
- [ ] Token types specified with `$type`
- [ ] Composite tokens use correct structure
- [ ] Group hierarchy documented
- [ ] File format follows specification (.tokens.json)

**WCAG 2.2 Compliance:**

- [ ] Color contrast ratios validated
- [ ] Level AA minimum met (4.5:1 normal, 3:1 large)
- [ ] Level AAA documented if met
- [ ] UI component contrast checked (3:1)

**Atomic Design Compliance:**

- [ ] All five stages represented (atoms → pages)
- [ ] Classification rationale documented
- [ ] Single responsibility principle followed for molecules
- [ ] Templates distinguished from pages (placeholder vs real content)

### 11.5 Documentation Completeness

**Final Documentation Checklist:**

- [ ] All design tokens cataloged with values
- [ ] All components classified (atom/molecule/organism/template/page)
- [ ] Source files referenced (URLs, file paths)
- [ ] Design system patterns identified
- [ ] Edge cases and variations documented
- [ ] Naming conventions explained
- [ ] Token hierarchy visualized
- [ ] Component relationships mapped
- [ ] Accessibility audit completed
- [ ] Standards compliance validated
