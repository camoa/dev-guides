---
description: Drupal Recipes — reusable configuration patterns for composable site setup
guide-meta:
  concepts:
    - Drupal recipes
    - recipe.yml
    - config actions
    - recipe composition
    - recipe inputs
    - default content
    - extension installation
    - core recipes catalog
  not:
    - Config Split (see drupal/config-management)
    - install profiles
  requires:
    - drupal/config-management
  complements:
    - drupal/config-management
    - drupal/entities
  specializes: ""
  category: drupal
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-14
---

# Drupal Recipes

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what recipes replace | [Recipe System Overview](recipe-system-overview.md) | Use Drupal Recipes (core since 10.3.0, May 2024) when you need shareable, tested configuration patterns that can be applied to any Drupal site. Use distributions for full site builds, config split for environment-specific config. |
| Create my first recipe | [Creating Your First Recipe](creating-first-recipe.md) | Follow this workflow to create a minimal working recipe from scratch. |
| Understand recipe.yml structure | [Recipe YAML Schema](recipe-yaml-schema.md) | Every recipe requires a `recipe.yml` file defining metadata, dependencies, extensions, configuration, inputs, and content. |
| Compose multiple recipes | [Recipe Composition & Dependencies](recipe-composition.md) | Use recipe composition when you need to build complex functionality from granular, reusable recipe building blocks. |
| Install modules/themes | [Extension Installation](extension-installation.md) | Use the `install:` key to declare modules and themes that your recipe requires. |
| Import configuration | [Config Import & Strict Mode](config-import-strict.md) | Use `config.import` to specify config files to copy from extensions. Use `config.strict` to control validation of existing config. |
| Update simple config | [Config Actions - Universal](config-actions-universal.md) | Use universal config actions when you need to update simple config or config entities without entity-type-specific methods. |
| Grant permissions or configure entities | [Config Actions - Entity-Specific](config-actions-entity-specific.md) | Use entity-specific config actions when you need to configure roles, text formats, displays, workflows, or other specialized entity types. |
| Chain config actions | [Config Actions - Advanced Patterns](config-actions-advanced.md) | Use advanced config action patterns when you need wildcards for bulk operations, optional config handling, chaining multiple actions, or input substitution. |
| Define user inputs | [Input System - Defining Inputs](input-defining.md) | Use inputs when you need to externalize site-specific data that varies per environment, making recipes portable and reusable. |
| Set default input values | [Input System - Default Sources](input-default-sources.md) | Use default sources to provide fallback values when inputs aren't explicitly collected from users. |
| Collect input from users | [Input Collection & Forms](input-collection-forms.md) | Use input collection when you need to gather user-provided values interactively before applying a recipe. |
| Decide between default content and migration | [Default Content - Overview](default-content-overview.md) | Use default content when you need demo or starter content bundled with your recipe. For ongoing content staging, use Workspaces or Migrate API. |
| Export content | [Default Content - Exporting](default-content-exporting.md) | Use content export when you need to bundle existing content entities with a recipe for demo or starter content. |
| Import content | [Default Content - Importing](default-content-importing.md) | Recipes automatically import default content from the `content/` directory during recipe application via RecipeRunner. |
| Publish a recipe | [Composer Integration & Publishing](composer-integration.md) | Use Composer packaging when you need to distribute recipes with version management and dependency resolution. |
| Use recipe tooling | [Recipe Tooling](recipe-tooling.md) | Use recipe tooling when you need to apply recipes, export content, or integrate recipes into custom workflows. |
| Browse core recipes | [Core Recipes Catalog](core-recipes-catalog.md) | Browse core recipes when you need reusable building blocks or want to learn recipe patterns from tested examples. |
| Follow best practices | [Best Practices & Patterns](best-practices-patterns.md) | Apply these practices when creating recipes to ensure maintainability, reusability, and testability. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-mistakes.md) | Avoid these anti-patterns when creating recipes to prevent brittle, untestable, or unmaintainable code. |
| Ensure security and performance | [Security & Performance](security-performance.md) | Apply security and performance best practices when creating recipes to ensure safe and efficient recipe application. |
| Find recipe classes | [Code Reference Map](code-reference-map.md) |  |
