---
description: Choose the right Search API backend — Database, Solr, Elasticsearch, OpenSearch, Typesense, or Meilisearch
tldr: "Use this when choosing which search engine to use with Search API. Default to Solr for production."
drupal_version: "11.x"
---

# Backend Comparison

## When to Use

> Use this when choosing which search engine to use with Search API. Default to Solr for production.

## Decision

| Backend | Module | Best For | Max Items | Typo Tolerance | Cost |
|---|---|---|---|---|---|
| **Database** | `search_api_db` (included) | Dev/staging, small sites | ~50K | No | Free |
| **Apache Solr** | `search_api_solr` 4.3.x | Most production sites | Millions | Via config | JVM server |
| **Elasticsearch** | `elasticsearch_connector` | ES ecosystem sites | Millions | Yes | JVM server |
| **OpenSearch** | `search_api_opensearch` | AWS-hosted sites | Millions | Yes | AWS managed |
| **Typesense** | `search_api_typesense` | Instant search, typo tolerance | Medium | Built-in | Lightweight |
| **Meilisearch** | `search_api_meilisearch` | Easy setup, small-medium | Medium | Built-in | Lightweight |

## Pattern

**When to use each:**

| Backend | Choose When |
|---|---|
| Database | Dev/staging, <50K items, zero infrastructure budget |
| Solr | Production default — multilingual, synonyms, spellcheck, enterprise |
| Elasticsearch | Already in ES ecosystem, combined search + analytics |
| OpenSearch | AWS-hosted sites on Amazon OpenSearch Service |
| Typesense | Instant search-as-you-type, AI/vector search, RAG — no Views integration |
| Meilisearch | Easy Solr alternative for small-to-medium, built-in typo tolerance |

Solr is available on Acquia (`acquia_search`), Pantheon (`pantheon_search`), and Platform.sh.

## Common Mistakes

- **Wrong**: Choosing Elasticsearch over Solr "because it's newer" → **Right**: Solr has far more mature Drupal integration, better multilingual support, and is available on more hosting platforms.
- **Wrong**: Using DB backend for a 100K+ item site → **Right**: Will cause severe performance issues, especially with facets. Switch to Solr.
- **Wrong**: Expecting Typesense to work with Views → **Right**: Typesense intentionally skips Views integration. Use InstantSearch.js on the frontend.

## See Also

- [Solr Best Practices](solr-best-practices.md)
- [Decoupled Search](decoupled-search.md) — Typesense and headless patterns
- [Recommended Module Stacks](recommended-module-stacks.md)
- Reference: https://www.drupal.org/project/search_api_solr
