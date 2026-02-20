---
description: What core/drupal.htmx loads — JavaScript files, dependencies, and differential asset loading
drupal_version: "11.x"
---

# Library Dependencies

## When to Use

> Reference this when diagnosing asset loading issues or understanding what attaches when you add `core/drupal.htmx`.

## Decision

| File | Purpose | Weight |
|------|---------|--------|
| `htmx-utils.js` | `Drupal.htmx.mergeSettings()`, `Drupal.htmx.addAssets()` | -20 |
| `htmx-assets.js` | Asset loading, settings merge, history cleanup, `ajax_page_state` integration | -19 |
| `htmx-behaviors.js` | Drupal behaviors integration, custom events `htmx:drupal:load`, `htmx:drupal:unload` | -18 |

## Pattern

Library definition in `/core/core.libraries.yml`:

```yaml
drupal.htmx:
  version: VERSION
  js:
    misc/htmx/htmx-utils.js: { weight: -20 }
    misc/htmx/htmx-assets.js: { weight: -19 }
    misc/htmx/htmx-behaviors.js: { weight: -18 }
  dependencies:
    - core/htmx          # HTMX vendor library v2.0.4
    - core/drupal        # Drupal core JS (behaviors, etc.)
    - core/drupalSettings
    - core/loadjs        # Asset loading utility for differential CSS/JS
```

## Common Mistakes

- **Wrong**: Manually loading HTMX vendor library → **Right**: Already included via `core/htmx` dependency
- **Wrong**: Expecting immediate behavior attach after swap → **Right**: Behaviors run AFTER `htmx:drupal:load` fires (after asset loading)
- **Wrong**: Not accounting for differential loading → **Right**: `ajax_page_state` means only new assets load, not all page assets
- **Wrong**: Loading deprecated HTMX versions → **Right**: Drupal 11.3 uses HTMX 2.0.4

## See Also

- [Basic Setup](basic-setup.md)
- [Asset Loading](asset-loading.md)
- [Drupal Behaviors Integration](drupal-behaviors.md)
- Reference: `/core/core.libraries.yml` lines 617-624
- Reference: `/core/misc/htmx/` directory
