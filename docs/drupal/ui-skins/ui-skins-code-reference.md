---
description: Key classes, services, plugin discovery paths, and theme settings storage schema for the UI Skins module.
tldr: UI Skins ships two plugin managers (CssVariablePluginManager, ThemePluginManager), a PreprocessHtml hook handler that emits the style tag and injects body/html attributes, and a theme settings form integration. Plugin files must live at the theme/module root and are discovered by YAML file name pattern.
drupal_version: "11.x"
---

# Code Reference Map

## Key Files & Classes

| Location | Role |
|---|---|
| `ui_skins.services.yml` | Service definitions for plugin managers |
| `ui_skins.module` | Hook implementations (form alter, preprocess) |
| `src/CssVariable/CssVariablePluginManager.php` | Discovers and manages CSS variable definitions |
| `src/Theme/ThemePluginManager.php` | Discovers and manages theme variant definitions |
| `src/Definition/CssVariableDefinition.php` | Value object for a parsed CSS variable plugin |
| `src/Definition/ThemeDefinition.php` | Value object for a parsed theme plugin |
| `src/Element/AlphaColor.php` | Color-picker form element with alpha channel |
| `src/Form/CssVariablesThemeSettingsForm.php` | Theme settings form integration |
| `src/HookHandler/PreprocessHtml.php` | Renders `<style>` tag and injects body/html attributes |
| `src/HookHandler/FormSystemThemeSettingsAlter.php` | Adds variable + theme controls to theme settings page |
| `src/HookHandler/PageTop.php` | Page-top render integration |
| `config/schema/ui_skins.schema.yml` | Schema for theme settings storage |

## Plugin Discovery

- CSS variables: `{module|theme}/{module|theme_name}.ui_skins.css_variables.yml` (theme/module root only)
- Themes: `{module|theme}/{module|theme_name}.ui_skins.themes.yml` (theme/module root only)
- Cache tags: `ui_skins_css_variables`, `ui_skins_themes`

## Theme Settings Storage

```yaml
# config/sync/{theme}.settings.yml (excerpt)
ui_skins_css_variables:
  brand_primary:
    ":root": "#aa00ccff"
ui_skins_theme: dark
```

- `ui_skins_css_variables` — map of `{plugin_id: {scope: value}}`
- `ui_skins_theme` — single string: active theme plugin ID

## Requirements

- UI Skins 1.2.1 requires Drupal `^11.4 || ^12`, PHP 8.3+
- No external Composer dependencies

## See Also

- [Render Pipeline](ui-skins-render-pipeline.md)
- [UI Suite DaisyUI — UI Skins Integration](../ui-suite-daisyui/ui-skins-integration.md)
- Reference: `drupal/ui_skins` on drupal.org
- Reference: `design-system-daisyui.md` — "Per-Page Theme Switching" for runtime alternative
