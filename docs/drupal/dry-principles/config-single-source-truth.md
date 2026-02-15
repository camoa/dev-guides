---
description: Use Drupal's configuration system as the single source of truth for site settings, entity definitions, and environment-portable values.
---

# Config as Single Source of Truth

## When to Use

Whenever you need to store site settings, entity definitions, field configurations, view definitions, or any setting that should be consistent across environments.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Site name, slogan, email | `system.site` config | Already exists, UI-editable, version-controlled |
| Module settings, API keys | Custom config entity (`mymodule.settings`) | Exportable, overridable per environment |
| Field definitions, entity types | Config entities via UI or install config | Schema-driven, validated, portable |
| Different values per environment (dev/prod) | Config overrides in settings.php or Config Split | Environment-specific without code changes |
| Never store in code | Nothing — read from config | Config is the source of truth |

## Pattern

```yaml
# config/install/mymodule.settings.yml
api:
  endpoint: 'https://api.example.com'
  timeout: 30
cache:
  enabled: true
  ttl: 3600
```

```php
// Read config (never duplicate values)
$config = $this->configFactory->get('mymodule.settings');
$endpoint = $config->get('api.endpoint');
$timeout = $config->get('api.timeout');

// WRONG: Duplicating config in code
const API_ENDPOINT = 'https://api.example.com'; // Don't do this

// Write config (only in install/update hooks or admin forms)
$config = $this->configFactory->getEditable('mymodule.settings');
$config->set('api.endpoint', $form_state->getValue('endpoint'))->save();
```

Reference: `core/lib/Drupal/Core/Config/ConfigFactoryInterface.php`, `core/modules/system/config/install/system.site.yml`

## Workflow for Config Changes

1. **Make change on local** — Update via UI or modify YAML in `config/sync/`
2. **Export config** — `drush config:export` (or `drush cex`)
3. **Commit to version control** — Config files in `config/sync/` directory
4. **Deploy to other environments** — Pull code, run `drush config:import` (or `drush cim`)
5. **Verify** — Check that changes applied correctly

This workflow ensures config is the single source of truth across all environments.

## Common Mistakes

- **Hardcoding values that belong in config** — Use config, not constants or hardcoded strings
- **Storing config in code variables** — Read dynamically from config, don't cache in class properties
- **Not exporting config after changes** — Changes via UI won't deploy unless exported
- **Mixing config and content** — Content entities (nodes, users) are not config; config entities (views, field definitions) are config
- **Ignoring config schema** — Define schema in `mymodule.schema.yml` for validation and IDE support

## See Also

- [DRY in Drupal Overview](dry-drupal-overview.md)
- [Services for Shared Logic](services-shared-logic.md)
- Reference: [Drupal's Configuration Management: Best Practices](https://reintech.io/blog/drupals-configuration-management-best-practices)
- Reference: [Configuration API | Drupal.org](https://www.drupal.org/docs/drupal-apis/configuration-api)
