---
description: Quick-reference for Tailwind utility categories — layout, spacing, typography, color, sizing, effects, and state variants.
tldr: "Use as a quick lookup for utility categories and patterns. Tailwind generates utilities for every theme token; this covers key classes and patterns."
---

# Utility Class Reference

## When to Use

> Quick-reference for the most commonly used Tailwind utility categories. Tailwind generates utilities for every theme token; this section covers the patterns and key classes, not an exhaustive list.

## Layout Utilities

### Flexbox

| Utility | CSS |
|---------|-----|
| `flex` | `display: flex` |
| `flex-col` | `flex-direction: column` |
| `flex-wrap` | `flex-wrap: wrap` |
| `items-center` | `align-items: center` |
| `justify-between` | `justify-content: space-between` |
| `gap-4` | `gap: var(--spacing-4)` (1rem at 4px base) |
| `grow` / `shrink` / `shrink-0` | `flex-grow` / `flex-shrink` |

### Grid

| Utility | CSS |
|---------|-----|
| `grid` | `display: grid` |
| `grid-cols-3` | `grid-template-columns: repeat(3, minmax(0, 1fr))` |
| `grid-cols-[200px_1fr]` | Arbitrary template (v4: also `grid-cols-15` works) |
| `col-span-2` | `grid-column: span 2 / span 2` |
| `gap-x-4 gap-y-2` | Column/row gap separately |

### Container

```html
<!-- v4: container is a utility, not a component -->
<div class="container mx-auto px-4">

<!-- Named container for container queries -->
<div class="@container/sidebar">
  <nav class="@lg/sidebar:flex-col">
```

## Spacing Utilities

All spacing uses a single scale based on `--spacing` (4px base by default). Pattern: `{property}-{size}`.

| Prefix | Property | Example | Output |
|--------|----------|---------|--------|
| `p-` | padding (all sides) | `p-4` | `padding: 1rem` |
| `px-` / `py-` | padding x/y | `px-6` | `padding-inline: 1.5rem` |
| `pt-` `pr-` `pb-` `pl-` | padding sides | `pt-2` | `padding-top: 0.5rem` |
| `m-` | margin (all sides) | `m-auto` | `margin: auto` |
| `mx-auto` | center horizontally | | `margin-inline: auto` |
| `gap-` | flex/grid gap | `gap-8` | `gap: 2rem` |
| `space-x-` | between children | `space-x-4` | Applies margin to children |

## Typography Utilities

| Utility | What it does |
|---------|-------------|
| `text-lg` / `text-2xl` | Font size |
| `font-bold` / `font-semibold` | Font weight |
| `font-display` | Font family (custom token) |
| `leading-tight` / `leading-relaxed` | Line height |
| `tracking-wide` | Letter spacing |
| `text-gray-700` | Color |
| `uppercase` / `capitalize` | Text transform |
| `truncate` | Overflow ellipsis (single line) |
| `line-clamp-3` | Multi-line clamp |
| `text-balance` | `text-wrap: balance` |

## Color Utilities

Color utilities follow the pattern `{property}-{color}-{shade}`. Every color token generates all of these:

| Utility pattern | Property |
|-----------------|----------|
| `bg-brand-500` | `background-color` |
| `text-brand-500` | `color` |
| `border-brand-500` | `border-color` |
| `ring-brand-500` | Box shadow ring color |
| `fill-brand-500` | SVG fill |
| `stroke-brand-500` | SVG stroke |

**Opacity modifier** (works on any color utility):

```html
<div class="bg-brand-500/50">    <!-- 50% opacity background -->
<div class="text-gray-900/80">   <!-- 80% opacity text -->
```

## Sizing Utilities

| Prefix | Pattern | Example |
|--------|---------|---------|
| `w-` | Width | `w-full`, `w-64`, `w-[340px]`, `w-1/2` |
| `h-` | Height | `h-screen`, `h-16`, `h-dvh` |
| `min-w-` / `max-w-` | Min/max width | `max-w-prose`, `min-w-0` |
| `min-h-` / `max-h-` | Min/max height | `min-h-screen` |
| `size-` | Width AND height | `size-12` (shorthand) |
| `aspect-` | Aspect ratio | `aspect-video`, `aspect-square` |

## Effects Utilities

**Shadow tokens in v4.2.0** (verified from source — names changed from v3):

| Utility | Effect | v4 Token |
|---------|--------|----------|
| `shadow-2xs` | Barely visible 1px shadow | `--shadow-2xs` |
| `shadow-xs` | 1px blur shadow | `--shadow-xs` |
| `shadow-sm` | Standard small shadow | `--shadow-sm` (was `shadow` in v3) |
| `shadow-md` | Medium shadow | `--shadow-md` (was `shadow-md` in v3) |
| `shadow-lg` | Large shadow | `--shadow-lg` |
| `inset-shadow-sm` | Inset shadow (inner depth) | `--inset-shadow-sm` |
| `drop-shadow-md` | Filter drop-shadow (works on SVG/PNG) | `--drop-shadow-md` |
| `text-shadow-sm` | Text shadow | `--text-shadow-sm` (new in v4) |
| `opacity-50` | Element opacity | — |
| `rounded-md` | Border radius | `--radius-md: 0.375rem` |
| `ring-2 ring-brand-500` | Outline ring (inset box-shadow) | — |
| `backdrop-blur-sm` | Backdrop filter | `--blur-sm: 8px` |
| `blur-md` | Element blur filter | `--blur-md: 12px` |
| `transition` / `duration-300` / `ease-in-out` | Transitions | `--default-transition-duration: 150ms` |
| `animate-spin` / `animate-bounce` | Keyframe animations | `--animate-spin`, `--animate-bounce` |
| `perspective-normal` | 3D perspective | `--perspective-normal: 500px` (new in v4) |

**v3 shadow rename**: v3's `shadow-sm` is now `shadow-xs` in v4. v3's `shadow` (bare) is now `shadow-sm`. Run `npx @tailwindcss/upgrade` to catch these.

## State Variants (Applied as Prefixes)

```html
<button class="
  bg-brand-500
  hover:bg-brand-600
  focus-visible:outline-2 focus-visible:outline-brand-500
  active:scale-95
  disabled:opacity-50 disabled:cursor-not-allowed
  aria-pressed:bg-brand-700
">
```

| Variant | When applied |
|---------|-------------|
| `hover:` | Mouse hover |
| `focus:` | Any focus |
| `focus-visible:` | Keyboard focus only (preferred for accessibility) |
| `active:` | Mouse/touch press |
| `disabled:` | Disabled state |
| `checked:` | Checkbox/radio checked |
| `aria-expanded:` | ARIA expanded state |
| `group-hover:` | Parent `.group` is hovered |
| `peer-checked:` | Sibling `.peer` is checked |

## Common Mistakes

- **Using `focus:` for focus rings instead of `focus-visible:`** — causes visible focus on mouse clicks, poor UX
- **Using `text-opacity-*` (v3 deprecated)** — use `text-gray-900/80` slash syntax
- **Hardcoding arbitrary values (`w-[340px]`) for values that should be design tokens** — add them to `@theme` instead

## See Also

- [Custom Theme Extension](custom-theme-extension.md)
- [Accessibility](accessibility.md)
- Reference: https://tailwindcss.com/docs
