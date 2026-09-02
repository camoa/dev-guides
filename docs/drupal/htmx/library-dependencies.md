---
description: "What core/drupal.htmx loads — JavaScript files, dependencies, and differential asset loading"
tldr: "Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`. The library loads three integration JS files and depends on the HTMX 2.0.4 vendor library, Drupal core JS, drupalSettings, and loadjs."
drupal_version: "11.x"
---

# Library Dependencies

## When to Use

> You need to understand what gets loaded when you attach `core/drupal.htmx`, or you're experiencing asset loading issues.

## Reference: core/drupal.htmx Library

**Definition** in `/core/core.libraries.yml` lines 617-634:

```yaml
drupal.htmx:
  version: VERSION
  js:
    misc/htmx/htmx-utils.js: {}
    misc/htmx/htmx-assets.js: {}
    misc/htmx/htmx-behaviors.js: {}
  dependencies:
    - core/htmx
    - core/drupal
    - core/drupalSettings
    - core/loadjs
  drupalSettings:
    # These placeholder values will be set by system_js_settings_alter().
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

## JavaScript Files

| File | Purpose |
|------|---------|
| `htmx-utils.js` | `Drupal.htmx.mergeSettings()`, `Drupal.htmx.addAssets()` |
| `htmx-assets.js` | Asset loading, settings merge, history cleanup, `ajax_page_state` integration |
| `htmx-behaviors.js` | Drupal behaviors integration, custom events (`htmx:drupal:load`, `htmx:drupal:unload`) |

Reference: `/core/misc/htmx/` directory

## Common Mistakes

- Manually loading HTMX vendor library — Already included via `core/htmx` dependency
- Expecting immediate behavior attach after swap — Behaviors run AFTER `htmx:drupal:load` fires (after asset loading)
- Not accounting for differential loading — `ajax_page_state` means only new assets load, not all page assets
- Loading deprecated HTMX versions — Drupal 11.3 uses HTMX 2.0.4

## See Also

- Previous: [Basic Setup](basic-setup.md)
- Next: [Request Detection](request-detection.md)
- Reference: `/core/core.libraries.yml` — Complete library definitions
