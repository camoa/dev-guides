---
description: Translate design tokens from Figma, Style Dictionary, or a design spec into Tailwind v4 or v3 configuration.
tldr: "Use after running the Design System Recognition Guide to identify tokens. Maps primitive and semantic token layers to Tailwind configuration."
---

# Design Token Mapping

## When to Use

> Translating a design system's tokens (from Figma, Style Dictionary, or a design spec) into Tailwind configuration. Use after running the Design System Recognition Guide to identify what tokens you have.

## Decision

| Token type | v4 CSS syntax | v3 JS syntax |
|------------|---------------|--------------|
| Color | `--color-primary-500: oklch(...)` | `colors: { primary: { 500: '#...' } }` |
| Font family | `--font-display: "Inter", sans-serif` | `fontFamily: { display: ['Inter'] }` |
| Font size | `--text-lg: 1.125rem` | `fontSize: { lg: '1.125rem' }` |
| Font weight | `--font-weight-semibold: 600` | `fontWeight: { semibold: '600' }` |
| Spacing step | `--spacing-18: 4.5rem` | `spacing: { 18: '4.5rem' }` |
| Border radius | `--radius-xl: 0.75rem` | `borderRadius: { xl: '0.75rem' }` |
| Box shadow | `--shadow-card: 0 4px 16px ...` | `boxShadow: { card: '0 4px 16px ...' }` |
| Breakpoint | `--breakpoint-3xl: 120rem` | `screens: { '3xl': '120rem' }` |
| Transition ease | `--ease-spring: cubic-bezier(...)` | `transitionTimingFunction: { spring: 'cubic-bezier(...)' }` |

## Pattern — Mapping a Token Set to v4

```css
@import "tailwindcss";

@theme {
  /* ─── Colors ─────────────────────────── */
  --color-brand-50:  oklch(0.97 0.02 260);
  --color-brand-500: oklch(0.65 0.18 260);
  --color-brand-900: oklch(0.30 0.12 260);

  /* ─── Typography ─────────────────────── */
  --font-body: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Fraunces", ui-serif, Georgia, serif;
  --text-xs:  0.75rem;
  --text-sm:  0.875rem;
  --text-base: 1rem;
  --text-2xl: 1.5rem;

  /* ─── Spacing ────────────────────────── */
  /* Replace default scale with 4px base */
  --spacing: 0.25rem; /* 1 unit = 4px */

  /* ─── Shape & Depth ──────────────────── */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-full: 9999px;
  --shadow-card: 0 1px 3px rgb(0 0 0 / 0.1), 0 1px 2px rgb(0 0 0 / 0.06);
}

/* Semantic aliases — separate @theme inline block resolves var() at build time */
@theme inline {
  --color-primary: var(--color-brand-500);
  --color-primary-hover: var(--color-brand-600);
}
```

## Semantic vs Primitive Tokens

Always define two layers:

1. **Primitive tokens** — raw values (`--color-slate-500`, `--spacing-4`)
2. **Semantic tokens** — purpose-named (`--color-primary`, `--color-error`, `--spacing-component-padding`)

Semantic tokens are aliases to primitives. They decouple component code from raw values — if the brand color changes, only the primitive changes, semantic tokens and utilities update automatically.

## Figma → Tailwind Pipeline

```
Figma Design Tokens plugin → JSON export → Style Dictionary transform → CSS vars / tailwind.config.js
```

- Use [Style Dictionary](https://styledictionary.com/) to transform token JSON into multiple output formats
- Use the [Tailwind Tokens Figma plugin](https://www.figma.com/community/plugin/1513618945140968492) for direct sync
- Name tokens in Figma matching Tailwind namespace conventions (`color/brand/500`, `spacing/18`) to minimize transform logic

## Common Mistakes

- **Using hex values in v4 instead of oklch** — v4's color palette uses oklch for P3 gamut; mixing color spaces causes subtle inconsistencies
- **Defining semantic tokens without `@theme inline`** — `--color-primary: var(--color-brand-500)` in `@theme` creates a CSS var reference, but Tailwind won't resolve it when generating utility classes without the `inline` modifier
- **One-to-one mapping between Figma components and CSS classes** — tokens should be design-system level, not component-specific

## See Also

- [v4 Configuration](v4-configuration.md)
- [Custom Theme Extension](custom-theme-extension.md)
- [Utility Class Reference](utility-class-reference.md)
- Reference: https://tailwindcss.com/docs/theme
- Reference: https://styledictionary.com/
