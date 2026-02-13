---
description: Group related services into purposes (categories) for clearer consent choices
drupal_version: "11.x"
---

# Purpose Management

## When to Use

> Create purposes to group related services into categories. Purposes appear as sections in the consent modal and allow users to enable/disable entire groups at once.

## Decision

| If you have... | Create purpose... | Why |
|---|---|---|
| Analytics/statistics services | "Statistics" purpose | Groups tracking tools for visitor analysis |
| YouTube, Vimeo embeds | "External content" purpose | Groups media embedding services |
| Social media widgets | "Social media" purpose | Groups share buttons, feeds, plugins |
| Advertising services | "Marketing" purpose | Groups ad networks and retargeting |
| Multiple services per category | Enable "Group by purpose" | Reduces modal complexity for users |

## Pattern

**Purpose Creation** (navigate to `/admin/config/user-interface/klaro/manage/purposes`):

```yaml
# Create "Statistics" purpose
label: "Visitor Statistics"
weight: 10  # Lower weight appears first in modal

# Assign services to purpose
services:
  - google_analytics
  - matomo
  - hotjar
```

**Configuration** (`/admin/config/user-interface/klaro`):
```yaml
# Enable purpose grouping
services_settings:
  group_by_purpose: true  # Show purposes as expandable sections
  verbose_descriptions: true  # Include privacy URLs in descriptions
```

**Reference**: `/modules/contrib/klaro/src/Entity/KlaroPurpose.php` for purpose entity structure

## Common Mistakes

- **Wrong**: Too many granular purposes → **Right**: Overwhelming for users; 3-5 purposes ideal
- **Wrong**: Not enabling "Group by purpose" → **Right**: Modal lists all services individually; harder to navigate
- **Wrong**: Assigning service to multiple unrelated purposes → **Right**: Confusing for users; one primary purpose per service
- **Wrong**: Generic purpose names like "Other" → **Right**: Not informative; use specific categories
- **Wrong**: Inconsistent purpose weight ordering → **Right**: Random modal appearance; order by importance/workflow
- **Wrong**: Missing purpose translations → **Right**: Multi-language sites show untranslated strings; translate all purposes

## See Also

- [Service Configuration](service-configuration.md)
- [Storage Settings](storage-settings.md)
- Reference: [Purpose Management Guide](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/klaro-cookie-consent-management)
