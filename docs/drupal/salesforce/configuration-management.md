---
description: Salesforce configuration management — mapping export paths, auth secrets handling, global settings, environment deployment workflow
drupal_version: "11.x"
---

# Configuration Management

## When to Use

> Use Drupal's standard config management (drush config:export/import) for mappings. Never commit auth credentials to version control — consumer secrets are not exported and must be configured per environment.

## Decision

| Config Type | Export Path | Notes |
|---|---|---|
| Salesforce mapping | `config/sync/salesforce_mapping.salesforce_mapping.[id].yml` | Safe to commit |
| Auth config structure | `config/sync/salesforce.salesforce_auth.[id].yml` | Structure only — no secrets |
| Consumer secrets | Not exported | Must be configured per environment |
| Global settings | `config/sync/salesforce.settings.yml` | Safe to commit |

**Global settings reference (`salesforce.settings.yml`):**
- `global_push_limit` — Max push items per cron run
- `pull_max_queue_size` — Max pull queue size
- `standalone` — Enable standalone queue endpoints
- `use_latest` — Always use latest API version
- `salesforce_auth_provider` — Default auth provider ID
- `short_term_cache_lifetime` — Object metadata cache (default: 300s)
- `long_term_cache_lifetime` — API version cache (default: 86400s)

## Pattern

**Standard environment deployment:**
```bash
# Dev: create mapping via UI, export
drush config:export

# Commit to version control, deploy to staging/prod
git add config/sync/
git commit -m "Add contact Salesforce mapping"

# On target environment: import config
drush config:import

# Then manually configure credentials (NOT via config import)
# /admin/config/salesforce/authorize/{auth_id}
# Enter Consumer Key/Secret, complete OAuth flow or set JWT key
```

## Common Mistakes

- **Wrong**: Expecting Salesforce consumer secrets to be imported with `drush config:import` → **Right**: Consumer secrets are not exported; configure credentials manually on each environment after config import
- **Wrong**: Setting `salesforce_auth_provider` to an auth provider ID that differs between environments without per-environment config overrides → **Right**: Use `settings.php` config overrides for environment-specific auth provider IDs

## See Also

- [OAuth Authentication](oauth-authentication.md)
- [JWT Authentication](jwt-authentication.md)
- [Queue Processing](queue-processing.md)
- Reference: `config/sync/salesforce.settings.yml`
- Docs: https://www.drupal.org/docs/contributed-modules/salesforce-suite/mapping
