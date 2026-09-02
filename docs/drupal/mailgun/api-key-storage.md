---
description: "Store the Mailgun API key securely using environment variables, Key module, or UI-only (with config exclusion) — never in git."
tldr: "Inject the Mailgun API key via getenv() in settings.php as the default method; never commit mailgun.settings.yml to git — add mailgun to config_exclude_modules first and rotate immediately if a key is accidentally committed."
drupal_version: "10.3+/11/12"
---

# API Key Storage

## When to Use

> At any point — but ideally before saving the API key in the UI for the first time. The choice affects security posture, multi-environment workflow, and audit trail.

## Decision

| Storage method | Security | Multi-env | Maturity | Recommended |
|---|---|---|---|---|
| **Environment variable via `settings.php`** (`getenv()`) | High — never on disk in git | Excellent | Stable, works today | **Yes (default)** |
| **Key module (#3452693 patch)** | Highest — supports HSM/KMS via Key providers | Excellent | Patch pending merge as of April 2026 | Yes if you already use Key module |
| **Plain config in `mailgun.settings.yml`** | Low — committed to git | Poor | Trivial | **Never** |
| **UI-only, with `config_exclude_modules`** | Medium — in active config (DB) but not in git | Per-environment manual | Stable | OK for solo projects, painful at scale |

## Pattern

#### Method 1: Environment variable (recommended)

In `settings.php`:

```php
if ($key = getenv('MAILGUN_API_KEY')) {
  $config['mailgun.settings']['api_key'] = $key;
}
```

Set the env var per environment (DDEV, Pantheon, Platform.sh, etc. — see [Settings Configuration](settings-configuration.md)).

The Mailgun module reads `api_key` via Drupal's Config API, so the override layer applies. Confirmed working as of module 2.1.0.

#### Method 2: Key module (with patch)

Apply patch from [issue #3452693](https://www.drupal.org/node/3452693) (16.43 KB; confirmed working on Drupal 11.2.5 + Mailgun 2.1.0 as of October 2025).

```bash
# Install
ddev composer require drupal/key:^1.18 cweagans/composer-patches:^1.7
# Apply patch (see [Module Installation](module-installation.md) for composer.json patches block)
ddev composer install
ddev drush en key -y

# Create a Key entity
# /admin/config/system/keys/add
# - Key type: Authentication
# - Key provider: Configuration / File / Environment / etc.
# - For env: set MAILGUN_API_KEY env var; provider reads it

# In Mailgun config UI, the API key field becomes a Key selector
# /admin/config/services/mailgun → choose your Key entity
```

The patch falls back to plain string if Key entity not loadable, so existing setups don't break.

#### Method 3: Plain config (anti-pattern — listed for awareness)

```yaml
# config/sync/mailgun.settings.yml — DO NOT DO THIS
api_key: 'key-abc123def456...'
api_endpoint: 'https://api.mailgun.net'
working_domain: 'mg.example.com'
```

If this happens accidentally:
1. **Rotate the key immediately** in Mailgun dashboard
2. Add `mailgun` to `config_exclude_modules`
3. Re-export config: `drush cex -y`
4. Confirm the file is gone from `config/sync/`
5. Force-push the removal to all branches; rotate again if the key was on public GitHub

## Common Mistakes
- **Wrong**: Storing the API key in `.env` and assuming Drupal reads it → **Right**: Drupal's `getenv()` reads OS environment; `.env` requires a loader. Use DDEV's `web_environment` or hosting provider secrets.
- **Wrong**: Using a single API key across all environments → **Right**: One key per environment minimum. Compromise of dev key shouldn't expose prod.
- **Wrong**: Committing `config/sync/mailgun.settings.yml` and adding it to `.gitignore` later → **Right**: Git history retains the key. Rotate it.

## See Also
- [Settings Configuration](settings-configuration.md)
- Reference: [Issue #3452693 — Add Key module support](https://www.drupal.org/node/3452693)
- Reference: [drupal/key project](https://www.drupal.org/project/key)
