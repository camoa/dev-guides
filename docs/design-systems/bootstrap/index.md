---
description: Design system to Bootstrap 5.3 mapping guides using the 6px threshold decision framework
guide-meta:
  concepts:
    - Bootstrap 5.3 mapping
    - 6px threshold
    - SCSS variables
    - design tokens to Bootstrap
    - atoms to Bootstrap components
    - molecules to Bootstrap
    - organisms to Bootstrap
    - Bootstrap grid
    - SCSS import order
    - Bootstrap utility API
  not:
    - Radix sub-theme implementation
    - Tailwind CSS
    - DaisyUI
  requires: []
  complements:
    - design-systems/recognition
    - design-systems/radix-sdc
    - design-systems/radix-components
  specializes: ""
  category: design-systems
---

# Bootstrap Design System Mapping

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the 6px threshold decision framework | [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) | Use this framework when deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE. Use the 6px threshold to systematically evaluate visual differences. |
| Apply systematic Bootstrap mapping decisions | [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) | Use this framework when deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE. Use the 6px threshold to systematically evaluate visual differences. |
| Learn SCSS best practices for Bootstrap | [SCSS Best Practices](scss-best-practices.md) | Use this when writing SCSS for Bootstrap customization. Apply these patterns to prevent technical debt and maintain upgrade compatibility. |
| Use advanced SCSS features (Dart Sass, maps, accessibility) | [Advanced SCSS Best Practices](advanced-scss-best-practices.md) | Use this for complex Bootstrap customizations requiring Dart Sass features, deep map merging, performance optimization, or accessibility patterns. |
| Validate Bootstrap mapping decisions | [Quality Assurance Framework](quality-assurance-framework.md) | Use this to validate Bootstrap accommodation decisions, review code for SCSS compliance, and ensure quality standards before deployment. |
| Implement progressive enhancement for modern CSS | [Progressive Enhancement Guidelines](progressive-enhancement-guidelines.md) | Use this when implementing CREATE category features (advanced features outside Bootstrap scope) to ensure graceful degradation and browser compatibility. |
| Organize a Bootstrap mapping project | [Project Organization Principles](project-organization-principles.md) | Use this when starting a design system → Bootstrap mapping project to organize analysis, documentation, and implementation files systematically. |
| Use standardized documentation templates | [Documentation Templates](documentation-templates.md) | Use these templates for consistent documentation across Bootstrap mapping projects, ensuring framework compliance and systematic analysis. |
| Resume work in a new session | [Project Continuation Guidelines](project-continuation-guidelines.md) | Use this when resuming a Bootstrap mapping project in a new session to ensure framework consistency and proper context loading. |
| Map color tokens to Bootstrap variables | [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) | Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system. |
| Map typography tokens to Bootstrap | [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) | Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system. |
| Map spacing tokens to Bootstrap | [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) | Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system. |
| Map border/radius/shadow tokens to Bootstrap | [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) | Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system. |
| Configure responsive breakpoints | [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md) | Use this after identifying design tokens to map colors, typography, spacing, borders, shadows, and breakpoints to Bootstrap's SCSS variable system. |
| Understand how Bootstrap generates utility classes | [Token to Utility Flow](token-to-utility-flow.md) | Use this to understand how Bootstrap auto-generates utility classes from tokens and how to extend the utility system with custom maps. |
| Extend Bootstrap's utility system | [Token to Utility Flow](token-to-utility-flow.md) | Use this to understand how Bootstrap auto-generates utility classes from tokens and how to extend the utility system with custom maps. |
| Map button atoms to Bootstrap | [Atoms → Bootstrap Components](atoms-bootstrap-components.md) | Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins. |
| Map form input atoms to Bootstrap | [Atoms → Bootstrap Components](atoms-bootstrap-components.md) | Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins. |
| Map badge/label atoms to Bootstrap | [Atoms → Bootstrap Components](atoms-bootstrap-components.md) | Use this to map atomic design system components (buttons, inputs, badges) to Bootstrap's component variables and mixins. |
| Map input group molecules to Bootstrap | [Molecules → Component Combinations](molecules-component-combinations.md) | Use this for mapping molecules (2-3 atoms working together) like input groups and card content to Bootstrap's component combinations. |
| Map card content molecules to Bootstrap | [Molecules → Component Combinations](molecules-component-combinations.md) | Use this for mapping molecules (2-3 atoms working together) like input groups and card content to Bootstrap's component combinations. |
| Map navbar organisms to Bootstrap | [Organisms → Layout + Components](organisms-layout-components.md) | Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system. |
| Map complete card organisms to Bootstrap | [Organisms → Layout + Components](organisms-layout-components.md) | Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system. |
| Map form organisms to Bootstrap | [Organisms → Layout + Components](organisms-layout-components.md) | Use this for mapping organisms (complex UI sections combining multiple molecules and atoms) like navbars and complete cards to Bootstrap's component system. |
| Map page templates to Bootstrap grid | [Templates → Bootstrap Grid](templates-bootstrap-grid.md) | Use this for mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures. |
| Configure responsive grid layouts | [Templates → Bootstrap Grid](templates-bootstrap-grid.md) | Use this for mapping templates (page layouts, content structures) to Bootstrap's grid system for responsive page structures. |
| Understand correct SCSS import order | [SCSS Integration Order](scss-integration-order.md) | Use this when setting up SCSS file structure or troubleshooting variable override issues. Import order is critical for Bootstrap customization. |
| Troubleshoot variable override issues | [SCSS Integration Order](scss-integration-order.md) | Use this when setting up SCSS file structure or troubleshooting variable override issues. Import order is critical for Bootstrap customization. |
| Understand Bootstrap's !default flag | [Key Bootstrap SCSS Mechanisms](key-bootstrap-scss-mechanisms.md) | Use this to understand Bootstrap's internal architecture, troubleshoot customization issues, and leverage built-in systems effectively. |
| Understand Bootstrap's map merging system | [Key Bootstrap SCSS Mechanisms](key-bootstrap-scss-mechanisms.md) | Use this to understand Bootstrap's internal architecture, troubleshoot customization issues, and leverage built-in systems effectively. |
| Use Bootstrap mixins correctly | [Key Bootstrap SCSS Mechanisms](key-bootstrap-scss-mechanisms.md) | Use this to understand Bootstrap's internal architecture, troubleshoot customization issues, and leverage built-in systems effectively. |
| Understand Bootstrap's utility API system | [Key Bootstrap SCSS Mechanisms](key-bootstrap-scss-mechanisms.md) | Use this to understand Bootstrap's internal architecture, troubleshoot customization issues, and leverage built-in systems effectively. |
