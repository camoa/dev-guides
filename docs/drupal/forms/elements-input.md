---
description: Input elements — text, numeric, password, date/time fields
drupal_version: "11.x"
---

# Form Elements: Input Elements

### Text Input Elements

| Element | HTML5 Type | Validation | Key Properties |
|---------|------------|------------|----------------|
| textfield | text | None | #maxlength, #size, #autocomplete_route_name |
| textarea | textarea | None | #rows, #cols, #resizable |
| email | email | Email format | #maxlength |
| tel | tel | None | #maxlength |
| url | url | URL format | #maxlength |
| search | search | None | #maxlength |

**Reference Files:**
- `/web/core/lib/Drupal/Core/Render/Element/Textfield.php`
- `/web/core/lib/Drupal/Core/Render/Element/Email.php`
- `/web/core/lib/Drupal/Core/Render/Element/Url.php`

**When to Use Each:**
```
Textfield: Generic short text (names, titles)
Textarea: Multi-line text (descriptions, messages)
Email: Email addresses (automatic @ validation)
Tel: Phone numbers (mobile keyboard hint)
Url: Web addresses (protocol validation)
Search: Search inputs (browser styling/history)
```

### Numeric Input Elements

| Element | Purpose | Properties | Browser Behavior |
|---------|---------|------------|------------------|
| number | Numeric input | #min, #max, #step | Spinner controls |
| range | Slider | #min, #max, #step | Visual slider |

**Number Validation:**
```
#min/#max: Browser validation + server validation
#step: Increment value (e.g., 0.01 for decimals)
No #step: Integers only (step="1")
```

### Password Elements

| Element | Purpose | Features |
|---------|---------|----------|
| password | Single password | #maxlength, #size, no #default_value |
| password_confirm | Password + confirm | Dual fields, automatic matching validation |

**Security Note:**
```
Never set #default_value on password fields
Never log password values
Always use PasswordConfirm for user-facing password changes
```

**Reference:** `/web/core/lib/Drupal/Core/Render/Element/PasswordConfirm.php`

### Date/Time Elements

| Element | Interface | Format | Properties |
|---------|-----------|--------|------------|
| date | Date picker | Y-m-d | #date_date_format |
| datetime | Date + time | Y-m-d H:i:s | #date_time_format, #date_date_format |
| datelist | Dropdowns | Custom | #date_part_order, #date_year_range |

**Date Element Decision:**
```
Modern browser, single date? → date
Date and time needed? → datetime
Need granular control/old browsers? → datelist
Complex date logic? → Custom element
```

**Common Mistakes:**
- Not setting #date_date_format (uses site default)
- Forgetting timezone handling
- Using textfield for dates (accessibility issue)

**See Also:**
- DateTime API Guide
- Timezone Handling Guide
