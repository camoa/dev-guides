---
description: "Guidelines for resuming Bootstrap mapping projects in new sessions"
tldr: "Use this when resuming a Bootstrap mapping project in a new session to ensure framework consistency and proper context loading."
drupal_version: "11.x"
---

# Project Continuation Guidelines

## When to Use

> Use this when resuming a Bootstrap mapping project in a new session to ensure framework consistency and proper context loading.

- You're resuming a Bootstrap mapping project in a new chat session
- You need to load project context for an AI assistant
- You want to ensure framework consistency across work sessions
- You're onboarding team members to an in-progress project

## How to Continue in New Chat Session

### Step 1: Load Project Context

**Pattern: Context Loading Message (8 lines)**

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

**Verification Checklist:**

- ✅ **Bootstrap capabilities researched first** for each component
- ✅ **6px threshold applied systematically** for quantitative decisions
- ✅ **Proper decision category selected** with documented rationale
- ✅ **SCSS best practices followed** (no @extend anti-patterns)
- ✅ **Progressive enhancement** considered for advanced features

### Step 3: Resume Systematic Analysis

**Resumption Process:**

1. **Review completed analysis** - Read project notes and check which phases are complete
2. **Identify next phase** - Determine which design system aspect to analyze next
3. **Apply Bootstrap research methodology** - Research capabilities before categorization
4. **Use 6px threshold framework** - Apply decision criteria systematically
5. **Select appropriate decision category** - ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE with rationale
6. **Document implementation strategy** - Follow framework guidelines and templates
7. **Validate against quality assurance checklist** - Ensure framework compliance

## Critical Principles to Maintain

### Framework Adherence

**Non-Negotiable Standards:**

- **Research Bootstrap capabilities FIRST** - Never categorize before investigating Bootstrap variables, maps, mixins, utilities
- **Apply 6px threshold consistently** - All quantitative decisions must reference threshold
- **Follow SCSS best practices** - NO @extend with Bootstrap classes, NO !important reactively, NO hardcoded values
- **Document all decisions** - Every mapping choice must have framework-based rationale
- **Progressive documentation** - Complete analysis before implementation phase

### Quality Standards

**Consistency Requirements:**

- **Complete analysis before implementation** - No SCSS code until analysis phase complete
- **Bootstrap integration priority** - Prefer ACCOMMODATE/EXTEND over CUSTOMIZE when < 6px difference
- **Progressive enhancement** - All CREATE category features must have fallbacks
- **Performance considerations** - Test advanced features on low-end devices

## Decision Table: Session Resumption Actions

| If previous session... | Next action... | Why |
|-----------------------|---------------|-----|
| Completed design system inventory | Start Bootstrap capabilities research | Analysis complete, ready for mapping |
| Completed mapping plan | Start component impact analysis | Understand downstream effects |
| Completed impact analysis | Generate implementation files | Ready for code generation |
| Incomplete analysis | Resume analysis phase | Don't skip phases |

## Common Mistakes

**Mistake:** Starting new analysis without reviewing project notes and completed work
**Correction:** Always read project notes first to understand current status and avoid duplicate work

**Mistake:** Changing decision framework mid-project
**Correction:** Maintain consistent 6px threshold and decision categories across all sessions

**Mistake:** Implementing code without completing analysis phases
**Correction:** Follow progressive documentation approach - analysis → mapping → impact → implementation

**Mistake:** Not confirming framework application before resuming work
**Correction:** Verify previous decisions follow framework before continuing

## See Also

- ← Previous: [Documentation Templates](documentation-templates.md)
- Next: [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Related: [Project Organization Principles](project-organization-principles.md)
- Related: [Quality Assurance Framework](quality-assurance-framework.md)
