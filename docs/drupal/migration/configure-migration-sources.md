---
description: Configure D7 database connection and source plugins for Migrate API
drupal_version: "11.x"
---

# Configure Migration Sources

## When to Use

Set up D7 database connection as migration source. Core provides source plugins for D7 nodes, users, taxonomy, files. Configure database credentials without editing settings.php (security risk).

## Decision

| Source type | Plugin | Configuration method |
|---|---|---|
| D7 MySQL database (same server) | d7_node, d7_user, etc. | settings.php database array |
| D7 database (different server) | d7_node, d7_user, etc. | settings.php with separate host |
| D7 database (wizard UI) | Same plugins | Migrate Wizard UI form |
| CSV/JSON files | migrate_source_csv | File path in source config |

## Pattern

**Database source configuration in settings.php:**

```php
// settings.php (D11 site)
$databases['migrate']['default'] = [
  'database' => 'd7_database_name',
  'username' => 'd7_db_user',
  'password' => 'd7_db_password',
  'host' => 'localhost',
  'port' => '3306',
  'driver' => 'mysql',
  'prefix' => '',
  'collation' => 'utf8mb4_general_ci',
];
```

**Migration YAML using database source:**

```yaml
source:
  plugin: d7_node
  node_type: page
  # Uses 'migrate' database connection from settings.php
```

**Reference**: `/core/modules/migrate_drupal/src/Plugin/migrate/source/` for D7 source plugins

## Common Mistakes

- **Wrong**: Editing settings.php on production → **Right**: Use settings.local.php or environment-specific includes
- **Wrong**: Using same database for D7 and D11 → **Right**: Keep databases separate, prevent conflicts
- **Wrong**: Hardcoding credentials in migration YAML → **Right**: Use settings.php database arrays
- **Wrong**: Not testing database connection → **Right**: Run test query before starting migrations

## See Also

- [Create migration definitions](create-migration-definitions.md) for YAML configuration
- Reference: [Executing migrations](https://www.drupal.org/docs/drupal-apis/migrate-api/executing-migrations)
