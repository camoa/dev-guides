---
description: Design System Recognition — extract tokens and components from HTML/CSS, Figma, or screenshots
guide-meta:
  concepts:
    - design token extraction
    - atomic design classification
    - atom recognition
    - molecule recognition
    - organism recognition
    - design system analysis
    - W3C DTCG
  not:
    - Bootstrap mapping implementation
    - Drupal SDC creation
    - Tailwind configuration
  requires: []
  complements:
    - design-systems/bootstrap
    - design-systems/tailwind-tokens
    - ai-tooling/figma-mcp
  specializes: ""
  category: design-systems
---

# Design System Recognition

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Extract color, typography, spacing, and surface tokens | [Foundation Layer: Design Tokens](foundation-layer-design-tokens.md) | You're looking at ANY design system source and need to identify the foundational values You need to extract design decisions from CSS custom properties, Figma styles, or JSON files You're mapping visual patterns to a structured token system |
| Classify components into atoms, molecules, organisms, templates, pages | [Component Classification Framework](component-classification-framework.md) | You need to categorize UI components into atoms, molecules, organisms, templates, or pages You're analyzing an existing design system and mapping its component hierarchy You're unsure if something is a molecule vs organism |
| Identify the smallest functional UI building blocks | [Atom Recognition](atom-recognition.md) | You're analyzing a UI and need to identify the smallest functional building blocks You're extracting foundational elements from HTML, Figma, or screenshots You need to catalog all atoms before identifying molecules |
| Recognize composite components that combine 2-3 atoms | [Molecule Recognition](molecule-recognition.md) | You've identified atoms and now need to find grouped patterns You're analyzing composite components that combine 2-3 atoms You need to determine if a component is a molecule vs organism |
| Identify complex interface sections | [Organism Recognition](organism-recognition.md) | You've identified atoms and molecules, now need to recognize complex sections You're analyzing interface sections that feel like "complete units" You need to distinguish organisms from templates |
| Distinguish layout structures from real implementations | [Templates vs Pages](templates-vs-pages.md) | You need to distinguish between layout structures (templates) and real implementations (pages) You're analyzing page-level patterns in a design system You're documenting layout systems vs actual page instances |
| Assess design system quality and maturity | [Design System Analysis Best Practices](design-system-analysis-best-practices.md) | You're beginning analysis of a design system from any source You need to assess the quality and maturity of a design system You're determining whether a collection of components constitutes a "system" |
| Extract design tokens and components from any source | [Source-Specific Recognition](source-specific-recognition.md) | You're analyzing an HTML design system or component library You need to extract design tokens from CSS custom properties You're reverse-engineering an existing website's design system |
| Compare to industry-leading design systems | [Reference Design Systems](reference-design-systems.md) | You're comparing your analysis to established design systems You need examples of token structures and component hierarchies You're learning patterns from industry-leading systems |
| Validate against W3C DTCG and atomic design standards | [Standards & Specifications](standards-specifications.md) | You need to validate your token structure against W3C standards You're implementing a design token system You need to ensure cross-tool compatibility |
| Validate analysis completeness | [Validation Checklist](validation-checklist.md) | You've completed your design system analysis and need to validate You're ensuring nothing was missed in the recognition process You're preparing documentation of your analysis |
| Understand the recognition framework | [Conclusion](conclusion.md) |  |
