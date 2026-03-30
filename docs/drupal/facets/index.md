---
description: Drupal Facets — decision guides for faceted search with Search API, widgets, processors, URL handling, SEO/bot protection, and custom plugin development
guide-meta:
  concepts:
    - Facets
    - facets module
    - faceted search
    - facet source
    - facet widget
    - facet processor
    - Search API facets
    - facets_exposed_filters
    - facets_summary
    - facets_range_widget
    - facets_searchbox_widget
    - facets_rest
    - facets_pretty_paths
    - facet_bot_blocker
    - LinksWidget
    - CheckboxWidget
    - DropdownWidget
    - translate_entity processor
    - count_limit processor
    - hide_non_narrowing_result_processor
    - url_processor_handler
    - hierarchy_processor
    - FacetManager
    - facets_filter cache context
    - query_string URL processor
    - PRE_QUERY POST_QUERY BUILD SORT stages
    - FacetInterface
    - WidgetPluginBase
    - ProcessorPluginBase
    - FacetsProcessor annotation
    - FacetsWidget annotation
    - search_api_string
    - search_api_range
    - search_api_date
    - search_api_granular
  not:
    - Better Exposed Filters (BEF widgets without Search API — see drupal/better-exposed-filters)
    - Views exposed filters without Search API
    - core Views filters
  requires:
    - drupal/views
  complements:
    - drupal/better-exposed-filters
    - drupal/views
    - drupal/seo-geo
  specializes: ""
  category: drupal
---

# Drupal Facets

| I need to... | Guide |
|---|---|
| Understand what Facets does and decide between Facets/BEF/core filters | [Overview](overview.md) |
| Install Facets and set up Search API | [Installation & Setup](installation-setup.md) |
| Understand facet sources and how they connect to Views | [Facet Sources](facet-sources.md) |
| Create and configure a facet entity | [Facet Configuration](facet-configuration.md) |
| Understand the processing pipeline (pre_query → build) | [Processing Pipeline](processing-pipeline.md) |
| Choose the right widget (links, checkbox, dropdown) | [Widgets](widgets.md) |
| Use the range slider sub-module | [Range Slider Widget](range-slider.md) |
| Add a searchbox to filter facet items | [Searchbox Widget](searchbox-widget.md) |
| Transform values (IDs to labels, dates, booleans) | [Value Transformation Processors](value-transformation-processors.md) |
| Filter and limit results (count limit, hide non-narrowing) | [Result Filtering Processors](result-filtering-processors.md) |
| Sort facet results (by count, display value, weight) | [Sort Processors](sort-processors.md) |
| Build hierarchical facets (taxonomy, dates) | [Hierarchy](hierarchy.md) |
| Understand URL parameter handling | [URL Processors](url-processors.md) |
| Know how query types work (string, date, range) | [Query Types](query-types.md) |
| Use Facets as Views exposed filters with BEF | [Facets Exposed Filters](facets-exposed-filters.md) |
| Display active facet selections with summary | [Facets Summary](facets-summary.md) |
| Expose facets via REST API | [Facets REST](facets-rest.md) |
| Prevent bot and AI scraper crawling of facet URLs | [SEO & Bot Protection](seo-bot-protection.md) |
| Handle facet URL canonicalization | [Canonical URLs & Duplicate Content](canonical-urls.md) |
| Override facet templates in my theme | [Theming & Templates](theming-templates.md) |
| Subscribe to facet events | [Events](events.md) |
| Understand facet caching | [Caching](caching.md) |
| Create custom processors, widgets, or query types | [Custom Plugin Development](custom-plugin-development.md) |
| Use the facets_pretty_paths contrib module | [Pretty Paths](pretty-paths.md) |
| Debug common facet problems | [Common Mistakes](common-mistakes.md) |
