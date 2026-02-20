---
description: Salesforce decision framework — submodule selection, events vs plugins vs config, when to customize vs configure
drupal_version: "11.x"
---

# Decision Framework

## When to Use

> Use this guide when starting a Salesforce integration to select the right submodules and approach. Return to it when deciding whether to use events, custom plugins, or plain configuration.

## Decision

**Submodule selection:**

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

**Events vs plugins:**

| Approach | Use For |
|---|---|
| EventSubscriber | Modify existing mapping behavior, conditional logic, veto operations, cross-cutting concerns |
| Field mapping plugin | Reusable field logic, custom field types, calculated values, integration with custom field types |
| Configuration only | Standard property mappings, simple triggers, basic WHERE clauses |

**When configuration is sufficient:**
- Standard field mappings (entity properties to SF fields)
- Simple sync triggers (create/update/delete)
- Basic WHERE clauses for pull filtering
- Standard pull frequency

**When customization is required:**
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

## See Also

- [Architecture Overview](salesforce-overview.md)
- [Event System](event-system.md)
- [Custom Field Mapping Plugin](custom-field-mapping-plugin.md)
- [Extension Patterns](extension-patterns.md)
- Docs: https://www.drupal.org/docs/contributed-modules/salesforce-suite/quick-start
- Salesforce REST API: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
