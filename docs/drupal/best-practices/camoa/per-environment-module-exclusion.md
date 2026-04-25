---
description: Use $settings['config_exclude_modules'] to prevent environment-specific module config (GTM, profiling) from being overwritten by config:import.
drupal_version: "11.x"
tldr: Modules with environment-specific config (Google Tag Manager, error reporting, profiling) use `$settings['config_exclude_modules']` in `settings.php` to exclude from config export/import.
---

# Per-Environment Module Exclusion

**What:** Modules with environment-specific config (Google Tag Manager, error reporting, profiling) use `$settings['config_exclude_modules']` in `settings.php` to exclude from config export/import.

**Rationale:** Some modules need different config per environment — GTM container ID is different on staging vs production; error reporting verbosity differs in dev. Config sync is one-way: what's in `config/sync` overwrites the active site. Without exclusion, deploying staging config to production overwrites the prod GTM container with the staging one. `config_exclude_modules` tells the config system to leave those modules' config alone during import.

**When it applies:** Modules whose config legitimately differs per environment. NOT a workaround for accidental local-only config drift — that's a separate problem (use `drush config:export` discipline).

**Example:**

```php
// settings.php (or a per-environment include like settings.local.php)
$settings['config_exclude_modules'] = [
  'google_tag',           // GTM container ID per env
  'config_inspector',     // dev-only diagnostic module
  'devel',                // dev-only
  'webprofiler',          // dev-only
];
```

```bash
# Verify the exclusion is honored
drush config:status      # excluded modules' config doesn't appear as "different"
drush config:import     # excluded modules' active config is preserved
```
