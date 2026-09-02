---
description: Search API server entity — properties, key methods, and backend-specific settings for Database and Solr
tldr: "Use this when creating or configuring a Search API server entity."
drupal_version: "11.x"
---

# Server Configuration

## When to Use

> When creating or configuring a Search API server entity.

## Decision: Server Entity Properties

| Property | Config Key | Purpose |
|---|---|---|
| Machine name | `id` | Unique identifier |
| Name | `name` | Human-readable label |
| Description | `description` | Purpose documentation |
| Backend | `backend` | Backend plugin ID ('search_api_db_defaults', 'search_api_solr', etc.) |
| Backend config | `backend_config` | Backend-specific settings |
| Status | `status` | Enabled/disabled |

## Pattern: Server Key Methods

| Method | Purpose |
|---|---|
| `getBackend()` | Get backend plugin instance |
| `getBackendIfAvailable()` | Get backend safely (no exception) |
| `getIndexes()` | Get all indexes using this server |
| `isAvailable()` | Is the backend reachable? |
| `supportsFeature($feature)` | Check backend capabilities |
| `getSupportedFeatures()` | List all supported features |

## Pattern: Database Backend Settings

| Setting | Purpose |
|---|---|
| Matching mode | "Whole words only" (faster) or "Partial matching" |
| Database | Which database connection to use |
| Min chars for search | Minimum characters for fulltext search |

## Pattern: Solr Backend Settings

| Setting | Purpose |
|---|---|
| Solr host/port/path | Connection details |
| Core/collection name | Solr core or collection |
| Authentication | Basic auth, API keys, or none |
| Retrieve data from Solr | Skip entity loads (index-only mode) |
| Highlighting | Enable Solr-native highlighting |

## See Also

- [Solr Best Practices](solr-best-practices.md) — detailed Solr configuration
- [Backend Comparison](backend-comparison.md) — choosing a backend
- Reference: `web/modules/contrib/search_api/src/Entity/Server.php`
