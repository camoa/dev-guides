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
    - custom_field_sdc
    - SDC view-mode rendering
    - PropWidget plugins
  not:
    - Paragraphs
    - core field types
    - Field API development (see drupal/entities)
    - sdc_display (separate contrib module, see the Decision table in SDC View-Mode Rendering)
  requires:
    - drupal/entities
  complements:
    - drupal/views
    - drupal/forms
    - drupal/ui-patterns
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
| Choose a text column type (string, email, telephone, uri, color) | [Column Types: Text Fields](column-types-text.md) | Six text column types (string, string_long, email, telephone, uri, color) cover short strings through long text; use string_long past 255 characters and the link type instead of uri when a title or attributes are needed. |
| Choose a numeric column type (integer, float, decimal, boolean) | [Column Types: Numeric Fields](column-types-numeric.md) | Four numeric column types cover whole numbers, floats, fixed-precision decimals and booleans; always use decimal (never float) for currency, and set unsigned on counts and IDs. |
| Choose a date/time column type | [Column Types: Date/Time Fields](column-types-datetime.md) | Five date/time column types match the exact sub-type needed (datetime vs date-only vs time-of-day vs range); daterange and time_range auto-calculate duration on save, and time_range has no cross-midnight support. |
| Choose an entity reference column type | [Column Types: Reference Fields](column-types-reference.md) | entity_reference is the only reference column type; target_type is required and locked after data exists, and it never auto-checks access -- validate in the widget and check in the formatter. |
| Choose a file or image column type | [Column Types: File Fields](column-types-file.md) | file stores a bare file entity ID; image adds extended field__alt/field__title/field__width/field__height properties with dimensions auto-populated on save -- widget settings, not storage, control allowed extensions. |
| Choose a link, map, or uuid column type | [Column Types: Data Fields](column-types-data.md) | link stores URI plus title/options extended properties; map and map_string serialize as PHP arrays (not JSON, not queryable); uuid auto-generates and must never be set by hand. |
| Find the right widget for a sub-field | [Widget Plugins Overview](widget-plugins-overview.md) | 37 widget plugins map to 23 custom field column types, each with a documented default; only override the default when UX calls for it (e.g., select/radios instead of autocomplete for small reference sets, or select_or_other for a constrained-but-extensible list). |
| Use stacked vs flexbox layouts for the entire field | [Field-Level Widgets](field-level-widgets.md) | You need to control how the entire custom field (all sub-fields together) is laid out on the edit form. CustomFlexWidget uses the module's own 12-column CSS grid, not Bootstrap -- works in any theme. |
| Render custom field data with templates or tables | [Field-Level Formatters](field-level-formatters.md) | You need to control how the entire custom field (all sub-fields together) is displayed on the view. Plugin IDs are short (custom_inline, not custom_inline_formatter) -- only custom_formatter carries the _formatter suffix. |
| Work with entity reference sub-fields | [Entity References](entity-references.md) | Pick EntityReferenceAutocompleteWidget for large reference sets and select/radios widgets for small ones; entity reference sub-fields never auto-check access, so validate in the widget and check in the formatter. |
| Handle file and image uploads | [Files and Images](files-images.md) | Use file type + FileWidget for plain uploads and image type + ImageWidget for accessible images with auto-populated alt/title/width/height; always check the loaded file entity is not NULL before rendering. |
| Work with dates, times, and ranges | [Date/Time Fields](datetime-fields.md) | Match the widget to the exact sub-type (datetime vs date-only vs time-of-day vs range); daterange/time_range auto-calculate duration on save and time_range has no cross-midnight support. |
| Add link fields with Linkit integration | [Link Fields](link-fields.md) | Use the link column type (not uri) when you need title and attributes on a link; always pair target="_blank" with rel="noopener noreferrer" to avoid a security vulnerability. |
| Query custom fields in Views | [Views Integration](views-integration.md) | Custom Field ships native Views field/filter/sort/argument plugins so all columns query from one table with no relationships needed -- prefer them over entity query or Paragraphs-style joins. |
| Use tokens in custom fields | [Token Support](token-support.md) | Custom field tokens use the format [entity:field_name:column_name] -- sub-fields use a colon separator while extended properties use double-underscore inside the column name itself. |
| Integrate with GraphQL, JSON:API, Search API, or SDC | [Sub-Modules](sub-modules.md) | Nine optional sub-modules ship with Custom Field 5.x for GraphQL, JSON:API, Entity Browser, Linkit, Media Library, Search API, Viewfield, SDC rendering, and AI integration -- enable only the ones you actually use. |
| Render a whole view mode through an SDC, and choose between this, UI Patterns and Canvas | [SDC View-Mode Rendering](sdc-view-modes.md) | custom_field_sdc replaces a whole view mode's render output with a component: props are static/token values typed on Manage display, slots pull a whole formatted field render array -- any failure falls back silently to normal field output except a failed validateComponent(), which logs. |
| Create custom field type plugins | [Custom Plugins](custom-plugins.md) | schema()/propertyDefinitions()/generateSampleValue() are static on CustomFieldTypeBase; there is no #[CustomFieldFormatter] attribute -- sub-field formatters use core's #[FieldFormatter] and implement formatValue(), not format(). |
| Import data via Feeds | [Feeds Integration](feeds-integration.md) | You need to import CSV or other data sources into custom field columns via the Feeds module. A single Feeds target delegates per sub-field to 23 FeedsType plugins, one per supported column type. Target format is field_name:column_name, not double-underscore. |
| Understand performance and security best practices | [Best Practices: Performance & Security](best-practices-performance.md) | Custom Field's single-table storage avoids Paragraphs' N+1 query problem; always check entity access before rendering references, sanitize formatter output with render arrays instead of raw concatenation, and use private:// for sensitive files. |
| Follow coding standards for Custom Field development | [Development Standards](development-standards.md) | Inject services instead of static \Drupal:: calls, use isEmpty() instead of checking individual sub-field properties, and deploy schema changes only through custom_field.update_manager in a hook_update_N() -- never raw SQL. |
| Find source code for specific functionality | [Code Reference Map](code-reference-map.md) | Reference map of every Custom Field 5.x source path -- field types, widgets, formatters, plugin managers, hook classes, Views plugins, templates, and the nine sub-module directories -- for locating implementation details fast. |
