---
description: Apache Solr with Search API — schema management, jump-start configsets, version compatibility, hosting, and Solr Cloud
drupal_version: "11.x"
---

# Solr Best Practices

## When to Use

> Use this when configuring Apache Solr as your Search API backend.

## Decision

**Never edit `schema.xml` or `solrconfig.xml` directly** — they will be overwritten on module updates. Use `search_api_solr_admin` sub-module.

| Platform | Solr Support | Module |
|---|---|---|
| Acquia | Built-in | `acquia_search` (wraps search_api_solr) |
| Pantheon | Built-in | `pantheon_search` |
| Platform.sh | Service | Standard search_api_solr |
| DDEV/Lando | Service | Standard search_api_solr |
| Self-hosted | Full control | Standard search_api_solr |

| search_api_solr | Solr Versions | Drupal |
|---|---|---|
| 4.3.x | 3.6 through 9.x | Drupal 10+ |
| 4.2.x | 3.6 through 9.x | Drupal 9+10 |

## Pattern

```bash
drush en search_api_solr_admin

# Upload configset to Solr Cloud
drush search-api-solr:upload-configset MY_SERVER_ID

# With shards
drush --numShards=1 search-api-solr:upload-configset MY_SERVER_ID
```

**Jump-start configsets workflow:**
1. Use jump-start configs to get started quickly
2. Once index is configured, generate a site-specific configset
3. After Solr version upgrades, regenerate and redeploy configset
4. Reindex after configset changes

**Solr processors to disable** (Solr handles these natively):
- Tokenizer, Ignore case, Stemmer, Stopwords

**Solr 9 caveat:** LRUCache was removed in Solr 9.0. Ensure you download the correct Solr 9 configset — known bug where the download button may serve the Solr 7/8 version.

## Common Mistakes

- **Wrong**: 4.2.x to 4.3.x migration without reindexing → **Right**: Existing indexes can be read but indexing may produce "cannot change field" errors. Full reindex required.
- **Wrong**: Editing Solr config files directly → **Right**: They get overwritten. Use the admin sub-module.
- **Wrong**: Running Solr without enough RAM → **Right**: Solr needs 2-4GB+ heap for production. Monitor with JMX/Prometheus.

## See Also

- [Backend Comparison](backend-comparison.md)
- [Indexing Performance](indexing-performance.md)
- Reference: https://www.drupal.org/project/search_api_solr
