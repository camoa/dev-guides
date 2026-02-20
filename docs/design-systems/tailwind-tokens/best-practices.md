---
description: Token management best practices for design systems
---

# Best Practices

## When to Use

> Use this as a reference for token architecture, color management, multi-platform strategy, and Drupal/DaisyUI specifics.

## Decision

**Token Architecture**

| Principle | Why | Implementation |
|---|---|---|
| Single source of truth | Prevents drift, simplifies updates | Define tokens in one place (Figma, @theme, or .tokens.json). Generate all other formats from that source. |
| Two-tier minimum | Balances flexibility and maintainability | Global tokens (raw values) + Semantic tokens (design intent). Add component tier only when needed. |
| Use @theme for utility tokens | Generates both variables and classes | Reserve :root for variables that should not create Tailwind utility classes. |
| Co-locate tokens with context | Improves discoverability | Typography tokens in typography.pcss, spacing in main @theme, colors in DaisyUI theme block. |

**Color Management**

| Principle | Why | Implementation |
|---|---|---|
| Use oklch for new projects | Perceptually uniform lightness | Easy to create consistent shade progressions |
| Always define content color pairs | Ensures readability | --color-primary needs --color-primary-content. Explicit is better than auto-generated. |
| Test dark mode separately | Inversion doesn't guarantee quality | Re-evaluate contrast and saturation for dark themes |
| Document color roles | Clarifies intent for team | Write down what each semantic color means in project context |

**Multi-Platform Strategy**

| Principle | Why | Implementation |
|---|---|---|
| W3C DTCG for interchange | Vendor-neutral, spec-driven | Use .tokens.json as canonical format for sharing between tools |
| Automate the pipeline | Eliminates manual drift | Figma export → W3C format → Tailwind @theme → DaisyUI theme. No manual copy. |
| Version your tokens | Enables review and rollback | Treat token files as first-class code artifacts. Review token changes in PRs. |
| Validate on every build | Catches breaking changes early | Check that all expected utilities exist and contrast ratios pass after token changes |

**Drupal / DaisyUI Specifics**

| Principle | Why | Implementation |
|---|---|---|
| Use UI Suite DaisyUI starterkit patterns | Proven structure | Follow established file structure for @theme, @plugin, and @utility definitions |
| Leverage ui_skins.css_variables.yml | Empowers site builders | Let site builders override tokens through Drupal admin UI without touching code |
| Map SDC props to semantic values | Improves DX | Components should accept primary/secondary, not oklch(55% 0.3 240) |

## See Also

- [Common Mistakes](common-mistakes.md)
- [Token Naming Conventions](token-naming-conventions.md)
- [W3C Design Tokens Format](w3c-design-tokens-format.md)
