---
description: What UI Skins does at render time — how it reads settings, resolves themes, injects attributes, and emits the style tag.
tldr: UI Skins runs via `HookHandler\PreprocessHtml` in `hook_preprocess_html()`. It reads theme settings, resolves transitive theme dependencies, merges class/attribute payloads onto `<html>` or `<body>`, emits a `<style>` tag with CSS variable rules, and attaches optional libraries. Theme settings config changes invalidate render caches automatically.
drupal_version: "11.x"
---

# Render Pipeline

## When to Use

> Use this when debugging what UI Skins does at render time, or when hooking into the injection process.

## Pattern

`HookHandler\PreprocessHtml` runs at `hook_preprocess_html()`:

1. **Read theme settings** — `theme_get_setting('ui_skins_css_variables')` and `theme_get_setting('ui_skins_theme')`
2. **Resolve theme dependencies** — recursively collect all transitively activated theme plugins
3. **Build attribute payload** — merge each active theme's `key`/`value` into `$variables['html_attributes']` (for `target: html`) or `$variables['attributes']` (for `target: body`) via `AttributeHelper::mergeCollections()`
4. **Build CSS variable payload** — for each declared CSS variable, emit `selector { --plugin-id: value; }` rules per scope, concatenate, output as a `<style>` tag in the page head
5. **Attach libraries** — for each active theme plugin with a `library`, append to `$variables['#attached']['library']`

### Storage in Theme Settings

```yaml
# config/sync/{theme}.settings.yml (excerpt)
ui_skins_css_variables:
  brand_primary:
    ":root": "#aa00ccff"
ui_skins_theme: dark
```

## Decision: where to hook in

| Goal | Hook / Service |
|---|---|
| Modify the rendered `<style>` tag | `hook_preprocess_html()` after UI Skins (use higher-weight module) |
| Conditionally activate a theme | Override theme settings via `hook_form_system_theme_settings_alter()` |

## Common Mistakes

- **Expecting the active theme selection to flow into Layout Builder context** → It doesn't. UI Skins is global per-page
- **Cache invalidation surprises** → `theme_settings` config changes invalidate render caches automatically. Custom alters need explicit cache tag bubbling

## See Also

- [Code Reference Map](ui-skins-code-reference.md)
- [Theme Authoring](ui-skins-theme-authoring.md)
- Reference: `src/HookHandler/PreprocessHtml.php`, `src/Form/CssVariablesThemeSettingsForm.php`
