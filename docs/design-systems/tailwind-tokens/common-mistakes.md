---
description: Common token extraction and naming mistakes to avoid
---

# Common Mistakes

## When to Use

> Use this to avoid common pitfalls in token extraction, naming, and workflow.

## Decision

**Token Extraction Mistakes**

| Mistake | Why It Fails | Fix |
|---|---|---|
| Hardcoding hex values in component CSS | Bypasses token system; breaks theme switching | Use var(--color-*) or utility classes |
| Using oklch without fallback for older browsers | oklch has ~96% global support; remaining 4% get broken colors | Use @supports fallback or accept the browser matrix. Tailwind v4 handles this via Lightning CSS |
| Forgetting -content color pairs in DaisyUI themes | Text becomes unreadable on colored backgrounds | Always define or let DaisyUI auto-generate content colors |
| Over-extracting tokens from utility classes | Not every Tailwind utility needs a design token | Only tokenize values that represent design decisions |
| Mixing v3 tailwind.config.js and v4 @theme in same project | Two conflicting configuration systems | Choose one. Migrate fully to v4 or stay on v3 |

**Naming Mistakes**

| Mistake | Why It Fails | Fix |
|---|---|---|
| Using --bg-primary instead of --color-primary | --color-* namespace feeds ALL color utilities (bg, text, border, ring) | Use the semantic --color-* namespace |
| Using platform-specific names in shared tokens | --ios-spacing-md is meaningless on web | Use platform-agnostic names; map to platform-specific at consumption |
| Inconsistent casing (--colorPrimary vs --color-primary) | Breaks tooling expectations; CSS convention is kebab-case | Always use kebab-case for CSS variables |

**Workflow Mistakes**

| Mistake | Why It Fails | Fix |
|---|---|---|
| Manually syncing Figma values to code | Values drift within days | Automate with Tokens Studio or Figma API |
| Defining tokens in both @theme and :root | Duplicate sources of truth | @theme for utility tokens, :root for non-utility variables |
| Not validating contrast ratios | WCAG failures | Test every color/content pair for 4.5:1 (AA) minimum |

## See Also

- [Best Practices](best-practices.md)
- [Token Naming Conventions](token-naming-conventions.md)
- [Tailwind v4 Token Architecture](tailwind-v4-token-architecture.md)
