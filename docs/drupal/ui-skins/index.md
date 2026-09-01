---
description: UI Skins — expose CSS custom properties and named theme variants as YAML plugins for site-builder configuration without theme forking.
tracks:
  - project: ui_skins
    channel: stable
    declared: "1.2.1"
    verified: 2026-08-20
guide-meta:
  concepts:
    - UI Skins
    - CSS custom properties
    - design tokens
    - theme variants
    - light/dark mode
    - ui_skins_alpha_color
    - css_variables.yml
    - themes.yml
    - theme settings
    - brand theming
    - data-theme
    - data-bs-theme
  not:
    - UI Styles (per-block class application — see drupal/ui-suite-daisyui or drupal/layout-builder)
    - DaisyUI runtime theme controller (user-facing runtime switching)
    - Tailwind design tokens (upstream token authoring — see design-systems/tailwind-tokens)
  requires:
    - drupal/ui-skins/ui-skins-installation
  complements:
    - drupal/ui-suite-daisyui
    - drupal/layout-builder
    - design-systems/tailwind-tokens
    - design-systems/daisyui
  category: drupal
---

# UI Skins

**Philosophy**: Expose CSS custom properties (design tokens) and theme variants as YAML plugins so site builders can pick brand colors, modes, and theme switches from theme settings — without forking the theme. Skins inject CSS variables and class/data attributes into the page head and root element at render time.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what UI Skins does and when to use it | [Overview](ui-skins-overview.md) | Use UI Skins when site builders need to adjust CSS custom property values (colors, tokens) or toggle named theme variants (light/dark/brand) from theme settings. It is config-time and theme-wide — not per-block and not runtime. |
| Install UI Skins | [Installation](ui-skins-installation.md) | Install UI Skins with composer and drush en. Single module only — no submodules exist. Requires Drupal ^11.4 \|\| ^12 and PHP 8.3+. Once enabled, it adds CSS variable and theme controls to every theme's settings form. |
| Declare a CSS variable plugin in YAML | [CSS Variable Definition](ui-skins-css-variable-definition.md) | Declare CSS variable plugins in `{theme}.ui_skins.css_variables.yml` at the theme root. Each plugin maps a machine name to a CSS variable, a form widget type, a label, and a map of CSS scope → default value. Plugin ID becomes the CSS variable name with `--` prefix. |
| Pick a form widget for a CSS variable | [Variable Types & Widgets](ui-skins-variable-types.md) | Use `ui_skins_alpha_color` for color tokens (stores 8-char hex with alpha), `textfield` for numeric/unit/arbitrary CSS values, or a custom form element plugin for specialized inputs. Mixing up type and value format silently breaks CSS. |
| Wire variable scopes for nested overrides | [Variable Scopes](ui-skins-variable-scopes.md) | `default_values` is a map of CSS selector → value. Multiple scopes emit separate CSS rules at render time, letting the cascade deliver the right default in different contexts (`:root`, `.theme-dark`, `.callout-warning`). Site-builder edits only replace the `:root` scope value. |
| Declare a theme plugin (light/dark/brand variant) | [Theme Definition](ui-skins-theme-definition.md) | Declare theme plugins in `{theme}.ui_skins.themes.yml` at the theme root. Each plugin specifies a target element (body or html), injection key (class or data-attribute), value, optional asset library, and optional dependencies. Site builder picks one; UI Skins injects the class or attribute at render time. |
| Apply a class vs a data attribute for theme switches | [Theme Targets & Keys](ui-skins-theme-targets-keys.md) | Match `target` and `key` to the CSS selectors your theme already uses. Bootstrap 5 uses `html[data-bs-theme]`; Tailwind dark mode uses `html.dark`; DaisyUI uses `html[data-theme]`. A mismatch between target and CSS selectors means nothing applies. |
| Chain themes via dependencies | [Theme Dependencies](ui-skins-theme-dependencies.md) | Theme dependencies are additive — declaring one theme as a dependency of another causes both to activate simultaneously, producing multiple classes on the target element. They are not a mutual-exclusivity mechanism; separate plugin IDs handle that. |
| Ship a sub-theme with its own variables and themes | [Theme Authoring](ui-skins-theme-authoring.md) | Author CSS using `var(--token)`, attach it via libraries.yml, declare matching plugins in `{theme}.ui_skins.css_variables.yml` and `{theme}.ui_skins.themes.yml` at the theme root, then clear cache. Both YAML files must be at the theme root — subdirectories are not scanned. Sub-themes inherit parent plugin definitions and can override with the same plugin ID. |
| Understand the render-time injection mechanism | [Render Pipeline](ui-skins-render-pipeline.md) | UI Skins splits its render-time work across two `#[Hook]`-attributed classes (no `.module` file): `Hook\PreprocessHtml` injects body/html class or data attributes and attaches libraries, `Hook\PageTop` emits a `<style>` tag into page top. Both read settings via `ThemeSettingsProvider::getSetting()`, not `theme_get_setting()`; flat `ui_skins_css_variables:`/`ui_skins_theme:` config keys are legacy and silently produce nothing. |
| Combine UI Skins with UI Styles | [UI Skins + UI Styles Together](ui-skins-with-ui-styles.md) | UI Skins and UI Styles are orthogonal. UI Skins controls the value of CSS variables (theme-wide), UI Styles controls which utility classes are applied to individual blocks. The pattern is: UI Skins sets `--brand-primary`, UI Styles applies `text-primary` to a block, CSS links them via `var(--brand-primary)`. |
| Avoid common mistakes | [Anti-Patterns](ui-skins-anti-patterns.md) | The most common mistakes are hardcoding hex colors in CSS files instead of declaring UI Skins variables, expecting runtime user-facing theme switching from a config-time module, and placing YAML files in theme subdirectories instead of the theme root. |
| Find key classes and services | [Code Reference Map](ui-skins-code-reference.md) | UI Skins ships two plugin managers (CssVariablePluginManager, ThemePluginManager), two `#[Hook]`-attributed classes under `src/Hook/` (PreprocessHtml, PageTop — no `.module` file), and stores its settings nested under `third_party_settings.ui_skins.*` per the keys on `UiSkinsInterface`. Plugin YAML files must live at the theme/module root. |
