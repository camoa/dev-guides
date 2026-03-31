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

| I need to... | Guide |
|---|---|
| Understand what Search API does and its architecture | [Overview](overview.md) |
| Choose a search backend (DB, Solr, Elasticsearch, Typesense, Meilisearch) | [Backend Comparison](backend-comparison.md) |
| Install Search API and create a server + index | [Installation & Setup](installation-setup.md) |
| Configure a Search API server | [Server Configuration](server-configuration.md) |
| Configure a Search API index | [Index Configuration](index-configuration.md) |
| Add and configure indexed fields | [Fields & Data Types](fields-data-types.md) |
| Understand the processor pipeline (indexing and querying) | [Processor Architecture](processor-architecture.md) |
| Choose the right processors for my backend | [Processor Recommendations](processor-recommendations.md) |
| Boost search relevance (field weights, HTML elements) | [Relevance & Boosting](relevance-boosting.md) |
| Build a search page with Views | [Views Integration](views-integration.md) |
| Understand the query system (conditions, sorts, programmatic queries) | [Query System](query-system.md) |
| Understand tracking and the indexing lifecycle | [Indexing Lifecycle](indexing-lifecycle.md) |
| Optimize indexing performance (batch size, drush, cron) | [Indexing Performance](indexing-performance.md) |
| Optimize query performance (caching, count queries) | [Query Performance](query-performance.md) |
| Add autocomplete to search | [Autocomplete](autocomplete.md) |
| Handle multilingual search | [Multilingual Search](multilingual-search.md) |
| Configure Solr (configsets, Solr Cloud, hosting) | [Solr Best Practices](solr-best-practices.md) |
| Build decoupled/headless search (JSON:API, Next.js) | [Decoupled Search](decoupled-search.md) |
| Secure search results (content access, permissions) | [Content Access & Security](content-access-security.md) |
| Use Search API with Facets | [Facets Integration](facets-integration.md) |
| Subscribe to Search API events | [Events System](events-system.md) |
| Create custom processors, backends, or datasources | [Custom Plugin Development](custom-plugin-development.md) |
| Override search templates in my theme | [Theming & Templates](theming-templates.md) |
| Pick the right module stack for my site size | [Recommended Module Stacks](recommended-module-stacks.md) |
| Debug common search problems | [Common Mistakes](common-mistakes.md) |
