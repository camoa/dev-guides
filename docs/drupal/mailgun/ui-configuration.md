---
description: Configure the Mailgun module admin UI with API key, working domain, region, tracking defaults, and per-environment overrides.
tldr: Navigate to /admin/config/services/mailgun and configure the Private/Sending API key, working domain, and API endpoint per environment; use settings.php env-var overrides rather than hardcoding values that differ between dev, stage, and prod.
drupal_version: "11.x"
---

# UI Configuration

## When to Use

> Use this after installing the module and configuring `system.mail.yml`. The UI configures the API key, working domain, region, and tracking defaults — values that are per-environment and should NOT be in git.

## Decision

| Field | Source |
|-------|--------|
| API key | Mailgun dashboard → "API Security" → Add new key (Private/Sending key) |
| Working domain | The verified domain you'll send from (e.g., `mg.example.com`) |
| API endpoint | `api.mailgun.net` (US) or `api.eu.mailgun.net` (EU) |
| Format | HTML or plain text default |
| Tracking | Whether to enable click/open tracking globally |
| Test mode | Send via Mailgun's test endpoint (no real delivery) |

## Pattern

Navigate to `/admin/config/services/mailgun`:

| Section | Setting | Recommended |
|---------|---------|-------------|
| API Settings | API Key | Paste Private/Sending key from Mailgun dashboard |
| API Settings | API endpoint | Match the region of your domain |
| API Settings | Working domain | Your verified Mailgun domain (e.g., `mg.example.com`) |
| Defaults | From email | `noreply@mg.example.com` |
| Defaults | From name | Your site name |
| Tracking | Enable open tracking | Yes for transactional |
| Tracking | Enable click tracking | Yes; can break email signature links if not customized |
| Test mode | Use test mode | OFF in production; ON when running automated tests |

After saving, click "Send test email" (or visit `/admin/config/services/mailgun/test` if `mailgun_test_form` enabled).

#### Per-environment overrides via settings.php

```php
$config['mailgun.settings']['working_domain'] = getenv('MAILGUN_DOMAIN');
$config['mailgun.settings']['api_endpoint'] = getenv('MAILGUN_API_ENDPOINT');
$config['mailgun.settings']['test_mode'] = filter_var(getenv('MAILGUN_TEST_MODE'), FILTER_VALIDATE_BOOLEAN);
```

| Environment | Working domain | Test mode |
|-------------|----------------|-----------|
| Dev | sandbox domain | ON |
| Stage | prod domain OR separate stage domain | ON |
| Prod | prod domain (`mg.example.com`) | OFF |

## Common Mistakes

- **Wrong**: Using "Public API key" → **Right**: Use the Private/Sending API key. Public keys are for read-only operations like email validation.
- **Wrong**: Configuring once in dev and assuming prod is set → **Right**: Per-environment config; configure each separately or use env-var injection.
- **Wrong**: Leaving "Test mode" on in production → **Right**: Test mode means Mailgun accepts the API call but doesn't deliver.
- **Wrong**: Forgetting to save the API key after pasting → **Right**: Click "Save configuration" at the bottom of the form.

## See Also

- [API Key Storage](api-key-storage.md)
- [Verification & Testing](verification-testing.md)
