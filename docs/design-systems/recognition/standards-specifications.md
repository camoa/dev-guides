---
description: Design system recognition — 10. standards & specifications
---

## 10. Standards & Specifications

### When to Use This Section
- You need to validate your token structure against W3C standards
- You're implementing a design token system
- You need to ensure cross-tool compatibility

### 10.1 W3C DTCG Token Format

**Official Specification:** [https://www.designtokens.org/tr/drafts/format/](https://www.designtokens.org/tr/drafts/format/)

**Core Requirements:**

**1. Token Structure**
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
- `$value` property (identifies token)
- Token name as parent object key

**Optional:**
- `$type` (can inherit from group)
- `$description` (plain text explanation)
- `$deprecated` (boolean or string)
- `$extensions` (vendor-specific metadata)

**2. Supported Types**
- **color:** Hex, RGB, color space values
- **dimension:** Numeric + unit (px, rem)
- **fontFamily:** String or array
- **fontWeight:** 100-1000 or keywords
- **duration:** Milliseconds or seconds
- **cubicBezier:** Four-number array
- **number:** Any numeric value

**3. Composite Tokens**
- **shadow:** color, offsetX, offsetY, blur, spread
- **border:** width, style, color
- **typography:** fontFamily, fontSize, fontWeight, lineHeight
- **gradient:** stops array
- **transition:** duration, delay, timingFunction

**4. Groups & Hierarchy**
- Objects without `$value` = groups
- Groups can inherit `$type` to children
- Dot notation for paths: `color.brand.primary`
- Reserved name: `$root` for group-level tokens

**5. File Format**
- **Format:** JSON
- **MIME type:** `application/design-tokens+json` or `application/json`
- **Extensions:** `.tokens` or `.tokens.json`

**6. References**
- Curly brace syntax: `{group.token}`
- JSON Pointer: `#/path/to/target`
- Tools MUST support JSON Pointer

**Reference:** [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/drafts/format/)

### 10.2 Accessibility Standards

**WCAG 2.2 Color Contrast Requirements:**

**Level AA (Standard):**
- Normal text: **4.5:1** minimum contrast ratio
- Large text (18pt+ or 14pt+ bold): **3:1** minimum
- UI components: **3:1** against adjacent colors

**Level AAA (Enhanced):**
- Normal text: **7:1** minimum
- Large text: **4.5:1** minimum

**Exceptions:**
- Incidental text (inactive controls, decorative)
- Logotypes and brand names

**Reference:** [Understanding WCAG 2.1 Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

**WCAG 2.2 Update:**
- Color contrast now moved from Level AA to **Level A** (strengthened)
- More stringent requirement for foundational accessibility

**Tools for Validation:**
- WebAIM Contrast Checker: [https://webaim.org/resources/contrastchecker/](https://webaim.org/resources/contrastchecker/)
- Browser DevTools built-in contrast checkers

### 10.3 Atomic Design Methodology

**Original Source:** Brad Frost, "Atomic Design" (2013)
**URL:** [https://atomicdesign.bradfrost.com/](https://atomicdesign.bradfrost.com/)

**Five-Stage Hierarchy:**
1. **Atoms** — Foundational building blocks (HTML elements)
2. **Molecules** — Simple groups of UI elements (2-3 atoms)
3. **Organisms** — Complex UI components (multiple molecules/atoms)
4. **Templates** — Page-level layouts (content structure)
5. **Pages** — Template instances with real content

**2025 Evolution:**
- Design tokens as foundation layer (not in original)
- Semantic naming preferred over strict categorization
- Behavioral patterns emphasized (Atlassian ADG approach)
- Flexible interpretation encouraged

**References:**
- [Atomic Design in 2025: From Rigid Theory to Flexible Practice](https://medium.com/design-bootcamp/atomic-design-in-2025-from-rigid-theory-to-flexible-practice-91f7113b9274)
- [Atomic Design Systems: Why the Labels Don't Matter](https://www.qt.io/blog/atomic-design-systems-why-the-labels-dont-matter)
