---
description: "Key classes, services, plugin discovery paths, and theme settings storage schema for the UI Skins module."
tldr: "UI Skins ships two plugin managers (CssVariablePluginManager, ThemePluginManager), two `#[Hook]`-attributed classes under `src/Hook/` (PreprocessHtml, PageTop — no `.module` file), and stores its settings nested under `third_party_settings.ui_skins.*` per the keys on `UiSkinsInterface`. Plugin YAML files must live at the theme/module root."
drupal_version: "11.x"
---

# Code Reference Map

## Key Files & Classes

| Location | Role |
|---|---|
| `ui_skins.services.yml` | Service definitions for plugin managers |
| `src/UiSkinsInterface.php` | The two theme-setting key constants |
| `src/UiSkinsUtility.php` | CSS variable/scope name + inline-CSS helpers |
| `src/CssVariable/CssVariablePluginManager.php` | Discovers and manages CSS variable definitions |
| `src/Theme/ThemePluginManager.php` | Discovers and manages theme variant definitions |
| `src/Definition/CssVariableDefinition.php` | Value object for a parsed CSS variable plugin |
| `src/Definition/ThemeDefinition.php` | Value object for a parsed theme plugin |
| `src/Element/AlphaColor.php` | Color-picker form element with alpha channel |
| `src/Form/CssVariablesThemeSettingsForm.php` | Theme settings form integration |
| `src/Hook/PreprocessHtml.php` | Injects body/html attributes and theme libraries |
| `src/Hook/FormSystemThemeSettingsAlter.php` | Adds variable + theme controls to theme settings page |
| `src/Hook/PageTop.php` | Renders the CSS-variables `<style>` tag into page top |
| `config/schema/ui_skins.schema.yml` | Schema for theme settings storage |

## Plugin Discovery

- CSS variables: `{module|theme}/{module|theme_name}.ui_skins.css_variables.yml` (theme/module root only)
- Themes: `{module|theme}/{module|theme_name}.ui_skins.themes.yml` (theme/module root only)
- Cache tags: `ui_skins_css_variables`, `ui_skins_themes`

## Theme Settings Storage

Both keys are nested under the theme's `third_party_settings.ui_skins` (see `config/schema/ui_skins.schema.yml`, which declares `theme_settings.third_party.ui_skins`), and are referenced in code through the constants on `UiSkinsInterface`:

```yaml
# config/sync/{theme}.settings.yml (excerpt)
third_party_settings:
  ui_skins:
    css_variables:
      brand_primary:
        ":root": "#aa00ccff"
    theme: dark
```

- `third_party_settings.ui_skins.css_variables` (`UiSkinsInterface::CSS_VARIABLES_THEME_SETTING_KEY`) — map of `{plugin_id: {scope: value}}`
- `third_party_settings.ui_skins.theme` (`UiSkinsInterface::THEME_THEME_SETTING_KEY`) — single string: active theme plugin ID

## Requirements

- UI Skins 1.2.1 requires Drupal `^11.4 || ^12`, PHP 8.3+
- No external Composer dependencies

## See Also

- [Render Pipeline](ui-skins-render-pipeline.md)
- [UI Suite DaisyUI — UI Skins Integration](../ui-suite-daisyui/ui-skins-integration.md)
- Reference: `drupal/ui_skins` on drupal.org
- Reference: `design-system-daisyui.md` — "Per-Page Theme Switching" for runtime alternative
