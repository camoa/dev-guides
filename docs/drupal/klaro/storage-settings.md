---
description: Configure cookie vs localStorage, expiration, and domain scope for consent storage
drupal_version: "11.x"
---

# Storage Settings

## When to Use

> Configure how Klaro stores user consent decisions. Storage method and duration affect user experience, browser compatibility, and compliance requirements.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Maximum browser compatibility | Cookie storage | Works in all browsers; survives incognito in some |
| Modern browser-only support | LocalStorage | Persistent across sessions; larger storage capacity |
| Multi-subdomain consent sharing | Cookie with domain setting | Single consent for www.example.com and blog.example.com |
| GDPR-compliant storage duration | 12-24 month expiration | Balances user convenience with re-consent requirements |
| Cross-domain tracking prevention | Default domain (empty) | Cookie scoped to current domain only |

## Pattern

**Cookie Storage** (recommended, navigate to `/admin/config/user-interface/klaro`):

```yaml
storage:
  method: cookie  # Default; best compatibility
  cookie_name: klaro  # Customize if conflicts exist
  expires_days: 365  # 12 months recommended for GDPR
  domain: ""  # Empty = current domain only

# Multi-subdomain example
storage:
  domain: ".example.com"  # Shares across *.example.com
  matching_domains:
    - "www.example.com"
    - "blog.example.com"
    - "shop.example.com"
```

**LocalStorage** (modern browsers):
```yaml
storage:
  method: local_storage
  # No expiration setting; persists until cleared
  # Note: Users clearing browser data removes consent
```

**Reference**: `/modules/contrib/klaro/config/schema/klaro.schema.yml` for storage options

## Common Mistakes

- **Wrong**: Setting expiration >24 months → **Right**: Requires re-consent too infrequently; regulators recommend 12-24 months
- **Wrong**: Using empty domain for multi-subdomain sites → **Right**: Users re-consent on each subdomain; set root domain
- **Wrong**: Not testing cookie domain settings → **Right**: Wrong domain scope breaks consent sharing; test thoroughly
- **Wrong**: Using LocalStorage without fallback → **Right**: Older browsers don't support; cookie more compatible
- **Wrong**: Custom cookie name conflicting with existing cookies → **Right**: Verify uniqueness; avoid generic names like "consent"
- **Wrong**: Setting domain without leading dot → **Right**: `.example.com` (correct) vs `example.com` (incorrect for subdomains)

## See Also

- [Purpose Management](purpose-management.md)
- [Styling and UI Customization](styling-and-ui-customization.md)
- Reference: [Cookie Storage Best Practices](https://secureprivacy.ai/blog/cookie-consent-implementation)
