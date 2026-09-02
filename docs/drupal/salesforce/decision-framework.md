---
description: "Salesforce decision framework — submodule selection, events vs plugins vs config, when to customize vs configure"
tldr: "Use this guide when starting a Salesforce integration to select the right submodules and approach. Return to it when deciding whether to use events, custom plugins, or plain configuration."
drupal_version: "11.x"
---

# Decision Framework

## When to Use

> Use this guide when starting a Salesforce integration to select the right submodules and approach. Return to it when deciding whether to use events, custom plugins, or plain configuration.

## Decision: Which Submodule

| Submodule | Status | When to Include |
|---|---|---|
| `salesforce` | Required | Always — base module |
| `salesforce_oauth` OR `salesforce_jwt` | Required (pick one) | One auth method required |
| `salesforce_mapping` | Required for sync | Any entity sync |
| `salesforce_mapping_ui` | Required for UI config | Admin UI-based configuration |
| `salesforce_push` | Conditional | Drupal → Salesforce direction |
| `salesforce_pull` | Conditional | Salesforce → Drupal direction |
| `salesforce_logger` | Recommended | Production — debugging and monitoring |
| `salesforce_example` | Development only | Reference patterns — never in production |
| `salesforce_webform` | Optional | Webform submissions → Salesforce |
| `salesforce_address` | Optional | Address (contrib) field → SF address fields |
| `salesforce_soap` | Legacy/rare | Specific SOAP-only operations |

**Required:**
- `salesforce` - Always required (base module)
- `salesforce_oauth` OR `salesforce_jwt` - One auth method required

**Mapping:**
- `salesforce_mapping` - Required for any entity sync
- `salesforce_mapping_ui` - Required for UI-based configuration

**Sync Direction:**
- `salesforce_push` - Enable for Drupal → Salesforce sync
- `salesforce_pull` - Enable for Salesforce → Drupal sync

**Optional:**
- `salesforce_logger` - Recommended for production debugging
- `salesforce_example` - Development reference only
- `salesforce_webform` - If using Webform module
- `salesforce_address` - If using Address field module
- `salesforce_soap` - Legacy/specific use cases only

## Decision: Events vs Plugins

| Approach | Use For |
|---|---|
| EventSubscriber | Modify existing mapping behavior, conditional logic, veto operations, cross-cutting concerns |
| Field mapping plugin | Reusable field logic, custom field types, calculated values, integration with custom field types |
| Configuration only | Standard property mappings, simple triggers, basic WHERE clauses |

**Events (EventSubscriber):**
- Modify behavior of existing mappings
- Cross-cutting concerns (logging, validation)
- Conditional logic (veto operations)
- Complex field transformations
- Related entity operations

**Plugins (SalesforceMappingField):**
- Reusable field mapping logic
- Custom field type handling
- Calculated/derived values
- Integration with custom field types

## Decision: Customize vs Configure

**Configuration Sufficient:**
- Standard field mappings (entity properties to SF fields)
- Simple sync triggers (create/update/delete)
- Basic WHERE clauses
- Standard pull frequency

**Customization Required:**
- Complex field transformations
- Conditional push/pull logic
- Related entity synchronization
- Custom validation rules
- File/attachment handling
- Integration with external systems

## Pattern

**Quickstart module selection:**
```
1. Base: salesforce
2. Auth: salesforce_oauth (interactive) OR salesforce_jwt (automated)
3. Mapping: salesforce_mapping + salesforce_mapping_ui
4. Direction: salesforce_push AND/OR salesforce_pull
5. Monitoring: salesforce_logger (recommended for production)
```

## Common Mistakes

- **Wrong**: Using EventSubscriber for reusable field transformation logic used across multiple mappings → **Right**: Create a field mapping plugin (`PropertiesBase`) for reusable logic; use events for one-off behavior
- **Wrong**: Customizing when configuration is sufficient — over-engineering → **Right**: Start with configuration; add events only when the standard mapping cannot express the required behavior

## Guide Maintenance

**Guide Maintenance:** This guide references specific file paths in the Salesforce module codebase. When upgrading the module, verify file locations and API changes. Event system is stable since 8.x-4.x branch.

## Related Documentation

**Drupal.org:**
- Quick Start: https://www.drupal.org/docs/contributed-modules/salesforce-suite/quick-start
- Mapping Guide: https://www.drupal.org/docs/contributed-modules/salesforce-suite/mapping
- Push/Pull: https://www.drupal.org/docs/contributed-modules/salesforce-suite/push-and-pull

**Salesforce Developer:**
- REST API: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
- SOQL: https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/
- Connected Apps: https://help.salesforce.com/articleView?id=connected_app_create.htm

**Code References:**
- API Documentation: https://api.drupal.org/api/salesforce
- Example Module: `/web/modules/contrib/salesforce/modules/salesforce_example`
- Event Examples: `/web/modules/contrib/salesforce/modules/salesforce_example/src/EventSubscriber/SalesforceExampleSubscriber.php`

## See Also

- [Architecture Overview](salesforce-overview.md)
- [Event System](event-system.md)
- [Custom Field Mapping Plugin](custom-field-mapping-plugin.md)
- [Extension Patterns](extension-patterns.md)
