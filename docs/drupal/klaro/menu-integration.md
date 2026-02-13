---
description: Add privacy settings links to menus or use floating toggle button for consent management
drupal_version: "11.x"
---

# Menu Integration

## When to Use

> Provide users a way to modify consent preferences after initial decision. GDPR requires the ability to withdraw consent at any time.

## Decision

| If you want... | Use... | Why |
|---|---|---|
| Floating button (easiest) | Toggle button setting | Always visible; no menu configuration needed |
| Privacy menu link | href="#klaro" | Standard menu item; works on all pages |
| Custom element/button | class="open-consent-manager" | Full control over styling and placement |
| Accessible link | rel="open-consent-manager" | Semantic HTML attribute; screen reader friendly |
| Footer privacy settings | Multiple methods combined | Redundant access points improve UX |

## Pattern

**Toggle Button** (navigate to `/admin/config/user-interface/klaro`):
```yaml
consent:
  show_toggle_button: true  # Floating button appears
  # Typically positioned bottom-right
  # No additional configuration needed
```

**Menu Link Method 1** (href attribute):
```yaml
# Create menu link
title: "Privacy Settings"
url: "#klaro"
# Clicking opens consent modal
```

**Menu Link Method 2** (CSS class):
```yaml
# Create menu link with class
title: "Cookie Preferences"
url: "<nolink>"
classes: "open-consent-manager"
```

**Menu Link Method 3** (rel attribute):
```yaml
# Using link_attributes or menu_link_attributes module
title: "Manage Consent"
url: "<nolink>"
attributes:
  rel: "open-consent-manager"
```

**Custom Button in Template**:
```twig
{# In page.html.twig or footer template #}
<button class="open-consent-manager">
  Cookie Settings
</button>
```

**Reference**: `/modules/contrib/link_attributes/` or `/modules/contrib/menu_link_attributes/` for attribute management

## Common Mistakes

- **Wrong**: Not providing any way to reopen modal → **Right**: Violates GDPR withdrawal requirement; always include toggle or link
- **Wrong**: Using only toggle button without menu option → **Right**: Some users prefer menu navigation; offer both
- **Wrong**: Creating menu link without proper attributes → **Right**: Link does nothing; use href="#klaro" or class/rel attributes
- **Wrong**: Forgetting to install link_attributes module → **Right**: Can't add rel attribute to links; install if using rel method
- **Wrong**: Not testing menu links on all pages → **Right**: Link works on home but not elsewhere; verify site-wide
- **Wrong**: Poor link placement (hidden in footer) → **Right**: Users can't find it; make prominent and accessible

## See Also

- [Automatic Resource Attribution](automatic-resource-attribution.md)
- [URL Pattern Exclusions](url-pattern-exclusions.md)
- Modules: [link_attributes](https://www.drupal.org/project/link_attributes), [menu_link_attributes](https://www.drupal.org/project/menu_link_attributes)
