---
description: Drupal Views — query and display entity lists with UI-based configuration
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-19
guide-meta:
  concepts:
    - Views configuration
    - views displays
    - views fields
    - views filters
    - exposed filters
    - contextual filters
    - views relationships
    - views pagers
    - style plugins
    - row plugins
    - custom field handler
    - custom filter handler
    - views plugin architecture
  not:
    - entity queries in code (see drupal/entities)
    - REST export API design (see drupal/jsonapi)
  requires:
    - drupal/entities
  complements:
    - drupal/entities
    - drupal/caching
    - drupal/taxonomy
  category: drupal
---

# Views

| I need to... | Guide | Summary |
|-------------|-------|---------|
| understand what Views are and when to use them | [Views System Overview](views-overview.md) | You need to query and display lists of content, users, taxonomy terms, or other entities with filtering, sorting, and display formatting. |
| understand the views.view.*.yml config schema | [View Config Schema](view-config-schema.md) | When writing or editing views.view.*.yml files directly, or understanding config structure for recipes and exports. |
| configure display options (title, access, cache, pager) | [Display Configuration](display-configuration.md) | When configuring common options shared across all display types: title, access, cache, pager, style, fields, filters, sorts. |
| create a page display with URL and menu integration | [Page Display](page-display.md) | When you need a full page with a dedicated URL, menu integration, and optional admin theme. |
| create a block display | [Block Display](block-display.md) | When you need a view placed in block regions, Layout Builder, or programmatically rendered contexts. |
| create a REST export (JSON/XML API) | [REST Export Display](rest-export-display.md) | When you need JSON, XML, or other serialized output for APIs, AJAX endpoints, or headless/decoupled applications. |
| create feed or attachment displays | [Feed & Attachment Displays](feed-attachment-displays.md) | When you need RSS/Atom feeds or attaching views to other display outputs. |
| configure fields and field handlers | [Fields Configuration](fields-configuration.md) | When configuring field output, labels, formatters, rewriting, and CSS classes in views using fields-based rows. |
| add filters and exposed filters | [Filters & Exposed Filters](filters-exposed.md) | When restricting query results via fixed criteria (filters) or user-selectable criteria (exposed filters). |
| add sorting and contextual filters (arguments) | [Sort & Contextual Filters](sort-contextual.md) | When ordering results (sorts) or filtering based on URL parameters (contextual filters/arguments). |
| configure entity relationships | [Relationships](relationships.md) | When you need to access fields from related entities (entity references, users, taxonomy terms, etc.) or apply filters/sorts on related entity data. |
| configure pagers (full, mini, load more) | [Pager Configuration](pager-configuration.md) | When controlling how many items display per page and how users navigate through results. |
| configure caching strategies | [Caching Configuration](caching-configuration.md) | When optimizing view performance by caching query results and rendered output. |
| configure access control | [Access Control](access-control.md) | When restricting who can view a display based on permissions or roles. |
| choose style and row plugins | [Style & Row Plugins](style-row-plugins.md) | When configuring how Views formats output (style) and renders individual rows (row). |
| configure query settings (distinct, aggregation, etc.) | [Query Settings](query-settings.md) | When tuning the underlying database query for performance, distinct results, or query debugging. |
| export views config or use in recipes | [Config Export & Recipes](config-export-recipes.md) | When managing views as exportable configuration, deploying via config sync, or packaging in recipes. |
| modify views programmatically via hooks | [Programmatic Modification](programmatic-modification.md) | When config-based approach isn't sufficient: runtime view modification, dynamic filter injection, custom display logic. |
| understand Views plugin architecture | [Views Plugin Architecture](views-plugin-architecture.md) | When Views UI configuration and programmatic view modification aren't sufficient — you need custom data processing, specialized formatting, or integration with non-standard data sources. |
| create a custom field handler | [Custom Field Handler](custom-field-handler.md) | When you need custom field output: computed values, external API data, complex formatting that can't be achieved with field templates or rewrite rules. |
| create a custom filter handler | [Custom Filter Handler](custom-filter-handler.md) | When standard filter operators aren't sufficient: custom logic, complex conditions, integration with external validation, multi-field filters. |
| create a custom sort handler | [Custom Sort Handler](custom-sort-handler.md) | Custom sort logic: computed fields, weighted sorting, multi-column sorts, integration with external ranking systems. |
| create a custom argument handler | [Custom Argument Handler](custom-argument-handler.md) | URL-based filtering with custom logic: argument validation, default values, custom summary views, title overrides. |
| create a custom relationship handler | [Custom Relationship Handler](custom-relationship-handler.md) | Complex JOIN logic beyond standard entity reference relationships: multi-column joins, conditional joins, subquery-based relationships. |
| create a custom display plugin | [Custom Display Plugin](custom-display-plugin.md) | New output channel beyond Page/Block/REST: CLI output, email rendering, queue processing, specialized API formats. |
| create custom style or row plugins | [Custom Style & Row Plugins](custom-style-row-plugins.md) | **Style Plugin**: Custom result set formatting (calendar, timeline, accordion) that standard Table/Grid/List can't achieve. **Row Plugin**: Custom per-row rendering (entity cards, custom templates) reusable across multiple views. |
| create a custom cache plugin | [Custom Cache Plugin](custom-cache-plugin.md) | Specialized caching beyond time-based and tag-based: per-user caching, geolocation-based, A/B testing variants, external cache backends. |
| integrate custom data with Views (hook_views_data) | [Views Data Integration](views-data-integration.md) | Exposing custom database tables, altering entity views integration, defining custom handlers for existing fields, adding computed/pseudo-fields. |
| follow Views best practices | [Best Practices](best-practices.md) | Guidelines for building maintainable, performant, secure views. |
| avoid common Views anti-patterns | [Anti-Patterns](anti-patterns.md) | What NOT to do and WHY. |
| secure Views and optimize performance | [Security & Performance](security-performance.md) | Critical security and performance considerations for production views. |
| find Views core code references | [Code Reference Map](code-reference-map.md) |  |
| understand guide sources and maintenance | [Sources & Maintenance](sources-maintenance.md) |  |
