---
description: Understand when and why to use consent management for GDPR and privacy compliance
drupal_version: "11.x"
---

# What is Consent Management

## When to Use

> Use consent management when your Drupal site loads external resources (scripts, iframes, images) that may collect visitor data or set cookies. Required for GDPR, ePrivacy Directive, and similar privacy regulations.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| GDPR compliance for EU visitors | Klaro with Notice/Modal mode | Explicit consent required before tracking |
| Block third-party scripts until consent | Klaro with automatic attribution | Prevents scripts from loading before user accepts |
| Simple "necessary cookies only" notice | Klaro Silent mode | No dialog displayed, just blocks external resources |
| Granular service control | Klaro with purposes/services | Users can accept/reject individual services |

## Pattern

Klaro manages consent through two concepts:

```yaml
# Service definition (what resource to control)
service:
  name: google_analytics
  purposes: [statistics]
  sources: ['https://www.google-analytics.com/analytics.js']

# User consent decision (stored in cookie/localStorage)
consent:
  google_analytics: true  # User accepted this service
```

**Reference**: `/modules/contrib/klaro/` module structure

## Common Mistakes

- **Wrong**: Loading tracking scripts before obtaining consent → **Right**: Configure automatic attribution to block scripts until consent
- **Wrong**: Using "opt-out" for optional services → **Right**: Illegal under GDPR; only strictly necessary services can default to enabled
- **Wrong**: Setting cookies on third-party domains then trying to delete them → **Right**: Impossible due to browser security; block scripts instead
- **Wrong**: Enabling all automatic attribution features at once → **Right**: Test "Process final HTML" on staging first; can break malformed HTML
- **Wrong**: Forgetting to enable the service after configuration → **Right**: Services with "Enabled" unchecked don't appear on consent modal

## See Also

- [Consent Mode Selection](consent-mode-selection.md)
- Reference: [Klaro Module Documentation](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/klaro-cookie-consent-management)
