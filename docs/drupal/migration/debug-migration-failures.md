---
description: Logging, verbose output, and debugging techniques for migration failures
drupal_version: "11.x"
---

# Debug Migration Failures

## When to Use

Migrations fail for many reasons: missing dependencies, data type mismatches, plugin errors. Use logging, verbose output, and incremental testing to isolate issues.

## Decision

| Failure symptom | Debug approach | Command |
|---|---|---|
| Migration shows "Importing" forever | Reset status | `drush migrate:reset-status migration_id` |
| Row errors during import | Verbose messages | `drush migrate:import --feedback=1` |
| Dependency errors | Check migration order | `drush migrate:status --group=d7` |
| Process plugin failures | Review messages table | Query migrate_message_* tables |
| Unknown source data structure | Inspect source | Add debug in prepareRow() |

## Pattern

**Debugging workflow:**

```bash
# 1. Check migration status
drush migrate:status

# 2. Enable verbose feedback (shows each row)
drush migrate:import d7_node_article --limit=1 --feedback=1

# 3. Check messages table for errors
drush sqlq "SELECT * FROM migrate_message_d7_node_article LIMIT 10"

# 4. Review migration configuration
drush config:get migrate_plus.migration.d7_node_article

# 5. Reset if stuck
drush migrate:reset-status d7_node_article

# 6. Test single source ID
drush migrate:import d7_node_article --idlist=123
```

**Custom debug logging:**

```php
// In custom process plugin or source
public function transform($value, MigrateExecutableInterface $migrate_executable, Row $row, $destination_property) {
  // Debug logging
  \Drupal::logger('my_migration')->debug('Processing @property: @value', [
    '@property' => $destination_property,
    '@value' => print_r($value, TRUE),
  ]);

  // Your transformation
  return $transformed_value;
}
```

**Reference**: `/modules/contrib/migrate_tools/src/MigrateExecutable.php` for migration execution

## Common Mistakes

- **Wrong**: Not reading error messages → **Right**: migrate_message tables contain specific failure reasons
- **Wrong**: Testing full migration after code changes → **Right**: Test with --limit=1 first
- **Wrong**: Not using --feedback flag → **Right**: Can't see which row failed
- **Wrong**: Ignoring warnings → **Right**: Warnings often indicate data quality issues
- **Wrong**: Not version controlling migration YAML → **Right**: Hard to track what changed

## See Also

- [Test migration results](test-migration-results.md) for validation
- Reference: [Migrate API debugging](https://www.drupal.org/docs/drupal-apis/migrate-api)
