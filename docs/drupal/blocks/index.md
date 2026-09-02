---
description: Drupal Blocks — block plugins, derivatives, contexts, Layout Builder, render pipeline
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-19
guide-meta:
  concepts:
    - block plugin
    - BlockBase
    - block_content
    - block derivatives
    - block contexts
    - block placement
  not:
    - inline blocks
    - layout sections
    - Layout Builder styles
  requires: []
  complements:
    - drupal/layout-builder
    - drupal/render-api
    - drupal/plugins
  category: drupal
---

# Drupal Blocks

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the 4-layer block architecture | [Block System Architecture](block-system-architecture.md) | Understand the 4 layers before starting any block development. Use this to orient yourself when deciding which layer to work with. |
| Decide between block plugin, content block, or inline block | [Block Type Decision Matrix](block-type-decision.md) | Use block plugins when you need logic, DI, or dynamic content. Use content blocks when editors need to manage content without code changes. |
| Create a custom block plugin with code | [Creating Block Plugins](creating-block-plugins.md) | Use a block plugin when you need programmatic logic, external data, or service integration. Use content blocks when editors need to manage content without code changes. |
| Add configuration options to my block | [Block Configuration Forms](block-configuration.md) | Use when your block plugin needs configurable settings that site builders can set per block instance. Use content block fields instead when editors (not devs) need to manage the values. |
| Control who can see my block | [Block Access Control](block-access-control.md) | Use `blockAccess()` for programmatic access control tied to code logic. Use Visibility Conditions for UI-configurable per-placement access (pages, roles, content type). |
| Implement proper caching for performance | [Block Caching Strategies](block-caching.md) | Ensure blocks are cached properly for performance while varying by necessary contexts and invalidating when data changes. Wrong caching = slow site or incorrect content shown to users. |
| Create custom block types with fields | [Custom Block Types](custom-block-types.md) | Use custom block types when content editors need to manage block content with custom fields without code changes. Use block plugins instead for logic-driven or dynamic content. |
| Work with content block entities | [Content Block Entities](content-blocks.md) | Use when working programmatically with instances of block content (content entities created from block types). Distinct from Block config entities — `BlockContent` is the content; `Block` is the placement. |
| Place and configure blocks via UI or code | [Block Placement & Configuration](block-placement.md) | Use when controlling where blocks appear (regions, themes) and their configuration (weight, visibility, settings). Block config entities are the placement layer — distinct from the block plugin itself. |
| Use or create visibility conditions | [Visibility Conditions](visibility-conditions.md) | Use visibility conditions for UI-configurable placement rules (pages, roles, node type). Use `blockAccess()` for programmatic logic that can't be expressed in conditions. |
| Theme and render blocks | [Block Rendering & Theming](block-rendering.md) | Use block templates for markup changes, preprocessing for adding template variables, and alter hooks to modify render arrays across blocks. Keep logic out of templates. |
| Programmatically load, create, or place blocks | [Programmatic Block Operations](programmatic-operations.md) | Use in update hooks, migrations, or automated tasks when you need to load, create, modify, or place blocks via code rather than the UI. |
| Use Layout Builder inline blocks or field blocks | [Layout Builder Integration](layout-builder-blocks.md) | Use Layout Builder blocks when placing content within layouts. Use inline blocks for one-off content, field blocks to display entity fields, and extra field blocks for pseudo-fields. |
| Find what core block plugins are available | [Core Block Plugins Reference](core-block-plugins.md) | Check here before creating a custom block. Many common needs (menus, branding, login, search, views) are covered by core plugins. |
| Inject services into my block plugin | [Dependency Injection in Blocks](dependency-injection.md) | Use when your block plugin needs access to Drupal services (database, config, entity manager, custom services). Always prefer DI over static `\Drupal::service()` calls. |
| React to block events or alter block output | [Block Hooks & Events](block-events-hooks.md) | Use alter hooks to modify block render arrays or access across all blocks or specific plugins. Use preprocess for adding template variables. |
| Export block config or use in recipes | [Config Management & Recipes](config-recipes.md) | Use when exporting block configuration for deployment, syncing between environments, or using `placeBlock` recipe actions (Drupal 11.1+). Block plugins have no exportable config — only Block config entities do. |
| Use SDC components or UI Patterns as blocks | [SDC Component Blocks](sdc-component-blocks.md) | Use when exposing Twig SDC components as placeable blocks. Component Block module handles zero-PHP cases. |
| Follow best practices and patterns | [Best Practices](best-practices.md) | Apply these patterns when building any block plugin. These are the architectural decisions that keep blocks maintainable, testable, and performant. |
| Avoid common mistakes and anti-patterns | [Anti-Patterns & Common Mistakes](anti-patterns.md) | Avoid common pitfalls that lead to bugs, performance issues, or maintenance problems when building block plugins. |
| Ensure security and performance | [Security & Performance](security-performance.md) | Apply these patterns when blocks handle user input, load entities, or call external APIs. Security issues in blocks affect every page they appear on. |
| Find key classes and interfaces | [Code Reference Map](code-reference-map.md) | Quick lookup of key classes, interfaces, and services in Drupal's block system when building or debugging block code. |
| Check source references and maintenance notes | [Sources & Maintenance](sources-maintenance.md) |  |
