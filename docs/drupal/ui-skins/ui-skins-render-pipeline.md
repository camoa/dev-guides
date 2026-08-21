---
description: "What UI Skins does at render time — two Hook attribute classes read theme settings via ThemeSettingsProvider, resolve theme dependencies, inject attributes, and emit the CSS variables style tag at page top."
tldr: "UI Skins splits its render-time work across two `#[Hook]`-attributed classes (no `.module` file): `Hook\\PreprocessHtml` injects body/html class or data attributes and attaches libraries, `Hook\\PageTop` emits a `<style>` tag into page top. Both read settings via `ThemeSettingsProvider::getSetting()`, not `theme_get_setting()`; flat `ui_skins_css_variables:`/`ui_skins_theme:` config keys are legacy and silently produce nothing."
drupal_version: "11.x"
---

# Render Pipeline

## When to Use

> Use this when debugging what UI Skins does at render time, or when hooking into the injection process.

## Pattern

The work is split across **two** hook classes, both registered with the `#[Hook]` attribute (no `.module` file). Both read their setting through `\Drupal\Core\Extension\ThemeSettingsProvider::getSetting()` — *not* `theme_get_setting()` — using the constants on `UiSkinsInterface`.

**`Hook\PreprocessHtml`** (`#[Hook('preprocess_html')]`) — the active theme variant:

1. **Read the theme setting** — `getSetting('third_party_settings.ui_skins.theme')`; bails out immediately if it is not a non-empty string
2. **Resolve theme dependencies** — `getDefinitionWithDependencies()` recursively collects all transitively activated theme plugins
3. **Build attribute payload** — for each definition, merge its `key`/`value` into either `$variables['html_attributes']` (for `target: html`) or `$variables['attributes']` (any other target) using `\Drupal\Core\Template\AttributeHelper::mergeCollections()`. A `key` of `class` is run through `Html::getClass()` first
4. **Attach libraries** — for each definition with a `library`, append to `$variables['#attached']['library']`

**`Hook\PageTop`** (`#[Hook('page_top')]`) — the CSS variables:

1. **Read the variables setting** — `getSetting('third_party_settings.ui_skins.css_variables')`; bails out if it is not an array
2. **Build CSS variable payload** — for each `{plugin_id: {scope: value}}` entry, `UiSkinsUtility::getCssVariableName()` turns the plugin ID into a custom property by replacing `_` with `-` and prefixing `--` (`brand_primary` → `--brand-primary`), and `getCssScopeName()` turns `%` back into `.` in the scope. Rules are then grouped by scope into `scope{--var:value;}`
3. **Emit the style tag** — one `#type: html_tag` `<style>` element added to the **page top** render array (not the page head), cache-tagged `config:{active_theme}.settings`

### Storage in Theme Settings

Both settings live under the theme's `third_party_settings.ui_skins` — **not** as flat top-level keys:

```yaml
# config/sync/{theme}.settings.yml (excerpt)
third_party_settings:
  ui_skins:
    css_variables:
      brand_primary:
        ":root": "#aa00ccff"
    theme: dark
```

The theme settings form (extended via `hook_form_system_theme_settings_alter()` and `Form\CssVariablesThemeSettingsForm`) writes here.

Scopes are stored with **`%` standing in for `.`**, because config keyed lists cannot contain a dot (`UiSkinsUtility::DOT_CONVERSION_CHARACTER`). A scope of `.dark` is stored as `%dark` and converted back at render time — so hand-written config must use the `%` form.

> **Flat `ui_skins_css_variables:` / `ui_skins_theme:` keys are the legacy layout and no longer work.** `ui_skins_update_10101()` migrates existing sites off them. A hand-written or recipe-shipped `{theme}.settings.yml` still using them produces zero CSS variables and no active theme variant — silently, because both hooks simply return early when their setting is missing.

## Decision: where to hook in

| Goal | Hook / Service |
|---|---|
| Modify variable definitions before form render | Custom plugin manager alter — none built-in for variables; alter the discovered definitions in a custom service or use the alter mechanism via the plugin manager |
| Modify the rendered `<style>` tag | A later-running `hook_page_top()` — `Hook\PageTop` adds the tag under the `ui_skins_css_variables` key of `$page_top`, so a higher-weight module can edit or unset it |
| Conditionally activate a theme | Override theme settings via `hook_form_system_theme_settings_alter()` |

## Common Mistakes

- **Expecting the active theme selection to flow into Layout Builder context** → It doesn't. UI Skins is global per-page
- **Cache invalidation surprises** → `theme_settings` config changes invalidate render caches automatically. Custom alters need explicit cache tag bubbling
- **Hand-writing `{theme}.settings.yml` with flat `ui_skins_css_variables:` / `ui_skins_theme:` keys** → Legacy layout, silently produces nothing. Use nested `third_party_settings.ui_skins.*` with `%`-encoded scopes

## See Also

- [Code Reference Map](ui-skins-code-reference.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- Reference: `src/Hook/PreprocessHtml.php`, `src/Hook/PageTop.php`, `src/Form/CssVariablesThemeSettingsForm.php`
