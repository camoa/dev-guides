---
description: Manage environment-specific configuration with Config Split and settings.php overrides to avoid duplicating config across dev/staging/prod.
---

# Config Split and Environments

## When to Use

When you need different configuration across environments (dev modules in dev only, production API keys in prod only) without duplicating config or managing it manually.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Dev modules only in dev | Config Split | Automatic, no manual enable/disable |
| Environment-specific simple values (API keys) | `$config` overrides in settings.php | Simple, no module needed |
| Different modules per environment | Config Split | Manages both module config and enabled state |
| Sensitive values not in version control | `$config` overrides + secrets management | Security best practice |
| Identical config across all environments | Standard config management (no split) | Simplest approach |

## Pattern

```yaml
# config/sync/config_split.config_split.dev.yml
id: dev
label: Development
folder: ../config/envs/dev
module:
  devel: 0
  kint: 0
  stage_file_proxy: 0
theme: {}
```

```php
// settings.php - Environment detection and split activation
if (getenv('ENVIRONMENT') === 'dev') {
  $config['config_split.config_split.dev']['status'] = TRUE;
}
elseif (getenv('ENVIRONMENT') === 'prod') {
  $config['config_split.config_split.prod']['status'] = TRUE;
}
```

```php
// settings.php - Simple config overrides (preferred for simple values)
if (getenv('ENVIRONMENT') === 'prod') {
  $config['mymodule.settings']['api_key'] = getenv('API_KEY');
  $config['system.logging']['error_level'] = 'hide';
}
```

Reference: Config Split module at `modules/contrib/config_split/`, `sites/default/settings.php`

## Workflow

1. **Install Config Split** — `composer require drupal/config_split`
2. **Create split configs** — Via UI or YAML in `config/sync/`
3. **Configure environment detection** — In `settings.php`, activate appropriate split
4. **Export config** — `drush config:export` exports split configs
5. **Deploy** — On each environment, `drush config:import` applies correct split

## Config Overrides vs Config Split

| Use Config Overrides When... | Use Config Split When... |
|------------------------------|---------------------------|
| Simple value changes (API keys, flags) | Entire modules differ per environment |
| Values shouldn't be in version control | Config should be in version control but different per env |
| Quick, single-value changes | Complex, multi-config differences |

## Common Mistakes

- **Storing secrets in version control** — Use `$config` overrides from environment variables, not config files
- **Manually enabling/disabling modules per environment** — Let Config Split handle module state
- **Not exporting config after split setup** — Config Split config must be exported like any other config
- **Overusing splits** — Start simple with `$config` overrides; use splits only when needed for modules or complex multi-config changes
- **Forgetting to set split status in settings.php** — Splits must be activated per environment

## See Also

- [Hook and Event Reuse](hook-event-reuse.md)
- [Recipes for Reusable Config](recipes-reusable-config.md)
- Reference: [Configuration Split | Drupal.org](https://www.drupal.org/docs/contributed-modules/configuration-split)
- Reference: [Per Environment Configuration | Drupal.org](https://www.drupal.org/docs/contributed-modules/configuration-split/per-environment-configuration)
