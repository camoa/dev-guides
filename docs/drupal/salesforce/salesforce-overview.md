---
description: "Salesforce module suite architecture — core components, service IDs, storage objects, and submodule responsibilities"
tldr: "Use the Salesforce module suite when you need bidirectional synchronization between Drupal entities and Salesforce objects. The base module is always required; submodules are added based on sync direction and features needed."
drupal_version: "11.x"
---

# Salesforce Module Architecture Overview

## When to Use

> Use the Salesforce module suite when you need bidirectional synchronization between Drupal entities and Salesforce objects. The base module is always required; submodules are added based on sync direction and features needed.

The Salesforce module suite provides bidirectional synchronization between Drupal entities and Salesforce objects using a plugin-based architecture. The suite consists of a base module with multiple submodules that handle specific functionality.

## Decision

| Component | Service ID / Location | Purpose |
|---|---|---|
| REST Client | `salesforce.client` | All API communication, token refresh, caching |
| Auth Plugin Manager | `plugin.manager.salesforce.auth_providers` | Manages OAuth/JWT auth provider plugins |
| Event System | `SalesforceEvents` class | Replaces legacy hooks for all integration points |
| SFID | `/web/modules/contrib/salesforce/src/SFID.php` | Salesforce ID value object (15 or 18 char) |
| SObject | `/web/modules/contrib/salesforce/src/SObject.php` | Salesforce object record wrapper |
| SelectQuery | `/web/modules/contrib/salesforce/src/SelectQuery.php` | SOQL query builder |

## Core Architecture Components

**REST API Client:**
- Location: `/web/modules/contrib/salesforce/src/Rest/RestClient.php`
- Service ID: `salesforce.client`
- Provides Salesforce REST API communication layer
- Handles authentication, token refresh, API calls, caching

**Authentication Plugin System:**
- Manager: `/web/modules/contrib/salesforce/src/SalesforceAuthProviderPluginManager.php`
- Service ID: `plugin.manager.salesforce.auth_providers`
- Interface: `/web/modules/contrib/salesforce/src/SalesforceAuthProviderInterface.php`
- Annotation: `/web/modules/contrib/salesforce/src/Annotation/SalesforceAuthProvider.php`
- Supports OAuth and JWT authentication providers

**Event System:**
- Events class: `/web/modules/contrib/salesforce/src/Event/SalesforceEvents.php`
- Replaces legacy hook system (see `/web/modules/contrib/salesforce/salesforce.api.php`)
- All integration points now use Symfony EventDispatcher

**Storage Objects:**
- `SFID`: Salesforce ID value object - `/web/modules/contrib/salesforce/src/SFID.php`
- `SObject`: Salesforce object wrapper - `/web/modules/contrib/salesforce/src/SObject.php`
- `SelectQuery`: SOQL query builder - `/web/modules/contrib/salesforce/src/SelectQuery.php`
- `SelectQueryResult`: Query result wrapper - `/web/modules/contrib/salesforce/src/SelectQueryResult.php`

## Pattern

```
salesforce (base module — always required)
├── salesforce_oauth OR salesforce_jwt (one auth method required)
├── salesforce_mapping (required for any entity sync)
├── salesforce_mapping_ui (required for UI-based config)
├── salesforce_push (Drupal → Salesforce direction)
└── salesforce_pull (Salesforce → Drupal direction)
```

## Base Module: salesforce

**Purpose:** Core REST API integration and authentication framework

**Key Services:**
```
salesforce.client - RestClient for API communication
plugin.manager.salesforce.auth_providers - Auth provider plugin manager
salesforce.http_client_wrapper - HTTP client wrapper
salesforce.auth_token_storage - Token storage service
```

**Configuration:**
- Schema: `/web/modules/contrib/salesforce/config/schema/salesforce.schema.yml`
- Settings form: `/web/modules/contrib/salesforce/src/Form/SettingsForm.php`
- Auth management: `/web/modules/contrib/salesforce/src/Form/SalesforceAuthForm.php`

**Admin Routes:**
- `/admin/config/salesforce` - Main configuration
- `/admin/config/salesforce/authorize` - Authorization setup

**Decision Point - When to Use:**
- Required as base dependency for all Salesforce integration
- Provides authentication and API client services

**Module version**: The current stable release is Salesforce 5.1.3, which requires Drupal `^11.3`. A 6.x branch exists but carries no tagged release at all — it is dev-only, earlier in the release process than even an alpha — so it is not documented here; this guide targets 5.1.3.

## Common Mistakes

- **Wrong**: Enabling only the base `salesforce` module and expecting sync to work → **Right**: Also enable a mapping submodule and at least one direction (push/pull)
- **Wrong**: Using legacy hook implementations from `salesforce.api.php` → **Right**: Use Symfony EventDispatcher subscribers via `SalesforceEvents`

## See Also

- [OAuth Authentication](oauth-authentication.md)
- [JWT Authentication](jwt-authentication.md)
- [Mapping Framework](mapping-framework.md)
- [Optional Submodules](optional-submodules.md)
- Reference: `/web/modules/contrib/salesforce/src/Rest/RestClient.php`
- Reference: `/web/modules/contrib/salesforce/src/Event/SalesforceEvents.php`
- Docs: https://www.drupal.org/docs/contributed-modules/salesforce-suite/quick-start
