---
description: Decide whether to use DaisyUI, raw Tailwind, shadcn/ui, or Radix UI for a project
---

# DaisyUI vs Alternatives

## When to Use

> Use DaisyUI when you need multi-theme support or a full design system out of the box. Use raw Tailwind when you need full design control. Use shadcn/ui when you need owned, modifiable component code. Use Radix + Tailwind when you need accessible primitives with full visual control.

## Decision

| If you need... | Use | Why |
|----------------|-----|-----|
| Fast prototyping, full design system out of box | DaisyUI | Pre-built component classes, 35+ built-in themes, single plugin |
| Full design control, no pre-built styling | Raw Tailwind + CVA | No opinionated component CSS to override |
| Accessible primitives + full visual control | Radix UI + Tailwind | Radix handles behavior/ARIA, you provide all visual styles |
| Unstyled Radix primitives with copy-paste patterns | shadcn/ui | Ships code into your repo; components are fully owned |
| Multi-theme support with CSS variable theming | DaisyUI | `data-theme` attribute switches entire palette instantly |
| Drupal/server-side-rendered no-JS components | Bootstrap or plain CSS | DaisyUI interactive patterns rely on checkbox/HTML tricks |
| React component library with TypeScript variants | CVA + shadcn/ui | DaisyUI has no built-in TypeScript variant API |

## Pattern

DaisyUI is a Tailwind plugin — not a replacement. Component classes and utilities compose together:

```html
<!-- btn btn-primary from DaisyUI, mt-4 w-full from Tailwind -->
<button class="btn btn-primary mt-4 w-full">Submit</button>
```

DaisyUI adds ~60 component CSS classes, a CSS custom property theming system (25+ variables per theme), and registers those variables as Tailwind color tokens (`bg-primary`, `text-base-content`).

## Common Mistakes

- **Wrong**: Thinking DaisyUI replaces Tailwind utilities — **Right**: Use both freely; DaisyUI layers on top
- **Wrong**: Choosing DaisyUI for pixel-perfect custom designs — **Right**: Overriding opinionated component CSS is friction; use raw Tailwind instead
- **Wrong**: Choosing raw Tailwind when you need multiple color themes — **Right**: DaisyUI's `data-theme` system is the easiest multi-theme solution
- **Wrong**: Using shadcn/ui as a "DaisyUI alternative" — **Right**: shadcn provides component code; DaisyUI provides component CSS classes — different problems

## See Also

- [Installation and Configuration](installation-configuration.md)
- [Theming System](theming-system.md)
- Reference: `design-system-tailwind.md` — Tailwind fundamentals, CVA, tailwind-merge
- Reference: `react-design-system.md` — CVA-based variant management in React
