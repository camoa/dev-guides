---
description: Choose between viewport breakpoints and container queries, and apply mobile-first responsive patterns in Tailwind.
---

# Responsive Design & Container Queries

## When to Use

> Use viewport breakpoints (`sm:`, `md:`) for layout changes at viewport widths. Use `@container` when a component needs to respond to its own width regardless of placement.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Layout changes at viewport widths | `sm:`, `md:`, `lg:` prefixes | Standard responsive breakpoints |
| Component changes based on its own width | `@container` + `@sm:`, `@md:` | True component portability regardless of placement |
| Target a range (not "and up") | `md:max-lg:` | Range modifiers without media query conflicts |
| One-off breakpoint | `min-[500px]:` / `max-[800px]:` | Arbitrary breakpoint without adding to theme |
| Breakpoint not in defaults | Add `--breakpoint-xs: 30rem` to `@theme` | Generates `xs:` prefix |

## Pattern

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

```html
<!-- Viewport breakpoints — mobile-first -->
<div class="text-base sm:text-lg lg:text-xl">

<!-- Range: only between md and lg -->
<div class="md:max-lg:hidden">
```

## Default Breakpoints

| Prefix | Min-width | Common use |
|--------|-----------|------------|
| `sm` | 40rem (640px) | Landscape phones |
| `md` | 48rem (768px) | Tablets |
| `lg` | 64rem (1024px) | Laptops |
| `xl` | 80rem (1280px) | Desktops |
| `2xl` | 96rem (1536px) | Wide screens |

## Container Query Sizes

| Syntax | Min-width | Token |
|--------|-----------|-------|
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
| `@max-md:` | Container < 28rem | range modifier |
| `@min-[475px]:` | Arbitrary width | arbitrary |

## Common Mistakes

- **Wrong**: Using viewport breakpoints for component-level layout — the component breaks when placed in a narrow sidebar. **Right**: Use `@container` for components that must work in any context.
- **Wrong**: Omitting `<meta name="viewport" content="width=device-width, initial-scale=1.0">`. **Right**: Required for Tailwind breakpoints to match expected pixel values.
- **Wrong**: Using `max-*` variants as the primary approach. **Right**: Tailwind is mobile-first; `max-` variants should be exceptions.

## See Also

- [Dark Mode](dark-mode.md)
- [Custom Theme Extension](custom-theme-extension.md)
- Reference: https://tailwindcss.com/docs/responsive-design
