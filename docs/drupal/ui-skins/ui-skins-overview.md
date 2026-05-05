---
description: When to use UI Skins vs UI Styles, DaisyUI, or theme settings for design token and theme variant management.
tldr: Use UI Skins when site builders need to adjust CSS custom property values (colors, tokens) or toggle named theme variants (light/dark/brand) from theme settings. It is config-time and theme-wide — not per-block and not runtime.
drupal_version: "11.x"
---

# UI Skins Overview

## When to Use

> Use UI Skins when your design system uses CSS custom properties for tokens and you want site builders to adjust token values or toggle named theme variants (light/dark/brand) from theme settings — without forking the theme. Use UI Styles for per-block class application. Use DaisyUI's `.theme-controller` or JS for runtime user-facing theme switching.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Site-wide brand color customization without theme forking | UI Skins CSS variables | YAML-declared variable plugins, color-picker form, `:root { --var: value; }` injected at render |
| User-toggleable light/dark mode at runtime | DaisyUI `.theme-controller` or JS theme switcher | UI Skins is a config-time selection, not a runtime toggle |
| Per-block CSS class application | UI Styles | UI Skins doesn't apply classes per element |
| Configurable `--space-*` or `--font-size-*` tokens | UI Skins CSS variables | Same pattern as colors; pick `textfield` widget |
| Multiple registered themes with one active | UI Skins themes | Site-builder picks active theme; UI Skins emits class/`data-theme` on `<html>` or `<body>` |
| Per-section / per-page theme override | UI Skins selection scoped via Layout Builder | Not supported out of the box — UI Skins is global. Use DaisyUI per-page `data-theme` instead |

## Pattern

A CSS variable plugin declares a token and its default values per scope:

```yaml
# my_theme.ui_skins.css_variables.yml
brand_primary:
  type: ui_skins_alpha_color
  label: "Brand primary"
  category: "Colors"
  default_values:
    ":root": "#0066ccff"
```

A theme plugin declares a named variant that toggles a class or attribute:

```yaml
# my_theme.ui_skins.themes.yml
dark:
  label: "Dark mode"
  target: body
  key: data-theme
  value: dark
```

Site builders pick values and active theme via the standard theme settings page. UI Skins emits a `<style>` tag with `:root { --brand-primary: #...; }` and adds the configured class/attribute to `<body>` or `<html>`.

## Common Mistakes

- **Treating UI Skins as a per-block tool** → It's theme-wide. Per-block class application is UI Styles' job
- **Expecting runtime user theme switching** → UI Skins reads from theme settings (config). Runtime toggling needs JS or DaisyUI's controller pattern
- **Storing token values in CSS files instead of UI Skins** → Loses the editor UI. Use UI Skins for any value a non-developer should adjust

## UI Suite Family

UI Skins is part of the **UI Suite** family of complementary modules:

| Module | Purpose |
|---|---|
| [UI Patterns](../ui-patterns/index.md) | Component definitions (props, slots, variants) backed by SDC |
| [UI Styles](../ui-styles/index.md) | Curated CSS-class options applied per element |
| **UI Skins** | CSS variable values + theme variants (this topic) |
| [UI Icons](../ui-icons/index.md) | Icon-pack registry shared across fields, CKEditor, components |
| [UI Suite DaisyUI](../ui-suite-daisyui/index.md) | DaisyUI starter using the suite |

UI Skins owns the *values* of design tokens; UI Styles owns the *classes that consume them*. UI Patterns owns *component structure*; UI Icons owns *iconography*.

## See Also

- [CSS Variable Definition](ui-skins-css-variable-definition.md)
- [Theme Definition](ui-skins-theme-definition.md)
- [UI Skins + UI Styles Together](ui-skins-with-ui-styles.md)
- Reference: `drupal/ui_skins` module
