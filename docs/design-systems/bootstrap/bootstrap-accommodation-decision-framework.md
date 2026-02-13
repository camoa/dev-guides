---
description: Core decision-making methodology for Bootstrap mapping using the 6px threshold
---

# Bootstrap Accommodation Decision Framework

## When to Use

> Use this framework when deciding whether to ACCOMMODATE, EXTEND, CUSTOMIZE, or CREATE. Use the 6px threshold to systematically evaluate visual differences.

## Core Principle

**"Minimal visual impact justifies accommodation, significant visual differences require customization"**

## Framework Goals

- **Maximize Bootstrap ecosystem compatibility** while preserving design integrity
- **Systematic decision-making** for any design system → Bootstrap conversion
- **Minimize maintenance overhead** through strategic accommodation
- **Enable advanced features** when Bootstrap scope is exceeded
- **Maintain upgrade compatibility** by working with Bootstrap's architecture

## The 6-Pixel Rule

| Condition | Decision | When |
|-----------|----------|------|
| < 6px difference | ACCOMMODATE | Minimal visual impact, functionally equivalent |
| ≥ 6px difference | CUSTOMIZE | Visual impact requires precision |
| Missing value | EXTEND | Bootstrap lacks the value but system exists |
| No equivalent | CREATE | Outside Bootstrap's scope entirely |

## Decision Categories

### ✅ ACCOMMODATE (Use Bootstrap As-Is)

**Criteria:**
- < 6px difference from Bootstrap defaults
- Same design intent achieved
- Low maintenance benefit

**Pattern:**
```scss
// Use Bootstrap variables directly
$primary: #194582;           // Override Bootstrap variable
$body-color: #141414;        // Override Bootstrap variable

// Use Bootstrap utilities in HTML
.btn-primary                 // Automatically uses $primary color
.p-2                        // Automatically uses Bootstrap 8px spacing
```

### 🔶 EXTEND (Add to Bootstrap System)

**Criteria:**
- Missing values in Bootstrap
- Useful additions to existing systems

**Pattern:**
```scss
// Add to Bootstrap's existing maps
$spacers: map-merge($spacers, (
  "3xs": 2px,               // Add missing micro-spacing
  "2xs": 6px,               // Add missing value
));

$theme-colors: map-merge($theme-colors, (
  "brand": #your-brand-color,
));
```

### 🔴 CUSTOMIZE (Replace Bootstrap Values)

**Criteria:**
- ≥ 6px difference from Bootstrap defaults
- Systematic scale changes
- Brand requirements

**Pattern:**
```scss
// Replace Bootstrap defaults
$spacers: (
  0: 0,
  "3xs": 2px,
  "2xs": 4px,
  "xs": 8px,
  "sm": 24px,               // Custom value ≥6px different
  "md": 32px,
  "lg": 40px,
  "xl": 64px,
);
```

### 🆕 CREATE (New Advanced Features)

**Criteria:**
- Modern design features not available in Bootstrap
- Advanced visual effects outside Bootstrap's scope

**Pattern:**
```scss
// Modern features not in Bootstrap
@mixin advanced-feature($base-value, $modifier: 1) {
  // Use Bootstrap variables when applicable
  border-radius: var(--bs-border-radius);

  // Implement advanced functionality
  @supports (backdrop-filter: blur(10px)) {
    backdrop-filter: blur(#{$base-value * $modifier});
  }
}
```

## Bootstrap Research Methodology

**CRITICAL: Research Bootstrap Capabilities FIRST**

1. **Bootstrap Documentation Review** - Check _variables.scss for existing variables
2. **Bootstrap Mixins Investigation** - Check mixins/_*.scss for reusable patterns
3. **Bootstrap Maps Examination** - Check _maps.scss for extensible systems
4. **Bootstrap Utilities Research** - Check utilities/_api.scss for utility generation

## Decision Tree After Research

| Bootstrap Status | Decision |
|-----------------|----------|
| Has exact feature | ✅ ACCOMMODATE |
| Has extensible system | 🔶 EXTEND |
| Has similar feature with ≥6px difference | 🔴 CUSTOMIZE |
| Has no equivalent or capability | 🆕 CREATE |

## Common Mistakes

- **Wrong**: Customizing before researching Bootstrap capabilities → **Right**: Research Bootstrap first, then decide
- **Wrong**: Accommodating ≥6px differences → **Right**: Apply 6px threshold rigorously
- **Wrong**: Creating from scratch when Bootstrap has extensible system → **Right**: Extend existing Bootstrap maps

## See Also

- [SCSS Best Practices](scss-best-practices.md)
- [Design Tokens → Bootstrap Variables](design-tokens-bootstrap-variables.md)
- Reference: [Bootstrap Sass Documentation](https://getbootstrap.com/docs/5.3/customize/sass/)
