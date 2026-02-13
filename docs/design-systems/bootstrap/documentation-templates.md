---
description: Standardized templates for Bootstrap mapping documentation
---

# Documentation Templates

## When to Use

> Use these templates for consistent documentation across Bootstrap mapping projects, ensuring framework compliance and systematic analysis.

## Template 1: Project Notes

Track overall project status and key decisions.

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

Analyze each design system aspect (colors, typography, spacing, etc.).

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

| Design Value | Bootstrap Value | Difference | Decision | Rationale |
|--------------|-----------------|-----------|----------|-----------|
| [value] | [bootstrap] | [diff] | [✅🔶🔴🆕] | [reasoning] |

## Implementation Strategy
[Specific SCSS implementation approach following framework guidelines]
```

## Template 3: Bootstrap Mapping Plan

Document Bootstrap accommodation strategy.

```markdown
# Bootstrap [System] Mapping Plan

## Bootstrap Capabilities Research
[What Bootstrap provides by default]

## Accommodation Strategy

✅ **ACCOMMODATE** (Direct Bootstrap Usage):
- [Design value] → [Bootstrap variable]

🔶 **EXTEND** (Add to Bootstrap Maps):
```scss
$theme-colors: map-merge($theme-colors, (
  'brand': #hex,
));
```

🔴 **CUSTOMIZE** (Override Bootstrap Values):
```scss
$spacers: (
  "sm": 24px, // Justification for ≥6px difference
);
```

🆕 **CREATE** (Advanced Features):
```scss
@mixin advanced-feature() {
  // Implementation for features outside Bootstrap scope
}
```

## Implementation Impact
[How these changes affect Bootstrap components]
```

## Template 4: Component Impact Analysis

Analyze how variable changes affect Bootstrap components.

```markdown
# [Component Type] Impact Analysis

## Affected Bootstrap Components
[List of Bootstrap components that will change]

## Accommodation Benefits
✅ **AUTOMATIC IMPROVEMENTS**:
- [Component] will automatically use personalized [aspect]

## Additional Customization Needs
❌ **REQUIRES ADDITIONAL WORK**:
- [Component] needs [customization beyond variables]

## Framework Category Application
- **ACCOMMODATE**: [Components that work with Bootstrap variables]
- **EXTEND**: [Components that benefit from map extensions]
- **CUSTOMIZE**: [Components requiring custom overrides]
- **CREATE**: [Components needing advanced features]

## Implementation Priority
[High/Medium/Low with rationale]
```

## Template 5: Implementation Validation

Validate implementations against framework standards.

```markdown
# [Feature] Implementation Validation

## Framework Compliance Checklist
- [ ] 6px threshold analysis completed and documented
- [ ] Bootstrap capabilities researched systematically
- [ ] Appropriate decision category selected with rationale
- [ ] SCSS best practices followed (no @extend anti-patterns)
- [ ] Progressive enhancement considered for advanced features

## Quality Assurance Validation
- [ ] Browser compatibility tested
- [ ] Performance impact assessed
- [ ] Bootstrap component integration verified
- [ ] Documentation complete
- [ ] Team review completed

## Success Metrics Verification
- [ ] Bootstrap accommodation rate maximized
- [ ] Custom implementation minimized
- [ ] CREATE category properly justified
- [ ] Design system compliance maintained
- [ ] Upgrade compatibility preserved
```

## Template Selection

| If you need to... | Use template... |
|-------------------|----------------|
| Track project status | Template 1: Project Notes |
| Analyze design system | Template 2: Design System Analysis |
| Plan Bootstrap mapping | Template 3: Bootstrap Mapping Plan |
| Analyze component impact | Template 4: Component Impact Analysis |
| Validate implementation | Template 5: Implementation Validation |

## Common Mistakes

- **Wrong**: Ad-hoc documentation without structure → **Right**: Use standardized templates
- **Wrong**: Skipping framework compliance sections → **Right**: Always include decision category and rationale
- **Wrong**: Not tracking analysis progress → **Right**: Use checkbox lists to track completion
- **Wrong**: Documenting "what" without "why" → **Right**: Always include rationale

## See Also

- [Project Organization Principles](project-organization-principles.md)
- [Project Continuation Guidelines](project-continuation-guidelines.md)
- [Quality Assurance Framework](quality-assurance-framework.md)
