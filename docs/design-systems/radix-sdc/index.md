---
description: Design System to Radix SDC Mapping — atomic guides for implementing design systems with Drupal Radix and Single Directory Components
tracks:
  - project: radix
    channel: stable
    declared: "6.x"
    verified: 2026-02-13
  - project: bootstrap
    registry: npm
    channel: stable
    declared: "5"
    verified: 2026-02-13
guide-meta:
  concepts:
    - Radix sub-theme
    - design tokens to Radix
    - atoms SDC
    - molecules SDC
    - organisms SDC
    - Layout Builder integration
    - Laravel Mix
    - Radix CLI
    - SDC YAML schema
  not:
    - Bootstrap mapping theory
    - DaisyUI components
    - Tailwind CSS
  requires:
    - drupal/sdc
    - design-systems/bootstrap
  complements:
    - design-systems/radix-components
    - design-systems/recognition
    - drupal/layout-builder
  specializes: ""
  category: design-systems
---

# Design System to Radix SDC Mapping

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Radix sub-theme folder structure | [Radix Sub-Theme Architecture](radix-sub-theme-architecture.md) | You're setting up a new Radix sub-theme You need to understand how Radix organizes files and loads Bootstrap You're mapping design system files to Radix file structure |
| Map design tokens to Bootstrap variables in Radix | [Design Tokens Configuration](design-tokens-radix-configuration.md) | You've identified design tokens using the Design System Recognition Guide You've mapped tokens to Bootstrap variables using the Bootstrap Mapping Guide You need to know WHERE to put variable overrides in Radix |
| Create atom SDC components | [Atoms SDC Components](atoms-sdc-components.md) | You've identified atoms using the Design System Recognition Guide You need to decide when to create an atom SDC vs use Bootstrap classes You're creating foundational UI components |
| Master SDC component best practices | [SDC Component Best Practices](sdc-component-best-practices.md) | You're deciding component granularity (too small vs too large) You need guidance on props vs slots architecture You're questioning whether a Bootstrap class is sufficient vs creating an SDC You want senior themer guidance on component… |
| Decide when to override vs extend Radix components | [Radix Sub-Theme Best Practices](radix-sub-theme-best-practices.md) | You're setting up a new Radix sub-theme You need to understand override strategy (when to override vs extend vs create) You're managing SCSS variables and compilation You want guidance on starterkit usage and library management |
| Configure build tools (Laravel Mix, PurgeCSS) | [Build Tools and Compilation](build-tools-compilation.md) | You're setting up build tools for a new Radix sub-theme You need to configure Laravel Mix for SCSS/JS compilation You want to optimize production builds with PurgeCSS You're setting up live reload with BrowserSync |
| Use Radix CLI for component creation | [Radix CLI Integration](radix-cli-integration.md) | You're creating new SDC components using Radix CLI You want to import existing Radix components into your sub-theme You need consistent component structure and Bootstrap integration |
| Compose atoms into molecule SDCs | [Molecules SDC Components](molecules-sdc-components.md) | You've identified molecules using the Design System Recognition Guide You need to compose multiple atoms into a reusable molecule You're implementing composite patterns like search bars, card content, form fields |
| Build organism SDCs with Layout Builder | [Organisms SDC Layout Builder](organisms-sdc-layout-builder.md) | You've identified organisms using the Design System Recognition Guide You're building complex sections like navbars, heroes, card grids You need to integrate organisms with Layout Builder |
| Override page templates in Radix | [Templates Drupal Theme Layer](templates-drupal-theme-layer.md) | You're implementing page-level layouts (templates) You need to override Drupal's default page structure You're composing organisms into complete pages |
| Master Layout Builder patterns and decisions | [Layout Builder Best Practices](layout-builder-best-practices.md) | You're deciding between Layout Builder, Paragraphs, or page templates You need guidance on when Layout Builder makes sense vs traditional theming You're implementing Layout Builder with SDC components You want to balance editorial… |
| Optimize theme performance (caching, assets, images) | [Performance Best Practices](performance-best-practices.md) | You're optimizing theme performance You need guidance on caching strategies You're implementing responsive images and modern formats You want to optimize asset loading |
| Write SDC YAML schema, props, and slots | [SDC Component Development](sdc-component-development.md) | You're creating new SDC components from scratch You need to define component props, slots, and schemas You're adding JavaScript to components |
| Master Twig and preprocess patterns | [Twig and Preprocess Best Practices](twig-and-preprocess-best-practices.md) | You're deciding whether logic belongs in Twig or preprocess function You need guidance on Twig template inheritance (extend vs include vs embed) You're working with the Drupal attributes object You want performance best practices for Twig… |
| Catalog and reuse existing Radix components | [Radix Component Reuse Strategy](radix-component-reuse-strategy.md) | You're evaluating whether to reuse, override, or create components You need a catalog of existing Radix SDC components You want to extend Radix components in your sub-theme |
| Troubleshoot SDC component issues | [Troubleshooting SDC Components](troubleshooting-sdc-components.md) | Your SDC component isn't being discovered by Drupal Bootstrap classes aren't being applied correctly in your component You need to debug component registration or rendering issues You've replaced/overridden a Radix component and it's not… |
