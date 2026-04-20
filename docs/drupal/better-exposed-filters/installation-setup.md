---
description: Install Better Exposed Filters, enable on a View, and configure the noUiSlider library
tldr: "Use this guide when installing BEF on a Drupal site and enabling it for Views."
drupal_version: "11.x"
---

# Installation & Setup

## When to Use

> Use this guide when installing BEF on a Drupal site and enabling it for Views.

## Decision

| Situation | Choose | Why |
|---|---|---|
| New site, need enhanced filter widgets | Install BEF | One command gets you all widgets |
| Sliders only needed | Install + enable noUiSlider | `drupal/nouislider_js` is required for sliders |
| Just want auto-submit | BEF general settings | No extra library needed |

## Pattern

```bash
# Install via Composer (includes nouislider_js dependency)
composer require drupal/better_exposed_filters

# Enable the module
drush en better_exposed_filters
```

**Enabling BEF on a View:**
1. Edit your View in the Views UI
2. Under **Advanced** → **Exposed Form**, click the current style (usually "Basic")
3. Change to **"Better Exposed Filters"**
4. Click **Settings** next to the exposed form style
5. Configure general settings and per-filter widget options
6. Save the View

**Verify noUiSlider library (required for sliders):**
```bash
ls web/libraries/nouislider/nouislider.min.js
```

Files must exist at `/libraries/nouislider/`: `nouislider.min.js` and `nouislider.min.css`

## Common Mistakes

- **Wrong**: Expecting BEF widget options to appear without changing the exposed form style → **Right**: Select "Better Exposed Filters" as the exposed form style under Advanced → Exposed Form.
- **Wrong**: Assuming Composer handles the noUiSlider files completely → **Right**: Some hosting setups strip `/libraries/` during deployment. Verify the files are in place after each deploy.

## See Also

- [Overview](overview.md)
- [General Settings](general-settings.md)
- Reference: https://www.drupal.org/project/better_exposed_filters
