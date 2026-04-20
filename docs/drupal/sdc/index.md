---
description: Single Directory Components (SDC) — component architecture, development patterns, and best practices
guide-meta:
  concepts:
    - "*.component.yml"
    - single directory components
    - SDC
    - component schema
    - Twig components
    - component libraries
  not:
    - UI Patterns
    - story.yml
    - source plugins
    - Storybook.js
  requires: []
  complements:
    - drupal/ui-patterns
    - drupal/twig
    - drupal/storybook
  specializes: ""
  category: drupal
---

# Single Directory Components (SDC)

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand SDC architecture and plugin system | [SDC Architecture](sdc-architecture.md) | Use this when you need to understand how Drupal discovers and loads components, debug component registration issues, or plan component organization across modules/themes. |
| Know component file structure and naming | [Component File Structure](component-file-structure.md) | Use this when creating a new component, debugging "component not found" errors, or understanding automatic asset loading. |
| Define component YAML schema properly | [Component YAML Schema](component-yaml-schema.md) | Use this when defining component metadata, specifying props and slots, or configuring library dependencies. |
| Write Twig templates for SDCs | [Twig Templates in SDCs](twig-templates-in-sdcs.md) | Use this when writing component Twig templates, accessing props and slots, or working with the `attributes` object. |
| Add SCSS/CSS to components with proper scoping | [SCSS/CSS in SDCs](scss-css-in-sdcs.md) | Use this when adding styles to components, ensuring proper CSS scoping, or importing Bootstrap variables in Radix sub-themes. |
| Add JavaScript with Drupal.behaviors | [JavaScript in SDCs](javascript-in-sdcs.md) | Use this when adding interactive behavior to components, implementing Drupal.behaviors pattern, or integrating with `once()` or other Drupal JS APIs. |
| Compose components (include/embed/render) | [Component Composition](component-composition.md) | Use this when including one component in another, deciding between `include()`, `embed`, or render arrays, or nesting components. |
| Decide between props and slots | [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md) | Use this when designing a component API, deciding if something should be a prop or slot, or debugging schema validation errors. |
| Create component variants (enum vs separate) | [Component Variants](component-variants.md) | Use this when you need multiple visual variations of a component, deciding between prop-based variants vs separate components, or implementing the new variants API (Drupal 11.1+). |
| Replace Drupal templates with SDCs | [Replacing Templates with SDCs](replacing-templates-with-sdcs.md) | Use this when migrating existing Twig templates to SDC, overriding contrib module/theme components, or implementing field formatters with components. |
| Test SDCs (Storybook, visual regression) | [Testing SDCs](testing-sdcs.md) | Use this when setting up component development workflow, testing components in isolation, or implementing visual regression testing. |
| Optimize performance (libraries, caching) | [Performance](performance.md) | Use this when optimizing component loading, debugging slow page loads with many components, or implementing caching strategies. |
| Prevent XSS and security issues | [Security](security.md) | Use this when handling user-generated content in components, passing data from untrusted sources, or working with attributes and HTML markup. |
| Avoid anti-patterns and code review issues | [Anti-Patterns](anti-patterns.md) | Use this when code reviewing component implementations, debugging component issues, or establishing component development standards. |
| Integrate SDC with UI Patterns 2.x | [UI Patterns 2 Integration](ui-patterns-2-integration.md) | Use this when building SDCs that will be exposed to site builders via UI Patterns, making components available as blocks/layouts/views without custom PHP, or understanding how `component.yml` maps to UI Patterns discovery. |
