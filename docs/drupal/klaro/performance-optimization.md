---
description: Optimize Klaro for fast page load, minimal render blocking, and efficient resource management
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Optimize Klaro for fast page load times, minimal render blocking, and efficient resource management.

## Decision

| Performance Goal | Strategy | Why |
|---|---|---|
| Reduce modal size | Group by purpose | Fewer UI elements to render |
| Fast initial load | Defer non-critical services | Load tracking scripts after consent |
| Minimize re-renders | Use only_once for one-time scripts | Prevent redundant executions |
| Reduce cookie size | Minimize service count | Consent cookie stores all decisions |
| Fast consent storage | Use cookies over localStorage | Faster read/write on each page load |

## Pattern

**Optimized Configuration**:

```yaml
# Group services to reduce modal complexity
services_settings:
  group_by_purpose: true  # Collapsible sections
  verbose_descriptions: false  # Shorter descriptions

# Defer non-critical services
service:
  name: advertising
  required: false
  toggled_by_default: false  # Load only if user consents

# One-time execution for expensive scripts
service:
  name: conversion_tracking
  only_once: true  # Fires once even if toggled multiple times

# Storage optimization
storage:
  method: cookie  # Faster than localStorage for small data
  expires_days: 365  # Balance between re-prompts and freshness
```

**Script Loading Strategy**:
```javascript
// Callback optimization: Lazy load after consent
callback: |
  if (consent) {
    // Load script asynchronously
    const script = document.createElement('script');
    script.src = 'https://analytics.example.com/tracker.js';
    script.async = true;
    document.head.appendChild(script);
  }
```

**Avoid Process final HTML When Possible** (performance cost):
```yaml
# Expensive: Parses entire HTML output
process_final_html: false  # Disable if not needed

# Cheaper: Targeted attribution
process_js_alter: true  # Only processes Drupal libraries
process_page_attachments: true  # Only render array attachments
process_preprocess_field: true  # Only field-level processing
```

**Reference**: [Web Performance Best Practices](https://web.dev/fast/)

## Common Mistakes

- **Wrong**: Enabling verbose_descriptions with many services → **Right**: Larger modal; slower render; disable if not needed
- **Wrong**: Not using group_by_purpose with 10+ services → **Right**: Overwhelming modal; always group when many services
- **Wrong**: Using process_final_html for all pages → **Right**: High CPU cost parsing HTML; use targeted attribution instead
- **Wrong**: Loading large tracking libraries synchronously → **Right**: Blocks page render; use async/defer
- **Wrong**: Setting very short cookie expiration → **Right**: Users re-prompted frequently; use 12-24 months
- **Wrong**: Not lazy-loading service scripts → **Right**: Everything loads on consent; defer heavy scripts
- **Wrong**: Configuring too many services → **Right**: Larger consent cookie; consolidate where possible

## See Also

- Reference: [Consent Mode Performance](https://secureprivacy.ai/blog/cookie-consent-implementation)
