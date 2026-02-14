---
description: Sync configuration between environments — export from dev, commit to Git, import to staging/production.
---

# Config Synchronization

## When to Use

When you need to sync configuration between environments — export config from dev, commit to Git, import to staging/production.

## Workflow

The config sync process compares active storage (database) vs sync storage (files), identifies differences, validates dependencies, and imports changes in dependency order.

## Steps

1. **Make config changes** — Via admin UI or code on local environment
2. **Export active config** — `drush cex` writes database config to sync directory
3. **Review changes** — `git diff` shows what changed
4. **Commit to version control** — `git add config/sync && git commit`
5. **Deploy to target environment** — `git pull` on staging/production
6. **Import config** — `drush cim` reads sync files, writes to database
7. **Validate** — Check site, test functionality

## Example: Full Sync Workflow

```bash
# Local environment — make changes via UI
# Export config
drush cex -y

# Review changes
git status
git diff config/sync/

# Commit
git add config/sync/
git commit -m "Add custom block type configuration"
git push origin main

# Production environment — pull code
git pull origin main

# Review import changes
drush config:status

# Import config
drush cim -y

# Clear cache
drush cr
```

**Reference:** `/core/lib/Drupal/Core/Config/ConfigImporter.php`, `/core/lib/Drupal/Core/Config/StorageComparer.php`

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Before export | Config in active storage differs from sync | Run `drush cex` to export |
| Before import | Sync files differ from active storage | Run `drush cim` to import |
| Reviewing changes | Many unexpected changes | Check for overrides, validate schema |
| Import fails | Dependency errors | Fix dependencies, import in order |
| Import fails | Validation errors | Fix schema issues, check constraints |
| After import | Features not working | Clear cache with `drush cr` |

## Config Status Commands

```bash
# Check differences between active and sync
drush config:status

# View specific config differences
drush config:diff system.site

# Export single config item
drush config:export system.site

# Import single config item
drush config:import system.site
```

## Common Mistakes

- Making config changes in production — Changes not in Git, lost on next import
- Not reviewing config diff before commit — Unexpected changes slip through
- Importing without checking status — Blindly overwriting production config
- Skipping dependency validation — Import fails mid-process, site broken
- Not clearing cache after import — Old cached config still in use
- Mixing manual and CM changes — Config drift between environments

## See Also

- [Config Import/Export](config-import-export.md) — Drush commands in detail
- [Config Split](config-split.md) — environment-specific config
- [Deployment Workflows](deployment-workflows.md) — production deployment patterns
- Reference: [Managing Your Site's Configuration](https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration)
