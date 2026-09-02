---
description: Decide whether to use DaisyUI, raw Tailwind, shadcn/ui, or Radix UI for a project
tldr: "Use DaisyUI when you need multi-theme support or a full design system out of the box. Use raw Tailwind when you need full design control."
---

# DaisyUI vs Alternatives

## When to Use

> Every project decision about UI library choice. DaisyUI competes with raw Tailwind utilities, Bootstrap, shadcn/ui, and Radix + CVA patterns.

Use DaisyUI when you need multi-theme support or a full design system out of the box. Use raw Tailwind when you need full design control. Use shadcn/ui when you need owned, modifiable component code. Use Radix + Tailwind when you need accessible primitives with full visual control.

## Decision: Which UI Library

| If you need... | Use... | Why |
|---|---|---|
| Fast prototyping, full design system out of box | DaisyUI | Pre-built component classes, 35+ built-in themes, single plugin |
| Full design control, no pre-built styling | Raw Tailwind + CVA | No opinionated component CSS to override; start from zero |
| Accessible primitives + full visual control | Radix UI + Tailwind | Radix handles behavior/ARIA, you provide all visual styles |
| Unstyled Radix primitives with copy-paste patterns | shadcn/ui | Ships code into your repo; components are fully owned and modifiable |
| Multi-theme support with CSS variable theming | DaisyUI | Best-in-class theming: `data-theme` attribute switches entire palette instantly |
| Drupal/server-side-rendered no-JS components | Bootstrap or plain CSS | DaisyUI interactive patterns (drawer, modal) rely on checkbox/HTML tricks; Drupal JS behaviors work better with explicit classes |
| React component library with TypeScript variants | CVA + shadcn/ui | DaisyUI has no built-in TypeScript variant API |

## What DaisyUI Actually Is

DaisyUI is a Tailwind CSS **plugin** that:

1. Adds ~60 component CSS classes (`.btn`, `.card`, `.modal`) on top of Tailwind
2. Provides a CSS custom property theming system (25+ variables per theme)
3. Registers those CSS variables as Tailwind color tokens (`bg-primary`, `text-base-content`)
4. Ships 35+ built-in themes switchable via `data-theme` attribute

DaisyUI does NOT replace Tailwind utilities. Every Tailwind utility still works alongside DaisyUI classes. The combination looks like: `<button class="btn btn-primary mt-4 w-full">` — `btn btn-primary` from DaisyUI, `mt-4 w-full` from Tailwind.

```html
<!-- btn btn-primary from DaisyUI, mt-4 w-full from Tailwind -->
<button class="btn btn-primary mt-4 w-full">Submit</button>
```

## Common Mistakes

- Thinking DaisyUI replaces Tailwind — it layers on top; use both freely
- Choosing DaisyUI when you need pixel-perfect custom designs — overriding opinionated component CSS is friction
- Choosing raw Tailwind when you need multiple color themes — DaisyUI's theme system is the easiest multi-theme solution available
- Using shadcn/ui as a "DaisyUI alternative" — they solve different problems; shadcn provides component code, DaisyUI provides component CSS classes

## See Also

- [Installation and Configuration](installation-configuration.md)
- [Theming System](theming-system.md)
- Reference: `design-system-tailwind.md` — Tailwind fundamentals, CVA, tailwind-merge
- Reference: `react-design-system.md` — CVA-based variant management in React
