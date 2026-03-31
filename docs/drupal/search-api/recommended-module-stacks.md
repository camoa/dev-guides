---
description: Search API module stacks by site size — small (DB), medium (Solr), large/enterprise (Solr Cloud), and decoupled (JSON:API)
drupal_version: "11.x"
---

# Recommended Module Stacks

## When to Use

> Use this when planning which modules to install for your site's search functionality.

## Decision

| Site Size | Backend | Key Modules |
|---|---|---|
| Small (<10K items) | Database | `search_api`, `search_api_db` |
| Medium (10K-100K) | Solr 8/9 | + `search_api_solr`, `facets`, `better_exposed_filters`, `search_api_autocomplete` |
| Large/Enterprise (100K+) | Solr Cloud | + `search_api_fast`, Solr Cloud config |
| Decoupled | Any | + `jsonapi_search_api` OR `search_api_typesense` |

## Pattern

**Small sites:**
```bash
composer require drupal/search_api
drush en search_api search_api_db
# Enable ALL processors (tokenizer, stemmer, stopwords, etc.)
# Cron batch size: 100
```

**Medium sites:**
```bash
composer require drupal/search_api drupal/search_api_solr
composer require drupal/facets drupal/better_exposed_filters
composer require drupal/search_api_autocomplete
drush en search_api search_api_solr search_api_solr_admin
drush en facets facets_exposed_filters better_exposed_filters
# DISABLE: tokenizer, stemmer, stopwords, ignore case (Solr handles these)
# Solr Terms suggester for autocomplete; Cron batch size: 50
```

**Large / Enterprise:**
```bash
# Same as medium, plus:
composer require drupal/search_api_fast
# Solr Cloud, search_api_fast with workers=4
# Cron batch size: 25; Solr index-only mode
# Cache warming for popular queries
```

**Decoupled:**
```bash
# Add to any stack above:
composer require drupal/jsonapi_search_api
# OR for Typesense instant search:
composer require drupal/search_api_typesense
```

## Common Mistakes

- **Wrong**: Using DB backend + all processors for a 50K+ site → **Right**: Switch to Solr. DB will degrade severely.
- **Wrong**: Not disabling Solr-duplicate processors on medium/large stacks → **Right**: Always disable Tokenizer, Stemmer, Stopwords, Ignore case when using Solr.

## See Also

- [Backend Comparison](backend-comparison.md)
- [Indexing Performance](indexing-performance.md)
- Reference: https://www.velir.com/ideas/2025/03/03/the-many-search-engines-that-drupal-cms-supports
