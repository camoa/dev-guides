---
description: Customize Klaro appearance with CSS variables, positioning, and HTML in descriptions
drupal_version: "11.x"
---

# Styling and UI Customization

## When to Use

> Customize Klaro's appearance to match your site's branding, position elements, and control HTML rendering in descriptions.

## Decision

| If you need... | Configure... | Why |
|---|---|---|
| Match site color scheme | CSS variables override | Changes colors without custom CSS files |
| Custom positioning (top/bottom) | CSS variables: top, bottom | Controls modal/notice placement |
| Brand-specific styling | Additional CSS classes | Scope custom CSS to Klaro elements |
| Clickable links in descriptions | Allow HTML in texts | Enables privacy policy hyperlinks |
| Custom button styles | CSS targeting | Style accept/decline buttons separately |

## Pattern

**CSS Variable Customization** (navigate to `/admin/config/user-interface/klaro`):

```yaml
styling:
  element_id: klaro  # Default container ID
  additional_classes: "brand-consent custom-theme"
  css_variable_override: "light, top"  # Light theme, top positioning
  allow_html_in_texts: true  # Enable for clickable links
```

**Available CSS Variables** (customize in theme CSS):
```css
/* Override Klaro variables */
#klaro {
  --primary-color: #3b82f6;  /* Brand blue */
  --accept-bg: #10b981;  /* Accept button green */
  --decline-bg: #ef4444;  /* Decline button red */
  --border-radius: 8px;  /* Rounded corners */
  --spacing: 1rem;  /* Internal padding */
}

/* Position adjustments */
.klaro.top {
  top: 20px;
}

.klaro.bottom {
  bottom: 20px;
}
```

**Service Description with HTML**:
```yaml
# Service configuration with HTML links
description: >
  We use Google Analytics to understand site usage.
  <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a>

# Requires: allow_html_in_texts: true
```

**Reference**: [Klaro CSS Variables Documentation](https://github.com/klaro-org/klaro-js#styling)

## Common Mistakes

- **Wrong**: Enabling "Allow HTML in texts" without sanitization → **Right**: XSS vulnerability; only enable if you control all service descriptions
- **Wrong**: Not testing HTML descriptions → **Right**: Broken HTML breaks modal rendering; validate all HTML
- **Wrong**: Using !important in custom CSS → **Right**: Specificity issues; use proper selectors instead
- **Wrong**: Overriding too many variables → **Right**: Harder to maintain; override only necessary variables
- **Wrong**: Forgetting to add custom classes → **Right**: CSS rules don't apply; add classes to Klaro container
- **Wrong**: Not accounting for mobile viewport → **Right**: Modal too large on small screens; test responsive behavior

## See Also

- [Storage Settings](storage-settings.md)
- [Translation and Localization](translation-and-localization.md)
- Security: [Security Best Practices](security-best-practices.md)
