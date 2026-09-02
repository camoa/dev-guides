---
description: "Configure settings.php to exclude Mailgun config from git export and inject the API key from environment variables."
tldr: "Always add mailgun to config_exclude_modules before saving the API key, then inject the key via getenv() in settings.php; skipping config_exclude_modules commits the API key to git on the next drush cex."
drupal_version: "10.3+/11/12"
---

# Settings Configuration

## When to Use

> Right after enabling the Mailgun module, before configuring the API key. Two `settings.php` changes are required regardless of how you store the key.

## Decision

| Setting | Purpose | Required? |
|---|---|---|
| `$settings['config_exclude_modules'][]` | Prevents `mailgun.settings.yml` from being exported to `config/sync` (and thus from being committed to git) | **Yes** |
| `$config['mailgun.settings']['api_key']` | Injects the API key from environment variable, bypassing UI storage | Recommended (see [API Key Storage](api-key-storage.md)) |
| `$config['mailgun.settings']['api_endpoint']` | Forces a specific region per environment | Optional — useful when dev uses sandbox (US) and prod uses EU |

## Pattern

#### Exclude Mailgun config from export (always)

In `web/sites/default/settings.php`:

```php
// Add 'mailgun' to the existing list (or create the line if absent)
$settings['config_exclude_modules'] = ['mailgun'];

// If you already exclude other modules:
$settings['config_exclude_modules'] = ['brevo', 'brevo_mailer', 'mailsystem', 'mailgun'];
```

The result: `drush config:export` will NOT write `config/sync/mailgun.settings.yml`. The API key, configured via UI, lives only in active config (database) and is set per-environment.

#### Inject API key from environment (recommended)

```php
// settings.php (or settings.local.php for dev)
if ($key = getenv('MAILGUN_API_KEY')) {
  $config['mailgun.settings']['api_key'] = $key;
}

// Optional: same pattern for endpoint
if ($endpoint = getenv('MAILGUN_API_ENDPOINT')) {
  $config['mailgun.settings']['api_endpoint'] = $endpoint;
}
```

Set `MAILGUN_API_KEY` per environment:

| Hosting | Where to set |
|---|---|
| DDEV (local) | `.ddev/config.yaml` `web_environment:` block |
| Pantheon | Pantheon Secrets API or `pantheon.yml` |
| Acquia Cloud | Cloud UI → Secrets, or `settings.acquia.php` |
| Platform.sh | `.platform.app.yaml` `variables:` or CLI `platform variable:create` |
| Lando | `.lando.yml` `services.appserver.overrides.environment` |
| Plain VM | `/etc/environment` or systemd unit `Environment=` directive |

DDEV example (`.ddev/config.yaml`):

```yaml
web_environment:
  - MAILGUN_API_KEY=key-abc123def456...
  - MAILGUN_API_ENDPOINT=https://api.eu.mailgun.net
```

After editing: `ddev restart`.

## Common Mistakes
- **Wrong**: Forgetting `config_exclude_modules` and committing the API key to git → **Right**: Always add `mailgun` to the exclusion list before saving the API key in the UI.
- **Wrong**: Using `Settings::get()` to read the API key in custom code → **Right**: Read it via `\Drupal::config('mailgun.settings')->get('api_key')` so the env override layer applies.
- **Wrong**: Setting `MAILGUN_API_KEY` only in `.env` and expecting Drupal to read it → **Right**: `getenv()` in `settings.php` reads OS environment; `.env` files require separate loaders (vlucas/phpdotenv) or DDEV's `web_environment`.

## See Also
- [Mail Routing](mail-routing.md)
- [API Key Storage](api-key-storage.md)
- Reference: [Drupal config override system](https://www.drupal.org/docs/8/api/configuration-api/configuration-override-system)
