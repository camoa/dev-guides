---
description: Declaring named theme variants in *.ui_skins.themes.yml — light/dark/brand-A with class or data-attribute injection.
tldr: Declare theme plugins in `{theme}.ui_skins.themes.yml` at the theme root. Each plugin specifies a target element (body or html), injection key (class or data-attribute), value, optional asset library, and optional dependencies. Site builder picks one; UI Skins injects the class or attribute at render time.
drupal_version: "11.x"
---

# Theme Definition

## When to Use

> Use this when declaring named theme variants (light, dark, brand-A) that a site builder selects via a dropdown in theme settings, triggering a class or `data-theme` attribute on `<body>` or `<html>`.

## Decision: target × key

| Goal | target | key |
|---|---|---|
| Toggle a Tailwind/utility framework's `dark` class on root | html | class |
| Use a CSS attribute selector (e.g. `[data-theme="dark"]`) | body or html | data-theme |
| Add a body-only class for legacy CSS | body | class |

## Pattern

**File location**: `{module|theme}/{module|theme_name}.ui_skins.themes.yml`

```yaml
plugin_id:                          # machine name
  enabled: true                     # optional
  label: "Dark mode"                # required, translatable
  description: "Lower-contrast variant for low-light reading"  # optional
  target: body                      # body | html (default: body)
  key: class                        # class | data-{name} (default: class)
  value: theme-dark                 # attribute value; if empty uses plugin_id
  library: my_theme/dark-mode       # optional asset library to attach when active
  dependencies:                     # optional list of other theme plugin IDs to activate first
    - high_contrast
```

When the site builder selects this theme:
- if `key: class` → `<body class="theme-dark">` (merged with existing classes)
- if `key: data-theme` → `<body data-theme="theme-dark">`
- if `target: html` → applied to `<html>` instead of `<body>`

## Common Mistakes

- **Forgetting `value`** → Falls back to plugin ID. If the plugin ID contains underscores you don't want in CSS, set `value` explicitly
- **Circular `dependencies`** → The plugin manager doesn't detect cycles; will recurse. Audit chains
- **Specifying a `library` that doesn't exist** → Drupal silently skips missing libraries; debug via `drush watchdog:show`

## See Also

- [Theme Targets & Keys](ui-skins-theme-targets-keys.md)
- [Theme Dependencies](ui-skins-theme-dependencies.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- Reference: `src/Theme/ThemePluginManager.php`, `src/Definition/ThemeDefinition.php`
