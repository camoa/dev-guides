---
description: What core/drupal.htmx loads — JavaScript files, dependencies, and differential asset loading
tldr: Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`. The library loads three integration JS files and depends on the HTMX 2.0.4 vendor library, Drupal core JS, drupalSettings, and loadjs.
drupal_version: "11.x"
---

# Library Dependencies

## When to Use

> Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`.

## Decision

| File | Purpose |
|------|---------|
| `htmx-utils.js` | `Drupal.htmx.mergeSettings()`, `Drupal.htmx.addAssets()` |
| `htmx-assets.js` | Asset loading, settings merge, history cleanup, `ajax_page_state` integration |
| `htmx-behaviors.js` | Drupal behaviors integration, custom events `htmx:drupal:load`, `htmx:drupal:unload` |

## Pattern

Library definition in `/core/core.libraries.yml` lines 617–634:

```yaml
drupal.htmx:
  version: VERSION
  js:
    misc/htmx/htmx-utils.js: {}
    misc/htmx/htmx-assets.js: {}
    misc/htmx/htmx-behaviors.js: {}
  dependencies:
    - core/htmx          # HTMX vendor library v2.0.4
    - core/drupal        # Drupal core JS (behaviors, etc.)
    - core/drupalSettings
    - core/loadjs        # Asset loading utility for differential CSS/JS
  drupalSettings:
    # Placeholder values set by system_js_settings_alter().
    ajaxPageState:
      libraries: null
      theme: null
      theme_token: null
    ajaxTrustedUrl: {}
```

**Dependencies:**
- `core/htmx` — HTMX library v2.0.4 at `/core/assets/vendor/htmx/htmx.min.js`
- `core/drupal` — Drupal core JavaScript (behaviors, etc.)
- `core/drupalSettings` — Settings system for drupalSettings object
- `core/loadjs` — Asset loading utility for differential CSS/JS loading

## Common Mistakes

- **Wrong**: Manually loading HTMX vendor library → **Right**: Already included via `core/htmx` dependency
- **Wrong**: Expecting immediate behavior attach after swap → **Right**: Behaviors run AFTER `htmx:drupal:load` fires (after asset loading completes)
- **Wrong**: Not accounting for differential loading → **Right**: `ajax_page_state` means only new assets load, not all page assets
- **Wrong**: Loading deprecated HTMX versions → **Right**: Drupal 11.3 uses HTMX 2.0.4

## See Also

- [Basic Setup](basic-setup.md)
- [Asset Loading](asset-loading.md)
- [Drupal Behaviors Integration](drupal-behaviors.md)
- Reference: `/core/core.libraries.yml` — complete library definitions
- Reference: `/core/misc/htmx/` — directory with all integration JS files
