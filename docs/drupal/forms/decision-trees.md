---
description: Decision trees and quick reference matrices for form development
drupal_version: "11.x"
---

# Decision Trees and Quick Reference

## Form Base Class Selection

```
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

## Validation Strategy Selection

```
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

## AJAX Implementation Selection

```
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

## Element Selection Quick Reference

| I need to... | Element Type |
|-------------|--------------|
| Short text input | textfield |
| Long text input | textarea |
| Email address | email |
| Phone number | tel |
| Web address | url |
| Number with spinner | number |
| Slider | range |
| Password | password |
| Password with confirmation | password_confirm |
| Date only | date |
| Date and time | datetime |
| Select from 2-5 options | radios or select |
| Select from >5 options | select |
| Select from >50 options | entity_autocomplete |
| Multiple choices | checkboxes |
| Single yes/no | checkbox |
| File upload (basic) | file |
| File upload (managed) | managed_file |
| Invisible wrapper | container |
| Visible grouping | fieldset |
| Collapsible section | details |
| Tabbed interface | vertical_tabs |

## Form Caching Decision

```
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

## Common Patterns Matrix

| Pattern | Base Class | Caching | Validation | Use Case |
|---------|------------|---------|------------|----------|
| Admin settings | ConfigFormBase | No | Typed config | Module config |
| Contact form | FormBase | No | Form-level | User submissions |
| Delete confirm | ConfirmFormBase | No | None | Delete operations |
| Multi-step wizard | FormBase | Yes (required) | Partial + form | Complex workflow |
| AJAX form | FormBase | Recommended | Form-level | Dynamic UI |
| Entity create | EntityForm | No | Entity + form | Content creation |
| Search form | FormBase | No | Minimal | GET method |
| Batch operation | FormBase | No | Form-level | Bulk processing |

## Performance Optimization Decision

| Situation | Action | Why |
|-----------|--------|-----|
| >50 options in select | entity_autocomplete | Prevent large HTML |
| >100 rows in query | Cache or defer | Slow database query |
| N+1 entity loads | loadMultiple() | One query vs many |
| External API in buildForm() | Defer to submit | Runs on every rebuild |
| AJAX on keyup | Debounce | Prevent request flood |

## Security Checklist

| Security Concern | Solution | Reference |
|------------------|----------|-----------|
| CSRF attacks | Never disable tokens | Automatic |
| XSS attacks | Use render arrays, t() | Never raw HTML |
| SQL injection | Parameterized queries | Entity Query best |
| File upload exploits | Whitelist extensions, private:// | #upload_validators |
| Access bypass | Check permissions | #access property |

## See Also

- [FormBase Pattern](pattern-standard-form.md)
- [ConfigFormBase Pattern](pattern-config-form.md)
- [Validation Architecture](validation-architecture.md)
- [AJAX Architecture](ajax-architecture.md)
- [Performance Optimization](performance-optimization.md)
