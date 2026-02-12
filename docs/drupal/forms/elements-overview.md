---
description: Form elements — types, categories, universal properties
drupal_version: "11.x"
---

# Form Elements: Overview and Categories

## When to Use

> Use this reference when choosing the right element type for user input or layout.

## Decision

| Input Need | Element Type | Category |
|-----------|--------------|----------|
| Short text | textfield, email, tel, url | Input |
| Long text | textarea | Input |
| Number | number, range | Input |
| Date/time | date, datetime, datelist | Input |
| Password | password, password_confirm | Input |
| Single choice | select, radios | Selection |
| Multiple choice | checkboxes, select (multiple) | Selection |
| File upload | managed_file, file | File |
| Button | submit, button | Action |
| Grouping | container, fieldset, details | Grouping |

## Element Categories

**Input Elements** (user enters data):
- Text: textfield, textarea, email, tel, url, search
- Numeric: number, range
- Security: password, password_confirm
- Date/Time: date, datetime, datelist

**Selection Elements** (user chooses options):
- Single: select, radios
- Multiple: checkboxes
- Binary: checkbox

**File Elements**: file, managed_file

**Action Elements**: submit, button, image_button

**Grouping Elements**: container, fieldset, details, vertical_tabs, actions

**Special Elements**: hidden, token, markup, item, table, entity_autocomplete

## Universal Element Properties

| Property | Purpose | All Elements |
|----------|---------|--------------|
| #type | Element type | Required |
| #title | Label text | Most |
| #description | Help text | Most |
| #required | Validation flag | Input elements |
| #default_value | Initial value | Input/selection |
| #access | Visibility (bool/AccessResult) | All |
| #weight | Sort order | All |
| #attributes | HTML attributes array | All |
| #prefix, #suffix | Wrapper markup | All |

## Element Discovery

```
All elements in: /web/core/lib/Drupal/Core/Render/Element/
Study element class for properties and behaviors
@FormElement annotation defines #type
```

## Common Mistakes

- **Wrong**: Using wrong element type for data (textfield for date) → **Right**: Use semantic HTML5 types
- **Wrong**: Not setting #required for mandatory fields → **Right**: Use #required property
- **Wrong**: Forgetting #default_value for edit forms → **Right**: Set default values from entity/config

## See Also

- [Input Elements](elements-input.md)
- [Selection Elements](elements-selection.md)
- [Grouping Elements](elements-grouping.md)
- [Element Lifecycle](elements-lifecycle.md)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/`
- Documentation: [Form Element Reference](https://drupalize.me/tutorial/form-element-reference)
