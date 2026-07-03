---
description: Drupal entities and fields — content types, field development, and entity patterns
guide-meta:
  concepts:
    - content entities
    - bundle entities
    - base fields
    - field types
    - field storage decision order
    - field widgets
    - field formatters
    - view modes
    - entity references
    - entity query
    - computed fields
  not:
    - config entities (see drupal/config-management)
    - Custom Field module (see drupal/custom-field)
    - taxonomy terms (see drupal/taxonomy)
  requires: []
  complements:
    - drupal/config-management
    - drupal/views
    - drupal/forms
    - drupal/render-api
  specializes: ""
  category: drupal
---

# Entities and Fields

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand entity architecture | [Entity Architecture Fundamentals](entity-architecture-fundamentals.md) | When starting any Drupal entity or field development work, you need to understand the two-layer architecture that separates configuration from content and how entity types relate to bundles. |
| Create a content type via config | [Content Type Configuration](content-type-configuration.md) | When creating content types via configuration management (YAML files) for deployment across environments, or when exporting existing content types for version control. |
| Build a custom bundle entity | [Bundle Entity Implementation](bundle-entity-implementation.md) | When building custom content entity types that need bundle support (multiple subtypes with different field configurations), requiring programmatic bundle creation or custom bundle behavior. |
| Add base fields to entities | [Base Field Definitions](base-field-definitions.md) | When adding fields that exist on ALL bundles of an entity type (e.g., title on all nodes, uid on all content), or creating non-configurable fields that store critical entity data. |
| Choose the right field type | [Field Type Selection](field-type-selection.md) | When adding fields to content types or entities, you must choose the appropriate field type that matches your data structure and validation requirements. |
| Decide field storage shape (compound / taxonomy / shared / wrapper) | [Field & Storage Decision Order](field-storage-decision.md) | Decide field-storage SHAPE in priority order: polymorphic -> custom compound field; classification -> taxonomy + entity_reference; shared concern -> concern-named storage; entity-worthy collection -> wrapper entity; else plain core field. |
| Create field storage config | [Field Storage Configuration](field-storage-configuration.md) | When creating fields that can be reused across multiple bundles, defining the technical specifications (data type, cardinality, storage schema) independent of bundle-specific settings. |
| Configure field instances | [Field Instance Configuration](field-instance-configuration.md) | When attaching a field storage to a specific bundle with bundle-specific settings (label, description, required status, default values, widget/formatter settings). |
| Build custom field types | [Custom Field Type Development](custom-field-type-development.md) | When core field types don't meet your data structure needs, requiring custom storage schema, validation, or business logic for a specific data pattern. |
| Develop field widgets | [Field Widget Development](field-widget-development.md) | When creating custom input interfaces for field types in entity forms, requiring specialized UI controls beyond core textfields/selects/checkboxes. |
| Create field formatters | [Field Formatter Development](field-formatter-development.md) | When creating custom display output for field values in view modes, requiring specialized rendering beyond core label/plain text formatters. |
| Configure form displays | [Form Display Configuration](form-display-configuration.md) | When controlling how fields appear in entity edit forms, including widget selection, field order, and visibility across different form modes. |
| Configure view displays | [View Display Configuration](view-display-configuration.md) | When controlling how fields appear in entity view modes (full, teaser, RSS, etc.), including formatter selection, label display, and field visibility. |
| Create custom view modes | [View Mode Development](view-mode-development.md) | When creating custom display contexts beyond default/teaser (e.g., 'card', 'embed', 'json_api'), requiring entity-specific formatter configurations. |
| Work with entity references | [Entity Reference Patterns](entity-reference-patterns.md) | When creating relationships between entities (nodes ↔ taxonomy, nodes ↔ users, nodes ↔ nodes), requiring referential integrity and access-controlled relationships. |
| Handle file/image fields | [File and Image Field Patterns](file-and-image-field-patterns.md) | When handling file uploads (documents, images, media) requiring file validation, storage organization, and derivative generation. |
| Implement computed fields | [Computed Field Patterns](computed-field-patterns.md) | When creating virtual/derived fields that calculate values from other fields without storing data, requiring dynamic values that update when dependencies change. |
| Use entity query API | [Entity Query Patterns](entity-query-patterns.md) | When querying entities by field values, properties, or relationships, requiring performant database queries with access control and cache invalidation. |
| Secure field access | [Field Access Control](field-access-control.md) | When restricting field visibility or editability based on user permissions, entity state, or custom business logic, requiring fine-grained access control beyond entity-level permissions. |
| Optimize entity queries | [Entity Query Performance](entity-query-performance.md) | When optimizing entity queries for large datasets, high-traffic scenarios, or complex filtering requirements, requiring careful query construction and caching. |
| Validate field data | [Field Validation Patterns](field-validation-patterns.md) | When enforcing data integrity constraints on field values, requiring validation beyond basic required/max_length checks, ensuring data quality and business rule compliance. |
