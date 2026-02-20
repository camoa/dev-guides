---
description: Salesforce module suite architecture — core components, service IDs, storage objects, and submodule responsibilities
drupal_version: "11.x"
---

# Salesforce Module Architecture Overview

## When to Use

> Use the Salesforce module suite when you need bidirectional synchronization between Drupal entities and Salesforce objects. The base module is always required; submodules are added based on sync direction and features needed.

## Decision

| Component | Service ID / Location | Purpose |
|---|---|---|
| REST Client | `salesforce.client` | All API communication, token refresh, caching |
| Auth Plugin Manager | `plugin.manager.salesforce.auth_providers` | Manages OAuth/JWT auth provider plugins |
| Event System | `SalesforceEvents` class | Replaces legacy hooks for all integration points |
| SFID | `/web/modules/contrib/salesforce/src/SFID.php` | Salesforce ID value object (15 or 18 char) |
| SObject | `/web/modules/contrib/salesforce/src/SObject.php` | Salesforce object record wrapper |
| SelectQuery | `/web/modules/contrib/salesforce/src/SelectQuery.php` | SOQL query builder |

## Pattern

```
salesforce (base module — always required)
├── salesforce_oauth OR salesforce_jwt (one auth method required)
├── salesforce_mapping (required for any entity sync)
├── salesforce_mapping_ui (required for UI-based config)
├── salesforce_push (Drupal → Salesforce direction)
└── salesforce_pull (Salesforce → Drupal direction)
```

**Admin routes:**
- `/admin/config/salesforce` — Main configuration
- `/admin/config/salesforce/authorize` — Authorization setup

## Common Mistakes

- **Wrong**: Enabling only the base `salesforce` module and expecting sync to work → **Right**: Also enable a mapping submodule and at least one direction (push/pull)
- **Wrong**: Using legacy hook implementations from `salesforce.api.php` → **Right**: Use Symfony EventDispatcher subscribers via `SalesforceEvents`

## See Also

- [OAuth Authentication](oauth-authentication.md)
- [JWT Authentication](jwt-authentication.md)
- [Mapping Framework](mapping-framework.md)
- Reference: `/web/modules/contrib/salesforce/src/Rest/RestClient.php`
- Reference: `/web/modules/contrib/salesforce/src/Event/SalesforceEvents.php`
- Docs: https://www.drupal.org/docs/contributed-modules/salesforce-suite/quick-start
