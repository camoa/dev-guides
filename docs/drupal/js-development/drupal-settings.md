---
description: Pass server-side PHP data to client-side JavaScript via drupalSettings
drupal_version: "10.x/11.x"
---

# drupalSettings

## When to Use

> Use when passing server-side data (PHP) to client-side JavaScript. Alternative to AJAX requests for static configuration data available at page render.

## Decision

drupalSettings is a JavaScript object containing data from PHP. Attach settings via `#attached['drupalSettings']` in render arrays. Settings are JSON-encoded and injected into page as `<script type="application/json">` for CSP compatibility.

**Security critical**: NEVER pass sensitive data (passwords, API keys, tokens, private user data) through drupalSettings - it's visible in page source.

## Pattern

**PHP: Attaching settings**:

```php
$build['#attached']['drupalSettings']['moduleName']['configKey'] = [
  'apiEndpoint' => '/api/data',
  'itemsPerPage' => 10,
  'enableFeature' => TRUE,
];
```

**JavaScript: Accessing settings**:

```javascript
Drupal.behaviors.moduleFeature = {
  attach(context, settings) {
    // Settings passed as second parameter
    const config = settings.moduleName.configKey;
    const endpoint = config.apiEndpoint;

    // Also available globally
    const globalConfig = drupalSettings.moduleName.configKey;
  }
};
```

**Namespacing pattern** (prevent conflicts):

```php
// Good: module.feature.setting
$build['#attached']['drupalSettings']['myModule']['featureName']['setting'] = $value;

// Bad: global namespace pollution
$build['#attached']['drupalSettings']['setting'] = $value;
```

**CSP compatibility**: Settings rendered as `<script type="application/json" data-drupal-selector="drupal-settings-json">` since Drupal 8.1 for Content Security Policy support.

## Common Mistakes

- **Wrong**: Passing sensitive data → **Right**: Never pass secrets or private data
  - **Why**: Visible in page source, creates security vulnerability
- **Wrong**: Not namespacing settings → **Right**: Use module.feature.setting hierarchy
  - **Why**: Conflicts with other modules, settings overwritten
- **Wrong**: Passing large datasets → **Right**: Use AJAX endpoints for large data
  - **Why**: Bloats page weight, impacts performance
- **Wrong**: HTML in settings without escaping → **Right**: Sanitize before DOM insertion
  - **Why**: XSS vulnerability when inserted into DOM
- **Wrong**: Modifying drupalSettings in JS → **Right**: Treat as read-only
  - **Why**: Changes don't persist, only affects current page instance

## See Also

- [Security](security.md) - XSS prevention with settings
- [AJAX Integration](ajax-integration.md) - When to use AJAX instead of settings
- Reference: [CSP-compatible JSON settings](https://www.drupal.org/node/2513818)
