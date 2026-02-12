---
description: Grouping and action elements — containers, fieldsets, buttons
drupal_version: "11.x"
---

# Form Elements: Grouping and Action Elements

### Grouping/Container Elements

**Layout Organization:**
| Element | Visual | Collapsible | When to Use |
|---------|--------|-------------|-------------|
| container | Invisible wrapper | No | Grouping for #states, AJAX wrapper |
| fieldset | Border + legend | No | Related fields group |
| details | Border + summary | Yes | Optional/advanced settings |
| vertical_tabs | Tabbed interface | Yes | Multiple setting groups |
| actions | Button wrapper | No | Form action buttons |

**Container Element:**
```
Purpose: Structural wrapper, AJAX target
No visual styling by default
Common use: AJAX callback wrapper
Properties: #attributes, #tree
```

**Fieldset Element:**
```
Purpose: Visual grouping with legend
Properties: #title (becomes <legend>)
Accessibility: Improves screen reader navigation
```

**Details Element:**
```
Purpose: Collapsible section
Properties:
  #title: Summary text (always visible)
  #open: TRUE (default expanded) or FALSE (collapsed)
Common: Advanced settings, optional fields
```

**Vertical Tabs:**
```
Complex element, study core usage
Reference: /web/core/lib/Drupal/Core/Render/Element/VerticalTabs.php
Common in: Node edit form, admin pages
Child elements become tabs
```

**Actions Container:**
```
Standard wrapper for submit/cancel buttons
Provides: Consistent spacing, styling
Usage: $form['actions']['submit'] = [...]
```

### Action Elements (Buttons)

**Button Types:**
| Element | Purpose | Submits Form | Custom Handler |
|---------|---------|--------------|----------------|
| submit | Primary action | Yes | Optional #submit |
| button | Custom action | Optional | #executes_submit_callback, #ajax |
| image_button | Image submit | Yes | #src, #submit |

**Submit Button Properties:**
```
#value: Button text
#submit: Custom submit handlers array
#validate: Custom validation handlers array
#limit_validation_errors: Partial validation (multi-step)
```

**Multiple Submit Buttons Pattern:**
```
Different buttons trigger different handlers
Use #submit property for button-specific logic
Example: "Save", "Save and Continue", "Preview"
```

**Button-Specific Handlers:**
```
Priority order:
1. Button #submit handlers (if button triggered)
2. Form #submit handlers
3. Class submitForm() method
```

**Common Mistakes:**
- Using button instead of submit (doesn't submit by default)
- Forgetting #executes_submit_callback on button elements
- Not using #limit_validation_errors on "Previous" buttons
- Creating custom buttons without AJAX for simple submits

**See Also:**
- Submission Architecture (dedicated section)
- Multi-Step Forms (dedicated section)
- AJAX Buttons (AJAX section)
