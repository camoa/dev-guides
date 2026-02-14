---
description: Manage environment-specific configuration with Config Split — dev modules, production settings, conditional overrides.
---

# Config Split

## When to Use

When you need to manage environment-specific configuration (dev modules, production settings) that should not be deployed to all environments.

## Config Split Concepts

**Complete Split** — Config removed from sync directory, only in split directory
- Use for: Dev modules (Devel, Webprofiler), environment-specific features
- On import: Config imported only if split is active in settings.php

**Conditional Split** — Config in both sync and split directories
- Use for: Config that differs per environment (settings, overrides)
- On import: Split version takes precedence if split is active

**Gray Split** — Config partially exported (subset of keys)
- Use for: Config where some keys are environment-specific (API keys)

## Pattern

```bash
# Install Config Split
composer require drupal/config_split

# Enable Config Split
drush en config_split -y

# Create split via UI: /admin/config/development/configuration/config-split
```

**Example: Dev Split Configuration**
```yaml
# config/sync/config_split.config_split.dev.yml
id: dev
label: 'Development'
folder: ../config/dev
module:
  devel: 0
  webprofiler: 0
  stage_file_proxy: 0
theme: {}
blacklist: []
graylist:
  - system.performance
graylist_dependents: true
graylist_skip_equal: true
weight: 0
status: true
```

**Reference:** Config Split contrib module at `/modules/contrib/config_split/`

## Workflow: Complete Split for Dev Modules

1. **Install dev modules** on local environment
2. **Create dev split** via UI: `/admin/config/development/configuration/config-split/add`
3. **Select dev modules** to split (Devel, Webprofiler, etc.)
4. **Export config** — `drush cex` exports to both sync and dev directories
5. **Activate split** in settings.local.php:
   ```php
   $config['config_split.config_split.dev']['status'] = TRUE;
   ```
6. **Commit both directories** — `config/sync/` and `config/dev/`
7. **Deploy to production** — Pull code
8. **Don't activate split** — Omit settings.php activation on prod
9. **Import config** — `drush cim` skips dev modules (split inactive)

## Workflow: Conditional Split for Settings

1. **Create prod split** for production-specific config
2. **Add config to graylist** — `system.performance`, `system.logging`
3. **Set production values** in split
4. **Activate prod split** only in production settings.php:
   ```php
   $config['config_split.config_split.prod']['status'] = TRUE;
   ```
5. **Export config** — Both sync and prod directories updated
6. **Import on each environment** — Active split takes precedence

## Settings.php Integration

```php
// settings.local.php (local/dev)
$config['config_split.config_split.dev']['status'] = TRUE;
$config['config_split.config_split.prod']['status'] = FALSE;

// settings.php (production, not gitignored)
$config['config_split.config_split.dev']['status'] = FALSE;
$config['config_split.config_split.prod']['status'] = TRUE;

// Or use environment variable
if (getenv('ENVIRONMENT') === 'dev') {
  $config['config_split.config_split.dev']['status'] = TRUE;
}
```

## Drush Commands

```bash
# Export with Config Split
drush cex -y
# Automatically splits config based on active splits

# Import with Config Split
drush cim -y
# Automatically merges splits based on active splits

# Export specific split
drush config-split:export dev

# Import specific split
drush config-split:import dev

# Check split status
drush config-split:status
```

## Common Mistakes

- Not activating split in settings.php — Split config ignored on import
- Activating wrong split on environment — Dev modules on production, prod settings on dev
- Using split for credentials — Use settings.php overrides instead (not exported)
- Graylist without skip_equal — Unnecessary exports when values identical
- Not gitignoring settings.local.php — Environment-specific split activation committed
- Forgetting to commit split directory — Split config missing from repo

## See Also

- [Config Synchronization](config-synchronization.md) — base sync workflow
- [Config Override System](config-override-system.md) — runtime overrides vs split
- [Deployment Workflows](deployment-workflows.md) — using splits in deployment
- Reference: [Configuration Split Documentation](https://www.drupal.org/docs/contributed-modules/configuration-split)
- Reference: [Creating a Simple Split Configuration](https://www.drupal.org/docs/contributed-modules/configuration-split/creating-a-simple-split-configuration-dev-modules-only-in-dev-environments)
