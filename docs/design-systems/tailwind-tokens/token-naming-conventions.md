---
description: Choose the right token naming convention for your use case
---

# Token Naming Conventions

## When to Use

> Use this when establishing naming conventions for tokens across platforms or when choosing between multiple standards.

## Decision

| Convention | Format | Example | When to Use |
|---|---|---|---|
| Tailwind v4 native | --{category}-{name} | --color-primary | Tailwind v4 projects; direct CSS consumption |
| DaisyUI semantic | --color-{role} | --color-base-100 | DaisyUI themes; semantic role-based theming |
| W3C Design Tokens (DTCG) | {group}.{name} in JSON | "color.primary.500" | Multi-platform token exchange; Figma sync |
| CSS custom props (namespaced) | --{prefix}-{category}-{name} | --ds-color-primary | Custom systems with collision avoidance |
| Tailwind v3 JS | theme.{category}.{name} | theme.colors.blue.500 | Legacy Tailwind v3 config files |

## Pattern

**Token Naming Tiers**

Design tokens are organized in tiers:

1. **Global** — raw values (e.g. --color-blue-500: oklch(62% 0.21 260))
2. **Semantic** — design intent (e.g. --color-primary: var(--color-blue-500))
3. **Component** — scoped (e.g. --btn-bg: var(--color-primary))

Use two tiers minimum (global + semantic). Add component tier only when scoped overrides are genuinely needed. Over-tiering adds indirection without benefit.

**Examples Across Conventions**

| Tier | Tailwind v4 | DaisyUI | W3C DTCG |
|---|---|---|---|
| Global | --color-blue-500 | (uses Tailwind colors) | color.blue.500 |
| Semantic | --color-primary | --color-primary | color.primary |
| Component | --btn-bg | (uses semantic) | component.button.background |

## Common Mistakes

- **Wrong**: Using platform-specific names in shared tokens (--ios-spacing-md). **Right**: Use platform-agnostic names; map to platform-specific at consumption.
- **Wrong**: Inconsistent casing (--colorPrimary vs --color-primary). **Right**: Always use kebab-case for CSS variables.
- **Wrong**: Creating 4+ tiers (global → brand → semantic → component → variant). **Right**: 2-3 tiers maximum. More creates confusion.

## See Also

- [W3C Design Tokens Format](w3c-design-tokens-format.md)
- [Tailwind v4 Namespace Reference](tailwind-v4-namespace-reference.md)
- Reference: https://www.designtokens.org/
