---
description: "Systematic folder structure for design system to Bootstrap mapping projects"
tldr: "Use this when starting a design system → Bootstrap mapping project to organize analysis, documentation, and implementation files systematically."
drupal_version: "11.x"
---

# Project Organization Principles

## When to Use

> Use this when starting a design system → Bootstrap mapping project to organize analysis, documentation, and implementation files systematically.

- You're starting a design system → Bootstrap mapping project
- You need to organize analysis, mapping documentation, and implementation files
- You want a systematic folder structure for multi-phase projects
- You're establishing documentation standards for team projects

## Universal Project Structure

Based on proven methodology for systematic design system → Bootstrap conversion. This folder structure supports progressive documentation, incremental analysis, and clear handoff to implementation.

### Pattern: Complete Project Folder Structure

```
/home/agent/Documents/memory_files/
└── [project_name]/                              # e.g., company_bootstrap_personalization/
    ├── project-notes.md                         # Project overview and status
    ├── design-system-analysis/                  # Complete design system documentation
    │   ├── design-system-inventory.md           # Complete design system inventory
    │   ├── color-system-analysis.md             # Detailed color system analysis
    │   ├── typography-system-analysis.md        # Typography system analysis
    │   ├── spacing-system-analysis.md            # Spacing system analysis
    │   ├── border-radius-analysis.md             # Border and radius analysis
    │   ├── shadow-elevation-analysis.md          # Shadow and elevation analysis
    │   └── advanced-features-analysis.md         # CREATE category features (if applicable)
    ├── bootstrap-mapping/                       # Bootstrap mapping documentation
    │   ├── bootstrap-variable-inventory.md      # What Bootstrap provides
    │   ├── direct-mapping-plan.md               # Direct design→Bootstrap mappings
    │   ├── custom-variables-plan.md              # Justified custom variables
    │   ├── extension-plan.md                     # EXTEND category implementations
    │   └── implementation-strategy.md             # Implementation approach
    ├── component-impact-analysis/               # How personalization affects components
    │   ├── button-components-impact.md          # Button system impact analysis
    │   ├── form-components-impact.md             # Form system impact analysis
    │   ├── navigation-components-impact.md       # Navigation impact analysis
    │   └── layout-components-impact.md            # Layout impact analysis
    └── final-implementation/                    # Ready-for-implementation files
        ├── variable-overrides.scss              # Final Bootstrap variable overrides
        ├── bootstrap-extensions.scss             # EXTEND category additions
        ├── custom-variables.scss                 # CUSTOMIZE category variables
        ├── advanced-features/                    # CREATE category implementations (if needed)
        │   ├── _advanced-mixins.scss            # Custom mixins for advanced features
        │   └── _advanced-utilities.scss          # Custom utilities for advanced features
        ├── implementation-guide.md               # Step-by-step implementation
        └── validation-checklist.md               # Testing and validation steps
```

## Progressive Documentation Approach

**Systematic Methodology:**

1. **Process each design system aspect incrementally** - Colors, typography, spacing, etc. one at a time
2. **Update consolidated documentation progressively** - Build complete picture as analysis progresses
3. **Build complete mapping strategy before implementation** - No code until analysis complete
4. **Present final implementation plan for approval** - Stakeholder review before execution

## Phase-Based Implementation Process

### Phase 1: System Inventory (Document-First)

1. **Create project folder structure** - Set up all directories and placeholder files
2. **Process each design system aspect incrementally** - One category at a time
3. **Update consolidated analysis progressively** - Keep central inventory current
4. **Build complete inventory before mapping** - Don't start mapping until inventory complete

### Phase 2: Bootstrap Assessment

1. **Document Bootstrap capabilities systematically** - Variables, maps, mixins, utilities
2. **Identify direct mapping opportunities** - ACCOMMODATE decisions first
3. **Justify custom variable needs** - CUSTOMIZE/CREATE decisions with rationale
4. **Plan implementation strategy** - Determine integration approach

### Phase 3: Component Impact Planning

1. **Analyze how personalization affects components** - Buttons, forms, navigation, etc.
2. **Plan component-specific customizations** - Beyond variable overrides
3. **Prioritize implementation order** - High-impact components first
4. **Validate approach with stakeholders** - Review before implementation

### Phase 4: Implementation Preparation

1. **Generate final SCSS files** - Create ready-to-use variable files
2. **Create implementation guide** - Step-by-step integration instructions
3. **Prepare validation checklist** - Testing and QA procedures
4. **Present complete plan for approval** - Final stakeholder review

## Decision Table: When to Use Each Folder

| If you need to... | Use folder... | Why |
|-------------------|--------------|-----|
| Document what design system provides | `design-system-analysis/` | Complete inventory before mapping |
| Plan Bootstrap mappings | `bootstrap-mapping/` | Strategy before implementation |
| Analyze component changes | `component-impact-analysis/` | Understand downstream effects |
| Store final SCSS files | `final-implementation/` | Ready-to-integrate code |

## Common Mistakes

**Mistake:** Starting implementation before completing analysis
**Correction:** Complete all analysis phases before writing any SCSS code

**Mistake:** Mixing analysis and implementation files in same directory
**Correction:** Separate analysis documentation from implementation code

**Mistake:** Skipping component impact analysis phase
**Correction:** Always analyze how variable changes affect downstream components

**Mistake:** Creating final SCSS files without approval process
**Correction:** Present mapping strategy for review before generating implementation files

## See Also

- ← Previous: [Progressive Enhancement Guidelines](progressive-enhancement-guidelines.md)
- Next: [Documentation Templates](documentation-templates.md)
- Related: [Bootstrap Research Methodology](bootstrap-accommodation-decision-framework.md)
