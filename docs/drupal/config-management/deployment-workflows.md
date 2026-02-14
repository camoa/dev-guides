---
description: Deploy configuration changes safely from development to staging to production with rollback capability.
---

# Deployment Workflows

## When to Use

When deploying configuration changes from development to staging to production, ensuring safe, repeatable, rollback-capable deployments.

## Standard Deployment Workflow

1. **Develop locally** — Make config changes via UI or code
2. **Export config** — `drush cex` exports to sync directory
3. **Review changes** — `git diff config/sync/` shows what changed
4. **Commit to Git** — `git add config/sync/ && git commit -m "Add feature"`
5. **Pull on staging** — `git pull origin main` on staging server
6. **Validate changes** — `drush config:status` shows pending imports
7. **Import on staging** — `drush cim -y` imports config
8. **Test on staging** — Validate functionality, check logs
9. **Pull on production** — `git pull origin main` on production server
10. **Import on production** — `drush cim -y` imports config
11. **Validate production** — Smoke tests, monitoring

## Pre-Deployment Checklist

**Before exporting:**
- [ ] All changes tested locally
- [ ] No active config overrides (check `hasOverrides()`)
- [ ] Cache cleared (`drush cr`)
- [ ] Config schema validated (`drush config:inspect --validate-constraints`)

**Before committing:**
- [ ] Review `git diff config/sync/` — no unexpected changes
- [ ] No credentials or sensitive data in config
- [ ] Dependencies correct (check `dependencies:` keys)
- [ ] Config Split splits active (dev modules in dev split)

**Before importing on production:**
- [ ] Database backup created
- [ ] `drush config:status` reviewed — no surprises
- [ ] Deployment window scheduled (off-peak)
- [ ] Rollback plan prepared

## Example: Automated Deployment Script

```bash
#!/bin/bash
# deploy-config.sh — Safe config deployment with rollback

set -e  # Exit on error

ENVIRONMENT=$1
BRANCH=${2:-main}

echo "=== Deploying config to $ENVIRONMENT ==="

# Backup database
echo "Creating database backup..."
drush sql:dump --gzip --result-file=/backup/pre-deploy-$(date +%s).sql

# Pull code
echo "Pulling code from $BRANCH..."
git fetch origin
git checkout $BRANCH
git pull origin $BRANCH

# Check config status
echo "Checking config status..."
drush config:status

# Prompt for confirmation
read -p "Import config? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "Deployment cancelled"
  exit 1
fi

# Import config
echo "Importing config..."
drush cim -y

# Clear cache
echo "Clearing cache..."
drush cr

# Run updates
echo "Running database updates..."
drush updb -y

# Verify
echo "Verifying deployment..."
drush status

echo "=== Deployment complete ==="
```

## Rollback Strategy

**If config import fails:**
1. **Check error logs** — `drush watchdog:show` or `/admin/reports/dblog`
2. **Revert Git** — `git reset --hard HEAD~1` to previous commit
3. **Import previous config** — `drush cim -y` re-imports old config
4. **Restore database** — If necessary, restore pre-deployment backup

**If import succeeds but site broken:**
1. **Restore database backup** — Fastest rollback, loses any post-import changes
2. **Revert Git + re-import** — `git reset --hard HEAD~1 && drush cim -y`
3. **Debug specific config** — `drush config:diff NAME` to find problematic config

## Config Split in Deployment

**Dev split (local/staging only):**
```php
// settings.local.php
$config['config_split.config_split.dev']['status'] = TRUE;
```

**Prod split (production only):**
```php
// settings.php (production)
$config['config_split.config_split.prod']['status'] = TRUE;
```

**Deployment flow:**
1. Export on local with dev split active — dev modules in `config/dev/`
2. Commit both `config/sync/` and `config/dev/`
3. Import on production with prod split active — dev modules skipped, prod settings applied

## Common Mistakes

- Importing config without backup — No rollback if import breaks site
- Not reviewing `config:status` first — Blind import, unexpected changes
- Making config changes in production UI — Changes not in Git, lost on next import
- Forgetting to clear cache after import — Old cached config active
- No validation before import — Schema errors, dependency failures
- Importing partial config — Use `drush cim --partial` only when intentional

## See Also

- [Config Synchronization](config-synchronization.md) — sync workflow
- [Config Import/Export](config-import-export.md) — Drush commands
- [Config Split](config-split.md) — environment-specific config
- Reference: [Managing Your Site's Configuration](https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration)
