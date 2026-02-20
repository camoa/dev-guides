---
description: Salesforce optional submodules — logger, example, webform, address, SOAP — when to enable each
drupal_version: "11.x"
---

# Optional Submodules

## When to Use

> Enable optional submodules only when you need their specific functionality. The `salesforce_example` module is for development reference only — never enable in production.

## Decision

| Submodule | Enable When | Avoid When |
|---|---|---|
| `salesforce_logger` | Production monitoring, debugging, troubleshooting | High-volume sites where log overhead is a concern |
| `salesforce_example` | Development — studying event subscriber patterns | Production — reference only |
| `salesforce_webform` | Pushing webform submissions to Salesforce | Not using Webform module |
| `salesforce_address` | Mapping Address (contrib) fields to Salesforce address fields | Not using the Address module |
| `salesforce_soap` | Specific operations only available via SOAP, legacy integrations | Standard use cases — prefer REST API |

## Pattern

**salesforce_logger** — logs to database via `SalesforceEvents::ERROR`, `WARNING`, `NOTICE`:
- Admin route: `/admin/config/salesforce/logger`
- Event subscriber: `/web/modules/contrib/salesforce/modules/salesforce_logger/src/EventSubscriber/SalesforceLoggerSubscriber.php`

**salesforce_webform** — field mapping plugins for webform submissions:
- Map `webform_submission` entity type, bundle = specific webform ID
- Dependencies: `salesforce_mapping`, `webform`

**salesforce_address** — street address as textarea widget:
- Salesforce stores street as single text field; Address module uses composite field
- Widget: `AddressDefaultWidgetStreetAsTextArea`
- Dependencies: `address`

**salesforce_example** — reference for all event patterns:
- Push: `pushAllowed`, `pushParamsAlter`, `pushSuccess`, `pushFail`
- Pull: `pullQueryAlter`, `pullPrepull`, `pullPresave`
- Custom field plugin: `Hardcoded` example
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_example/src/EventSubscriber/SalesforceExampleSubscriber.php`

## Common Mistakes

- **Wrong**: Enabling `salesforce_example` in production → **Right**: Copy patterns from it to your custom module; never enable example modules in production
- **Wrong**: Using `salesforce_soap` for standard CRUD operations → **Right**: Use REST API (`salesforce.client`) for all standard operations; SOAP only for Metadata API or bulk operations

## See Also

- [Event System](event-system.md)
- [Extension Patterns](extension-patterns.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_example/`
