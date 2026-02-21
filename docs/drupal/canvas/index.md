---
description: Drupal Canvas — decision guides for the React-based visual page builder using SDC and Code Components on Drupal 11.2+.
---

# Drupal Canvas

Atomic decision guides for building with Drupal Canvas — the first-party visual page builder for Drupal 11.2+. Covers architecture decisions, SDC component authoring, Code Component (React/Preact) development, CLI tooling, theming, Storybook, AI assistant, decoupled patterns, and security.

- [Canvas Overview](canvas-overview.md) — What Canvas is, when to use it, and how it differs from standard Drupal content types
- [Component Types Decision](component-types-decision.md) — Choose between SDC (Twig), Code Component (React), or External JS Component
- [SDC Component Format](sdc-component-format.md) — File structure, YAML schema, and Twig template patterns for Canvas SDC components
- [SDC Props Reference](sdc-props-reference.md) — All prop types with YAML syntax, Canvas editor widgets, and gotchas
- [SDC Slots](sdc-slots.md) — When and how to define drop zones for nested Canvas component composition
- [SDC Image Handling](sdc-image-handling.md) — Render image props correctly using the `canvas:image` built-in component
- [Code Component Format](code-component-format.md) — JSX structure, component.yml schema, and allowed package imports for Code Components
- [Canvas NPM Tools](canvas-npm-tools.md) — Reference for `@drupal-canvas/cli`, `@drupal-canvas/create`, and related packages
- [Canvas CLI Workflow](canvas-cli.md) — Local Code Component development — scaffold, build, push, and pull
- [Acquia Nebula](acquia-nebula.md) — The official Canvas Code Component development template with Storybook and AI skills preconfigured
- [Design Tokens and Theming](design-tokens-and-theming.md) — How Canvas handles CSS custom properties, Tailwind `@theme`, and SDC/Code Component styling
- [Storybook Integration](storybook-integration.md) — Story formats and setup for Code Component and SDC component development
- [Canvas AI Assistant](canvas-ai-assistant.md) — `canvas_ai` submodule setup and how component metadata affects AI page building
- [Decoupled Frontend Patterns](decoupled-frontend-patterns.md) — Canvas with Next.js, Astro, Nuxt — component tree API, CLI sync, canvas_extjs
- [Canvas vs Standard SDC Decision](canvas-vs-standard-sdc-decision.md) — Architectural decision: Canvas page builder vs standard Drupal theming
- [Security Considerations](security-considerations.md) — Known vulnerabilities, access control, and safe Twig/JSX patterns for production
- [Component Creation Workflow](component-creation-workflow.md) — End-to-end steps for creating a new SDC or Code Component from scratch
