---
description: Drupal UI Patterns 2.x guides — SDC plugin architecture, props/slots/source systems, Layout Builder, Views, field formatters, blocks, pattern library, custom source plugins
tracks:
  - project: ui_patterns
    channel: stable
    declared: "2.0.19"
    verified: 2026-08-16
guide-meta:
  concepts:
    - story.yml
    - UI Patterns 2.x
    - prop definitions
    - slots
    - source plugins
    - component mapping
    - pattern library
  not:
    - storybook
    - stories.yml
    - Storybook.js
    - component preview
  requires:
    - drupal/sdc
  complements:
    - drupal/twig
    - drupal/blocks
    - drupal/layout-builder
    - drupal/views
  specializes: ""
  category: drupal
---

# UI Patterns 2.x

Bridges SDC components to Drupal's site-builder UI via a plugin architecture — covering props, slots, source plugins, Layout Builder, Views, field formatters, blocks, and the pattern library.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide whether to use UI Patterns vs SDC alone | [Overview & Decision](overview-and-decision.md) | UI Patterns 2.x overview — when to use SDC plugins vs standalone SDC |
| Understand the plugin system and rendering pipeline | [Architecture](architecture.md) | UI Patterns plugin system — managers, services, and rendering pipeline |
| Define a component with props and slots | [Defining Components](defining-components.md) | Component definition structure — YAML keys, JSON Schema props, and required fields |
| Know what prop types are available and how typing works | [Props System](props-system.md) | Prop types — built-in types, JSON Schema compatibility, and normalize/preprocess pipeline |
| Understand how slots work and support multiple sources | [Slots System](slots-system.md) | Slots — renderables, multiple sources, and normalization for component placeholders |
| Map Drupal data (fields, menus, blocks) to component props/slots | [Source Plugins](source-plugins.md) | Source plugins bridge Drupal data (entity fields, menus, user input) to component props/slots. Three categories — widgets (direct input), API sources (Drupal data), and context switchers (entity_field, entity_reference) that unlock sibling-field sources via a mandatory 3-level colon-keyed YAML nesting. |
| Add visual variants to a component | [Variants](variants.md) | Variants are declared in component YAML and auto-converted to a string enum prop named variant. For per-instance variants in Layout Builder, use either an entity field (Option 1 — same variant everywhere the block is placed) or a block template reading configuration.{prop} (Option 2 — different variant per placement, requires Plus Suite BlockPropertiesEvent). |
| Understand how UI Patterns relates to Drupal core SDC | [SDC Integration](sdc-integration.md) | SDC integration — how UI Patterns decorates, extends, and maintains SDC compatibility |
| Use components as Layout Builder sections | [Layout Builder Integration](layout-builder-integration.md) | Layout Builder integration — exposing components as layout plugins with slot regions |
| Use components as Views row/style plugins | [Views Integration](views-integration.md) | Views integration — row and style plugins for rendering Views results as components |
| Display fields using component formatters | [Field Formatters](field-formatters.md) | Two formatters — ui_patterns_component (multi-value) and ui_patterns_component_per_item (per-item). Per-item scopes sources to the trigger field only; reach sibling fields via entity_field context switcher. field_property source IDs are field_property:{entity_type}:{field_name}:{column} — no bundle segment. For 5+ slots reading different fields, Twig include() is often cleaner. |
| Expose components as block plugins | [Blocks Integration](blocks-integration.md) | Blocks integration — exposing components as block plugins and embedding blocks in slots |
| Browse and preview components in a library | [Pattern Library](pattern-library.md) | Pattern Library — browsable component preview with stories |
| Write a custom source plugin | [Creating Custom Source Plugins](creating-custom-source-plugins.md) | Creating custom source plugins — widgets, API sources, and derivers |
| Follow best practices and avoid anti-patterns | [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md) | Best practices and anti-patterns — component naming, slot vs prop decisions, and when NOT to use UI Patterns |
| Handle security and accessibility correctly | [Security & Accessibility](security-and-accessibility.md) | Security and accessibility — XSS protection, sanitization, and a11y considerations |
| Export and review config YAML for components, layouts, blocks | [Config Export Reference](config-export-reference.md) | When you need to understand, construct, or debug UI Patterns configuration YAML for deployment, recipes, config management, or programmatic setup. This section documents the core schema that all four integrations share and provides a… |
| Check source references and maintenance notes | [Sources & Maintenance](sources-maintenance.md) |  |
