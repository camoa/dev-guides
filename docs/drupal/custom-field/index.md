---
description: Drupal Custom Field module guides -- compound fields with multiple sub-fields stored in a single table for optimal performance.
guide-meta:
  concepts:
    - Custom Field module
    - compound fields
    - sub-field types
    - custom field widgets
    - custom field formatters
    - entity reference sub-fields
    - single table storage
  not:
    - Paragraphs
    - core field types
    - Field API development (see drupal/entities)
  requires:
    - drupal/entities
  complements:
    - drupal/views
    - drupal/forms
  specializes: ""
  category: drupal
---

# Custom Field

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Custom Field is and when to use it vs Paragraphs/entity references | [Overview](overview.md) | You need to store multiple related values together in a single field without creating entity references or separate content types -- for example, an address with street/city/state/zip, a product with SKU/price/weight/dimensions, or a… |
| Understand the plugin architecture and extensibility | [Architecture](architecture.md) | You need to understand how Custom Field's plugin system works to extend it with custom field types, widgets, or formatters, or to debug plugin discovery issues. |
| Create a custom field using YAML config | [Config-First Creation](config-first-creation.md) | You want to create a compound field through the Drupal UI using configuration, not code -- the recommended approach for site builders and most use cases. |
| Add/remove columns from existing fields with data | [Schema Updates](schema-updates.md) | You need to add, remove, or modify columns in a Custom Field that already has data, without losing existing content. |
| Choose the right column type for my data | [Column Types](column-types.md) | All 27 custom field column types organized by category -- text, numeric, date/time, reference, file, and data fields with schema details and gotchas. |
| Find the right widget for a sub-field | [Widget Plugins](widget-plugins.md) | You need to choose the right widget for collecting data for each sub-field in your custom field. |
| Use stacked vs flexbox layouts for the entire field | [Field-Level Widgets](field-level-widgets.md) | You need to control how the entire custom field (all sub-fields together) is laid out on the edit form. |
| Render custom field data with templates or tables | [Field-Level Formatters](field-level-formatters.md) | You need to control how the entire custom field (all sub-fields together) is displayed on the view. |
| Work with entity reference sub-fields | [Entity References](entity-references.md) | You need to reference entities (taxonomy terms, nodes, users, media) from within a custom field column. |
| Handle file and image uploads | [Files and Images](files-images.md) | You need file uploads or images within a custom field column. |
| Work with dates, times, and ranges | [Date/Time Fields](datetime-fields.md) | Working with date, time, date range, time range, or duration columns in custom fields. |
| Add link fields with Linkit integration | [Link Fields](link-fields.md) | You need full link functionality (URL + title + attributes) within a custom field column. |
| Query custom fields in Views | [Views Integration](views-integration.md) | You need to query, filter, sort, or display custom field data in Views. |
| Use tokens in custom fields | [Token Support](token-support.md) | You need to use custom field values in token replacement contexts (Pathauto, Rules, email templates). |
| Integrate with GraphQL, JSON:API, Search API | [Sub-Modules](sub-modules.md) | You need extended functionality like GraphQL, JSON:API normalization, Entity Browser, Linkit, Media Library, Search API, or AI integration. |
| Create custom field type plugins | [Custom Plugins](custom-plugins.md) | You need to create custom field type, widget, or formatter plugins specific to your application. |
| Import data via Feeds | [Feeds Integration](feeds-integration.md) | You need to import CSV or other data sources into custom field columns via the Feeds module. |
| Understand performance and security best practices | [Best Practices](best-practices.md) | Performance optimization, security hardening, dependency injection, and coding standards for custom field development. |
| Find source code for specific functionality | [Code Reference Map](code-reference-map.md) | You need to find specific source code for custom field functionality. |
