---
description: Configure services to control external resources (scripts, iframes, cookies) per user consent
drupal_version: "11.x"
---

# Service Configuration

## When to Use

> Configure a service when you need to control external resources (scripts, iframes, images) that collect data or set cookies. Each third-party integration requires a service definition.

## Decision

| If the service is... | Configure... | Why |
|---|---|---|
| Strictly necessary (session, security) | `required: true` | Cannot be disabled by users; GDPR allows this |
| Optional tracking/analytics | `required: false, toggled_by_default: false` | User must opt in; GDPR requirement |
| Already-tracking (legacy migration) | `opt_out: true` | Loads before consent (use cautiously; may violate laws) |
| One-time operation | `only_once: true` | Executes once even if toggled multiple times |
| Pre-configured (YouTube, Vimeo, etc.) | Use built-in service | Edit and adapt to your needs |

## Pattern

**Basic Service Configuration** (navigate to `/admin/config/user-interface/klaro/services`):

```yaml
# Create service for Google Analytics
label: "Visitor Statistics"
description: "We use Google Analytics to understand how visitors use our site."
machine_name: google_analytics  # Cannot change after creation
purposes: [statistics]  # At least one required
required: false  # Optional service
toggled_by_default: false  # User must opt in
privacy_policy_url: "https://policies.google.com/privacy"
sources:
  - "https://www.google-analytics.com/analytics.js"
  - "https://www.googletagmanager.com/gtag/js"
cookies:
  - "_ga"
  - "_gid"
  - "_gat"
callback: |
  // Initialize analytics when consent given
  if (consent) {
    gtag('config', 'GA_MEASUREMENT_ID');
  }
```

**Reference**: `/modules/contrib/klaro/src/Entity/KlaroService.php` for service entity structure

## Common Mistakes

- **Wrong**: Creating service but leaving it disabled → **Right**: Service won't appear on modal; enable when configuration complete
- **Wrong**: Not assigning a purpose → **Right**: Validation error; at least one purpose required
- **Wrong**: Using opt-out for optional services → **Right**: Illegal under GDPR; only use for strictly necessary services
- **Wrong**: Machine name with spaces/special characters → **Right**: Use underscores/lowercase only; cannot change later
- **Wrong**: Missing privacy policy URL → **Right**: Fails GDPR transparency requirement; always include
- **Wrong**: Generic descriptions like "Third-party service" → **Right**: Users can't make informed choice; explain specific purpose
- **Wrong**: Adding sources without testing → **Right**: Verify URLs are correct; incorrect sources won't be blocked properly

## See Also

- [Installation Methods](installation-methods.md)
- [Purpose Management](purpose-management.md)
- Reference: [Service Configuration Tutorial](https://www.thedroptimes.com/64498/how-set-klaro-cookie-consent-drupal-in-3-simple-steps)
