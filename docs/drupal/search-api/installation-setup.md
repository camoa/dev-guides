---
description: Install Search API, create a server and index, and run the initial index via admin UI and Drush
tldr: "Use this when installing Search API and creating your first server and index."
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> Use this when installing Search API and creating your first server and index.

## Decision

| Step | Action | Where |
|---|---|---|
| 1 | Uninstall core Search module | `drush pm:uninstall search` |
| 2 | Create a server | `/admin/config/search/search-api/add-server` |
| 3 | Create an index | `/admin/config/search/search-api/add-index` |
| 4 | Select datasources | Index edit form — usually "Content" (nodes) |
| 5 | Add fields to index | Index → Fields tab |
| 6 | Configure processors | Index → Processors tab |
| 7 | Create a "Search index" view mode | `/admin/structure/types/manage/{type}/display` |
| 8 | Index content | `drush sapi-i` |
| 9 | Create a View | Select the search index as data source |
| 10 | Add facets (optional) | `/admin/config/search/facets/add-facet` |

## Pattern

```bash
# Core Search API (includes database backend)
composer require drupal/search_api
drush en search_api search_api_db

# For Solr (production):
composer require drupal/search_api_solr
drush en search_api_solr

# Common companions:
composer require drupal/facets drupal/search_api_autocomplete
drush en facets search_api_autocomplete
```

Current stable releases are `search_api` 8.x-1.41 and `search_api_solr` 4.4.0. Pulling `search_api_solr` 4.4 also pulls `search_api ^1.41`, and 4.4.x requires Drupal 11.3 or newer.

**Drush commands:**

| Command | Purpose |
|---|---|
| `drush sapi-l` | List all indexes |
| `drush sapi-i` | Index all items |
| `drush sapi-i --batch-size=50` | Index with specific batch size |
| `drush sapi-i --time-limit=300` | Index for max 5 minutes |
| `drush sapi-r` | Mark all items for reindexing |
| `drush sapi-c` | Clear all indexed data |
| `drush sapi-rt` | Rebuild tracking information |
| `drush sapi-s` | View index status |

## Common Mistakes

- **Wrong**: Not uninstalling core Search → **Right**: Running both wastes resources. `drush pm:uninstall search`.
- **Wrong**: Forgetting to index after adding fields or changing processors → **Right**: Always reindex after configuration changes.
- **Wrong**: Not creating a search view mode → **Right**: The default "Full content" view mode indexes too much. Create a dedicated view mode.

## See Also

- [Server Configuration](server-configuration.md)
- [Index Configuration](index-configuration.md)
- Reference: `/admin/config/search/search-api`
