---
description: "Install Better Exposed Filters, enable it on a View, and configure the noUiSlider library"
tldr: "Use this guide when installing BEF on a Drupal site and enabling it for Views. BEF 7.1.3 requires Drupal core ^10.3 || ^11 — the 8.0.x branch is a separate, newer alpha line and is not production-safe."
drupal_version: "10.3 / 11.x"
---

# Installation & Setup

## When to Use

> When installing BEF on a Drupal site and enabling it for Views.

## Pattern: Installation

This guide documents Better Exposed Filters 7.1.3, which declares `core_version_requirement: ^10.3 || ^11` and is covered by Drupal's security advisory policy.

The 8.0.x branch is a separate, newer line: `8.0.0-alpha1` requires Drupal core `^11.4 || ^12`. It is an alpha, so it is **not** covered by security advisories — do not adopt it on a production site. Do not read the 8.0.x core requirement as 7.1.x's; 7.1.3 still supports Drupal 10.3.

```bash
# Install via Composer (includes nouislider_js dependency)
composer require drupal/better_exposed_filters

# Enable the module
drush en better_exposed_filters
```

**Dependencies:**
- `drupal:views` (core)
- `drupal/nouislider_js` (composer dependency for sliders)

## Pattern: Enabling BEF on a View

1. Edit your View in the Views UI
2. Under **Advanced** → **Exposed Form**, click the current style (usually "Basic")
3. Change to **"Better Exposed Filters"**
4. Click **Settings** next to the exposed form style
5. Configure general settings and per-filter widget options
6. Save the View

## Pattern: noUiSlider Library

The slider widget requires the noUiSlider JavaScript library at `/libraries/nouislider/`:
- `nouislider.min.js`
- `nouislider.min.css`

The `drupal/nouislider_js` Composer package manages this. Verify the files exist:
```bash
ls web/libraries/nouislider/nouislider.min.js
```

## Common Mistakes

- **Not switching the exposed form style** — BEF is a Views exposed form plugin. It does nothing until you select "Better Exposed Filters" as the exposed form style.
- **Missing noUiSlider files** — If sliders don't work, check that the library files are in place. Some hosting setups strip `/libraries/` during deployment.

## See Also

- [Overview](overview.md) — what BEF provides
- [General Settings](general-settings.md) — configuring BEF after installation
