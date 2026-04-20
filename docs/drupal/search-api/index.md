---
description: Drupal Search API — decision guides for backends, indexing, processors, Views integration, Solr, facets, autocomplete, multilingual, decoupled search, and custom plugins
guide-meta:
  concepts:
    - Search API
    - search_api
    - search_api_db
    - search_api_solr
    - search_api_typesense
    - search_api_meilisearch
    - search_api_autocomplete
    - search_api_fast
    - jsonapi_search_api
    - SearchApiQuery
    - IndexInterface
    - ServerInterface
    - ProcessorInterface
    - ProcessorPluginBase
    - BackendInterface
    - DatasourceInterface
    - TrackerInterface
    - SearchApiEvents
    - QueryPreExecuteEvent
    - IndexingItemsEvent
    - search_api.server
    - search_api.index
    - sapi-i
    - sapi-r
    - sapi-c
    - sapi-s
    - sapi-rt
    - processor pipeline
    - search backend
    - search index
    - search server
    - fulltext search
    - search_api_relevance
    - cron_limit
    - index_directly
    - track_changes_in_references
    - rendered_item processor
    - content_access processor
    - entity_status processor
    - html_filter processor
    - highlight processor
    - type_boost processor
    - aggregated_field processor
    - STAGE_PREPROCESS_INDEX
    - STAGE_PREPROCESS_QUERY
    - STAGE_ALTER_ITEMS
    - STAGE_POSTPROCESS_QUERY
    - jump-start configset
    - Solr Cloud
    - search_api_solr_admin
    - acquia_search
    - pantheon_search
  not:
    - Facets widgets and processors (see drupal/facets)
    - Better Exposed Filters widgets (see drupal/better-exposed-filters)
    - core Search module
  requires:
    - drupal/views
  complements:
    - drupal/facets
    - drupal/better-exposed-filters
    - drupal/views
    - drupal/multilingual
  specializes: ""
  category: drupal
---

# Drupal Search API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Search API does and its architecture | [Overview](overview.md) | Use Search API when you need flexible, backend-agnostic search for Drupal. Always use Search API over core Search — uninstall the core `search` module, it performs redundant indexing. |
| Choose a search backend (DB, Solr, Elasticsearch, Typesense, Meilisearch) | [Backend Comparison](backend-comparison.md) | Use this when choosing which search engine to use with Search API. Default to Solr for production. |
| Install Search API and create a server + index | [Installation & Setup](installation-setup.md) | Use this when installing Search API and creating your first server and index. |
| Configure a Search API server | [Server Configuration](server-configuration.md) | Use this when creating or configuring a Search API server entity. |
| Configure a Search API index | [Index Configuration](index-configuration.md) | Use this when creating or configuring a Search API index — the central entity defining what gets indexed, how it's processed, and where it's stored. |
| Add and configure indexed fields | [Fields & Data Types](fields-data-types.md) | Use this when adding fields to a Search API index and choosing the correct data type for each. |
| Understand the processor pipeline (indexing and querying) | [Processor Architecture](processor-architecture.md) | Use this when you need to understand how Search API processors work — the stages, weights, and execution order. |
| Choose the right processors for my backend | [Processor Recommendations](processor-recommendations.md) | Use this when deciding which processors to enable for your Search API index. |
| Boost search relevance (field weights, HTML elements) | [Relevance & Boosting](relevance-boosting.md) | Use this when tuning search result relevance — making the most relevant results appear first. |
| Build a search page with Views | [Views Integration](views-integration.md) | Use this when building search pages using Views — the most common approach for Search API. |
| Understand the query system (conditions, sorts, programmatic queries) | [Query System](query-system.md) | Use this when building Search API queries programmatically or understanding how the query system works. |
| Understand tracking and the indexing lifecycle | [Indexing Lifecycle](indexing-lifecycle.md) | Use this when you need to understand how content gets tracked, indexed, and maintained in the search engine. |
| Optimize indexing performance (batch size, drush, cron) | [Indexing Performance](indexing-performance.md) | Use this when optimizing how fast content gets indexed, especially for large sites or initial indexing. |
| Optimize query performance (caching, count queries) | [Query Performance](query-performance.md) | Use this when optimizing search query speed and reducing server load. |
| Add autocomplete to search | [Autocomplete](autocomplete.md) | Use this when adding search-as-you-type suggestions to search forms. |
| Handle multilingual search | [Multilingual Search](multilingual-search.md) | Use this when building search for multilingual Drupal sites. |
| Configure Solr (configsets, Solr Cloud, hosting) | [Solr Best Practices](solr-best-practices.md) | Use this when configuring Apache Solr as your Search API backend. |
| Build decoupled/headless search (JSON:API, Next.js) | [Decoupled Search](decoupled-search.md) | Use this when building headless/decoupled frontends (Next.js, React, etc.) that need search functionality. |
| Secure search results (content access, permissions) | [Content Access & Security](content-access-security.md) | Use this when you need to ensure search results respect content access permissions. Search API does NOT restrict access by default. |
| Use Search API with Facets | [Facets Integration](facets-integration.md) | Use this when adding faceted search navigation to your Search API-powered search page. |
| Subscribe to Search API events | [Events System](events-system.md) | Use this when hooking into Search API's query or indexing pipeline without creating full custom processors. |
| Create custom processors, backends, or datasources | [Custom Plugin Development](custom-plugin-development.md) | Use this when you need a custom processor, backend, datasource, or other Search API plugin. |
| Override search templates in my theme | [Theming & Templates](theming-templates.md) | Use this when customizing the display of search results or search-related elements. |
| Pick the right module stack for my site size | [Recommended Module Stacks](recommended-module-stacks.md) | Use this when planning which modules to install for your site's search functionality. |
| Debug common search problems | [Common Mistakes](common-mistakes.md) | Use this when debugging search issues or reviewing a Search API implementation. |
