---
description: Drupal Facets — decision guides for faceted search with Search API, widgets, processors, URL handling, SEO/bot protection, and custom plugin development
tracks:
  - project: facets
    channel: stable
    declared: "3.x"
    verified: 2026-03-30
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

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Facets does and decide between Facets/BEF/core filters | [Overview](overview.md) | Use Facets when you need faceted search navigation with result counts, narrowing behavior, and hierarchical filtering — and you are using Search API. Use Better Exposed Filters when you want enhanced widgets for any Views exposed form… |
| Install Facets and set up Search API | [Installation & Setup](installation-setup.md) | Use this guide when setting up Facets on a Drupal site with Search API. |
| Understand facet sources and how they connect to Views | [Facet Sources](facet-sources.md) | Use this guide when you need to understand how facets connect to your search backend and Views displays, or when a facet source is not appearing. |
| Create and configure a facet entity | [Facet Configuration](facet-configuration.md) | Use this guide when creating or configuring a facet entity — selecting the source, field, widget, operators, and processors. |
| Understand the processing pipeline (pre_query → build) | [Processing Pipeline](processing-pipeline.md) | Use this guide when you need to understand how facets process data from query to rendering, or when debugging unexpected facet behavior. |
| Choose the right widget (links, checkbox, dropdown) | [Widgets](widgets.md) | Use this guide when choosing how facet results should be rendered to the user. |
| Use the range slider sub-module | [Range Slider Widget](range-slider.md) | Use this guide when you have numeric facets (price, rating, year) and want a visual slider interface. |
| Add a searchbox to filter facet items | [Searchbox Widget](searchbox-widget.md) | Use this guide when a facet has many items and you want users to type to filter the visible options client-side. |
| Transform values (IDs to labels, dates, booleans) | [Value Transformation Processors](value-transformation-processors.md) | Use this guide when facet raw values need to be converted to human-readable labels — entity IDs to names, boolean values to Yes/No, dates to formatted strings. |
| Filter and limit results (count limit, hide non-narrowing) | [Result Filtering Processors](result-filtering-processors.md) | Use this guide when you need to control which facet items are displayed — hiding items with low counts, removing specific values, or showing only narrowing results. |
| Sort facet results (by count, display value, weight) | [Sort Processors](sort-processors.md) | Use this guide when you need to control the order of facet result items. |
| Build hierarchical facets (taxonomy, dates) | [Hierarchy](hierarchy.md) | Use this guide when faceting on hierarchical data — taxonomy vocabularies with parent-child relationships or date facets with year → month → day grouping. |
| Understand URL parameter handling | [URL Processors](url-processors.md) | Use this guide when you need to understand how facet selections are represented in URLs, or when customizing URL behavior. |
| Know how query types work (string, date, range) | [Query Types](query-types.md) | Use this guide when you need to understand how facet selections are translated into search backend queries, or when facets are not filtering correctly for a field type. |
| Use Facets as Views exposed filters with BEF | [Facets Exposed Filters](facets-exposed-filters.md) | Use facets_exposed_filters when you want facets integrated into the Views exposed form — the recommended approach in Facets 3.x. This gives you native Views AJAX, BEF widget support, and simpler configuration. |
| Display active facet selections with summary | [Facets Summary](facets-summary.md) | Use this guide when you want to display active facet selections as removable breadcrumbs — "Color: Blue (x) \| Size: Large (x) \| Reset all". |
| Expose facets via REST API | [Facets REST](facets-rest.md) | Use this guide when building a headless or decoupled frontend and you need facet data (values, counts, active states, URLs) in API responses. |
| Prevent bot and AI scraper crawling of facet URLs | [SEO & Bot Protection](seo-bot-protection.md) | Use this guide when deploying any site with Facets. Facets have ZERO built-in SEO or bot protection. |
| Handle facet URL canonicalization | [Canonical URLs & Duplicate Content](canonical-urls.md) | Use this guide when faceted pages create duplicate content issues — the same results appearing at multiple URLs due to different facet parameter ordering or pagination combinations. |
| Override facet templates in my theme | [Theming & Templates](theming-templates.md) | Use this guide when customizing the HTML output of facets in your theme. |
| Subscribe to facet events | [Events](events.md) | Use this guide when you need to hook into the facets processing pipeline without creating a full custom processor — for example, modifying URL formats, overriding active filter detection, or adjusting cache metadata. |
| Understand facet caching | [Caching](caching.md) | Use this guide when you need to understand or debug facet caching behavior, or when facets show stale data or wrong results after caching. |
| Create custom processors, widgets, or query types | [Custom Plugin Development](custom-plugin-development.md) | Use this guide when you need a custom processor, widget, query type, or URL processor that doesn't exist in the built-in set. |
| Use the facets_pretty_paths contrib module | [Pretty Paths](pretty-paths.md) | Use this guide when you want cleaner facet URLs — `/search/color/blue/size/large` instead of `?f[0]=color:blue&f[1]=size:large`. |
| Debug common facet problems | [Common Mistakes](common-mistakes.md) | Use this guide when debugging facet issues or reviewing a faceted search implementation before going to production. |
