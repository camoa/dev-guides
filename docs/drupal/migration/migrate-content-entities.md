---
description: Execute migrations in dependency order with Drush commands
drupal_version: "11.x"
---

# Migrate Content Entities

## When to Use

Execute migrations in dependency order: users first, then taxonomy, files, then nodes. Use Drush commands for batch processing. Monitor progress and handle failures incrementally.

## Decision

| Execution method | Use when | Command |
|---|---|---|
| Drush import | Production migrations | `drush migrate:import migration_id` |
| Drush import group | Batch related migrations | `drush migrate:import --group=d7_content` |
| Drush status | Check progress | `drush migrate:status` |
| Drush rollback | Undo migration | `drush migrate:rollback migration_id` |
| Drush reset | Fix stuck migration | `drush migrate:reset-status migration_id` |

## Pattern

**Standard migration execution order:**

```bash
# 1. Users (no dependencies)
drush migrate:import d7_user --execute-dependencies

# 2. Taxonomy (depends on users for term authors)
drush migrate:import d7_taxonomy_term_tags
drush migrate:import d7_taxonomy_term_category

# 3. Files (depends on users for file owners)
drush migrate:import d7_file

# 4. Paragraphs (if used, before nodes)
drush migrate:import d7_paragraph_slide
drush migrate:import d7_paragraph_testimonial

# 5. Nodes (depends on all above)
drush migrate:import d7_node_article
drush migrate:import d7_node_page
drush migrate:import d7_node_landing_page

# Check status
drush migrate:status --group=d7_content

# Rollback if needed (reverse order)
drush migrate:rollback d7_node_article
drush migrate:rollback d7_file
drush migrate:rollback d7_user
```

**Reference**: `/modules/contrib/migrate_tools/src/Commands/MigrateToolsCommands.php` for Drush commands

## Common Mistakes

- **Wrong**: Migrating nodes before referenced entities → **Right**: Lookup failures, broken references
- **Wrong**: Not monitoring memory during large migrations → **Right**: PHP memory exhaustion on high-volume imports
- **Wrong**: Running full migration without testing → **Right**: Use limit option for testing: `--limit=10`
- **Wrong**: Not resetting stuck migrations → **Right**: Status shows "Importing" forever after crashes

## See Also

- [Handle field mappings](handle-field-mappings.md) for process configuration
- [Performance optimization](performance-optimization.md) for large-scale imports
- [Debug migration failures](debug-migration-failures.md) for troubleshooting
- Reference: [Executing migrations](https://www.drupal.org/docs/drupal-apis/migrate-api/executing-migrations)
