---
description: "Apply UI Styles classes to theme regions and the page wrapper via theme settings."
tldr: "Enable ui_styles_page; the theme settings page gains a section to apply styles to the page wrapper and each region. Selections store in theme settings YAML and apply via hook_preprocess_region/page. These are theme-level (all pages) — don't duplicate with LB section styles."
drupal_version: "11.x"
---

# Integration: Pages & Regions

## When to Use

> Use this guide when applying classes to theme regions (header, sidebar, footer) or the entire page wrapper, configured per-theme via theme settings.

## Pattern

Enable `ui_styles_page`. The theme settings page (`/admin/appearance/settings/{theme}`) gains a section to apply styles to the page wrapper and to each region defined in `{theme}.info.yml`.

Selections are stored in theme settings (`config/sync/{theme}.settings.yml`) and applied via `hook_preprocess_region()` and `hook_preprocess_page()`.

## Common Mistakes

- **Confusing region styles with section/block styles** → Region styles are theme-level and apply to all pages; LB section styles are per-page. Don't duplicate across both layers

## See Also

- [Integration: Layout Builder](layout-builder.md)
- [Theme Authoring](theme-authoring.md)
- Reference: `modules/ui_styles_page/` in the UI Styles module
