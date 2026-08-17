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
| **Apache Solr** | `search_api_solr` 4.4.x | Most production sites | Millions | Via config | JVM server |
| **Elasticsearch** | `elasticsearch_connector` | ES ecosystem sites | Millions | Yes | JVM server |
| **OpenSearch** | `search_api_opensearch` | AWS-hosted sites | Millions | Yes | AWS managed |
| **Typesense** | `search_api_typesense` | Instant search, typo tolerance | Medium | Built-in | Lightweight |
| **Meilisearch** | `search_api_meilisearch` | Easy setup, small-medium | Medium | Built-in | Lightweight |

**Elasticsearch has no stable release** — the Drupal 10 and Drupal 11 branches of `elasticsearch_connector` have only alpha tags. A build policy that forbids pre-releases rules this backend out.

## Pattern

**When to use each:**

| Backend | Choose When |
|---|---|
| Database | Dev/staging, <50K items, zero infrastructure budget |
| Solr | Production default — multilingual, synonyms, spellcheck, enterprise |
| Elasticsearch | Already in ES ecosystem, combined search + analytics — accept the alpha-only risk |
| OpenSearch | AWS-hosted sites on Amazon OpenSearch Service (fork of Elasticsearch 7.10.2, PSR-18 HTTP client) |
| Typesense | Instant search-as-you-type, AI/vector search, RAG — no Views integration; first stable release achieved (2025) |
| Meilisearch | Easy Solr alternative for small-to-medium, built-in typo tolerance, covered by security advisory policy |

Solr is available on Acquia (`acquia_search`), Pantheon (`search_api_pantheon`), and Platform.sh. `search_api_solr` 4.4.0 requires Drupal 11.3+.

## Common Mistakes

- **Wrong**: Choosing Elasticsearch over Solr "because it's newer" → **Right**: Solr has far more mature Drupal integration, better multilingual support, and is available on more hosting platforms. Elasticsearch also has no stable release.
- **Wrong**: Using DB backend for a 100K+ item site → **Right**: Will cause severe performance issues, especially with facets. Switch to Solr.
- **Wrong**: Expecting Typesense to work with Views → **Right**: Typesense intentionally skips Views integration. Use InstantSearch.js on the frontend.

## See Also

- [Solr Best Practices](solr-best-practices.md)
- [Decoupled Search](decoupled-search.md) — Typesense and headless patterns
- [Recommended Module Stacks](recommended-module-stacks.md)
- Reference: https://www.drupal.org/project/search_api_solr
