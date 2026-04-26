---
description: Choose between Mailgun's US and EU regions when creating a sending domain — region mismatch is the top cause of 401 errors.
tldr: Default to the US region unless GDPR or contractual requirements mandate EU data residency; the region choice is permanent per domain and a US API key will return 401 Unauthorized if used against the EU endpoint.
drupal_version: "11.x"
---

# Region Selection

## When to Use

> Use this when creating a Mailgun account or adding a sending domain. The region choice affects where email content is stored and which API endpoint your Drupal site hits. The choice is not retroactive — wrong-region keys won't authenticate.

## Decision

| Region | API host | SMTP host | Use When |
|--------|----------|-----------|----------|
| **US** | `api.mailgun.net` | `smtp.mailgun.org` | Default. US data residency acceptable. Lower latency from US servers. |
| **EU** | `api.eu.mailgun.net` | `smtp.eu.mailgun.org` | GDPR data-residency requires EU storage of email content/metadata. |

## Pattern

**Picking a region:**
1. Default to US unless legal/contractual requirement specifies EU
2. If GDPR scope: pick EU at account/domain creation
3. Decision is per-domain — you can have US and EU domains in the same Mailgun account, but each needs its own API key

**Setting region in drupal/mailgun** (`settings.php`):

```php
$config['mailgun.settings']['api_endpoint'] = 'https://api.eu.mailgun.net';
```

**Setting region in Symfony Mailer DSN:**

```yaml
mailer_dsn:
  scheme: mailgun+api
  host: default
  user: '{{ MAILGUN_API_KEY }}'
  password: 'mg.example.com'
  options:
    region: eu
```

Or via Admin UI: `/admin/config/services/mailgun` → "API endpoint" dropdown.

## Common Mistakes

- **Wrong**: Generating an API key on the US dashboard but configuring Drupal to use `api.eu.mailgun.net` → **Right**: 401 Unauthorized — region mismatch is the #1 support ticket. Match endpoint to where the domain was created.
- **Wrong**: Assuming you can switch regions later → **Right**: Effectively no — the domain belongs to one region; to migrate, recreate the domain in the other region, redo DNS, regenerate keys.

## See Also

- [Common Errors](common-errors.md) — 401 troubleshooting
- [API Key Storage](api-key-storage.md)
