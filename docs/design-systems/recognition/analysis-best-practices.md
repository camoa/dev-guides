---
description: Assess design system quality and maturity during analysis
---

# Design System Analysis Best Practices

## When to Use

> Use when beginning analysis of any design system. Use to assess quality, maturity, and whether a collection of components is truly a "system."

## Decision

| Quality Indicator | Mature System | Immature System |
|------------------|---------------|-----------------|
| **Token Structure** | 3-layer hierarchy (reference → semantic → component) | Hardcoded colors in every component |
| **Spacing Consistency** | Consistent values (8px, 16px, 24px) | Random values (13px, 19px, 27px) |
| **Color Palette** | Structured scale (Tailwind gray-50 to gray-950) | 5 different grays (#333, #3a3a3a, #444, #4a4a4a, #555) |
| **Typography** | 6-8 sizes following ratio (1.25× or 1.333×) | 15+ sizes with no relationship |
| **Dark Mode** | Token values swap, components unchanged | Every component has duplicate styles |
| **Governance** | Public changelog, contribution process, deprecation policy | No changelog, rogue components, abandoned dead code |

## Pattern

**Start with Tokens, Not Components:**

```
1. Analyze color tokens
   - Repeated values → Token system
   - Unique hex codes everywhere → No system

2. Check spacing tokens
   - Consistent gaps (8px scale) → System
   - Random values (13px, 19px) → Design debt

3. Verify typography tokens
   - Type scale with ratio → System
   - Arbitrary pixel values → No scale

4. Assess semantic layer
   - 3-layer hierarchy → Mature
   - Only raw values → Immature
```

**Inconsistency Patterns (Design Debt):**

| Anti-Pattern | Indicates | Good System Example |
|-------------|-----------|---------------------|
| 5 different grays (#333, #3a3a3a, #444, #4a4a4a, #555) | No shared palette, designers make up values | Tailwind gray-50 through gray-950 |
| Button heights (32px, 36px, 38px, 40px, 42px) | No sizing scale, built in isolation | Small (32px), Medium (40px), Large (48px) |
| 15+ font sizes with no ratio | Random adjustments, no hierarchy | 6-8 sizes at 1.25× ratio |

**Dark Mode as Litmus Test:**

Good implementation:
```css
/* Light */
:root { --color-background: white; --color-text: black; }
/* Dark */
.theme-dark { --color-background: black; --color-text: white; }
/* Components unchanged */
.button { background: var(--color-background); }
```

Bad implementation (2× maintenance, theme drift):
```css
.button-light { background: white; color: black; }
.button-dark { background: black; color: white; }
```

**Responsive Behavior Check:**

- **Good**: Breakpoint tokens, systematic adaptation, mobile-first, spacing scales responsively
- **Bad**: Components break at 768px/1024px, completely different mobile structure, no documented patterns

**Governance Indicators:**

| Good Signs | Poor Signs |
|-----------|------------|
| Public changelog | No changelog (teams don't know what changed) |
| Contribution process | Rogue component creation |
| Deprecation policy | Dead components accumulate |
| Semantic versioning | Breaking changes without warning |
| Component ownership (DRI) | Orphaned components |

## Common Mistakes

- **Wrong**: Starting with components before tokens → **Right**: Token analysis reveals if you have a system or just a library
- **Wrong**: Ignoring inconsistencies → **Right**: 5 different grays = no system, governance failure
- **Wrong**: Accepting desktop-only designs → **Right**: System must work across breakpoints
- **Wrong**: Missing dark mode token swap → **Right**: If tokens can't swap, architecture is wrong
- **Wrong**: No documented governance → **Right**: Changelog, contribution process, deprecation policy separate maintained systems from abandoned ones

## See Also

- [Design Tokens](./design-tokens.md)
- [Component Classification](./component-classification.md)
- [Validation Checklist](./validation-checklist.md)
- Reference: [Design System Governance](https://bradfrost.com/blog/post/a-design-system-governance-process/)
- Reference: [Design System Trends 2025](https://www.netguru.com/blog/key-design-systems-trends-and-best-practices)
