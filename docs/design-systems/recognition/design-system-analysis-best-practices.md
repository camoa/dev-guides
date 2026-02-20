---
description: Design system recognition — 7. design system analysis best practices
---

## 7. Design System Analysis Best Practices

### When to Use This Section
- You're beginning analysis of a design system from any source
- You need to assess the quality and maturity of a design system
- You're determining whether a collection of components constitutes a "system"

### 7.1 Analysis Process Best Practices

**Start with Tokens, Not Components:**

**Why this matters:** Identifying the token system first reveals whether you're analyzing a true design system or just a component library. [Design Systems Guide 2025](https://thedesignsystem.guide/design-tokens) emphasizes tokens as the foundation that makes a design system scalable across platforms.

**What to look for:**
1. **Color tokens:** Do you see repeated color values, or is every component using unique hex codes?
2. **Spacing tokens:** Are gaps consistent (8px, 16px, 24px), or random (13px, 19px, 27px)?
3. **Typography tokens:** Does type scale follow a ratio, or are font sizes arbitrary?

**Red flags (NOT a mature system):**
- Every component has hardcoded colors (no token abstraction)
- Spacing values are inconsistent (design debt accumulation)
- Typography uses pixel values without scale relationship
- No semantic layer (only raw values, no contextual meaning)

**Good signs (mature system):**
- 3-layer token hierarchy (reference → semantic → component)
- Consistent naming conventions across token categories
- Theme variants (light/dark) swap token values, not components
- Documentation explains token usage patterns

### 7.2 Look for Inconsistencies (Design Debt Indicators)

**Why inconsistencies matter:** They reveal lack of systematic thinking. [Design System Governance](https://www.uxpin.com/studio/blog/design-system-governance/) identifies "design drift" as a primary anti-pattern where components diverge from production due to poor governance.

**Common inconsistency patterns:**

**5 Different Grays = No System:**
If you find `#333333`, `#3a3a3a`, `#444444`, `#4a4a4a`, `#555555` all in use, this indicates:
- No shared color palette
- Designers/developers making up values per component
- No review process catching drift
- System is decorative documentation, not source of truth

**What a good gray scale looks like:** Tailwind's gray-50 through gray-950 in consistent perceptual steps, with all components using token references.

**Button Size Chaos:**
If buttons have heights of 32px, 36px, 38px, 40px, 42px with no pattern:
- No sizing scale
- Components built in isolation
- Each designer/developer making local decisions
- Missing design system governance

**What good button sizing looks like:** Small (32px), Medium (40px), Large (48px) based on 8px grid, with all instances using these 3 sizes.

**Typography Anarchy:**
If you find 15+ different font sizes with no ratio relationship:
- No type scale
- Random size adjustments to "make it look right"
- Impossible to maintain visual hierarchy
- Mobile responsive sizing becomes arbitrary

**What a good type scale looks like:** 6-8 sizes following 1.25× or 1.333× ratio, with semantic names (xs, sm, base, lg, xl) and consistent usage.

### 7.3 Check Responsive Behavior

**Why responsive matters:** A design system that only works at one breakpoint isn't a system—it's a desktop mockup.

**What to analyze:**

**Breakpoint Strategy:**
- Does system define breakpoint tokens? (mobile: 0-767px, tablet: 768-1023px, desktop: 1024px+)
- Do components adapt systematically, or is each responsive behavior custom?
- Are spacing/typography values responsive (fluid typography with clamp())?

**Red flags:**
- Components break at common viewport sizes (768px, 1024px)
- Mobile layout is completely different structure (not adaptation)
- Responsive behavior requires custom CSS per component
- No documented responsive patterns or guidelines

**Good signs:**
- Container queries or breakpoint tokens define adaptation rules
- Components use same token values, but spacing scales at breakpoints
- Mobile-first approach (base styles for mobile, enhancements for larger screens)
- Responsive patterns documented with examples at each breakpoint

### 7.4 Dark Mode as Litmus Test

**Why dark mode reveals token architecture quality:** If the system can't support dark mode by swapping token values, the token architecture is wrong.

**Good dark mode implementation:**
```
Light theme: --color-background: white; --color-text: black;
Dark theme:  --color-background: black; --color-text: white;
Components:  background: var(--color-background); color: var(--color-text);
```

**Components unchanged. Only token values swap.**

**Bad dark mode implementation:**
```
.button-light { background: white; color: black; }
.button-dark { background: black; color: white; }
```

**Every component has duplicate styles for each theme.**

**What goes wrong with bad implementation:**
- 2× maintenance burden (every component change requires updating both themes)
- Theme drift (dark theme falls behind as new components added)
- Can't support third theme (high contrast) without another full duplication
- New components often ship without dark mode support (forgotten in rush)

**Accessibility in dark mode:** Dark mode must maintain WCAG contrast ratios. Common mistake: taking light mode colors and inverting them produces insufficient contrast. [Accessible Design Systems](https://montanab.com/2025/03/accessible-design-systems-building-components-for-everyone/) emphasizes testing contrast ratios in all themes.

### 7.5 Governance and Maintenance Indicators

**Why governance matters:** Without governance, design systems decay into component junkyards. [Brad Frost on Governance](https://bradfrost.com/blog/post/a-design-system-governance-process/) provides the definitive governance framework.

**Signs of good governance:**
- Public changelog documents all updates
- Contribution process documented (how to propose new components)
- Deprecation policy (how old components sunset)
- Version control with semantic versioning
- Component ownership assigned (DRI - Directly Responsible Individual)
- Regular sync meetings documented

**Signs of poor governance:**
- No changelog (teams don't know what changed)
- No contribution process (leads to rogue component creation)
- No deprecation plan (dead components accumulate forever)
- No versioning (breaking changes ship without warning)
- No ownership (components become orphaned when creator leaves)

**Three governance models:** [Design System Governance Models](https://uxplanet.org/design-system-governance-models-f66a97367ad5) identifies:

1. **Centralized:** Single team owns system. **Pros:** Consistency. **Cons:** Bottleneck.
2. **Federated:** Distributed ownership with central coordination. **Pros:** Scales. **Cons:** Requires strong process.
3. **Standalone:** Each team owns their components. **Pros:** Autonomy. **Cons:** Divergence.

**2025 Best Practice:** Federated model with lightweight governance. Central team maintains tokens + core components. Product teams contribute patterns that get promoted to system after validation.

#### See Also
- [1. Foundation Layer: Design Tokens](#1-foundation-layer-design-tokens)
- [2. Atomic Design Hierarchy](#2-atomic-design-hierarchy)
- [11. Validation Checklist](#11-validation-checklist)
