---
description: Search API module stacks by site size — small (DB), medium (Solr), large/enterprise (Solr Cloud), and decoupled (JSON:API)
tldr: "Use this when planning which modules to install for your site's search functionality."
drupal_version: "11.x"
---

# Recommended Module Stacks

## When to Use

> When planning which modules to install for your site's search functionality.

## Decision: By Site Size

**Small Sites (< 10K items):**
```bash
composer require drupal/search_api
drush en search_api search_api_db

# Optional:
composer require drupal/facets drupal/search_api_autocomplete
```
- Database backend is sufficient
- Enable ALL processors (tokenizer, stemmer, stopwords, etc.)
- Cron batch size: 100

**Medium Sites (10K-100K items):**
```bash
composer require drupal/search_api drupal/search_api_solr
composer require drupal/facets drupal/better_exposed_filters
composer require drupal/search_api_autocomplete
drush en search_api search_api_solr search_api_solr_admin
drush en facets facets_exposed_filters better_exposed_filters
drush en search_api_autocomplete
```
- Solr 9 or 10 backend
- DISABLE redundant processors (tokenizer, stemmer, stopwords, ignore case)
- Use Facets Exposed Filters + BEF
- Solr Terms suggester for autocomplete
- Cron batch size: 50

**Large / Enterprise Sites (100K+ items):**
```bash
# Same as medium — parallel indexing needs no extra module on Solr:
drush search-api-solr:index-parallel my_index --threads=8 --batch-size=100
```
- Solr Cloud for horizontal scaling
- `search-api-solr:index-parallel` for parallel indexing (`search_api_fast` only if the backend is not Solr)
- Solr index-only mode (retrieve data from Solr, skip entity loads)
- Dedicated "Search index" view mode
- Cache warming for popular queries
- Frequent cron (every 1-2 min) + drush reindexing strategy
- Cron batch size: 25

**Decoupled / Headless:**
```bash
# Add to any stack above:
composer require drupal/jsonapi_search_api
# OR for Typesense:
composer require drupal/search_api_typesense
```

## See Also

- [Backend Comparison](backend-comparison.md) — backend selection
- [Indexing Performance](indexing-performance.md) — performance tuning
