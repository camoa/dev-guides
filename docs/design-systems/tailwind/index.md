---
description: Tailwind CSS design system guides — v3/v4 migration, configuration, tokens, variants, responsive, dark mode, CVA, tailwind-merge, performance, accessibility
tracks:
  - project: tailwindcss
    registry: npm
    channel: stable
    declared: "4.x"
    verified: 2026-02-19
guide-meta:
  concepts:
    - Tailwind CSS v4
    - Tailwind CSS v3
    - CSS-first configuration
    - "@theme"
    - utility classes
    - dark mode
    - CVA
    - tailwind-merge
    - "@apply"
  not:
    - design token extraction (see tailwind-tokens)
    - DaisyUI theming
    - Bootstrap utilities
  requires: []
  complements:
    - design-systems/tailwind-tokens
    - design-systems/daisyui
    - design-systems/react-design-system
  category: design-systems
---

# Tailwind CSS

Atomic decision guides for Tailwind CSS v4 (current) and v3. Covers CSS-first configuration, design token mapping, utility patterns, component variant strategies, and integration workflows.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between Tailwind v3 and v4 | [Tailwind v3 vs v4](tailwind-v3-vs-v4.md) | Use v4 for new projects targeting modern browsers. Use v3 when you need legacy browser support or have an existing stable v3 project. |
| Set up Tailwind from scratch | [Installation & Integration](installation-integration.md) | Use when setting up Tailwind in a new or existing project. Choose Vite plugin for Vite-based projects; PostCSS for everything else. |
| Configure a v4 project (CSS-first) | [v4 Configuration](v4-configuration.md) | Use when configuring a Tailwind v4 project. All configuration lives in CSS via `@theme` — no JS config file required. |
| Configure a v3 project (JS config) | [v3 Configuration](v3-configuration.md) | Use for projects running Tailwind v3, or when using `@config` in v4 to load a JS config during gradual migration. |
| Map design tokens to Tailwind | [Design Token Mapping](design-token-mapping.md) | Use after running the Design System Recognition Guide to identify tokens. Maps primitive and semantic token layers to Tailwind configuration. |
| Look up utility class patterns | [Utility Class Reference](utility-class-reference.md) | Use as a quick lookup for utility categories and patterns. Tailwind generates utilities for every theme token; this covers key classes and patterns. |
| Add custom utilities, variants, or animations | [Custom Theme Extension](custom-theme-extension.md) | Use when adding project-specific utilities, custom variants, animations, or sharing a theme across a monorepo. |
| Build responsive layouts and container queries | [Responsive Design](responsive-design.md) | Use viewport breakpoints (`sm:`, `md:`) for layout changes at viewport widths. Use `@container` when a component needs to respond to its own width regardless of placement. |
| Implement dark mode | [Dark Mode](dark-mode.md) | Use the default `dark:` variant for automatic system preference. Use class or data-attribute strategy when a manual toggle is required. |
| Decide when to extract a component class | [Component Patterns](component-patterns.md) | Use when deciding how to handle repeated style patterns — when to extract into a component class, when to use a framework component, and when utilities directly in markup are correct. |
| Know when @apply is appropriate | [@apply Guidance](apply-guidance.md) | Use `@apply` only when you don't control the HTML being styled. Avoid it when framework components are available. |
| Manage component variants with TypeScript | [Class Variance Authority](class-variance-authority.md) | Use CVA when a component has 2+ orthogonal variant dimensions, needs compound variants, or requires TypeScript autocompletion on variant props. |
| Merge Tailwind classes safely at runtime | [tailwind-merge & clsx](tailwind-merge-clsx.md) | Use `clsx` alone for conditional class joining with no override conflicts. Use `twMerge` (via `cn()`) when a consumer needs to override component-internal classes. |
| Connect Figma or Style Dictionary to Tailwind | [Design System Integration](design-system-integration.md) | Use when connecting a design tool (Figma) or token management system to Tailwind configuration — keeping design and implementation in sync. |
| Reduce bundle size and build time | [Performance Optimization](performance-optimization.md) | Use when diagnosing large CSS bundles, slow builds, or missing classes at runtime. |
| Know idiomatic Tailwind patterns and anti-patterns | [Best Practices](best-practices.md) | Reference before code review, architecture decisions, or when evaluating whether a Tailwind implementation is idiomatic. |
| Make components accessible | [Accessibility](accessibility.md) | Apply to every interactive component. Accessibility is a correctness requirement, not an optional feature. |
