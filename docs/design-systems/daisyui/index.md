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
    - data-theme
    - mockup-browser
    - mockup-phone
    - loading spinner
    - skeleton placeholder
    - radial-progress
    - floating-label
    - validator
    - filter chips
    - dock
    - timeline
    - status dot
    - per-page theme switching
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
| Decide whether to use DaisyUI vs raw Tailwind vs shadcn/ui | [DaisyUI vs Alternatives](daisyui-vs-alternatives.md) | Use DaisyUI when you need multi-theme support or a full design system out of the box. Use raw Tailwind when you need full design control. shadcn provides component code; DaisyUI provides component CSS classes — they solve different problems. |
| Install DaisyUI with Tailwind v4 or v3 | [Installation and Configuration](installation-configuration.md) | Use `@plugin "daisyui"` in CSS for Tailwind v4 (not the JS config). Add `--default` flag on the root theme or no color applies. |
| Implement multi-theme, light/dark mode, or per-page theme switching | [Theming System](theming-system.md) | Use DaisyUI theming for multi-theme support, light/dark mode switching, brand color customization, or white-labeling. The `data-theme` attribute switches the entire palette with no JavaScript class manipulation required. All themes must be registered at build time; per-page scoping works by placing `data-theme` on any container element. |
| Understand the CSS variables and color tokens | [Color System and Design Tokens](color-system-design-tokens.md) | Use this guide when you need to understand which CSS variables control which visual properties, and how to use DaisyUI semantic colors as Tailwind utility classes. |
| Use button, dropdown, modal, or swap | [Actions Components](actions-components.md) | Interactive elements that trigger actions: buttons, dropdowns, modals, and content swap toggles. |
| Use badge, card, alert, stat, table, avatar, chat, timeline, or tooltip | [Data Display Components](data-display-components.md) | Presenting information: status indicators, grouped content, statistics, tables, collapsible sections, avatars, chat bubbles, timelines, and tooltips. Add `role='alert'` to `.alert`, `overflow-x-auto` to `.table`, and explicit dimensions on countdown/skeleton. |
| Use navbar, menu, tabs, breadcrumbs, dock, or pagination | [Navigation Components](navigation-components.md) | Site navigation, wayfinding, and multi-section navigation patterns. Tabs require `aria-label` on radio inputs. Dock is mobile-only — use `lg:hidden`. Pagination is composed from `.join` + `.btn`. |
| Use input, select, textarea, checkbox, toggle, file-input, or validator | [Data Input Components](data-input-components.md) | Form elements: text fields, selections, toggles, form structure, file pickers, floating labels, and CSS-driven validation display. Replace v4's `form-control` with `fieldset`. Use `.validator` only with native HTML validation attributes. |
| Use drawer, hero, divider, join, stack, footer, or mask | [Layout Components](layout-components.md) | Page structure, sidebars, overlays, and content arrangement patterns. Use `lg:drawer-open` + `lg:hidden` for responsive sidebar. `.mask` clips visually but leaves box model unchanged. |
| Use browser, code, phone, or window mockup frames | [Mockup Components](mockup-components.md) | Decorative device and UI frames for documentation, marketing, and onboarding screens where the UI itself is the content being shown. Always add `border border-base-300` — without it the frame has no visible edge. |
| Show loading spinners, progress bars, or skeleton placeholders | [Feedback Components](feedback-components.md) | Communicating async operation states: loading spinners, linear progress bars, skeleton placeholders, and radial progress indicators. Always add `aria-label` and `role='status'` to `.loading`. |
| Extend or override DaisyUI components or know when to go custom | [Customization Patterns](customization-patterns.md) | Extending DaisyUI components with project-specific styles, overriding defaults, and creating custom components. Work through native primitive → composite → custom in order and stop at the first that fits. |
| Use DaisyUI in React with CVA | [DaisyUI and React](daisyui-react.md) | Building React components that use DaisyUI classes, managing variants with CVA, and integrating DaisyUI theming with React patterns. |
| Know best practices and anti-patterns | [Best Practices](best-practices.md) | Code review, architecture decisions, and onboarding guidance for DaisyUI projects. |
| Handle accessibility gaps and ARIA requirements | [Security and Accessibility](security-accessibility.md) | Every component implementation. Accessibility and security are part of shipping correct code, not optional steps. |
| Review sources and version information | [Sources and Maintenance](sources-maintenance.md) |  |
