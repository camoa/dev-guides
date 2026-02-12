---
description: Decision trees and quick reference — form selection, validation, AJAX, elements
drupal_version: "11.x"
---

# Decision Trees and Quick Reference

### Form Base Class Selection

```
Decision Flow:

Need to manage configuration?
├─ Yes → ConfigFormBase
│         - Admin settings
│         - Module configuration
│         - Use #config_target (10.2+)
│
└─ No → Need confirmation dialog?
        ├─ Yes → ConfirmFormBase
        │         - Delete operations
        │         - Destructive actions
        │         - Yes/no decisions
        │
        └─ No → Need entity create/edit?
                ├─ Yes → EntityForm
                │         - Content entities
                │         - Config entities
                │         - See Entity API Guide
                │
                └─ No → FormBase
                          - General forms
                          - Custom business logic
                          - Integrations
```

### Validation Strategy Selection

```
Validation Decision:

Single field format/range check?
├─ Yes → Element Validation
│         - #element_validate property
│         - Email format, number range
│         - Runs per-element
│
└─ No → Need cross-field validation?
        ├─ Yes → Form Validation
        │         - validateForm() method
        │         - Cross-field checks
        │         - Business logic
        │
        └─ No → Using ConfigFormBase?
                ├─ Yes → Typed Config Validation
                │         - Define in schema.yml
                │         - Automatic constraints
                │         - Works outside forms
                │
                └─ No → Combine multiple levels
```

### AJAX Implementation Selection

```
AJAX Decision:

Need dynamic options based on user input?
├─ Yes → AJAX Required
│         - Dependent dropdowns
│         - Load entities/data
│         - Server-side logic
│
└─ No → Just show/hide fields?
        ├─ Yes → Use #states (Client-side)
        │         - Faster, no server calls
        │         - Simple conditions
        │         - Better UX
        │
        └─ No → Need multiple updates?
                ├─ Yes → AjaxResponse + Commands
                │         - Multiple elements
                │         - Modal dialogs
                │         - Custom JS
                │
                └─ No → Simple Element AJAX
                          - Single element update
                          - Return render array
```

### Element Selection Quick Reference

```
Input Type Needed:

Short text (< 255 chars)?
├─ Email address? → email
├─ Phone number? → tel
├─ Web address? → url
├─ Search query? → search
└─ Generic text? → textfield

Long text (> 255 chars)?
└─ textarea

Number?
├─ Slider interface? → range
└─ Numeric input? → number

Date/Time?
├─ Just date? → date
├─ Date + time? → datetime
└─ Need dropdowns? → datelist

Password?
├─ Single password? → password
└─ With confirmation? → password_confirm

Selection?
├─ 2-5 options? → radios or select
├─ > 5 options? → select
├─ > 50 options? → entity_autocomplete
├─ Multiple choices? → checkboxes
└─ Single boolean? → checkbox

File upload?
├─ Need file entity? → managed_file
└─ Basic upload? → file

Grouping?
├─ Invisible wrapper? → container
├─ Visible with border? → fieldset
├─ Collapsible? → details
└─ Tabs? → vertical_tabs
```

### Form Caching Decision

```
Cache Decision:

Multi-step form?
└─ Yes → setCached(TRUE) REQUIRED

Expensive #options generation?
├─ Database query with 100+ results? → Yes
├─ Remote API call? → Yes
└─ Complex calculation? → Yes
        └─ setCached(TRUE) recommended

Frequent AJAX rebuilds?
└─ Yes → setCached(TRUE) recommended

Simple form, no rebuilds?
└─ No caching needed
```

### Common Form Patterns Matrix

| Pattern | Base Class | Caching | Validation | Typical Use |
|---------|------------|---------|------------|-------------|
| Admin settings | ConfigFormBase | No | Typed config | Module config page |
| Contact form | FormBase | No | Form-level | User submissions |
| Delete confirm | ConfirmFormBase | No | None | Delete operations |
| Multi-step wizard | FormBase | Yes (required) | Partial + form | Complex workflow |
| AJAX form | FormBase | Recommended | Form-level | Dynamic UI |
| Entity create | EntityForm | No | Entity + form | Content creation |
| Search form | FormBase | No | Minimal | GET method search |
| Batch operation | FormBase | No | Form-level | Bulk processing |

**See Also:**
- Architecture sections for details
- Pattern sections for implementation
- Element reference for properties
