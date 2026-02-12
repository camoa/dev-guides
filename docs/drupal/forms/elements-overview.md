---
description: Form elements — types, categories, universal properties
drupal_version: "11.x"
---

# Form Elements: Overview and Categories

### Element Type System

**Architecture:**
- Location: `/web/core/lib/Drupal/Core/Render/Element/`
- Base classes: `FormElementBase`, `RenderElementBase`
- Plugin system: Element annotations define metadata

**Element Discovery:**
```
All elements in Element/ directory
Study element class for properties and behaviors
@FormElement annotation defines #type
```

### Element Categories

**Input Elements** (user enters data):
- Text: textfield, textarea, email, tel, url, search
- Numeric: number, range
- Security: password, password_confirm
- Date/Time: date, datetime, datelist

**Selection Elements** (user chooses options):
- Single: select, radios
- Multiple: checkboxes
- Binary: checkbox

**File Elements** (file uploads):
- file, managed_file

**Action Elements** (trigger behavior):
- submit, button, image_button

**Grouping Elements** (organize layout):
- container, fieldset, details, vertical_tabs, actions

**Special Elements** (specific purposes):
- hidden, token, markup, item, table, tableselect
- entity_autocomplete (entity reference)

### Universal Element Properties

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

**See Also:**
- Input Elements Reference (next section)
- Selection Elements Reference
- Element Lifecycle (callbacks section)
- Official: [Form Element Reference](https://drupalize.me/tutorial/form-element-reference)
