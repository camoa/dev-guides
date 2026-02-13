---
description: Form element type system - categories, discovery, and universal properties
drupal_version: "11.x"
---

# Form Elements: Overview

## When to Use

> Choose element types based on data type and UI needs. All elements are plugins discovered from Element/ directory.

## Decision

| Data Type | Element Category | Examples |
|-----------|------------------|----------|
| User enters data | Input elements | textfield, textarea, email, number |
| User chooses options | Selection elements | select, radios, checkboxes |
| User uploads files | File elements | file, managed_file |
| Trigger behavior | Action elements | submit, button |
| Organize layout | Grouping elements | container, fieldset, details |

## Element Categories

**Input Elements:** textfield, textarea, email, tel, url, search, number, range, password, date, datetime

**Selection Elements:** select, radios, checkboxes, checkbox

**File Elements:** file, managed_file

**Action Elements:** submit, button, image_button

**Grouping Elements:** container, fieldset, details, vertical_tabs, actions

**Special Elements:** hidden, token, markup, item, table, entity_autocomplete

## Universal Properties

| Property | Purpose | Applicable To |
|----------|---------|---------------|
| #type | Element type (required) | All |
| #title | Label text | Most |
| #description | Help text | Most |
| #required | Validation flag | Input/selection |
| #default_value | Initial value | Input/selection |
| #access | Visibility control | All |
| #weight | Sort order | All |
| #attributes | HTML attributes | All |
| #prefix, #suffix | Wrapper markup | All |

## Element Discovery

All elements located in `/web/core/lib/Drupal/Core/Render/Element/`

Study element class for available properties and behaviors.

## Common Mistakes

- **Wrong**: Hardcoding HTML for form elements → **Right**: Use form element types
- **Wrong**: Ignoring #access property → **Right**: Use for visibility control
- **Wrong**: Not setting #title for accessibility → **Right**: Always provide labels

## See Also

- [Input Elements](elements-input.md)
- [Selection Elements](elements-selection.md)
- [Grouping Elements](elements-grouping.md)
- [Element Lifecycle](elements-lifecycle.md)
- Reference: [Form Element Reference](https://drupalize.me/tutorial/form-element-reference)
