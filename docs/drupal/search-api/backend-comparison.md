---
description: Choose the right Search API backend — Database, Solr, Elasticsearch, OpenSearch, Typesense, or Meilisearch
tldr: "Use this when choosing which search engine to use with Search API. Default to Solr for production; DB backend for dev/small sites; Elasticsearch has no stable release."
drupal_version: "11.x"
---

# Backend Comparison

## When to Use

> When choosing which search engine to use with Search API.

## Decision: Backend Selection

| Backend | Module | Best For | Max Items | Typo Tolerance | Facets | Cost |
|---|---|---|---|---|---|---|
| **Database** | `search_api_db` (included) | Dev/staging, small sites | ~50K | No | Basic | Free |
| **Apache Solr** | `search_api_solr` 4.4.x | Most production sites | Millions | Via config | Excellent | JVM server |
| **Elasticsearch** | `elasticsearch_connector` (alpha only) | ES ecosystem sites | Millions | Yes | Excellent | JVM server |
| **OpenSearch** | `search_api_opensearch` | AWS-hosted sites | Millions | Yes | Good | AWS managed |
| **Typesense** | `search_api_typesense` | Instant search, typo tolerance | Medium | Built-in | Yes | Lightweight |
| **Meilisearch** | `search_api_meilisearch` | Easy setup, small-medium | Medium | Built-in | Yes (sub-module) | Lightweight |

## Decision: When to Use Each

**Database Backend (`search_api_db`):**
- Development and staging environments
- Sites with fewer than ~50K indexed items
- Simple search needs (no fuzzy matching needed)
- Zero infrastructure budget
- Limitations: No typo tolerance, no fuzzy matching, slow COUNT queries on MySQL InnoDB, poor full-text capabilities

**Apache Solr (`search_api_solr`):**
- **The default recommendation for production**
- Enterprise sites with complex search needs
- Multilingual sites (built-in language-specific analyzers)
- Sites needing synonyms, spellcheck, "More Like This"
- Available on Acquia, Pantheon, Platform.sh
- Module version: 4.4.0 — supports Solr 6.4 through 10.x. Solr 3.6 / 4.5 / 5.x reach only through the optional `search_api_solr_legacy` sub-module. 4.4.x requires Drupal 11.3+

**Elasticsearch (`elasticsearch_connector`):**
- Sites already in an Elasticsearch ecosystem
- Combined search + analytics requirements
- Does NOT support OpenSearch — separate module needed
- Less mature Drupal integration than Solr
- **No stable release** — the Drupal 10 and Drupal 11 branches have only alpha tags. A build policy that forbids pre-releases rules this backend out

**OpenSearch (`search_api_opensearch`):**
- AWS-hosted sites using Amazon OpenSearch Service
- Fork of Elasticsearch 7.10.2 — APIs have diverged
- Uses PSR-18 HTTP Client

**Typesense (`search_api_typesense`):**
- Sites needing blazing-fast search-as-you-type
- AI/vector search and RAG workflows
- No Views integration by design — uses InstantSearch.js on frontend
- First stable release achieved (2025)

**Meilisearch (`search_api_meilisearch`):**
- Easy alternative to Solr for small-to-medium sites
- Built-in typo tolerance without complex configuration
- Covered by security advisory policy

## Common Mistakes

- **Choosing Elasticsearch over Solr "because it's newer"** — Solr has far more mature Drupal integration, better multilingual support, and is available on more hosting platforms.
- **Using DB backend for a 100K+ item site** — Will cause severe performance issues, especially with facets.
- **Expecting Typesense to work with Views** — Typesense intentionally skips Views integration. Use InstantSearch.js on the frontend.

## See Also

- [Solr Best Practices](solr-best-practices.md) — Solr-specific configuration
- [Decoupled Search](decoupled-search.md) — Typesense and headless patterns
- [Recommended Module Stacks](recommended-module-stacks.md) — by site size
