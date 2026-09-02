---
description: Choose between viewport breakpoints and container queries, and apply mobile-first responsive patterns in Tailwind.
tldr: "Use viewport breakpoints (`sm:`, `md:`) for layout changes at viewport widths. Use `@container` when a component needs to respond to its own width regardless of placement."
---

# Responsive Design & Container Queries

## When to Use

> Building responsive layouts — both viewport-based breakpoints and component-level container queries.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Layout changes at viewport widths | `sm:`, `md:`, `lg:` prefixes | Standard responsive breakpoints |
| Component changes based on its own width | `@container` + `@sm:`, `@md:` | True component portability regardless of placement |
| Target a range (not "and up") | `md:max-lg:` | Range modifiers without media query conflicts |
| One-off breakpoint | `min-[500px]:` / `max-[800px]:` | Arbitrary breakpoint without adding to theme |
| Breakpoint not in defaults | Add `--breakpoint-xs: 30rem` to `@theme` | Generates `xs:` prefix |

## Pattern — Mobile-First with Container Queries

```html
<!-- Mobile-first: unprefixed styles apply to all sizes -->
<div class="@container">
  <div class="
    grid grid-cols-1 gap-4
    @sm:grid-cols-2
    @lg:grid-cols-3
  ">
    <!-- Cards reflow based on container width, not viewport -->
  </div>
</div>

<!-- Named containers for nested context -->
<aside class="@container/sidebar w-64">
  <nav class="
    flex flex-col
    @lg/sidebar:flex-row
  ">
```

## Pattern — Viewport Breakpoints

```html
<!-- ✓ Mobile-first: applies class at sm and above -->
<div class="text-base sm:text-lg lg:text-xl">

<!-- ✓ Range: only between md and lg -->
<div class="md:max-lg:hidden">

<!-- ✗ Wrong: non-mobile-first approach -->
<div class="lg:max-xl:text-center">   <!-- fights the cascade, avoid -->
```

## Default Breakpoints Reference

| Prefix | Min-width | Common use |
|--------|-----------|------------|
| `sm` | 40rem (640px) | Landscape phones |
| `md` | 48rem (768px) | Tablets |
| `lg` | 64rem (1024px) | Laptops |
| `xl` | 80rem (1280px) | Desktops |
| `2xl` | 96rem (1536px) | Wide screens |

## Container Query Reference

Container sizes from `--container-*` tokens (verified from `node_modules/tailwindcss/theme.css`):

| Syntax | Min-width | Token |
|--------|-----------|-------|
| `@container` | Mark parent as a container | — |
| `@3xs:` | 16rem | `--container-3xs` |
| `@2xs:` | 18rem | `--container-2xs` |
| `@xs:` | 20rem | `--container-xs` |
| `@sm:` | 24rem | `--container-sm` |
| `@md:` | 28rem | `--container-md` |
| `@lg:` | 32rem | `--container-lg` |
| `@xl:` | 36rem | `--container-xl` |
| `@2xl:` | 42rem | `--container-2xl` |
| `@3xl:` | 48rem | `--container-3xl` |
| `@4xl:` | 56rem | `--container-4xl` |
| `@5xl:` | 64rem | `--container-5xl` |
| `@6xl:` | 72rem | `--container-6xl` |
| `@7xl:` | 80rem | `--container-7xl` |
| `@max-md:` | At container width < 28rem | range modifier |
| `@min-[475px]:` | Arbitrary container width | arbitrary |
| `@container/{name}` | Named container reference | — |

## Common Mistakes

- **Using viewport breakpoints for component-level layout** — the component breaks when placed in a narrow sidebar; use `@container` instead
- **Omitting `<meta name="viewport" content="width=device-width, initial-scale=1.0">`** — Tailwind's breakpoints match CSS `rem` to pixel expectations only with this tag
- **Using `max-*` variants as the primary approach** — Tailwind is mobile-first; `max-` variants should be exceptions, not the rule

## See Also

- [Dark Mode](dark-mode.md)
- [Custom Theme Extension](custom-theme-extension.md)
- Reference: https://tailwindcss.com/docs/responsive-design
