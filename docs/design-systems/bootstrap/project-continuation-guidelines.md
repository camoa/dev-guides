---
description: Guidelines for resuming Bootstrap mapping projects in new sessions
---

# Project Continuation Guidelines

## When to Use

> Use this when resuming a Bootstrap mapping project in a new session to ensure framework consistency and proper context loading.

## How to Continue in New Chat Session

### Step 1: Load Project Context

```markdown
I'm continuing the [Project Name] Bootstrap accommodation project using the 6px threshold framework.
Please load these documents to understand current status:

1. Project notes: [path to project notes]
2. Latest analysis: [path to recent analysis]
3. Implementation status: [path to current work]

The project follows the Bootstrap Accommodation Decision Framework with:
- 6px threshold decision criteria
- 4 decision categories (ACCOMMODATE, EXTEND, CUSTOMIZE, CREATE)
- Bootstrap-first research methodology
- Systematic documentation approach
```

### Step 2: Confirm Framework Application

Verification checklist:

- ✅ Bootstrap capabilities researched first for each component
- ✅ 6px threshold applied systematically
- ✅ Proper decision category selected with rationale
- ✅ SCSS best practices followed (no @extend anti-patterns)
- ✅ Progressive enhancement considered for advanced features

### Step 3: Resume Systematic Analysis

| Step | Action |
|------|--------|
| 1 | Review completed analysis - check which phases are complete |
| 2 | Identify next phase - determine next design system aspect |
| 3 | Apply Bootstrap research methodology - research before categorization |
| 4 | Use 6px threshold framework - apply decision criteria |
| 5 | Select decision category - ACCOMMODATE/EXTEND/CUSTOMIZE/CREATE with rationale |
| 6 | Document implementation strategy - follow framework guidelines |
| 7 | Validate against QA checklist - ensure framework compliance |

## Critical Principles to Maintain

### Framework Adherence (Non-Negotiable)

- **Research Bootstrap capabilities FIRST** - Never categorize before investigating variables, maps, mixins, utilities
- **Apply 6px threshold consistently** - All quantitative decisions must reference threshold
- **Follow SCSS best practices** - NO @extend with Bootstrap classes, NO reactive !important, NO hardcoded values
- **Document all decisions** - Every mapping choice needs framework-based rationale
- **Progressive documentation** - Complete analysis before implementation phase

### Quality Standards

- **Complete analysis before implementation** - No SCSS code until analysis complete
- **Bootstrap integration priority** - Prefer ACCOMMODATE/EXTEND over CUSTOMIZE when < 6px difference
- **Progressive enhancement** - All CREATE category features must have fallbacks
- **Performance considerations** - Test advanced features on low-end devices

## Session Resumption Actions

| If previous session... | Next action... | Why |
|-----------------------|---------------|-----|
| Completed design system inventory | Start Bootstrap capabilities research | Analysis complete, ready for mapping |
| Completed mapping plan | Start component impact analysis | Understand downstream effects |
| Completed impact analysis | Generate implementation files | Ready for code generation |
| Incomplete analysis | Resume analysis phase | Don't skip phases |

## Common Mistakes

- **Wrong**: Starting new analysis without reviewing notes → **Right**: Read project notes first to understand status
- **Wrong**: Changing decision framework mid-project → **Right**: Maintain consistent 6px threshold and categories
- **Wrong**: Implementing code without completing analysis → **Right**: Follow progressive documentation approach
- **Wrong**: Not confirming framework application → **Right**: Verify previous decisions follow framework

## See Also

- [Documentation Templates](documentation-templates.md)
- [Project Organization Principles](project-organization-principles.md)
- [Quality Assurance Framework](quality-assurance-framework.md)
- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
