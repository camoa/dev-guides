---
description: ConfirmFormBase — confirmation dialogs for destructive actions
drupal_version: "11.x"
---

# Pattern: Confirmation Form (ConfirmFormBase)

### When to Use

**Appropriate Use Cases:**
- Delete operations (content, entities, config)
- Destructive actions (purge, reset, uninstall)
- Critical confirmations (irreversible operations)
- Yes/no decision points

**When NOT to Use:**
- Multi-field forms → Use FormBase
- Confirmations with additional inputs → Use FormBase with custom styling

### Implementation Pattern

**Core Example:**
- File: `/web/core/modules/dblog/src/Form/DblogClearLogConfirmForm.php`
- Pattern: Minimal form, clear question, cancel link, custom confirm text

**Form Structure:**
```
Automatically provides:
- Question text (from getQuestion())
- Confirm button (from getConfirmText())
- Cancel link (from getCancelUrl())
- Standard confirmation form styling
```

### Required Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `getQuestion()` | TranslatableMarkup | Main confirmation question |
| `getCancelUrl()` | Url object | Destination if user cancels |
| `getConfirmText()` | TranslatableMarkup | Submit button text (default: "Confirm") |
| `getDescription()` | String (optional) | Additional warning/info text |
| `getFormName()` | String (optional) | Internal form name |

**URL Pattern:**
```
Cancel URL: Usually entity/list page or referring page
Use Url::fromRoute('entity.type.collection')
Or $entity->toUrl('collection')
```

### Customization Options

**Custom Confirm Text:**
```
Different from "Confirm":
- "Delete" for delete operations
- "Remove" for remove operations
- "Reset" for reset operations
```

**Additional Elements:**
```
Can add elements in buildForm()
Common: Checkboxes for "don't ask again", deletion options
Must call parent::buildForm() to preserve structure
```

**Common Mistakes:**
- Forgetting to implement required methods (getQuestion, getCancelUrl)
  - **WHY BAD:** PHP fatal error on form build, ConfirmFormBase expects these methods, form won't render
- Returning string instead of Url object from getCancelUrl()
  - **WHY BAD:** Type error in Drupal 9+, expects Url object for route access checking and language prefix handling
- Adding complex form elements (defeats purpose of confirm form)
  - **WHY BAD:** Users expect simple yes/no, complex forms confuse purpose, accessibility issues with mixed UI patterns
- Not using descriptive confirm text (users ignore generic "Confirm")
  - **WHY BAD:** Users click without reading "Confirm", destructive actions executed without understanding, poor UX

**See Also:**
- Delete Form Patterns (Entity API Guide)
- URL Generation Guide
- User Experience Guidelines
