---
description: Store the Mailgun API key securely using environment variables, Key module, or UI-only (with config exclusion) — never in git.
tldr: Inject the Mailgun API key via getenv() in settings.php as the default method; never commit mailgun.settings.yml to git — add mailgun to config_exclude_modules first and rotate immediately if a key is accidentally committed.
drupal_version: "11.x"
---

# API Key Storage

## When to Use

> Use this at any point — but ideally before saving the API key in the UI for the first time. The choice affects security posture, multi-environment workflow, and audit trail.

## Decision

| Storage method | Security | Multi-env | Recommended |
|----------------|----------|-----------|-------------|
| **Environment variable via `settings.php`** | High — never on disk in git | Excellent | **Yes (default)** |
| **Key module (#3452693 patch)** | Highest — supports HSM/KMS via Key providers | Excellent | Yes if you already use Key module |
| **Plain config in `mailgun.settings.yml`** | Low — committed to git | Poor | **Never** |
| **UI-only, with `config_exclude_modules`** | Medium — in active config (DB) only | Per-environment manual | OK for solo projects |

## Pattern

#### Method 1: Environment variable (recommended)

```php
// settings.php
if ($key = getenv('MAILGUN_API_KEY')) {
  $config['mailgun.settings']['api_key'] = $key;
}
```

Set the env var per environment. The Mailgun module reads `api_key` via Drupal's Config API, so the override layer applies. Confirmed working as of module 2.1.0.

#### Method 2: Key module (with patch)

Apply patch from [issue #3452693](https://www.drupal.org/node/3452693) (confirmed working on Drupal 11.2.5 + Mailgun 2.1.0 as of October 2025).

```bash
ddev composer require drupal/key:^1.18 cweagans/composer-patches:^1.7
ddev drush en key -y
# /admin/config/system/keys/add — create Key entity with env provider
# /admin/config/services/mailgun — API key field becomes a Key selector
```

#### Method 3: Plain config — anti-pattern; listed for recovery only

If a key was accidentally committed:

1. **Rotate the key immediately** in Mailgun dashboard
2. Add `mailgun` to `config_exclude_modules`
3. Run `drush cex -y` — confirm the file is gone from `config/sync/`
4. Force-push the removal to all branches; rotate again if the key was on public GitHub

## Common Mistakes

- **Wrong**: Storing the API key in `.env` and assuming Drupal reads it → **Right**: `getenv()` reads OS environment; `.env` requires a loader. Use DDEV's `web_environment` or hosting provider secrets.
- **Wrong**: Using a single API key across all environments → **Right**: One key per environment minimum. Compromise of dev key shouldn't expose prod.
- **Wrong**: Committing `config/sync/mailgun.settings.yml` and adding it to `.gitignore` later → **Right**: Git history retains the key. Rotate it.

## See Also

- [Settings Configuration](settings-configuration.md)
- Reference: [Issue #3452693 — Add Key module support](https://www.drupal.org/node/3452693)
- Reference: [drupal/key project](https://www.drupal.org/project/key)
