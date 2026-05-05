---
description: End-to-end pattern for shipping a sub-theme with UI Skins variables and themes wired to its CSS.
tldr: Author CSS using `var(--token)`, attach it via libraries.yml, declare matching plugins in `{theme}.ui_skins.css_variables.yml` and `{theme}.ui_skins.themes.yml` at the theme root, then clear cache. Both YAML files must be at the theme root — subdirectories are not scanned. Sub-themes inherit parent plugin definitions and can override with the same plugin ID.
drupal_version: "11.x"
---

# Theme Authoring

## When to Use

> Use this when shipping a sub-theme with its own UI Skins variables and themes. Covers the full sequence from CSS authoring to theme settings form appearance.

## Pattern

1. Author CSS that consumes the variables:

   ```css
   /* css/theme.css */
   :root { --brand-primary: #0066cc; }
   body.theme-dark { --brand-primary: #3399ff; }
   .btn-primary { background: var(--brand-primary); }
   ```

2. Attach CSS in `{theme}.libraries.yml`:

   ```yaml
   global-styling:
     css:
       theme:
         css/theme.css: {}
   ```

3. Declare CSS variables in `{theme}.ui_skins.css_variables.yml`:

   ```yaml
   brand_primary:
     type: ui_skins_alpha_color
     label: "Brand primary"
     category: "Colors"
     default_values:
       ":root": "#0066ccff"
       ".theme-dark": "#3399ffff"
   ```

4. Declare themes in `{theme}.ui_skins.themes.yml`:

   ```yaml
   dark:
     label: "Dark"
     target: body
     key: class
     value: theme-dark
   ```

5. Clear cache so YamlDiscovery picks up the files.

6. Site builder visits **Appearance → Settings → {your theme}**, sees a "Colors" fieldset with a color picker and a "Theme" select.

### Subtheme Inheritance

Sub-themes inherit parent theme UI Skins plugin definitions automatically. Override by declaring the same plugin ID in the sub-theme's YAML, or disable with `enabled: false`.

## Common Mistakes

- **Putting the YAML files in subdirectories** → Discovery scans only the theme/module root for `*.ui_skins.css_variables.yml` and `*.ui_skins.themes.yml`
- **Forgetting to attach the CSS that uses the variables** → The values inject correctly, but no CSS rules consume them
- **Hardcoding values in CSS instead of using `var()`** → Variable values inject but have no effect. Always reference `var(--brand-primary)` in CSS

## See Also

- [CSS Variable Definition](ui-skins-css-variable-definition.md)
- [Theme Definition](ui-skins-theme-definition.md)
- [Variable Scopes](ui-skins-variable-scopes.md)
- [Render Pipeline](ui-skins-render-pipeline.md)
