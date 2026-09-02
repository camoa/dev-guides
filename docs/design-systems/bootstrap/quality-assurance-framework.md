---
description: "Validation checklists and success metrics for Bootstrap mapping decisions"
tldr: "Use this to validate Bootstrap accommodation decisions, review code for SCSS compliance, and ensure quality standards before deployment."
drupal_version: "11.x"
---

# Quality Assurance Framework

## When to Use

> Use this to validate Bootstrap accommodation decisions, review code for SCSS compliance, and ensure quality standards before deployment.

- You need to validate your Bootstrap accommodation decisions
- You're reviewing code for SCSS best practices compliance
- You want to ensure quality standards before deployment
- You're establishing team QA processes

## Decision Validation Checklist

### 1. Bootstrap Capabilities Verification

- [ ] **Bootstrap documentation researched** - confirmed no existing solution
- [ ] **Bootstrap mixins investigated** - confirmed no applicable mixin available
- [ ] **Bootstrap maps examined** - confirmed extension not possible
- [ ] **Bootstrap utilities reviewed** - confirmed no similar utility exists

### 2. SCSS Anti-Patterns Prevention

- [ ] **NO @extend usage** with Bootstrap classes anywhere in codebase
- [ ] **NO hardcoded Bootstrap values** - all references use variables
- [ ] **NO selector pollution** - clean, maintainable CSS output
- [ ] **NO Bootstrap core modifications** - only variable overrides and extensions

### 3. Variable Consistency Verification

- [ ] **ALL font families** use established variables (`$font-family-base`) - NO hardcoded strings
- [ ] **ALL font weights** use established variables (`$font-weight-*`) - NO numeric values
- [ ] **ALL colors** use established variables when available - NO hex codes in components
- [ ] **ALL spacing values** use Bootstrap spacing variables when available - NO hardcoded rem/px
- [ ] **ALL line heights** use established variables when available - NO hardcoded decimals

### 4. Integration Compatibility

- [ ] **Bootstrap class compatibility** maintained - works with existing Bootstrap classes
- [ ] **Component isolation** - custom styles don't interfere with Bootstrap components
- [ ] **Upgrade path preserved** - implementation won't break with Bootstrap updates
- [ ] **Documentation complete** - all decisions and rationale documented

## Success Metrics

- **≥70% Bootstrap accommodation rate** - Maximize ecosystem compatibility
- **<20% traditional custom implementation** - Minimize maintenance for core features
- **CREATE category justified** - Advanced features outside Bootstrap scope acceptable
- **100% design system compliance** - Maintain brand integrity
- **Zero @extend anti-patterns** - Proper SCSS practices maintained
- **Progressive enhancement** - Advanced features degrade gracefully

## Common Mistakes

- **Wrong**: Skipping Bootstrap capabilities research → **Right**: Complete all 4 verification steps
- **Wrong**: Using @extend on Bootstrap classes → **Right**: Use variables and mixins
- **Wrong**: Hardcoding font-weight: 700 → **Right**: Use $font-weight-bold
- **Wrong**: Starting implementation before QA checklist → **Right**: Validate decisions first

## See Also

- ← Previous: [Advanced SCSS Best Practices](advanced-scss-best-practices.md)
- Next: [Progressive Enhancement Guidelines](progressive-enhancement-guidelines.md)
