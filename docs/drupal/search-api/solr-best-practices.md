---
description: Apache Solr with Search API — schema management, jump-start configsets, version compatibility, hosting, and Solr Cloud
tldr: "Use this when configuring Apache Solr as your Search API backend."
drupal_version: "11.x"
---

# Solr Best Practices

## When to Use

> When configuring Apache Solr as your Search API backend.

## Decision: Schema Management

**Never edit `schema.xml` or `solrconfig.xml` directly** — they will be overwritten on module updates.

Use `search_api_solr_admin` sub-module (included with `search_api_solr`):

```bash
drush en search_api_solr_admin

# Upload configset to Solr Cloud
drush search-api-solr:upload-configset MY_SERVER_ID

# With shards for Solr Cloud — these are command options, so they follow the command
drush search-api-solr:upload-configset --numShards=3 --replicationFactor=2 MY_SERVER_ID
```

Or use the "Upload Configset" button on the server admin page.

## Decision: Jump-Start Configsets

Every release includes pre-generated configsets for Solr 3 through 10, both single-core (`config-set/`) and Solr Cloud (`cloud-config-set/`), under `jump-start/solr3` … `jump-start/solr10`.

**Workflow:**
1. Use jump-start configs to get started quickly
2. Once index is configured, generate a site-specific configset
3. After Solr version upgrades, regenerate and redeploy configset
4. Reindex after configset changes

## Decision: Solr Version Compatibility

| search_api_solr | Solr Versions | Drupal |
|---|---|---|
| 4.4.x | 6.4 through 10.x | Drupal 11.3+ |

Solr 3.6 / 4.5 / 5.x are reachable only through the optional `search_api_solr_legacy` sub-module; mainline support starts at Solr 6.4.

**Solr 9 and the LRUCache removal:** LRUCache was removed in Solr 9.0, and the shipped configsets already account for it — `jump-start/solr9` and `jump-start/solr10` use `CaffeineCache`, only `solr8` still declares `LRUCache`. Take the configset for your actual Solr major version and no cache edit is needed.

## Decision: Hosting

| Platform | Solr Support | Module |
|---|---|---|
| Acquia | Built-in | `acquia_search` (wraps search_api_solr) |
| Pantheon | Built-in | `search_api_pantheon` |
| Platform.sh | Service | Standard search_api_solr |
| DDEV/Lando | Service | Standard search_api_solr |
| Self-hosted | Full control | Standard search_api_solr |

## Pattern: Solr Cloud

- "Collections" replace "cores"
- Use `search_api_solr_admin` to create/manage collections
- Collections can span multiple shards for large datasets

## Pattern: Solr-Specific Processors to DISABLE

| Processor | Why Disable for Solr |
|---|---|
| Tokenizer | Solr handles natively |
| Ignore case | Solr handles natively |
| Stemmer | Solr has language-specific stemmers |
| Stopwords | Solr has language-specific stop word lists |

## Common Mistakes

- **Reindexing "just in case" on the 4.3.x → 4.4.0 upgrade** — Unnecessary. 4.4.0 is code-identical to 4.3.13 apart from dropping the Drupal 10 procedural hook wrappers; `src/` and `config/` are unchanged, so no reindex and no configset regeneration. The only real requirement is Drupal 11.3+.
- **Editing Solr config files directly** — They get overwritten. Use the admin sub-module.
- **Running Solr without enough RAM** — Solr needs 2-4GB+ heap for production. Monitor with JMX/Prometheus.

## See Also

- [Backend Comparison](backend-comparison.md) — why Solr is recommended
- [Indexing Performance](indexing-performance.md) — Solr index-only mode
