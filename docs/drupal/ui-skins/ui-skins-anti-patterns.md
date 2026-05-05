---
description: Common UI Skins mistakes — hardcoded CSS values, runtime switching, per-block theming, file placement.
tldr: The most common mistakes are hardcoding hex colors in CSS files instead of declaring UI Skins variables, expecting runtime user-facing theme switching from a config-time module, and placing YAML files in theme subdirectories instead of the theme root.
drupal_version: "11.x"
---

# UI Skins Anti-Patterns

## When to Use

> Reference this when setting up a UI Skins integration to avoid the most common configuration and authoring errors.

## Common Mistakes

- **Wrong**: hardcoded hex colors in `.css` files for any value an editor should adjust → **Right**: declare a UI Skins CSS variable, use `var(--name)` in CSS
- **Wrong**: building runtime user theme switching with UI Skins alone → **Right**: UI Skins is config-time. Use DaisyUI's `.theme-controller` (or any JS toggler) for user-facing runtime switching
- **Wrong**: declaring one theme plugin per brand color combination, expecting per-component scoping → **Right**: themes are global. Use UI Skins variable scopes (`.callout-warning`) or component-level CSS for per-component variation
- **Wrong**: putting `.ui_skins.themes.yml` inside a subdirectory of the theme → **Right**: at the theme root only
- **Wrong**: depending on plugin-manager evaluation order to compose themes → **Right**: use explicit `dependencies` and write CSS that handles the resulting class combinations
- **Wrong**: storing brand colors in UI Styles options → **Right**: store the *class* in UI Styles (e.g., `text-primary`) and the *value* in UI Skins (`--brand-primary: #0066cc`)

## See Also

- [UI Skins Overview](ui-skins-overview.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- [UI Skins + UI Styles Together](ui-skins-with-ui-styles.md)
