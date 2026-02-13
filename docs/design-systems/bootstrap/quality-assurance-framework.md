---
description: Quality Assurance Framework — validation checklist for Bootstrap accommodation decisions and SCSS best practices
---

# Quality Assurance Framework

## When to Use

> Use when validating Bootstrap accommodation decisions, reviewing code for SCSS best practices compliance, or establishing team QA processes.

## Decision

| Review Area | Check | Success Criteria |
|-------------|-------|------------------|
| Bootstrap research | Variables, mixins, maps, utilities investigated | No existing solution found |
| SCSS anti-patterns | No `@extend` with Bootstrap classes | Clean, maintainable CSS output |
| Variable consistency | All fonts/weights/colors use variables | No hardcoded values |
| Bootstrap compatibility | Works with existing Bootstrap classes | Upgrade path preserved |
| Accommodation rate | ≥70% Bootstrap accommodation | Maximize ecosystem compatibility |

## Pattern

**Decision Validation Checklist**:

**1. Bootstrap Capabilities Verification**
- Bootstrap documentation researched
- Bootstrap mixins investigated
- Bootstrap maps examined
- Bootstrap utilities reviewed

**2. SCSS Anti-Patterns Prevention**
- NO `@extend` usage with Bootstrap classes
- NO hardcoded Bootstrap values
- NO selector pollution
- NO Bootstrap core modifications

**3. Variable Consistency Verification**
- ALL font families use `$font-family-base`
- ALL font weights use `$font-weight-*`
- ALL colors use established variables
- ALL spacing uses Bootstrap spacing variables
- ALL line heights use established variables

**4. Integration Compatibility**
- Bootstrap class compatibility maintained
- Component isolation verified
- Upgrade path preserved
- Documentation complete

## Common Mistakes

- **Wrong**: Skipping Bootstrap research → **Right**: Complete research checklist first
- **Wrong**: Using `@extend .btn` → **Right**: Verify NO `@extend` usage with Bootstrap classes
- **Wrong**: `font-family: "Helvetica"` → **Right**: Verify ALL fonts use variables
- **Wrong**: No documentation → **Right**: Document all decisions and rationale
- **Wrong**: <70% accommodation → **Right**: Maximize Bootstrap ecosystem compatibility

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [SCSS Best Practices](scss-best-practices.md)
- [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
