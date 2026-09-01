---
description: "Drupal Configuration Management — the Config API, simple config vs config entities, schema, storage, synchronization, overrides, Config Split, dependencies, and deployment workflows."
tracks:
  - project: config_split
    channel: stable
    declared: "2.0.2"
    verified: 2026-08-17
guide-meta:
  concepts:
    - Config API
    - simple config
    - config entities
    - config schema
    - Config Split
    - config synchronization
    - config override system
    - config dependencies
    - config deployment
  not:
    - content entities (see drupal/entities)
    - ConfigFormBase (see drupal/config-forms)
  requires: []
  complements:
    - drupal/recipes
    - drupal/config-forms
    - drupal/entities
  category: drupal
---

# Drupal Configuration Management

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand config system architecture | [Config System Overview](config-system-overview.md) | When you need to understand Drupal's configuration management architecture — how config data is structured, stored, validated, synchronized, and overridden. |
| Choose between simple config vs config entity | [Simple Config vs Config Entities](simple-config-vs-config-entities.md) | When deciding whether to implement config as simple config (singleton YAML) or config entities (multiple instances, CRUD, UI). |
| Define config schema YAML | [Config Schema YAML](config-schema-yaml.md) | When defining the structure and data types for your module's configuration so Drupal can validate, cast, and translate config values. |
| Use core data types in schema | [Core Data Types Schema](core-data-types-schema.md) | When writing config schema and you need to know which core data types are available for scalars (string, integer, boolean), containers (mapping, sequence), and specialized types (email, uri, label). |
| Write config schema for my module | [Writing Config Schema](writing-config-schema.md) | When creating a new module with config (simple or entity) and you need to define schema so Drupal validates and casts config values correctly. |
| Read config in code | [Config Factory & Reading Config](config-factory-and-reading-config.md) | When you need to read configuration values in custom code — forms, controllers, services, hooks. |
| Create config entities | [Config Entities](config-entities.md) | When you need to create user-manageable lists of configuration items (like views, image styles, vocabularies) with CRUD operations, dependencies, and admin UI. |
| Define config entity schema | [Config Entity Schema Definition](config-entity-schema-definition.md) | When defining config schema for config entities — schema must match exported YAML structure and include all entity keys. |
| Choose storage backend | [Config Storage](config-storage.md) | When you need to understand how Drupal stores configuration data — active storage (database), sync storage (filesystem), and custom storage backends. |
| Sync config between environments | [Config Synchronization](config-synchronization.md) | When you need to sync configuration between environments — export config from dev, commit to Git, import to staging/production. |
| Export/import with Drush | [Config Import/Export](config-import-export.md) | When you need to export config from active storage to sync directory, or import config from sync directory to active storage using Drush commands. |
| Override config per environment | [Config Override System](config-override-system.md) | When you need to override config values per environment (e.g., API keys, site name) without modifying stored config or committing credentials to Git. |
| Split config by environment | [Config Split](config-split.md) | When you need to manage environment-specific configuration (dev modules, production settings) that should not be deployed to all environments. Config Split 2.0.2 is the current stable release; install with composer require drupal/config_split:^2.0. |
| Understand config dependencies | [Config Dependencies](config-dependencies.md) | When you need to understand how Drupal tracks which modules, themes, and config entities depend on each other, and how dependencies affect import order and deletion. |
| React to config changes | [Config Events](config-events.md) | When you need to react to config changes — save, delete, import, rename — via event subscribers. |
| Handle module install config | [Config Installer](config-installer.md) | When your module needs to provide default configuration that's installed when the module is enabled — content types, views, fields, module settings. |
| Deploy config safely | [Deployment Workflows](deployment-workflows.md) | When deploying configuration changes from development to staging to production, ensuring safe, repeatable, rollback-capable deployments. |
| Use config with Recipes | [Config & Recipes Integration](config-and-recipes-integration.md) | When you need to distribute reusable configuration bundles (Recipes) that install modules, config, and content together as a single unit for features or starter kits. |
| Follow best practices | [Best Practices & Patterns](best-practices-and-patterns.md) | When you need guidance on config management patterns, architecture decisions, and proven approaches for maintainable config workflows. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md) | When you need to identify and fix common config management mistakes — patterns that break deployment, cause data loss, or create security issues. |
| Secure config & optimize performance | [Security & Performance](security-and-performance.md) | When you need to secure configuration data, prevent vulnerabilities, and optimize config access for performance. |
| Find code references | [Code Reference Map](code-reference-map.md) |  |
