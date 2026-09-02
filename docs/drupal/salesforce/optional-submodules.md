---
description: "Salesforce optional submodules — logger, example, webform, address, SOAP — when to enable each"
tldr: "Enable optional submodules only when you need their specific functionality. The `salesforce_example` module is for development reference only — never enable in production."
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

## salesforce_logger

**Purpose:** Centralized logging for Salesforce operations

**Event Subscriber:**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_logger/src/EventSubscriber/SalesforceLoggerSubscriber.php`
- Subscribes to: `SalesforceEvents::ERROR`, `SalesforceEvents::WARNING`, `SalesforceEvents::NOTICE`
- Logs to: Database (dblog), custom log table

**Configuration:**
- Settings form: `/web/modules/contrib/salesforce/modules/salesforce_logger/src/Form/SettingsForm.php`
- Route: `/admin/config/salesforce/logger`

**Decision Point - Logging Strategy:**
- Enable for: Debugging, production monitoring, troubleshooting
- Disable for: High-volume sites where log overhead is concern
- Alternative: Use event subscribers to log to external systems

## salesforce_example

**Purpose:** Reference implementation for event subscribers and custom plugins

**Event Subscriber:**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_example/src/EventSubscriber/SalesforceExampleSubscriber.php`
- Demonstrates: All major event implementations
- Service definition: `/web/modules/contrib/salesforce/modules/salesforce_example/salesforce_example.services.yml`

**Key Patterns Demonstrated:**

**Push Event Handling:**
- `pushAllowed()` - Veto push based on entity type/conditions
- `pushParamsAlter()` - Modify field values before push
- `pushSuccess()` - Post-push processing
- `pushFail()` - Error handling

**Pull Event Handling:**
- `pullQueryAlter()` - Modify SOQL query (add fields, subqueries, conditions)
- `pullPrepull()` - Pre-processing, veto pull, modify SF data
- `pullPresave()` - Final entity modifications, fetch related data

**Custom Field Plugin:**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_example/src/Plugin/SalesforceMappingField/Hardcoded.php`
- Pattern: Hardcoded/calculated values

**Hook Implementations:**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_example/salesforce_example.module`
- Demonstrates: Entity CRUD hooks for custom processing

**Decision Point - Using Examples:**
- Copy subscriber pattern for: Event-based customizations
- Copy plugin pattern for: Custom field mapping logic
- Reference query modifications for: Complex pull requirements

## salesforce_webform

**Purpose:** Integrate Webform module with Salesforce mappings

**Field Mapping Plugins:**
- `WebformElements`: `/web/modules/contrib/salesforce/modules/salesforce_webform/src/Plugin/SalesforceMappingField/WebformElements.php`
- `WebformEntityElements`: `/web/modules/contrib/salesforce/modules/salesforce_webform/src/Plugin/SalesforceMappingField/WebformEntityElements.php`

**Dependencies:**
- `salesforce:salesforce_mapping`
- `webform:webform`

**Decision Point - Webform Integration:**
- Use when: Need to push webform submissions to Salesforce
- Map: `webform_submission` entity type
- Bundle: Specific webform ID
- Fields: Webform element keys

## salesforce_address

**Purpose:** Salesforce-compatible address field widget

**Purpose:** Provide textarea widget for street addresses (Salesforce stores as single text field)

**Widget:**
- Location: `/web/modules/contrib/salesforce/modules/salesforce_address/src/Plugin/Field/FieldWidget/AddressDefaultWidgetStreetAsTextArea.php`
- Field type: Address field (contrib module)
- Modification: Street field rendered as textarea instead of separate line inputs

**Dependencies:**
- `address:address`

**Decision Point - Address Mapping:**
- Use when: Mapping Address field to Salesforce address fields
- Salesforce pattern: Separate fields (Street, City, State, PostalCode, Country)
- Drupal Address module: Composite field
- Widget handles: Street field as single textarea (matches Salesforce behavior)

## salesforce_soap

**Purpose:** SOAP API support (legacy, REST recommended)

**Use Cases:**
- Metadata API operations
- Batch processing (bulk API)
- Legacy integrations requiring SOAP

**Decision Point - SOAP vs REST:**
- Prefer REST API: Modern approach, better performance, simpler
- Use SOAP when: Specific API operations only available via SOAP, legacy requirements

## Common Mistakes

- **Wrong**: Enabling `salesforce_example` in production → **Right**: Copy patterns from it to your custom module; never enable example modules in production
- **Wrong**: Using `salesforce_soap` for standard CRUD operations → **Right**: Use REST API (`salesforce.client`) for all standard operations; SOAP only for Metadata API or bulk operations

## See Also

- [Event System](event-system.md)
- [Extension Patterns](extension-patterns.md)
- [Class Reference](class-reference.md) — `SoapClient` methods
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_example/`
