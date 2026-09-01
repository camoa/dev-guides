---
description: React design system guides — component architecture, props patterns, composition, Tailwind, CVA variants, TypeScript, accessibility, Storybook, performance, testing
tracks:
  - project: react
    registry: npm
    channel: stable
    declared: "19"
    verified: 2026-02-19
  - project: tailwindcss
    registry: npm
    channel: stable
    declared: "4.x"
    verified: 2026-02-19
guide-meta:
  concepts:
    - React component architecture
    - compound components
    - headless components
    - CVA variants
    - Radix UI primitives
    - React props patterns
    - asChild pattern
    - cn() utility
    - design token consumption
  not:
    - Drupal SDC components
    - Twig templates
    - Next.js page routing
  requires: []
  complements:
    - design-systems/tailwind
    - design-systems/daisyui
    - design-systems/jsx-to-twig
  category: design-systems
---

# React Design System

Atomic decision guides for building reusable, composable, well-typed React components. Targets React 19, Next.js App Router, Tailwind CSS v4, Radix UI, and CVA.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide component architecture (flat vs compound vs headless) | [Component Architecture Decisions](component-architecture-decisions.md) | Use flat props for simple single-purpose UI. Use compound components when the caller needs to place named slots (header/body/footer) in their markup. |
| Design a component's props API | [Props Patterns](props-patterns.md) | Use these patterns when defining the public API of a component. Well-designed props prevent breaking changes and communicate intent clearly. |
| Handle children, slots, or asChild | [Children and Slot Patterns](children-and-slot-patterns.md) | Use when a component needs to render content it doesn't control — layouts, wrappers, trigger+panel pairs. |
| Build compound components with shared state | [Composition Patterns](composition-patterns.md) | Use when building multi-part components (select, tabs, accordion, dialog) where sub-components need to share state without prop drilling. |
| Use Tailwind with cn() and CVA | [Tailwind Integration](tailwind-integration.md) | Use `cn()` and CVA in every component that uses Tailwind classes. `cn()` handles merging; CVA handles variant definitions. |
| Manage size/color/state variants | [Variant Management](variant-management.md) | Use when a component has multiple dimensions of variation (size, color/intent, state) that combine in predictable ways. CVA makes these combinations type-safe and conflict-free. |
| Connect design tokens in Tailwind v4 | [Design Token Consumption](design-token-consumption.md) | Use when connecting design tokens (colors, spacing, typography scales) from a design tool or token file into React components. Tailwind v4 changes the approach significantly — there is no `tailwind.config.ts`. |
| Type components in TypeScript | [TypeScript Patterns](typescript-patterns.md) | Use in every design system component. TypeScript is how the system communicates its API to consumers — it's not optional. |
| Make components accessible | [Accessibility Patterns](accessibility-patterns.md) | Use in every interactive component. Accessibility is a correctness requirement — a design system that ships inaccessible components ships broken components. |
| Document components in Storybook | [Storybook Integration](storybook-integration.md) | Use for all design system components. Storybook is the development environment, living documentation, and visual regression baseline — not optional. |
| Organize component files and folders | [Component Organization](component-organization.md) | Use when setting up a design system repository or deciding where to put a new component. |
| Build form components with react-hook-form | [Form Components](form-components.md) | Use when building Input, Select, Checkbox, Textarea, or any form field component. Form components have unique requirements: validation state, error display, accessibility linking, and library integration. |
| Build layout primitives (Stack, Flex, Grid) | [Layout Components](layout-components.md) | Use when building reusable spacing, flex, and grid primitives. Layout components standardize spacing and remove repetitive Tailwind class sets from feature code. |
| Optimize render performance | [Performance](performance.md) | Use when a design system component is causing measurable performance issues, or when designing components that appear in long lists, frequently updating UIs, or high-traffic render paths. Profile first — do not optimize speculatively. |
| Test design system components | [Testing](testing.md) | Use for every design system component. Tests protect the API contract — they catch regressions before consumers notice. |
| Follow best practices and avoid anti-patterns | [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md) | Use before shipping a component to design system consumers, and during code review. |
| Find source references and maintenance notes | [Sources and Maintenance](sources-maintenance.md) |  |
