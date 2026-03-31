---
description: Search API server entity — properties, key methods, and backend-specific settings for Database and Solr
drupal_version: "11.x"
---

# Server Configuration

## When to Use

> Use this when creating or configuring a Search API server entity.

## Decision

| Property | Config Key | Purpose |
|---|---|---|
| Machine name | `id` | Unique identifier |
| Name | `name` | Human-readable label |
| Backend | `backend` | Backend plugin ID (`search_api_db`, `search_api_solr`, etc.) |
| Backend config | `backend_config` | Backend-specific settings |
| Status | `status` | Enabled/disabled |

## Pattern

**Key server methods:**

| Method | Purpose |
|---|---|
| `getBackend()` | Get backend plugin instance |
| `getBackendIfAvailable()` | Get backend safely (no exception) |
| `getIndexes()` | Get all indexes using this server |
| `isAvailable()` | Is the backend reachable? |
| `supportsFeature($feature)` | Check backend capabilities |

**Database backend settings:**

| Setting | Purpose |
|---|---|
| Matching mode | "Whole words only" (faster) or "Partial matching" |
| Min chars for search | Minimum characters for fulltext search |

**Solr backend settings:**

| Setting | Purpose |
|---|---|
| Solr host/port/path | Connection details |
| Core/collection name | Solr core or collection |
| Authentication | Basic auth, API keys, or none |
| Retrieve data from Solr | Skip entity loads (index-only mode) |
| Highlighting | Enable Solr-native highlighting |

## Common Mistakes

- **Wrong**: Editing Solr config files directly → **Right**: Use `search_api_solr_admin` sub-module. Direct edits are overwritten on module updates.
- **Wrong**: Partial matching on DB backend for large sites → **Right**: "Whole words only" is significantly faster. Only use partial if required.

## See Also

- [Solr Best Practices](solr-best-practices.md)
- [Backend Comparison](backend-comparison.md)
- Reference: `web/modules/contrib/search_api/src/Entity/Server.php`
