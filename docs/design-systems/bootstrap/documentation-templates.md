---
description: "Standardized templates for Bootstrap mapping documentation"
tldr: "Use these templates for consistent documentation across Bootstrap mapping projects, ensuring framework compliance and systematic analysis."
drupal_version: "11.x"
---

# Documentation Templates

## When to Use

> Use these templates for consistent documentation across Bootstrap mapping projects, ensuring framework compliance and systematic analysis.

- You need standardized templates for Bootstrap mapping projects
- You're documenting design system analysis and mapping decisions
- You want consistent format for team projects
- You're establishing documentation standards

## Template 1: Project Notes

Use this template to track overall project status and key decisions.

### Pattern: Project Notes Template

```markdown
# [Project Name] Bootstrap Accommodation Project

## Project Context
- **Design System**: [Name]
- **Bootstrap Version**: [Version]
- **Theme Framework**: [Framework if applicable]
- **Project Location**: [Path]

## Analysis Progress
- [ ] Color system inventory
- [ ] Typography system analysis
- [ ] Spacing system mapping
- [ ] Border & radius analysis
- [ ] Shadow & elevation review
- [ ] Advanced features review (CREATE category)
- [ ] Bootstrap capability assessment
- [ ] Direct mapping identification
- [ ] Custom variable justification
- [ ] Component impact analysis
- [ ] Implementation planning

## Key Decisions
[Record major mapping decisions and rationale using framework criteria]

## Implementation Status
[Track implementation progress against framework guidelines]
```

## Template 2: Design System Analysis

Use this template for analyzing each design system aspect (colors, typography, spacing, etc.).

### Pattern: Design System Analysis Template

```markdown
# [System Name] [Component] Analysis

**Analysis Date**: [Date]
**Framework Applied**: 6px Threshold Decision Guide
**Status**: [In Progress/Complete/Approved]

## Design System Specifications

### [Component] Inventory
[Complete list of design system values]

### Usage Contexts
[How and where these values are used]

### Semantic Meanings
[What each value represents functionally]

## Bootstrap Research Results
**Bootstrap Variables**: [List relevant Bootstrap variables]
**Bootstrap Mixins**: [List applicable Bootstrap mixins]
**Bootstrap Maps**: [List extensible Bootstrap maps]
**Bootstrap Utilities**: [List related Bootstrap utilities]

## Framework Decision Application

| Design Value | Bootstrap Value | Difference | **Decision** | **Rationale** |
|--------------|-----------------|-----------|---------------|----------------|
| [value] | [bootstrap] | [diff] | [✅🔶🔴🆕] | [reasoning based on framework] |

## Implementation Strategy
[Specific SCSS implementation approach following framework guidelines]
```

## Template 3: Bootstrap Mapping Plan

Use this template to document Bootstrap accommodation strategy.

### Pattern: Bootstrap Mapping Template

```markdown
# Bootstrap [System] Mapping Plan

## Bootstrap Capabilities Research
[What Bootstrap provides by default - variables, mixins, maps, utilities]

## Accommodation Strategy

✅ **ACCOMMODATE** (Direct Bootstrap Usage):
- [Design value] → [Bootstrap variable]
- [Rationale for direct mapping]

🔶 **EXTEND** (Add to Bootstrap Maps):
```scss
$theme-colors: map-merge($theme-colors, (
  'brand': #[hex], // [Brand color] added to Bootstrap system
));
```

🔴 **CUSTOMIZE** (Override Bootstrap Values):
```scss
$spacers: (
  "sm": 24px, // [Justification for ≥6px difference]
);
```

🆕 **CREATE** (Advanced Features):
```scss
@mixin advanced-feature() {
  // [Implementation for features outside Bootstrap scope]
}
```

## Implementation Impact
[How these changes affect Bootstrap components and ecosystem]
```

## Template 4: Component Impact Analysis

Use this template to analyze how variable changes affect Bootstrap components.

### Pattern: Component Impact Template

```markdown
# [Component Type] Impact Analysis

## Affected Bootstrap Components
[List of Bootstrap components that will change with personalization]

## Accommodation Benefits
✅ **AUTOMATIC IMPROVEMENTS**:
- [Component] will automatically use personalized [design system aspect]
- [Specific benefit and visual improvement]

## Additional Customization Needs
❌ **REQUIRES ADDITIONAL WORK**:
- [Component] needs [specific customization beyond variables]
- [Justification and implementation approach]

## Framework Category Application
- **ACCOMMODATE**: [Components that work with Bootstrap variables]
- **EXTEND**: [Components that benefit from Bootstrap map extensions]
- **CUSTOMIZE**: [Components requiring custom variable overrides]
- **CREATE**: [Components needing advanced features]

## Implementation Priority
[High/Medium/Low priority with framework-based rationale]
```

## Template 5: Implementation Validation

Use this template to validate implementations against framework standards.

### Pattern: Implementation Validation Template

```markdown
# [Feature] Implementation Validation

## Framework Compliance Checklist
- [ ] 6px threshold analysis completed and documented
- [ ] Bootstrap capabilities researched systematically
- [ ] Appropriate decision category selected with clear rationale
- [ ] SCSS best practices followed (no @extend anti-patterns)
- [ ] Progressive enhancement considered for advanced features

## Quality Assurance Validation
- [ ] Browser compatibility tested across target browsers
- [ ] Performance impact assessed for advanced features
- [ ] Bootstrap component integration verified
- [ ] Documentation complete and framework-compliant
- [ ] Team review completed against framework guidelines

## Success Metrics Verification
- [ ] Bootstrap accommodation rate maximized where appropriate
- [ ] Custom implementation minimized for traditional features
- [ ] CREATE category properly justified for advanced features
- [ ] Design system compliance maintained
- [ ] Upgrade compatibility preserved
```

## Decision Table: Template Selection

| If you need to... | Use template... | Why |
|-------------------|----------------|-----|
| Track project status | Template 1: Project Notes | Central overview and checklist |
| Analyze design system | Template 2: Design System Analysis | Systematic feature evaluation |
| Plan Bootstrap mapping | Template 3: Bootstrap Mapping Plan | Document accommodation strategy |
| Analyze component impact | Template 4: Component Impact Analysis | Understand downstream effects |
| Validate implementation | Template 5: Implementation Validation | QA and framework compliance |

## Common Mistakes

**Mistake:** Using ad-hoc documentation format without structure
**Correction:** Use standardized templates for consistency and completeness

**Mistake:** Skipping framework compliance sections in templates
**Correction:** Always include decision category, rationale, and validation sections

**Mistake:** Not tracking analysis progress in project notes
**Correction:** Use checkbox lists to track completion and identify gaps

**Mistake:** Documenting implementation without rationale
**Correction:** Always include "Why" alongside "What" in all templates

## See Also

- ← Previous: [Project Organization Principles](project-organization-principles.md)
- Next: [Project Continuation Guidelines](project-continuation-guidelines.md)
- Related: [Quality Assurance Framework](quality-assurance-framework.md)
