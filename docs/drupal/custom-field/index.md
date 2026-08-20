---
description: "Drupal Custom Field module guides -- compound fields with multiple sub-fields stored in a single table for optimal performance."
tracks:
  - project: custom_field
    channel: stable
    declared: "5.0.2"
    verified: 2026-08-20
guide-meta:
  concepts:
    - Custom Field module
    - compound fields
    - sub-field types
    - custom field widgets
    - custom field formatters
    - entity reference sub-fields
    - single table storage
    - SDC prop widgets
    - select_or_other widget
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
| Understand what Custom Field is and when to use it vs Paragraphs/entity references | [Overview](overview.md) | Use Custom Field to store 3-10 related values in one table row instead of creating entity references or Paragraphs; a compound column can even hold an entity_reference sub-field, so "needs a reference" alone doesn't force a wrapper entity. |
| Understand the plugin architecture and extensibility | [Architecture](architecture.md) | Custom Field discovers types/widgets/formatters/feeds/link-attributes/prop-widget plugins through six services under custom_field.services.yml; formatter plugins use core's #[FieldFormatter] attribute, not a custom_field one. |
| Create a custom field using YAML config | [Config-First Creation](config-first-creation.md) | Create a custom field via Structure > Manage fields, define sub-field columns before any data exists (column types lock once data is present), then configure widgets/formatters per sub-field. |
| Add/remove columns from existing fields with data | [Schema Updates](schema-updates.md) | Use addColumn()/removeColumn() on custom_field.update_manager inside a hook_update_N() to change existing custom-field columns without data loss -- there is no updateFieldSchema(), and 5.x adds a one-time taxonomy-index backfill post-update. |
| Choose the right column type for my data | [Column Types](column-types.md) | All 23 custom field column types organized by category -- text, numeric, date/time, reference, file, and data fields with schema details and gotchas. |
| Find the right widget for a sub-field | [Widget Plugins](widget-plugins.md) | 37 widget plugins map to 23 custom field column types, each with a documented default; only override the default when UX calls for it (e.g., select/radios instead of autocomplete for small reference sets, or select_or_other for a constrained-but-extensible list). |
| Use stacked vs flexbox layouts for the entire field | [Field-Level Widgets](field-level-widgets.md) | You need to control how the entire custom field (all sub-fields together) is laid out on the edit form. CustomFlexWidget uses the module's own 12-column CSS grid, not Bootstrap -- works in any theme. |
| Render custom field data with templates or tables | [Field-Level Formatters](field-level-formatters.md) | You need to control how the entire custom field (all sub-fields together) is displayed on the view. Plugin IDs are short (custom_inline, not custom_inline_formatter) -- only custom_formatter carries the _formatter suffix. |
| Work with entity reference sub-fields | [Entity References](entity-references.md) | Pick EntityReferenceAutocompleteWidget for large reference sets and select/radios widgets for small ones; entity reference sub-fields never auto-check access, so validate in the widget and check in the formatter. |
| Handle file and image uploads | [Files and Images](files-images.md) | Use file type + FileWidget for plain uploads and image type + ImageWidget for accessible images with auto-populated alt/title/width/height; always check the loaded file entity is not NULL before rendering. |
| Work with dates, times, and ranges | [Date/Time Fields](datetime-fields.md) | Match the widget to the exact sub-type (datetime vs date-only vs time-of-day vs range); daterange/time_range auto-calculate duration on save and time_range has no cross-midnight support. |
| Add link fields with Linkit integration | [Link Fields](link-fields.md) | Use the link column type (not uri) when you need title and attributes on a link; always pair target="_blank" with rel="noopener noreferrer" to avoid a security vulnerability. |
| Query custom fields in Views | [Views Integration](views-integration.md) | Custom Field ships native Views field/filter/sort/argument plugins so all columns query from one table with no relationships needed -- prefer them over entity query or Paragraphs-style joins. |
| Use tokens in custom fields | [Token Support](token-support.md) | Custom field tokens use the format [entity:field_name:column_name] -- sub-fields use a colon separator while extended properties use double-underscore inside the column name itself. |
| Integrate with GraphQL, JSON:API, Search API, or SDC | [Sub-Modules](sub-modules.md) | Nine optional sub-modules ship with Custom Field 5.x for GraphQL, JSON:API, Entity Browser, Linkit, Media Library, Search API, Viewfield, SDC rendering, and AI integration -- enable only the ones you actually use. |
| Create custom field type plugins | [Custom Plugins](custom-plugins.md) | schema()/propertyDefinitions()/generateSampleValue() are static on CustomFieldTypeBase; there is no #[CustomFieldFormatter] attribute -- sub-field formatters use core's #[FieldFormatter] and implement formatValue(), not format(). |
| Import data via Feeds | [Feeds Integration](feeds-integration.md) | You need to import CSV or other data sources into custom field columns via the Feeds module. A single Feeds target delegates per sub-field to 23 FeedsType plugins, one per supported column type. Target format is field_name:column_name, not double-underscore. |
| Understand performance and security best practices | [Best Practices](best-practices.md) | Custom Field's single-table storage avoids Paragraphs' N+1 query problem; always check entity access before rendering references, sanitize formatter output, and use custom_field.update_manager -- never raw SQL -- for schema changes. |
| Find source code for specific functionality | [Code Reference Map](code-reference-map.md) | Reference map of every Custom Field 5.x source path -- field types, widgets, formatters, plugin managers, hook classes, Views plugins, templates, and the nine sub-module directories -- for locating implementation details fast. |
