---
description: Drupal-specific DRY (Don't Repeat Yourself) principles - config, services, base classes, traits, plugins, templates, SDC, render arrays, hooks, and more.
tracks: []
guide-meta:
  concepts:
    - Drupal DRY patterns
    - config as single source of truth
    - services for shared logic
    - base classes
    - traits
    - plugin reuse
    - Twig template inheritance
    - SDC component reuse
    - recipes for reusable config
  not:
    - tool-agnostic DRY theory
    - SOLID principles
  requires: []
  complements:
    - drupal/services
    - drupal/sdc
    - drupal/config-management
  category: drupal
---

# DRY Principles in Drupal

Apply DRY (Don't Repeat Yourself) principles to Drupal development. Understand how Drupal's architecture supports code reuse through configuration, services, base classes, traits, plugins, templates, and components.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand DRY in Drupal's architecture | [DRY in Drupal Overview](dry-drupal-overview.md) | When making architectural decisions about code organization in Drupal projects — deciding between configuration vs code, services vs static calls, base classes vs traits, plugins vs custom implementations, or template inheritance vs… |
| Use config as single source of truth | [Config as Single Source of Truth](config-single-source-truth.md) | Whenever you need to store site settings, entity definitions, field configurations, view definitions, or any setting that should be consistent across environments. |
| Extract shared logic into services | [Services for Shared Logic](services-shared-logic.md) | When you have business logic, API integrations, calculations, or data transformations that are used in multiple places (controllers, forms, event subscribers, Drush commands). |
| Extend base classes properly | [Base Classes and Inheritance](base-classes-inheritance.md) | When you have multiple classes of the same type (entities, forms, blocks, controllers) that share common patterns or need to override specific base functionality. |
| Use traits for cross-cutting concerns | [Traits for Cross-Cutting Concerns](traits-cross-cutting.md) | When you need to share functionality across classes that don't share the same inheritance hierarchy, or when you want to compose behaviors without deep inheritance. |
| Reuse plugin patterns | [Plugin Reuse Patterns](plugin-reuse.md) | When you need extensible, discoverable, swappable components (blocks, field types, filters, conditions, actions), or when multiple plugins share common patterns. |
| Leverage Twig template inheritance | [Twig Template Inheritance](twig-template-inheritance.md) | When you need to override theme templates but want to reuse most of the structure, changing only specific sections. |
| Build reusable UI components with SDC | [SDC Component Reuse](sdc-component-reuse.md) | When you need reusable UI components (buttons, cards, modals, forms) used across multiple pages, content types, or blocks. SDCs (Single Directory Components) are Drupal's native component system (core since 10.3). |
| Create reusable render patterns | [Render Array Patterns](render-array-patterns.md) | When you need consistent rendering patterns across multiple controllers, blocks, or preprocess functions. Render arrays are Drupal's structured way to describe renderable content. |
| Share hook and event logic | [Hook and Event Reuse](hook-event-reuse.md) | When you need to respond to system events (entity operations, form alterations, request processing) without duplicating logic across similar hooks or event subscribers. |
| DRY across environments | [Config Split and Environments](config-split-environments.md) | When you need different configuration across environments (dev modules in dev only, production API keys in prod only) without duplicating config or managing it manually. |
| Use recipes for config distribution | [Recipes for Reusable Config](recipes-reusable-config.md) | When you want to package and distribute reusable configuration setups (content types, fields, views, modules) across multiple Drupal sites or projects. Recipes are Drupal 11's successor to installation profiles and features. |
| Reuse logic in CLI and web contexts | [Drush and CLI Reuse](drush-cli-reuse.md) | When you need to perform operations via command line (cron, batch processing, deployments) and want to reuse the same business logic that exists in web controllers/forms. |
| Avoid common over-DRY mistakes | [Over-DRY Anti-Patterns](over-dry-anti-patterns.md) | When deciding whether to abstract or duplicate. Over-DRY is worse than under-DRY because wrong abstractions are harder to remove than duplication. |
| Get a decision framework | [Best Practices Decision Framework](best-practices-decision-framework.md) | When making any decision about abstracting, reusing, or duplicating code in Drupal. |
| Find reference code examples | [Code Reference Map](code-reference-map.md) |  |
