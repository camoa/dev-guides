---
description: Never remove a module from composer.json before all environments have uninstalled it via drush config:import — wrong order causes fatal bootstrap errors.
drupal_version: "11.x"
tldr: Never remove modules from `composer.json` before all environments have uninstalled them via `drush config:import`. CI/CD runs `composer install` — missing packages cause fatal errors.
---

# Composer Module Removal Order

**What:** Never remove modules from `composer.json` before all environments have uninstalled them via `drush config:import`. CI/CD runs `composer install` — missing packages cause fatal errors.

**Rationale:** Module uninstall is a config operation: it removes the module from `core.extension.yml` and lets Drupal cleanly remove its config and tables. If you remove the package from `composer.json` first, the next `composer install` fails to find a module that's still listed in active config. The site bootstraps fail with class-not-found errors, deployments break, and rolling back means re-adding the package.

**When it applies:** Every module removal. The correct sequence: uninstall via UI/drush → export config (removes from `core.extension`) → deploy that config to all environments → THEN remove from `composer.json` → deploy.

**Example:**

```bash
# Right — sequenced removal
# Step 1: locally
drush pm:uninstall mymodule
drush config:export
git add config/sync/core.extension.yml config/sync/mymodule.*
git commit -m "Uninstall mymodule"
# Deploy to staging → production. Verify drush config:status is clean everywhere.

# Step 2: only after all environments have imported the config
composer remove drupal/mymodule
git add composer.json composer.lock
git commit -m "Remove mymodule package"
# Deploy. composer install now succeeds — the module isn't referenced in active config.

# Wrong — reverse order, breaks composer install
composer remove drupal/mymodule    # ← class not found on next install
```
