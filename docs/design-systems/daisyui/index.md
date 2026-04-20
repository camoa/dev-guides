---
description: DaisyUI v5 guides — theming, color tokens, component reference, React integration, customization, accessibility
guide-meta:
  concepts:
    - DaisyUI v5
    - oklch theming
    - semantic component classes
    - DaisyUI themes
    - CVA variants
    - DaisyUI React
  not:
    - UI Suite DaisyUI Drupal theme
    - raw Tailwind utility classes
    - shadcn/ui
  requires:
    - design-systems/tailwind
  complements:
    - design-systems/tailwind-tokens
    - design-systems/react-design-system
    - drupal/ui-suite-daisyui
  specializes: ""
  category: design-systems
---

# DaisyUI

DaisyUI v5 component library built on Tailwind CSS. Semantic component classes, oklch theming system, 35+ built-in themes, and React integration patterns.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide whether to use DaisyUI vs raw Tailwind vs shadcn/ui | [DaisyUI vs Alternatives](daisyui-vs-alternatives.md) | Use DaisyUI when you need multi-theme support or a full design system out of the box. Use raw Tailwind when you need full design control. |
| Install DaisyUI with Tailwind v4 or v3 | [Installation and Configuration](installation-configuration.md) | Setting up DaisyUI in a new or existing Tailwind project. |
| Implement multi-theme or light/dark mode | [Theming System](theming-system.md) | Use DaisyUI theming for multi-theme support, light/dark mode switching, brand color customization, or white-labeling. The `data-theme` attribute switches the entire palette with no JavaScript class manipulation required. |
| Understand the CSS variables and color tokens | [Color System and Design Tokens](color-system-design-tokens.md) | Use this guide when you need to understand which CSS variables control which visual properties, and how to use DaisyUI semantic colors as Tailwind utility classes. |
| Use button, dropdown, modal, or swap | [Actions Components](actions-components.md) | Interactive elements that trigger actions: buttons, dropdowns, modals, and content swap toggles. |
| Use badge, card, alert, stat, or table | [Data Display Components](data-display-components.md) | Presenting information: status indicators, grouped content, statistics, tables, and collapsible sections. |
| Use navbar, menu, tabs, or breadcrumbs | [Navigation Components](navigation-components.md) | Site navigation, wayfinding, and multi-section navigation patterns. |
| Use input, select, textarea, checkbox, or toggle | [Data Input Components](data-input-components.md) | Form elements: text fields, selections, toggles, and form structure. |
| Use drawer, hero, divider, or stack | [Layout Components](layout-components.md) | Page structure, sidebars, overlays, and content arrangement patterns. |
| Extend or override DaisyUI components | [Customization Patterns](customization-patterns.md) | Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components that follow DaisyUI conventions. |
| Use DaisyUI in React with CVA | [DaisyUI and React](daisyui-react.md) | Building React components that use DaisyUI classes, managing variants with CVA, and integrating DaisyUI theming with React patterns. |
| Know best practices and anti-patterns | [Best Practices](best-practices.md) | Code review, architecture decisions, and onboarding guidance for DaisyUI projects. |
| Handle accessibility gaps and ARIA requirements | [Security and Accessibility](security-accessibility.md) | Every component implementation. Accessibility and security are part of shipping correct code, not optional steps. |
| Review sources and version information | [Sources and Maintenance](sources-maintenance.md) |  |
