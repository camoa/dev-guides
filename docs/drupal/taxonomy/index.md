---
description: Drupal Taxonomy — vocabulary and term management, config-first development
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-14
guide-meta:
  concepts:
    - taxonomy vocabulary
    - taxonomy terms
    - term reference fields
    - hierarchical taxonomy
    - taxonomy permissions
    - term storage querying
  not:
    - content entities (see drupal/entities)
    - Views filters (see drupal/views)
  requires:
    - drupal/entities
  complements:
    - drupal/views
    - drupal/config-management
  category: drupal
---

# Taxonomy

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand when to use taxonomy vs other content organization | [Taxonomy System Overview](taxonomy-overview.md) | Use taxonomy when you need to categorize, tag, or organize content with reusable terms. Use list fields when you have a fixed list of options specific to one content type. |
| Create a vocabulary via YAML config | [Vocabulary Configuration Schema](vocabulary-config-schema.md) | Use this schema when creating or modifying vocabulary YAML config files. These are the complete properties for `taxonomy.vocabulary.*.yml`. |
| Deploy vocabularies via config management | [Creating Vocabularies via Config](creating-vocabularies-config.md) | Use config-first approach for vocabularies to ensure consistent structure across environments. Create YAML files for module installation or config sync. |
| Add a taxonomy term reference field to content | [Term Reference Field Configuration](term-reference-config.md) | Use this workflow to add taxonomy term reference fields to content types, users, or other entities using the config-first approach. |
| Decide between flat or hierarchical taxonomy | [Hierarchical Taxonomy](hierarchical-taxonomy.md) | Use flat taxonomy for simple tagging (blog tags, keywords). Use hierarchical taxonomy for categorization with subcategories (Geography: Country > State > City). |
| Create and manage terms via UI or code | [Term Management](term-management.md) | Use UI for manual term creation. Use Drush or code for bulk operations or programmatic term management. |
| Build Views with taxonomy filters | [Taxonomy Views Integration](taxonomy-views.md) | Use taxonomy Views plugins when building Views that filter, sort, or display content by taxonomy terms. |
| Set up per-vocabulary permissions | [Taxonomy Permissions & Access](taxonomy-permissions.md) | Use per-vocabulary permissions for granular term CRUD control. Grant `administer taxonomy` only to trusted site administrators. |
| Query terms programmatically | [Term Storage & Querying](term-storage-querying.md) | Use TermStorage specialized methods for hierarchy operations. Use entity queries for standard term lookups. |
| Create terms programmatically | [Programmatic Term Operations](programmatic-terms.md) | Use programmatic approach for migrations, imports, install hooks, drush commands. Complements config-first vocabulary management. |
| Configure entity reference widgets/formatters | [Taxonomy with Entity Reference](entity-reference-taxonomy.md) | Use this guide to configure entity reference field widgets and formatters for taxonomy term fields. Widget choice affects UX and term creation workflow. |
| Export taxonomy config or create recipes | [Config Export & Recipes](taxonomy-config-recipes.md) | Use this guide when packaging taxonomy vocabulary config for reuse, distribution via modules, or deployment via recipes. |
| Follow taxonomy best practices | [Best Practices & Patterns](best-practices.md) | Use these guidelines when planning taxonomy architecture, naming conventions, and maintenance strategies. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns.md) | Use this guide when reviewing taxonomy implementations to identify and fix problematic patterns. |
| Optimize security and performance | [Security & Performance](security-performance.md) | Use this guide when hardening taxonomy implementations against security vulnerabilities and optimizing for large-scale performance. |
| Find key classes and files | [Code Reference Map](code-reference-map.md) |  |
