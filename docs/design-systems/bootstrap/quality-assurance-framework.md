---
description: Validation checklists and success metrics for Bootstrap mapping decisions
---

# Quality Assurance Framework

## When to Use

> Use this to validate Bootstrap accommodation decisions, review code for SCSS compliance, and ensure quality standards before deployment.

## Decision Validation Checklist

### 1. Bootstrap Capabilities Verification

- [ ] Bootstrap documentation researched - confirmed no existing solution
- [ ] Bootstrap mixins investigated - confirmed no applicable mixin
- [ ] Bootstrap maps examined - confirmed extension not possible
- [ ] Bootstrap utilities reviewed - confirmed no similar utility

### 2. SCSS Anti-Patterns Prevention

- [ ] NO @extend usage with Bootstrap classes
- [ ] NO hardcoded Bootstrap values - all use variables
- [ ] NO selector pollution - clean CSS output
- [ ] NO Bootstrap core modifications - only overrides/extensions

### 3. Variable Consistency Verification

- [ ] ALL font families use `$font-family-*` variables
- [ ] ALL font weights use `$font-weight-*` variables
- [ ] ALL colors use established variables when available
- [ ] ALL spacing uses Bootstrap spacing variables when available
- [ ] ALL line heights use established variables when available

### 4. Integration Compatibility

- [ ] Bootstrap class compatibility maintained
- [ ] Component isolation - custom styles don't interfere
- [ ] Upgrade path preserved - won't break with Bootstrap updates
- [ ] Documentation complete - all decisions and rationale documented

## Success Metrics

| Metric | Target | Why |
|--------|--------|-----|
| Bootstrap accommodation rate | ≥70% | Maximize ecosystem compatibility |
| Traditional custom implementation | <20% | Minimize maintenance for core features |
| CREATE category justified | All documented | Advanced features acceptable when justified |
| Design system compliance | 100% | Maintain brand integrity |
| @extend anti-patterns | Zero | Proper SCSS practices |
| Progressive enhancement | All advanced features | Graceful degradation |

## Common Mistakes

- **Wrong**: Skipping Bootstrap capabilities research → **Right**: Complete all 4 verification steps
- **Wrong**: Using @extend on Bootstrap classes → **Right**: Use variables and mixins
- **Wrong**: Hardcoding font-weight: 700 → **Right**: Use $font-weight-bold
- **Wrong**: Starting implementation before QA checklist → **Right**: Validate decisions first

## See Also

- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md)
- [SCSS Best Practices](scss-best-practices.md)
- [Progressive Enhancement Guidelines](progressive-enhancement-guidelines.md)
